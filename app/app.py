import os
import sys

from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database_uri = 'postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'.format(
    dbuser=os.environ.get('DBUSER', "user"),
    dbpass=os.environ.get('DBPASS', "pass"),
    dbhost=os.environ.get('DBHOST', "dbhost"),
    dbport=os.environ.get('DBPORT', "5678"),
    dbname=os.environ.get('DBNAME', "dbname")
)

app = Flask(__name__)
port = int(os.getenv('PORT', '8000'))

app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

print("Connecting to:", database_uri)
# initialize the database connection
db = SQLAlchemy(app)
if not db:
    print("Could not connect!!!")
    sys.exit(1)

print("Migrating...")
# initialize database migration management
migrate = Migrate(app, db)


@app.route('/')
def view_registered_guests():
    from models import Guest
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@app.route('/health', methods=['GET'])
def health():
    return 'OK'


@app.route('/register', methods=['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@app.route('/register', methods=['POST'])
def register_guest():
    from models import Guest
    name = request.form.get('name')
    email = request.form.get('email')

    guest = Guest(name, email)
    db.session.add(guest)
    db.session.commit()

    return render_template(
        'guest_confirmation.html', name=name, email=email)

# start the app
if __name__ == '__main__':
    print('listening on port', port)
    app.run(host='0.0.0.0', port=port)