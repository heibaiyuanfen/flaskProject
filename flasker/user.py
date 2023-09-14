
from flask import (
    Blueprint, flash, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from flasker import db

bp = Blueprint('gpt', __name__, )
bp.route('/')

# 注册功能
@bp.route('/register', methods=['GET', 'POST'])
def register():

# 数据格式为formdata
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('请填写用户名和密码', 'error')
        else:
            conn = db.get_db()
            cursor = conn.cursor()

            # 检查用户名是否已存在
            cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                flash('该用户名已被注册', 'error')
            else:
                # 插入新用户信息到数据库
                hashed_password = generate_password_hash(password)
                cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()
                conn.close()
                flash('注册成功，请登录', 'success')
                # return redirect(url_for('login'))
                return  "login"

    # return render_template('register.html')
    return 1

# 登录功能
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('请填写用户名和密码', 'error')
        else:
            conn = db.get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                # 登录成功，将用户信息存储在session中
                session['user_id'] = user[0]
                flash('登录成功', 'success')
                # return redirect(url_for('dashboard'))
                return "dashboard"
            else:
                flash('用户名或密码不正确', 'error')

    # return render_template('login.html')
    return "login"
# 仪表盘页面（需要登录才能访问）
@bp.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # return render_template('dashboard.html')
        return "dashboard"
    else:
        # return redirect(url_for('login'))
        return "login"

# 注销功能
@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('已成功注销', 'success')
    # return redirect(url_for('login'))
    return "login"