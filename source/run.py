from routes import app
from database import init_db
from database_loader import DB_Loader
from defines import debug

db_load = DB_Loader()
init_db()
if(debug):  # wipe db if debug  set true
    db_load.db_load()
app.run(debug=True)
