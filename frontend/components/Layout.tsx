import { ReactNode } from 'react';
import Head from 'next/head';
import Navbar from './Navbar';
import Footer from './Footer';
import { useTheme } from '../lib/ThemeContext';

interface LayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

export default function Layout({ children, title, description }: LayoutProps) {
  const { theme } = useTheme();
  const pageTitle = title ? `${title} - 术数推理命理智能体` : '术数推理命理智能体';
  const pageDescription = description || '融合传统命理学与现代 AI 技术，提供八字、紫微斗数、奇门遁甲、大六壬、梅花易数、六爻、太乙数等七大术数域的综合分析与推演';

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        backgroundColor: theme.colors.background,
        color: theme.colors.text,
      }}
    >
      <Head>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta charSet="utf-8" />
        <link rel="icon" href="/favicon.ico" />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:type" content="website" />
      </Head>

      <Navbar />

      <main
        style={{
          flex: 1,
          width: '100%',
        }}
      >
        <div
          style={{
            maxWidth: 1200,
            margin: '0 auto',
            padding: '2rem 1rem',
          }}
        >
          {children}
        </div>
      </main>

      <Footer />
    </div>
  );
}
