from flask import Flask, request, Response
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = 'shop.db'

def json_response(data):
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

def init_db():
    conn = sqlite3.connect(DB_PATH)
    # 기존 테이블 삭제 후 재생성
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("DROP TABLE IF EXISTS posts")
    conn.execute("DROP TABLE IF EXISTS accounts")
    conn.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT, password TEXT,
        phone TEXT, email TEXT
    )''')
    conn.execute('''CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        content TEXT, author TEXT
    )''')
    conn.execute('''CREATE TABLE accounts (
        id INTEGER PRIMARY KEY,
        username TEXT, balance INTEGER
    )''')
    # 더미 데이터
    conn.execute("INSERT INTO users VALUES (1,'관리자','admin1234','010-1234-5678','admin@naver.com')")
    conn.execute("INSERT INTO users VALUES (2,'하태훈','taehoon124','010-5876-5432','taehoon@gmail.com')")
    conn.execute("INSERT INTO users VALUES (3,'김철수','kim5678','010-1111-2222','kim@wuk.ac.kr')")
    conn.execute("INSERT INTO accounts VALUES (1,'김도영',1000000)")
    conn.execute("INSERT INTO accounts VALUES (2,'김중규',500000)")
    conn.commit()
    conn.close()
       

# SQL Injection 취약한 로그인
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            result = conn.execute(query).fetchall()
            if result:
                return json_response({
                    "status": "success",
                    "leaked_data": [{"username": r[1], "phone": r[3], "email": r[4]} for r in result]
                })
            return json_response({"status": "fail", "message": "로그인 실패"})
        except Exception as e:
            return json_response({"status": "error", "message": str(e)})
    return render_template_string('''
        <h2>🛒 ShopDemo 로그인</h2>
        <form method="post">
            아이디:   <input name="username"><br><br>
            비밀번호:  <input name="password"><br><br>
            <input type="submit" value="로그인">
        </form>
    ''')

# XSS 취약한 게시판
@app.route('/board', methods=['GET','POST'])
def board():
    conn = sqlite3.connect(DB_PATH)
    if request.method == 'POST':
        content = request.form['content']
        author = request.form['author']
        conn.execute("INSERT INTO posts (content, author) VALUES (?, ?)", (content, author))
        conn.commit()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    posts_html = ''.join([f"<div><b>{p[2]}</b>: {p[1]}</div>" for p in posts])
    
    html = f"""
    <h2>📋 게시판</h2>
    <form method="post">
        이름: <input name="author"><br><br>
        내용: <input name="content"><br><br>
        <input type="submit" value="작성">
    </form>
    <hr>
    {posts_html}
    """
    return Response(html, mimetype='text/html')

# CSRF 취약한 송금
@app.route('/transfer', methods=['GET','POST'])
def transfer():
    conn = sqlite3.connect(DB_PATH)
    if request.method == 'POST':
        amount = request.form['amount']
        to_user = request.form['to']
        conn.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE username = '홍길동'")
        conn.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE username = '{to_user}'")
        conn.commit()
        return jsonify({"status": "success", "message": f"{amount}원이 {to_user}에게 이체됐습니다"})
    accounts = conn.execute("SELECT * FROM accounts").fetchall()
    accounts_html = ''.join([f"<div>{a[1]}: {a[2]}원</div>" for a in accounts])
    return render_template_string(f'''
        <h2>💸 송금</h2>
        {accounts_html}
        <hr>
        <form method="post">
            받는 사람: <input name="to"><br><br>
            금액: <input name="amount"><br><br>
            <input type="submit" value="송금">
        </form>
    ''')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

