from flask import Flask, render_template, request, redirect, session, url_for, flash
from sql_connect import (
    add_to_table, check_in_table, get_user_id,
    add_anime, get_anime_list
)

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'  # Required for session

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['password']
        add_to_table(username, password)
        flash('Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('create.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['password']
        if check_in_table(username, password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('anime_list'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/anime_list', methods=['GET', 'POST'])
def anime_list():
    if 'user' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))

    user = session['user']
    user_id = get_user_id(user)

    if request.method == 'POST':
        name = request.form['name']
        season = request.form['season']
        episode = request.form['episode']
        add_anime(user_id, name, season, episode)
        flash('Anime added!', 'success')

    entries = get_anime_list(user_id)
    return render_template('anime_list.html', user=user, anime_entries=entries)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
