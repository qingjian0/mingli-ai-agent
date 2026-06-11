export type ThemeMode = 'modern' | 'traditional' | 'data-viz';

export interface WuxingColors {
  jin: string;
  mu: string;
  shui: string;
  huo: string;
  tu: string;
  [key: string]: string;
}

export interface ThemeConfig {
  mode: ThemeMode;
  name: string;
  description: string;
  colors: {
    primary: string;
    secondary: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
    accent: string;
    success: string;
    warning: string;
    error: string;
    wuxing: WuxingColors;
  };
  fonts: {
    body: string;
    heading: string;
    chinese: string;
  };
}

export const themes: Record<ThemeMode, ThemeConfig> = {
  modern: {
    mode: 'modern',
    name: '现代简约',
    description: '简洁现代的设计风格',
    colors: {
      primary: '#2563eb',
      secondary: '#475569',
      background: '#ffffff',
      surface: '#f8fafc',
      text: '#1e293b',
      textSecondary: '#64748b',
      border: '#e2e8f0',
      accent: '#8b5cf6',
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      wuxing: {
        jin: '#9ca3af',
        mu: '#22c55e',
        shui: '#3b82f6',
        huo: '#ef4444',
        tu: '#f59e0b',
      },
    },
    fonts: {
      body: 'system-ui, -apple-system, sans-serif',
      heading: 'system-ui, -apple-system, sans-serif',
      chinese: '"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif',
    },
  },
  traditional: {
    mode: 'traditional',
    name: '传统中式',
    description: '古典红木风格',
    colors: {
      primary: '#8b4513',
      secondary: '#a0522d',
      background: '#f5f0e8',
      surface: '#ebe0d0',
      text: '#2c1810',
      textSecondary: '#5c4033',
      border: '#8b4513',
      accent: '#b8860b',
      success: '#2e7d32',
      warning: '#f57c00',
      error: '#c62828',
      wuxing: {
        jin: '#fff8dc',
        mu: '#8fbc8f',
        shui: '#4682b4',
        huo: '#cd5c5c',
        tu: '#deb887',
      },
    },
    fonts: {
      body: '"Noto Serif SC", "SimSun", serif',
      heading: '"Noto Serif SC", "SimSun", serif',
      chinese: '"Noto Serif SC", "KaiTi", "STKaiti", serif',
    },
  },
  'data-viz': {
    mode: 'data-viz',
    name: '数据可视化',
    description: '深色主题，适合图表展示',
    colors: {
      primary: '#3b82f6',
      secondary: '#10b981',
      background: '#0f172a',
      surface: '#1e293b',
      text: '#f1f5f9',
      textSecondary: '#94a3b8',
      border: '#334155',
      accent: '#8b5cf6',
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      wuxing: {
        jin: '#94a3b8',
        mu: '#22c55e',
        shui: '#06b6d4',
        huo: '#f43f5e',
        tu: '#f59e0b',
      },
    },
    fonts: {
      body: 'system-ui, -apple-system, sans-serif',
      heading: 'system-ui, -apple-system, sans-serif',
      chinese: '"Noto Sans SC", "PingFang SC", sans-serif',
    },
  },
};

export const defaultTheme: ThemeMode = 'modern';
