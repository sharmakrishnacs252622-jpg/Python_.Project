import database
import auth

if __name__ == "__main__": 
    database.init_db()
    auth.AuthWindow()