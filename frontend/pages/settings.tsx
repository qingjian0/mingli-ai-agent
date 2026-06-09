import { useTheme } from '../lib/ThemeContext';
import Layout from '../components/Layout';

export default function SettingsPage() {
  const { theme, mode, setMode } = useTheme();

  const themes = [
    { id: 'modern', name: '现代简约', desc: '干净简洁的现代设计风格', emoji: '🎨' },
    { id: 'traditional', name: '传统中式', desc: '古典红木风格，富有传统韵味', emoji: '🏯' },
    { id: 'data-viz', name: '数据可视化', desc: '深色主题，适合图表展示', emoji: '📊' },
  ];

  const wuxingList = [
    { key: 'jin', name: '金', cn: '金' },
    { key: 'mu', name: '木', cn: '木' },
    { key: 'shui', name: '水', cn: '水' },
    { key: 'huo', name: '火', cn: '火' },
    { key: 'tu', name: '土', cn: '土' },
  ];

  return (
    <Layout title="主题设置" description="界面主题与偏好设置">
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>⚙️ 主题设置</h1>
          <p style={{ fontSize: '1.1rem', color: theme.colors.textSecondary }}>
            选择您喜欢的界面风格
          </p>
        </div>

        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1rem', marginBottom: '3rem',
        }}>
          {themes.map((t) => (
            <button key={t.id} onClick={() => setMode(t.id as any)}
              style={{
                padding: '2rem 1.5rem', textAlign: 'left', cursor: 'pointer',
                backgroundColor: mode === t.id ? theme.colors.primary : theme.colors.surface,
                color: mode === t.id ? 'white' : theme.colors.text,
                borderRadius: '1rem',
                border: `2px solid ${mode === t.id ? theme.colors.primary : theme.colors.border}`,
                transition: 'all 0.2s ease',
              }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>{t.emoji}</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>{t.name}</div>
              <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>{t.desc}</div>
              {mode === t.id && (
                <div style={{ marginTop: '1rem', fontSize: '0.875rem', fontWeight: 600 }}>✓ 当前选中</div>
              )}
            </button>
          ))}
        </div>

        <div style={{
          backgroundColor: theme.colors.surface, padding: '2rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
        }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>🎯 当前主题配色</h2>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
            gap: '0.75rem',
          }}>
            <div style={{
              padding: '1.25rem', backgroundColor: theme.colors.primary, color: 'white',
              borderRadius: '0.5rem', textAlign: 'center',
            }}>
              <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>主色</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, marginTop: '0.25rem' }}>Primary</div>
            </div>
            <div style={{
              padding: '1.25rem', backgroundColor: theme.colors.accent, color: 'white',
              borderRadius: '0.5rem', textAlign: 'center',
            }}>
              <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>强调色</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, marginTop: '0.25rem' }}>Accent</div>
            </div>
            <div style={{
              padding: '1.25rem', backgroundColor: theme.colors.success, color: 'white',
              borderRadius: '0.5rem', textAlign: 'center',
            }}>
              <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>成功</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, marginTop: '0.25rem' }}>Success</div>
            </div>
            <div style={{
              padding: '1.25rem', backgroundColor: theme.colors.warning, color: 'white',
              borderRadius: '0.5rem', textAlign: 'center',
            }}>
              <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>警告</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, marginTop: '0.25rem' }}>Warning</div>
            </div>
          </div>

          <h3 style={{ fontSize: '1.1rem', marginTop: '2rem', marginBottom: '0.75rem' }}>🪵 五行配色</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.75rem' }}>
            {wuxingList.map((el) => (
              <div key={el.key} style={{
                padding: '1.25rem',
                backgroundColor: (theme.colors.wuxing as any)[el.key] || '#888',
                color: 'white', borderRadius: '0.5rem', textAlign: 'center',
                fontSize: '1.25rem', fontWeight: 700,
              }}>
                {el.cn}
              </div>
            ))}
          </div>
        </div>

        <div style={{
          marginTop: '2rem', padding: '1.5rem', backgroundColor: theme.colors.surface,
          borderRadius: '1rem', border: `1px solid ${theme.colors.border}`,
          color: theme.colors.textSecondary, fontSize: '0.9rem', textAlign: 'center',
        }}>
          💡 提示：主题偏好会自动保存在本地，下次访问时自动使用上次选择的主题
        </div>
      </div>
    </Layout>
  );
}
