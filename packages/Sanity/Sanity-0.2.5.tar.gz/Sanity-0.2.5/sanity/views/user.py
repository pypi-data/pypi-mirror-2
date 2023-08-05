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

from flask import Module, render_template, g, request, flash, session, \
redirect, url_for
from sanity.models import User, Group
from sanity import config, db

user = Module(__name__)

@user.route('/register', methods=['GET', 'POST'])
def register():
    error = ""
    groups = Group.query.all()
    if not config.REGISTRATION:
        flash(u'Registration is turned off. Please contact an administrator.')
        return redirect(url_for('frontend.index'))
    if g.user is not None:
        return redirect(url_for('frontend.index'))
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        group = request.form.get('group')
        if '@' not in email:
            error = "Needs to be a valid email!"
        elif not name:
            error = "Please provide a username"
        elif not password:
            error = "Please provide a password"
        elif password != password2:
            error = "Passwords don't match"
        else:
            flash(u'Successfully created account')
            u = User(name=name, email=email)
            u.set_password(password)
            if group:
                u.group = Group.query.filter(Group.name == group).first()
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('frontend.index'))
    return render_template('user/register.html', error=error, groups=groups)

@user.route('/edit', methods=['GET', 'POST'])
def edit():
    error = ""
    groups = Group.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        group = request.form.get('group')
        if '@' not in email:
            error = "Needs to be a valid email!"
        elif not name:
            error = "Please provide a username"
        else:
            flash(u'Successfully changed info')
            g.user.name = name
            g.user.email = email
            g.user.group = Group.query.filter(Group.name == group).first()
            db.session.commit()
            return redirect(url_for('frontend.index'))
    return render_template('user/edit.html', error=error, groups=groups, \
            user=g.user)

@user.route('/edit/password', methods=['GET', 'POST'])
def edit_password():
    error = ""
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if not password:
            error = "Please enter a password"
        elif password != password2:
            error = "Passwords don't match"
        else:
            flash(u'Successfully changed password')
            g.user.set_password(password)
            db.session.commit()
            return redirect(url_for('frontend.index'))
    return render_template('user/edit_password.html', error=error)

@user.route('/login', methods=['GET', 'POST'])
def login():
    """docstring for login"""
    error = ""
    next = request.args.get('next', '')
    if g.user is not None:
        return redirect(url_for('frontend.index'))
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        remember = request.form.get('remember')
        next = request.form.get('next')
        user = User.query.filter_by(name=name).first()
        if user is None:
            error = "User does not exist"
        elif not user.check_password(password):
            error = "Password is incorrect"
        else:
            session['name'] = name
            if remember == "y":
                session.permanent = True
            flash('You were logged in')
            if next:
                return redirect(next)
            return redirect(url_for('frontend.index'))
    return render_template('user/login.html', error=error, next=next)

@user.route('/user/logout')
def logout():
    """docstring for logout"""
    session.pop('name', None)
    flash(u'You were signed out')
    return redirect(url_for('frontend.index'))


