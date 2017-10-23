import sys
from routes import app
from database import init_db
from database_loader import DB_Loader
from classes import tests

_debug = False

db_load = DB_Loader()
init_db()
db_load.db_load()

if len(sys.argv) > 1:
    if '--testonly' in sys.argv:
        runner = tests.TestRunner()
        runner.run()
        sys.exit()
    elif '--testfirst' in sys.argv:
        runner = tests.TestRunner()
        runner.run()
    if '--debug' in sys.argv:
        _debug = True

app.run(debug=_debug)
