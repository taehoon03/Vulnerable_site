import { useState } from 'react';
import { loginApi } from '../api/client';
import './LoginPage.css';

interface LoginResponse {
  status: string;
  leaked_data?: Array<{
    username: string;
    phone: string;
    email: string;
  }>;
  message?: string;
}

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<LoginResponse | null>(null);
  const [error, setError] = useState('');
  const [showExplanation, setShowExplanation] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await loginApi.login(username, password);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.message || '로그인 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>🔐 SQL Injection 실습</h1>
        
        <div className="info-section">
          <h3>📚 학습 목표</h3>
          <p>
            이 페이지는 SQL Injection 취약점을 체험하고 방어 방법을 학습하기 위한 
            교육용 플랫폼입니다.
          </p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">아이디</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="아이디를 입력하세요"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호를 입력하세요"
              disabled={loading}
            />
          </div>

          <button type="submit" disabled={loading} className="login-btn">
            {loading ? '로그인 중...' : '로그인'}
          </button>
        </form>

        <button 
          className="explanation-toggle"
          onClick={() => setShowExplanation(!showExplanation)}
        >
          {showExplanation ? '💡 설명 숨기기' : '💡 공격 방법 보기'}
        </button>

        {showExplanation && (
          <div className="explanation-box">
            <h4>🎯 SQL Injection 공격 예제</h4>
            <div className="attack-example">
              <p><strong>아이디:</strong> <code>' OR '1'='1' --</code></p>
              <p><strong>비밀번호:</strong> 아무거나</p>
            </div>
            <h4>⚙️ 작동 원리</h4>
            <pre>{`정상 쿼리:
SELECT * FROM users 
WHERE username='hong' AND password='1234'

공격 후 실행되는 쿼리:
SELECT * FROM users 
WHERE username='' OR '1'='1' --' AND password='...'

결과: '1'='1'은 항상 참이므로 모든 회원 정보가 반환됩니다!`}</pre>
            <h4>🛡️ 방어 방법</h4>
            <p>
              입력값을 SQL 쿼리에 직접 삽입하지 말고, 
              <strong>파라미터 바인딩(Prepared Statements)</strong>을 사용하세요.
            </p>
          </div>
        )}

        {error && (
          <div className="error-box">
            <p>❌ {error}</p>
          </div>
        )}

        {result && (
          <div className={`result-box ${result.status === 'success' ? 'success' : 'fail'}`}>
            <h3>
              {result.status === 'success' 
                ? '⚠️ 공격 성공!' 
                : '✅ 로그인 실패'}
            </h3>
            
            {result.status === 'success' && result.leaked_data ? (
              <div className="leaked-data">
                <p className="warning">
                  유출된 회원 정보 ({result.leaked_data.length}명):
                </p>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>아이디</th>
                      <th>전화</th>
                      <th>이메일</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.leaked_data.map((user, idx) => (
                      <tr key={idx}>
                        <td>{user.username}</td>
                        <td>{user.phone}</td>
                        <td>{user.email}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <p className="alert">
                  💥 비밀번호를 입력하지 않아도 전체 회원 정보가 유출되었습니다!
                </p>
              </div>
            ) : (
              <p>{result.message || '로그인이 거부되었습니다.'}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
