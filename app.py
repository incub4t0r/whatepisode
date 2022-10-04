from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(ROOT, 'database.db')

app = Flask(__name__)

# access sqlite3 database
def db_connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# create database if it doesn't exist
def db_check():
    if not os.path.isfile(DATABASE):
        db_create()

# create database
def db_create():
    conn = db_connect()
    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, episodes TEXT, current_episode TEXT)')
    conn.commit()
    conn.close()

# insert data into database
def db_insert(title, episodes, current_episode):
    conn = db_connect()
    conn.execute('INSERT INTO posts (title, episodes, current_episode) VALUES (?, ?, ?)', (title, episodes, current_episode))
    conn.commit()
    conn.close()

# select data from database
def db_select():
    conn = db_connect()
    cur = conn.execute('SELECT * FROM posts')
    posts = cur.fetchall()
    conn.close()
    return posts

# delete data from database
def db_delete(id):
    conn = db_connect()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# update data from database
def db_update(id, title, episodes):
    conn = db_connect()
    conn.execute('UPDATE posts SET title = ?, episodes = ? WHERE id = ?', (title, episodes, id))
    conn.commit()
    conn.close()

# update current_episode from database
def db_update_current_episode(id, current_episode):
    conn = db_connect()
    conn.execute('UPDATE posts SET current_episode = ? WHERE id = ?', (current_episode, id))
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')

# show all posts through a post
@app.route('/shows', methods=['GET', 'POST'])
def shows():
    # if request.method == 'POST':
    posts = db_select()
    return render_template('shows.html', posts=posts)
    # return render_template('shows.html')

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        episodes = request.form['episodes']
        current_episode = request.form['current_episode']
        db_insert(title, episodes, current_episode)
        return redirect(url_for('shows'))
    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        db_delete(id)
        return redirect(url_for('shows'))
    return render_template('delete.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # if request.method == 'POST':
    current_episode = request.form['current_episode']
    db_update_current_episode(id, current_episode)
    return redirect(url_for('shows'))
    # return render_template('update.html')

if __name__ == '__main__':
    db_check()
    app.run(debug=True, host="0.0.0.0", port=4000)