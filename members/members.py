# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , members.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'members.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv  

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()    

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
           
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#When u want to close a funtion and call out a funtion.
#If it's their it will call out and get it .

#it will desplay all the entries that are stored in the db 
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select fullname,phone_number,ocupation,gender from entries order by id desc')
    entries = cur.fetchall()
    return render_template('entries.html', entries=entries)

#Adding new entries to the db
@app.route('/add', methods=['GET','POST'])
def add_entry():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db()
    db.execute('insert into entries (fullname,phone_number,ocupation,gender ) values (?,?,?,?)',
                 [request.form['fullname'], request.form['phone_number'],request.form['ocupation'],request.form['gender']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
