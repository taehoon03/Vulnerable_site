import './HomePage.css';

interface HomePageProps {
  setPage: (page: string) => void;
}

export default function HomePage({ setPage }: HomePageProps) {
  return (
    <div className="home-container">
      {/* ==================== HERO SECTION ==================== */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">🔐 웹 취약점 학습 플랫폼</h1>
          <p className="hero-subtitle">
            실제 공격 사례를 안전하게 체험하며 웹 보안을 배웁니다
          </p>

          <div className="hero-buttons">
            <button 
              onClick={() => setPage('login')}
              className="btn btn-primary"
            >
              🔐 SQL Injection 시작
            </button>
            <button 
              onClick={() => setPage('board')}
              className="btn btn-secondary"
            >
              💬 XSS 체험하기
            </button>
          </div>
        </div>
      </section>

      {/* ==================== MODULES SECTION ==================== */}
      <section className="modules-section">
        <h2 className="section-title">📚 학습 모듈</h2>
        <div className="modules-grid">
          {/* SQL Injection Card */}
          <article className="module-card">
            <div className="card-header">
              <div className="card-icon">🔐</div>
              <h3>SQL Injection</h3>
            </div>
            
            <p className="card-description">
              데이터베이스 쿼리 조작을 통한 공격을 직접 체험합니다
            </p>

            <ul className="card-learnings">
              <li>입력 검증의 중요성</li>
              <li>데이터베이스 보안</li>
              <li>파라미터 바인딩</li>
            </ul>

            <div className="card-footer">
              <span className="difficulty">난이도: ⭐ 초급</span>
              <button 
                onClick={() => setPage('login')}
                className="btn btn-small"
              >
                시작하기 →
              </button>
            </div>
          </article>

          {/* XSS Card */}
          <article className="module-card">
            <div className="card-header">
              <div className="card-icon">💬</div>
              <h3>XSS (Cross-Site Scripting)</h3>
            </div>
            
            <p className="card-description">
              클라이언트 측 스크립트 공격을 직접 실행해 봅니다
            </p>

            <ul className="card-learnings">
              <li>JavaScript 실행 원리</li>
              <li>DOM 보안</li>
              <li>입력 이스케이프</li>
            </ul>

            <div className="card-footer">
              <span className="difficulty">난이도: ⭐ 초급</span>
              <button 
                onClick={() => setPage('board')}
                className="btn btn-small"
              >
                시작하기 →
              </button>
            </div>
          </article>
        </div>
      </section>

      {/* ==================== HOW-TO SECTION ==================== */}
      <section className="how-to-section">
        <h2 className="section-title">🚀 시작하기</h2>
        <ol className="steps-list">
          <li className="step-item">
            <span className="step-number">1</span>
            <div className="step-content">
              <h4>원하는 모듈 선택</h4>
              <p>위의 카드에서 SQL Injection 또는 XSS 중 선택하세요</p>
            </div>
          </li>
          <li className="step-item">
            <span className="step-number">2</span>
            <div className="step-content">
              <h4>공격 시뮬레이션</h4>
              <p>실제 보안 취약점을 안전한 환경에서 체험해봅시다</p>
            </div>
          </li>
          <li className="step-item">
            <span className="step-number">3</span>
            <div className="step-content">
              <h4>방어 기법 학습</h4>
              <p>각 공격에 대한 방어 방법을 배웁니다</p>
            </div>
          </li>
        </ol>
      </section>

      {/* ==================== FEATURES SECTION ==================== */}
      <section className="features-section">
        <h2 className="section-title">✨ 특징</h2>
        <ul className="features-list">
          <li className="feature-item">
            <span className="feature-icon">🎯</span>
            <span className="feature-text">실습 중심 학습</span>
          </li>
          <li className="feature-item">
            <span className="feature-icon">🛡️</span>
            <span className="feature-text">방어 기법 설명</span>
          </li>
          <li className="feature-item">
            <span className="feature-icon">📚</span>
            <span className="feature-text">단계별 학습</span>
          </li>
          <li className="feature-item">
            <span className="feature-icon">💻</span>
            <span className="feature-text">모바일 대응</span>
          </li>
        </ul>
      </section>

      {/* ==================== WARNING SECTION ==================== */}
      <section className="warning-section">
        <h3>⚠️ 중요한 안내</h3>
        <p>
          이 플랫폼은 <strong>교육 목적으로만</strong> 설계되었습니다.
          다른 사람의 시스템을 승인 없이 공격하는 것은 범죄입니다.
        </p>
      </section>
    </div>
  );
}
