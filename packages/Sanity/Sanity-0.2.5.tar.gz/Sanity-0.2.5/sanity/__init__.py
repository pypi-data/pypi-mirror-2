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

"""
    Sanity
    ~~~~~~

    A quick and simple task manager built for teams in an intranet setting.
    It's very simple to use by just about anyone on a team.

    :copyright: (c) 2010 by Aaron Toth.
    :license: Apache License 2.0, see LICENSE for more details.
"""

from flask import Flask, g, session, redirect, url_for, request
from flaskext.sqlalchemy import SQLAlchemy
from sanity import config

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 7200

db = SQLAlchemy(app)

# Take and store the current user from the database, and keep it in the global
# variable, g 
from sanity.models import User
@app.before_request
def lookup_current_user():
    g.user = None
    if 'name' in session:
        g.user = User.query.filter_by(name=session['name']).first()

# Configure logging errors by email
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                                'servererror@example.com',
                                config.ADMINS, 'Sanity Failure')
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
    '''))
    app.logger.addHandler(mail_handler)
    
# Register all the elements of the application
from sanity.views.frontend import frontend
from sanity.views.admin import admin
from sanity.views.user import user
app.register_module(frontend)
app.register_module(admin, url_prefix='/admin')
app.register_module(user, url_prefix='/user')
