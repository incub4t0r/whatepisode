from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(ROOT, 'database.db')

app = Flask(__name__)

#####################
# databse functions #
#####################

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

# update number of episodes from database
def db_update_episodes(id, episodes):
    conn = db_connect()
    conn.execute('UPDATE posts SET episodes = ? WHERE id = ?', (episodes, id))
    conn.commit()
    conn.close()

# update title from database
def db_update_title(id, title):
    conn = db_connect()
    conn.execute('UPDATE posts SET title = ? WHERE id = ?', (title, id))
    conn.commit()
    conn.close()

# update current_episode from database
def db_update_current_episode(id, current_episode):
    conn = db_connect()
    conn.execute('UPDATE posts SET current_episode = ? WHERE id = ?', (current_episode, id))
    conn.commit()
    conn.close()

# get number of episodes from databse
def db_get_episodes(id):
    conn = db_connect()
    cur = conn.execute('SELECT episodes FROM posts WHERE id = ?', (id,))
    episodes = cur.fetchone()
    conn.close()
    return episodes

# get current_episode from databse
def db_get_current_episode(id):
    conn = db_connect()
    cur = conn.execute('SELECT current_episode FROM posts WHERE id = ?', (id,))
    current_episode = cur.fetchone()
    conn.close()
    return current_episode

#####################
# Main page         #
#####################

# home page
@app.route('/')
def home():
    posts = db_select()
    return render_template('home.html', posts=posts)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    posts = db_select()
    return render_template('manager.html', posts=posts)


#####################
# API endpoints     #
#####################

# add a new post
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        episodes = request.form['episodes']
        current_episode = request.form['current_episode']
        db_insert(title, episodes, current_episode)
        return redirect(url_for('home'))
    return render_template('add.html')

# delete a post
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        db_delete(id)
    return redirect(url_for('manager'))

# update a post's current_episode
@app.route('/update/current_episode/<int:id>', methods=['GET', 'POST'])
def update_current_episode(id):
    if request.method == 'POST':
        total_episodes = db_get_episodes(id)[0]
        current_episode = request.form['current_episode']
        if (int(current_episode) <= int(total_episodes)):
            db_update_current_episode(id, current_episode)
    return redirect(url_for('home'))
    # return render_template('update.html')

# update a post's current_episode
@app.route('/update/current_episode/increment/<int:id>', methods=['GET', 'POST'])
def increment_curr_episode(id):
    if request.method == 'POST':
        total_episodes = int(db_get_episodes(id)[0])
        current_episode = int(db_get_current_episode(id)[0])
        if (current_episode < total_episodes):
            db_update_current_episode(id, str(current_episode+1))
    return redirect(url_for('home'))

# update a post's current_episode
@app.route('/update/current_episode/decrement/<int:id>', methods=['GET', 'POST'])
def decrement_curr_episode(id):
    if request.method == 'POST':
        current_episode = int(db_get_current_episode(id)[0])
        if (int(current_episode) > 0):
            db_update_current_episode(id, str(current_episode-1))
    return redirect(url_for('home'))


# update a post's total number of episodes
@app.route('/update/episodes/<int:id>', methods=['GET', 'POST'])
def update_episodes(id):
    if request.method == 'POST':
        episodes = request.form['episodes']
        db_update_episodes(id, episodes)
        # total_episodes = db_get_episodes(id)[0]
        # current_episode = request.form['current_episode']
        # if (int(current_episode) <= int(total_episodes)):
        #     db_update_current_episode(id, current_episode)
        return redirect(url_for('manager'))
    return redirect(url_for('home'))

# update a post's title
@app.route('/update/title/<int:id>', methods=['GET', 'POST'])
def update_title(id):
    if request.method == 'POST':
        title = request.form['title']
        db_update_title(id, title)
        return redirect(url_for('manager'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    db_check()
    app.run(debug=True, host="0.0.0.0", port=4000)