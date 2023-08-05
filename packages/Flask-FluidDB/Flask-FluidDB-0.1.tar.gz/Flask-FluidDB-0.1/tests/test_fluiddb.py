
from flask import Flask
from flaskext.fluiddb import init_fluiddb

def test_session():
    app = Flask('test')
    init_fluiddb(app, sandbox=True)
    assert 'indexed' in app.fluiddb.tags[u'fluiddb/about'].get().content

