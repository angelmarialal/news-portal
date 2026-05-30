from flask import Flask, render_template, request, redirect, session,flash,url_for
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import bcrypt
import os

app = Flask(__name__)

app.secret_key = 'secretkey'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MYSQL CONFIG
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'newsuser'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'news_portal'

mysql = MySQL(app)

# HOME PAGE
@app.route('/')
def home():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM posts ORDER BY id DESC")

    posts = cursor.fetchall()

    return render_template('index.html', posts=posts)
@app.route('/admin')
def admin():

    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]

    return render_template(
        'admin.html',
        total_users=total_users,
        total_posts=total_posts
    )
# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']

        password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'),
            bcrypt.gensalt()
        )

        cursor = mysql.connection.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name,email,password)
        )

        mysql.connection.commit()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user:

            if bcrypt.checkpw(
                password.encode('utf-8'),
                user['password'].encode('utf-8')
            ):

                session['loggedin'] = True
                session['name'] = user['name']
                session['role'] = user['role']

                return redirect('/dashboard')

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:

        return render_template('dashboard.html')

    return redirect('/login')

# ADD POST
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():

    if 'loggedin' not in session:
        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        image = request.files['image']

        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        author = session['name']

        cursor = mysql.connection.cursor()

        cursor.execute(
            "INSERT INTO posts(title,content,image,author) VALUES(%s,%s,%s,%s)",
            (title,content,filename,author)
        )

        mysql.connection.commit()

        return redirect('/')

    return render_template('add_post.html')

# DELETE POST
@app.route('/delete_post/<int:id>')
def delete_post(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM posts WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    return redirect('/')

# EDIT POST
@app.route('/edit_post/<int:id>', methods=['GET','POST'])
def edit_post(id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        cursor.execute(
            "UPDATE posts SET title=%s, content=%s WHERE id=%s",
            (title,content,id)
        )

        mysql.connection.commit()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM posts WHERE id=%s",
        (id,)
    )

    post = cursor.fetchone()

    return render_template('edit_post.html', post=post)

# SEARCH
@app.route('/search')
def search():

    keyword = request.args.get('keyword')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM posts WHERE title LIKE %s",
        ('%' + keyword + '%',)
    )

    posts = cursor.fetchall()

    return render_template('index.html', posts=posts)

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
