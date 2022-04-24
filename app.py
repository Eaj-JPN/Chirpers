from flask import (
    Flask, request, render_template, session, flash, redirect, url_for, jsonify
)

from db import db_connection
import re

app = Flask(__name__)
app.secret_key = 'IAMMENTALLYSICKINEEDHELPPLEASE'

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ function to show and process login page """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = db_connection()
        cur = conn.cursor()
        sql = """
            SELECT id, username
            FROM users
            WHERE username = '%s' AND password = '%s'
        """ % (username, password)
        cur.execute(sql)
        user = cur.fetchone()

        error = ''
        if user is None:
            error = 'Wrong credentials. No user found'
        else:
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))

        flash(error)
        cur.close()
        conn.close()

    return render_template('account/login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form:

        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        conn = db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cur.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.search(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not name:
            msg = 'Please fill out the form!'
        elif (len(password)<5):
            msg = 'Password must be minimum 5 character'
        elif not re.search("[A-Z]", password):
            msg = 'Password must contain 1 Uppercase'
        else:
            sql = """
            INSERT INTO users (username, name, password) VALUES ('%s', '%s', '%s');
            """ % (username, name, password)
            cur.execute(sql)
            conn.commit()
            return redirect(url_for('index'))

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('account/signup.html', msg=msg)

@app.route('/logout')
def logout():
    """ function to do logout """
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    chirps = get_all_chirps()
    return render_template('index.html', chirps=chirps)

@app.route('/chirp/<int:chirp_id>', methods=['GET'])
def read(chirp_id):
    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT chr.id, chr.title, usr.username, chr.body
        FROM chirps chr
        JOIN users usr on usr.id = chr.user_id
        WHERE chr.id = %d
    """ % chirp_id
    cur.execute(sql)
    chirp = cur.fetchone()
    cur.close()
    db.close()

    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT usr.username, cmt.body, cmt.id
        FROM commentary cmt
        JOIN users usr on usr.id = cmt.user_id
        WHERE cmt.chirp_id = %d
        ORDER BY cmt.id
    """ % chirp_id
    cur.execute(sql)
    comments = cur.fetchall()
    cur.close()
    db.close()

    return render_template('chirp/view.html', chirp=chirp, comments=comments,)

@app.route('/chirp/create', methods=['GET', 'POST'])
def create():
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json() or {}
        # check existence of title and body
        if data.get('title') and data.get('body'):
            user_id = session.get('user_id')
            title = data.get('title', '')
            body = data.get('body', '')

            title = title.strip()
            body = body.strip()

            conn = db_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO chirps (user_id, title, body) VALUES (%d, '%s', '%s')
            """ % (user_id, title, body)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 200, 'message': 'Success', 'redirect': '/'})

        return jsonify({'status': 500, 'message': 'No Data submitted'})

    return render_template('chirp/create.html')

@app.route('/chirp/delete/<int:chirp_id>', methods=['GET', 'POST'])
def delete(chirp_id):
    if not session:
        return redirect(url_for('login'))

    conn = db_connection()
    cur = conn.cursor()
    sql = """
        DELETE FROM commentary WHERE chirp_id = %s;
        DELETE FROM chirps WHERE id = %s 
    """ % (chirp_id,chirp_id)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return jsonify({'status': 200, 'redirect': '/'})

@app.route('/chirp/edit/<int:chirp_id>', methods=['GET', 'POST'])
def edit(chirp_id):
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = db_connection()
        cur = conn.cursor()

        title = request.form['title']
        body = request.form['body']

        title = title.strip()
        body = body.strip()

        sql_params = (title, body, chirp_id)

        sql = "UPDATE chirps SET title = '%s', body = '%s' WHERE id = %s" % sql_params
        print(sql)
        cur.execute(sql)

        cur.close()
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = db_connection()
    cur = conn.cursor()
    sql = 'SELECT id, title, body FROM chirps WHERE id = %s' % chirp_id
    cur.execute(sql)
    chirp = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('chirp/edit.html', chirp=chirp)

def get_all_chirps():
    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT chirps.title, users.username, chirps.body, chirps.id
        FROM chirps
        JOIN users ON chirps.user_id = users.id
        ORDER BY chirps.id
    """
    cur.execute(sql)
    chirp = cur.fetchall()
    cur.close()
    db.close()
    return chirp

@app.route("/comment/create/<int:chirp_id>", methods = ["GET", "POST"])
def createCmt(chirp_id):

    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT chirps.id
        FROM chirps chirps
        WHERE chirps.id = %d
    """ % chirp_id
    cur.execute(sql)
    chirps = cur.fetchone()
    cur.close()
    db.close()

    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json() or {}
        if data.get('body'):
            user_id = session.get('user_id')
            body = data.get('body', '')          
            
            body = body.strip()
            sql_params = (chirp_id, user_id, body)

            conn = db_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO commentary (chirp_id, user_id, body) VALUES (%d, %d, '%s')
            """ % sql_params
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 200, 'message': 'Success', 'redirect': '/'})

        return jsonify({'status': 500, 'message': 'No Data submitted'})

    return render_template('comment/create.html', chirp_id=chirps)

@app.route('/comment/delete/<int:cmt_id>', methods=['GET', 'POST'])
def deleteCmt(cmt_id):
    if not session:
        return redirect(url_for('login'))

    conn = db_connection()
    cur = conn.cursor()
    sql = """
        DELETE FROM commentary WHERE id = %d;
    """ % (cmt_id)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return jsonify({'status': 200, 'redirect': '/'})