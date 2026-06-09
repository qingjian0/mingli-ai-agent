import Link from 'next/link';
import Layout from '../components/Layout';
import { useTheme } from '../lib/ThemeContext';

export default function HomePage() {
  const { theme } = useTheme();

  const domains = [
    { id: 'bazi', name: '八字', icon: '🀄', description: '四柱八字命理分析，大运流年推演', color: '#3b82f6' },
    { id: 'ziwei', name: '紫微斗数', icon: '⭐', description: '星曜宫位，洞察人生轨迹', color: '#8b5cf6' },
    { id: 'qimen', name: '奇门遁甲', icon: '🌀', description: '九宫八门，预测决策', color: '#10b981' },
    { id: 'liuren', name: '大六壬', icon: '🔯', description: '三传四课，干支推演', color: '#f59e0b' },
    { id: 'meihua', name: '梅花易数', icon: '🌸', description: '先天起卦，体用生克', color: '#ec4899' },
    { id: 'liuyao', name: '六爻', icon: '☯', description: '六爻断卦，六亲世应', color: '#6366f1' },
    { id: 'taiyi', name: '太乙数', icon: '🔮', description: '太乙神数，统运推算', color: '#14b8a6' },
  ];

  const features = [
    { title: '可解释性', desc: '每步计算有推理链追踪，透明可查', icon: '🧠' },
    { title: '多流派支持', desc: '支持传统命理多种流派，可对比分析', icon: '📚' },
    { title: '历史验证', desc: '基于历代名人案例库，回归测试验证', icon: '📜' },
    { title: 'AI 辅助', desc: '自然语言解释，智能问答辅助理解', icon: '🤖' },
  ];

  return (
    <Layout title="首页" description="术数推理命理智能体平台">
      {/* Hero Section */}
      <div
        style={{
          textAlign: 'center',
          padding: '4rem 1rem',
          background: `linear-gradient(135deg, ${theme.colors.primary}10 0%, ${theme.colors.accent}10 100%)`,
          borderRadius: '1.5rem',
          marginBottom: '3rem',
        }}
      >
        <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🔮</div>
        <h1
          style={{
            fontSize: '2.75rem',
            marginBottom: '1rem',
            background: `linear-gradient(135deg, ${theme.colors.primary} 0%, ${theme.colors.accent} 100%)`,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          术数推理命理智能体
        </h1>
        <p style={{ fontSize: '1.15rem', color: theme.colors.textSecondary, maxWidth: 600, margin: '0 auto 2rem' }}>
          融合传统命理学与现代 AI 技术，为您提供可解释、可验证、可追溯的命理分析
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link href="/calculator">
            <button
              style={{
                padding: '0.875rem 2rem',
                backgroundColor: theme.colors.primary,
                color: 'white',
                border: 'none',
                borderRadius: '0.5rem',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              🔍 立即排盘
            </button>
          </Link>
          <Link href="/figures">
            <button
              style={{
                padding: '0.875rem 2rem',
                backgroundColor: theme.colors.surface,
                color: theme.colors.text,
                border: `1px solid ${theme.colors.border}`,
                borderRadius: '0.5rem',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              📜 历史名人库
            </button>
          </Link>
        </div>
      </div>

      {/* 七大术数域 */}
      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '0.5rem' }}>七大术数域</h2>
        <p style={{ textAlign: 'center', color: theme.colors.textSecondary, marginBottom: '2rem' }}>
          涵盖中国传统命理主要流派与方法
        </p>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '1rem',
          }}
        >
          {domains.map((domain) => (
            <div
              key={domain.id}
              style={{
                padding: '1.5rem',
                backgroundColor: theme.colors.surface,
                borderRadius: '1rem',
                border: `1px solid ${theme.colors.border}`,
                transition: 'transform 0.2s ease',
                cursor: 'pointer',
              }}
            >
              <div
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: '0.75rem',
                  backgroundColor: `${domain.color}20`,
                  color: domain.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.75rem',
                  marginBottom: '1rem',
                }}
              >
                {domain.icon}
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{domain.name}</h3>
              <p style={{ color: theme.colors.textSecondary, fontSize: '0.95rem', lineHeight: 1.6 }}>
                {domain.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 核心特点 */}
      <section
        style={{
          backgroundColor: theme.colors.surface,
          padding: '2.5rem',
          borderRadius: '1.5rem',
          border: `1px solid ${theme.colors.border}`,
          marginBottom: '3rem',
        }}
      >
        <h2 style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '2rem' }}>核心特点</h2>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {features.map((feature, i) => (
            <div
              key={i}
              style={{
                textAlign: 'center',
                padding: '1.5rem',
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>{feature.icon}</div>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>{feature.title}</h3>
              <p style={{ color: theme.colors.textSecondary, fontSize: '0.9rem' }}>{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 快速入口 */}
      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '2rem' }}>快速开始</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <Link href="/calculator" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div
              style={{
                padding: '2rem',
                backgroundColor: `${theme.colors.primary}10`,
                borderRadius: '1rem',
                border: `2px solid ${theme.colors.primary}30`,
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>🧮</div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: theme.colors.primary }}>命盘计算器</h3>
              <p style={{ color: theme.colors.textSecondary, fontSize: '0.95rem' }}>
                输入出生日期时间，获得完整命盘
              </p>
            </div>
          </Link>
          <Link href="/figures" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div
              style={{
                padding: '2rem',
                backgroundColor: `${theme.colors.accent}10`,
                borderRadius: '1rem',
                border: `2px solid ${theme.colors.accent}30`,
                cursor: 'pointer',
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>👤</div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: theme.colors.accent }}>历史名人库</h3>
              <p style={{ color: theme.colors.textSecondary, fontSize: '0.95rem' }}>
                浏览历史名人命理案例，对比分析
              </p>
            </div>
          </Link>
          <Link href="/chat" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div
              style={{
                padding: '2rem',
                backgroundColor: theme.colors.surface,
                borderRadius: '1rem',
                border: `1px solid ${theme.colors.border}`,
                cursor: 'pointer',
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>💬</div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>智能问答</h3>
              <p style={{ color: theme.colors.textSecondary, fontSize: '0.95rem' }}>
                与 AI 对话，深入了解命盘含义
              </p>
            </div>
          </Link>
        </div>
      </section>
    </Layout>
  );
}
