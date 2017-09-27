from routes import app
from database import init_db
from database_loader import db_load

init_db()
db_load()
app.run(debug=False)