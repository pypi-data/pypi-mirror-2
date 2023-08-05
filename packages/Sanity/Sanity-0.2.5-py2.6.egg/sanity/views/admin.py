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

from functools import wraps
from flask import Module, render_template, g, request, flash, session, \
redirect, url_for, escape
from sanity.models import User, Task, Tag, Group
from sanity import db

admin = Module(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        elif not g.user.admin:
            return redirect(url_for('frontend.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@admin_required
def index():
    return "Hello admin!"

@admin.route('/groups', methods=['GET', 'POST'])
@admin_required
def groups():
    error = ""
    if request.method == 'POST':
        name = request.form.get('name')
        if name is None:
            error = "You must enter a group name"
        else:
            db.session.add(Group(name))
            db.session.commit()
            return redirect(url_for('index'))
    else:
        groups = Group.query.all()
    return render_template('admin/groups.html', error=error, groups=groups)

@admin.route('/tags', methods=['GET', 'POST'])
def tags(): pass

@admin.route('/tasks', methods=['GET', 'POST'])
def tasks(): pass

@admin.route('/users', methods=['GET', 'POST'])
def users(): pass
