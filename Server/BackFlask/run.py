from app import app
from utils.init_database import run

if __name__ == '__main__':
    if not run():
        print("Can't init the database")
    else:
        print("Database initialized successfully")
    app.run(host="0.0.0.0")