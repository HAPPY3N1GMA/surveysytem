from routes import app
from database import init_db
from database_loader import DB_Loader
from defines import debug
from classes import unit_tests

db_load = DB_Loader()
init_db()
db_load.db_load()

# Run Unit Tests pre run
runner = unit_tests.TestRunner()
runner.run()

app.run(debug=True)
