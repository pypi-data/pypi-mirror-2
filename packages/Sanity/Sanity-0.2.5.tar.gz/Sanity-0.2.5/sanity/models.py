#  
#   Copyright 2010 Aaron Toth
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from datetime import date
from sanity import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(120), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, name=None, password=None, email=None):
        self.name = name
        self.password = password
        self.email = email
    
    def set_password(self, passwd):
        self.password = generate_password_hash(passwd)

    def check_password(self, passwd):
        return check_password_hash(self.password, passwd)
    
    def __repr__(self):
        return '<User %r>' % (self.name, self.email)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=task_tags, backref='task')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=date.today())
    created_by = db.Column(db.String(50), db.ForeignKey('user.name'))
    worker = db.Column(db.String(50), db.ForeignKey('user.name'))
    done_by = db.Column(db.String(50), db.ForeignKey('user.name'))

    def __init__(self, description):
        self.description = description

    def get_status(self):
        if self.done:
            return 2
        elif self.worker:
            return 1
        else:
            return 0

    def get_days_since(self):
        delta = date.today() - self.created_at
        return delta.days

    def __repr__(self):
        return '<Task %r>' % self.description

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, tag):
        self.tag = tag

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', backref=db.backref('group', order_by=id))
    tasks = db.relationship('Task', backref=db.backref('group', order_by=id))

    def __init__(self, name):
        self.name = name
        
task_tags = db.Table('task_tags', db.Model.metadata, db.Column('task_id', 
    db.Integer, db.ForeignKey('task.id')), db.Column('tag_id', db.Integer, 
    db.ForeignKey('tag.id')))
