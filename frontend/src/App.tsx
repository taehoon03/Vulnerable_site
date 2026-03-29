import { useState } from 'react';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import BoardPage from './pages/BoardPage';
import './App.css';

function App() {
  const [page, setPage] = useState('home');

  return (
    <div className="app">
      {/* ==================== HEADER ==================== */}
      {/* 피츠의 법칙: 주요 네비게이션을 상단에 고정 배치 */}
      <header className="app-header">
        <div className="header-content">
          <button 
            onClick={() => setPage('home')} 
            className="logo-button"
          >
            🔐 보안 학습
          </button>
          
          {/* 피츠의 법칙 & 힉의 법칙: 3개 주요 선택지만 표시 (밀러의 법칙) */}
          <nav className="main-nav">
            <button 
              onClick={() => setPage('home')}
              className={`nav-button ${page === 'home' ? 'active' : ''}`}
            >
              <span className="nav-icon">🏠</span>
              <span className="nav-label">홈</span>
            </button>
            
            <button 
              onClick={() => setPage('login')}
              className={`nav-button ${page === 'login' ? 'active' : ''}`}
            >
              <span className="nav-icon">🔐</span>
              <span className="nav-label">SQL</span>
            </button>
            
            <button 
              onClick={() => setPage('board')}
              className={`nav-button ${page === 'board' ? 'active' : ''}`}
            >
              <span className="nav-icon">💬</span>
              <span className="nav-label">XSS</span>
            </button>
          </nav>
        </div>
      </header>

      {/* ==================== MAIN CONTENT ==================== */}
      <main className="app-main">
        {/* 힉의 법칙: 명확한 상태 표시로 사용자 인지 부하 감소 */}
        {page === 'home' && <HomePage setPage={setPage} />}
        {page === 'login' && <LoginPage />}
        {page === 'board' && <BoardPage />}
      </main>

      {/* ==================== FOOTER ==================== */}
      <footer className="app-footer">
        <p> 웹 보안 교육 플랫폼 | 교육 목적으로만 사용하세요</p>
      </footer>
    </div>
  );
}

export default App;
