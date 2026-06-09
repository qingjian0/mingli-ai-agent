import { useTheme } from '../lib/ThemeContext';

export default function Footer() {
  const { theme } = useTheme();
  const year = new Date().getFullYear();

  return (
    <footer
      style={{
        backgroundColor: theme.colors.surface,
        borderTop: `1px solid ${theme.colors.border}`,
        padding: '2rem 0',
        marginTop: '4rem',
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: '0 auto',
          padding: '0 1rem',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '1rem',
          color: theme.colors.textSecondary,
          fontSize: '0.9rem',
        }}
      >
        <div style={{ fontSize: '1.1rem', fontWeight: 600, color: theme.colors.text }}>
          术数推理命理智能体
        </div>
        <div style={{ textAlign: 'center' }}>
          <p style={{ margin: '0.25rem 0' }}>
            融合传统命理学与现代 AI 技术，为您提供可解释、可验证的命理分析
          </p>
          <p style={{ margin: '0.25rem 0' }}>
            支持八字、紫微斗数、奇门遁甲、大六壬、梅花易数、六爻、太乙数七大术数域
          </p>
        </div>
        <div
          style={{
            display: 'flex',
            gap: '1.5rem',
            marginTop: '0.5rem',
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          <span>📅 {year} 版权所有</span>
          <span>⚡ Powered by Next.js + FastAPI</span>
          <span>🔬 传统命理 × 人工智能</span>
        </div>
        <div style={{ textAlign: 'center', marginTop: '0.5rem', fontSize: '0.8rem', opacity: 0.8 }}>
          <p>本项目仅供学习研究使用，不得用于商业目的</p>
          <p>传统命理学是中国传统文化的重要组成部分，请理性看待，科学理解</p>
        </div>
      </div>
    </footer>
  );
}
