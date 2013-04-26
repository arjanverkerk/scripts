# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from album import config
from album import views

import flask

# App
app = flask.Flask(__name__)
app.config.from_object(config.Config)

# Urls
app.add_url_rule('/', 
                 view_func=views.FileView.as_view(b'pageview'))

app.add_url_rule('/page/<path:relative_path>', 
                 view_func=views.PageView.as_view(b'pageview'))

app.add_url_rule('/file/<path:relative_path>', 
                 view_func=views.FileView.as_view(b'fileview'))


# Main
def run():
    app.run(host='0.0.0.0')
