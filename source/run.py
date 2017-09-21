from routes import app
from database import init_db

init_db()
app.run(debug=True)
