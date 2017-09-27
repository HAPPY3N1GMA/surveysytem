from routes import app
from database import init_db
from database_loader import db_load
from defines import debug


init_db()
if(debug):  # wipe db if debug  set true
    db_load()
app.run(debug=True)
