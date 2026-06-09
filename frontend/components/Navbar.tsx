import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import { useTheme } from '../lib/ThemeContext';

export default function Navbar() {
  const router = useRouter();
  const { theme, cycleTheme } = useTheme();
  const [isMobile, setIsMobile] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const navItems = [
    { href: '/', label: '首页' },
    { href: '/calculator', label: '命盘计算器' },
    { href: '/figures', label: '历史名人' },
    { href: '/reasoning', label: '推理链' },
    { href: '/chat', label: '智能问答' },
    { href: '/settings', label: '主题设置' },
  ];

  const isActive = (href: string) => {
    if (href === '/') {
      return router.pathname === '/';
    }
    return router.pathname.startsWith(href);
  };

  const renderNavLinks = () => (
    navItems.map((item) => {
      const active = isActive(item.href);
      return (
        <Link key={item.href} href={item.href}>
          <div
            style={{
              padding: isMobile ? '0.75rem 1rem' : '0.5rem 1rem',
              borderRadius: '0.5rem',
              color: active ? theme.colors.primary : theme.colors.textSecondary,
              backgroundColor: active ? 'rgba(37, 99, 235, 0.1)' : 'transparent',
              cursor: 'pointer',
              fontSize: isMobile ? '1rem' : '0.95rem',
              fontWeight: 500,
              transition: 'all 0.2s ease',
            }}
            onClick={() => setMobileMenuOpen(false)}
          >
            {item.label}
          </div>
        </Link>
      );
    })
  );

  return (
    <nav
      style={{
        backgroundColor: theme.colors.surface,
        borderBottom: `1px solid ${theme.colors.border}`,
        padding: '1rem 0',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        backdropFilter: 'saturate(180%) blur(10px)',
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: '0 auto',
          padding: isMobile ? '0 0.75rem' : '0 1rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1rem',
        }}
      >
        {/* Logo */}
        <Link href="/" style={{ textDecoration: 'none' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div
              style={{
                width: 36,
                height: 36,
                borderRadius: '50%',
                backgroundColor: theme.colors.primary,
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.25rem',
                fontWeight: 700,
              }}
            >
              命
            </div>
            {!isMobile && (
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: theme.colors.text }}>
                术数推理命理智能体
              </div>
            )}
          </div>
        </Link>

        {/* 桌面导航 */}
        {!isMobile && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            {renderNavLinks()}
            <button
              onClick={cycleTheme}
              style={{
                padding: '0.625rem 1.25rem',
                borderRadius: '0.5rem',
                fontWeight: 500,
                fontSize: '0.95rem',
                backgroundColor: theme.colors.surface,
                color: theme.colors.text,
                border: `1px solid ${theme.colors.border}`,
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                marginLeft: '1rem',
              }}
              title="切换主题"
            >
              🌓 {theme.name}
            </button>
          </div>
        )}

        {/* 移动端菜单按钮 */}
        {isMobile && (
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{
              padding: '0.5rem',
              color: theme.colors.text,
              cursor: 'pointer',
              fontSize: '1.5rem',
            }}
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>
        )}
      </div>

      {/* 移动端菜单 */}
      {isMobile && mobileMenuOpen && (
        <div
          style={{
            maxWidth: 1200,
            margin: '1rem auto 0',
            padding: '0 0.75rem 1rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem',
            borderTop: `1px solid ${theme.colors.border}`,
            paddingTop: '1rem',
          }}
        >
          {renderNavLinks()}
          <button
            onClick={() => {
              cycleTheme();
              setMobileMenuOpen(false);
            }}
            style={{
              padding: '0.75rem 1rem',
              borderRadius: '0.5rem',
              fontWeight: 500,
              fontSize: '1rem',
              backgroundColor: theme.colors.surface,
              color: theme.colors.text,
              border: `1px solid ${theme.colors.border}`,
              cursor: 'pointer',
              marginTop: '0.5rem',
            }}
          >
            🌓 切换主题 ({theme.name})
          </button>
        </div>
      )}
    </nav>
  );
}
