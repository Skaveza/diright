import sys
import os
from website import create_app, db
from website.models import User


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'website')))

app = create_app()

def check_user_role(username):
    with app.app_context():  
        user = User.query.filter_by(username=username).first()
        if user:
            print(f'Username: {user.username}, Role: {user.role}')
        else:
            print('User not found')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_user_role.py <username>")
        sys.exit(1)
    username = sys.argv[1]
    check_user_role(username)
