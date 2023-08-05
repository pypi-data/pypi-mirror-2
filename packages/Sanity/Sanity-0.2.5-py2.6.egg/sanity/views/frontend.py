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

import re
from functools import wraps
from flask import Module, render_template, g, request, flash, session, \
redirect, url_for
from sanity.models import Task, Tag, Group
from sanity import config, db

frontend = Module(__name__)

#
#   Decorator Functions
#

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@frontend.route('/')
@login_required
def index():
    """docstring for index"""
    tags = Tag.query.all()
    tasks = []
    if g.user.group:
        tasks = Task.query.join(Group).filter(Group.id==g.user.group.id) \
                .filter(Task.done==False).all()
    return render_template('frontend/index.html', tasks=tasks, tags=tags)

@frontend.route('/tasks/progress')
@login_required
def tasks_progress():
    """docstring for index"""
    tags = Tag.query.all()
    tasks = []
    if g.user.group:
        tasks = Task.query.join(Group).filter(Group.id==g.user.group.id) \
                .filter(Task.done==False).filter(Task.worker!=None) \
                .all()
    return render_template('frontend/tasks_progress.html', tasks=tasks, tags=tags)

@frontend.route('/tasks/completed')
@login_required
def tasks_completed():
    """docstring for index"""
    tags = Tag.query.all()
    tasks = []
    if g.user.group:
        tasks = Task.query.join(Group).filter(Group.id==g.user.group.id) \
                .filter(Task.done==True).all()
    return render_template('frontend/tasks_completed.html', tasks=tasks, tags=tags)

@frontend.route('/add/tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    error = ""
    if request.method == 'POST':
        tag = request.form.get('tag')
        if tag is None:
            error = "You must enter a tag"
        elif re.search('\s', tag):
            error = "Tags must not have spaces"
        elif Tag.query.filter(Tag.tag == tag).first():
            error = "A tag already exists by that name"
        else:
            flash(u'Tag added')
            db.session.add(Tag(tag.lower()))
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('frontend/add_tag.html', error=error)

@frontend.route('/add/task', methods=['GET', 'POST'])
@login_required
def add_task():
    """docstring for add_task"""
    error = ""
    tags_available = Tag.query.all()
    groups = Group.query.all()
    if request.method == 'POST':
        description = request.form.get('description')
        tags = request.form.getlist('tags')
        group = request.form.get('group')
        if description is None:
            error = "Please provide a task description"
        else:
            flash(u'Task added')
            task = Task(description)
            task.tags = Tag.query.filter(Tag.tag.in_(tags)).all()
            grp = Group.query.filter_by(name=group).first()
            task.group_id = grp.id
            task.creator = g.user.name
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('frontend/add_task.html', ta=tags_available, groups=groups, error=error)

@frontend.route('/tag/<tag>')
@login_required
def tag(tag):
    tasks = []
    tags = Tag.query.all()
    if g.user.group:
        tasks = Task.query.join(Group).filter(Task.tags.any(tag=tag)).filter(Task.done == False).all()
    return render_template('frontend/tag.html', tasks=tasks, tag=tag, tags=tags)

@frontend.route('/tags')
@login_required
def tags():
    tags = Tag.query.all()
    return render_template('frontend/tags.html', tags=tags)

@frontend.route('/finish/<int:id>')
@login_required
def finish(id):
    task = Task.query.filter(Task.id == id).first()
    if task.group_id == g.user.group.id:
        flash(u'Task finished')
        task.done = True
        task.done_by = g.user.name
        task.worker = None
        db.session.commit()
    return redirect('/')

@frontend.route('/unfinish/<int:id>')
@login_required
def unfinish(id):
    task = Task.query.filter(Task.id == id).first()
    if task.group_id == g.user.group.id and task.get_status() == 2:
        flash(u'Task unfinished')
        task.done = False
        task.done_by = None
        db.session.commit()
    return redirect(url_for('tasks_completed'))

@frontend.route('/work/<int:id>')
@login_required
def work(id):
    task = Task.query.filter(Task.id == id).first()
    if task.group_id == g.user.group.id and task.get_status() == 0:
        flash(u'Working on task')
        task.worker = g.user.name
        db.session.commit()
    return redirect(url_for('tasks_progress'))

@frontend.route('/tasks/group/tag/<tag>')
def group_by_tag(tag=None):
    tasks = Task.query.join(Group).filter(Group.id == g.user.group.id).filter(Task.done == False).filter(Task.tags.any(tag=tag)).all()
    return render_template('ajax/group_by_tag.html', tasks=tasks, tag=tag)

@frontend.route('/tasks/completed/tag/<tag>')
def completed_by_tag(tag=None):
    tasks = Task.query.join(Group).filter(Group.id == g.user.group.id).filter(Task.done == True).filter(Task.tags.any(tag=tag)).all()
    return render_template('ajax/completed_by_tag.html', tasks=tasks, tag=tag)

@frontend.route('/tasks/progress/tag/<tag>')
def all_by_tag(tag=None):
    tasks = Task.query.join(Group).filter(Task.worker!=None).filter(Group.id == g.user.group.id).filter(Task.tags.any(tag=tag)).all()
    return render_template('ajax/progress_by_tag.html', tasks=tasks, tag=tag)
