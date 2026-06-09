import { useState } from 'react';
import Layout from '../components/Layout';
import { DomainChart } from '../components/Charts';
import { useTheme } from '../lib/ThemeContext';
import {
  calculateBazi, calculateZiwei, calculateQimen, calculateLiuren,
  calculateMeihua, calculateLiuyao, calculateTaiyi,
} from '../lib/api';
import type {
  ApiResponse, BaziResult, ZiweiResult, QimenResult, LiurenResult,
  MeihuaResult, LiuyaoResult, TaiyiResult,
} from '../lib/types';

type AllResults = BaziResult | ZiweiResult | QimenResult | LiurenResult | MeihuaResult | LiuyaoResult | TaiyiResult;

interface DomainOption {
  id: string;
  name: string;
  description: string;
  calculate: (params: { birth_date: string; birth_time: string; timezone: string; location: string; gender: string }) => Promise<ApiResponse<AllResults>>;
}

const DOMAINS: DomainOption[] = [
  { id: 'bazi', name: '八字', description: '四柱八字命理分析', calculate: calculateBazi as any },
  { id: 'ziwei', name: '紫微斗数', description: '紫微斗数排盘', calculate: calculateZiwei as any },
  { id: 'qimen', name: '奇门遁甲', description: '奇门遁甲预测', calculate: calculateQimen as any },
  { id: 'liuren', name: '大六壬', description: '大六壬预测', calculate: calculateLiuren as any },
  { id: 'meihua', name: '梅花易数', description: '梅花易数占卜', calculate: calculateMeihua as any },
  { id: 'liuyao', name: '六爻', description: '六爻起卦', calculate: calculateLiuyao as any },
  { id: 'taiyi', name: '太乙数', description: '太乙神数', calculate: calculateTaiyi as any },
];

export default function CalculatorPage() {
  const { theme } = useTheme();
  const [birthDate, setBirthDate] = useState('1990-05-15');
  const [birthTime, setBirthTime] = useState('10:30');
  const [gender, setGender] = useState('男');
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const [results, setResults] = useState<Record<string, ApiResponse<AllResults>>>({});
  const [activeDomains, setActiveDomains] = useState<string[]>(['bazi']);

  const handleCalculate = async () => {
    const params = {
      birth_date: birthDate,
      birth_time: birthTime,
      timezone: 'UTC+8',
      location: '北京',
      gender,
    };

    const newLoading: Record<string, boolean> = {};
    activeDomains.forEach((d) => { newLoading[d] = true; });
    setLoading(newLoading);

    for (const domain of activeDomains) {
      try {
        const option = DOMAINS.find((d) => d.id === domain);
        if (option) {
          const result = await option.calculate(params);
          setResults((prev) => ({ ...prev, [domain]: result }));
        }
      } catch (error: any) {
        setResults((prev) => ({
          ...prev,
          [domain]: { success: false, error: error.message || '计算失败', confidence: 0 },
        }));
      }
    }
    setLoading({});
  };

  const toggleDomain = (id: string) => {
    setActiveDomains((prev) =>
      prev.includes(id) ? prev.filter((d) => d !== id) : [...prev, id]
    );
  };

  return (
    <Layout title="命盘计算器" description="输入出生日期时间，获得七大术数域的命盘排盘">
      <div style={{ maxWidth: 960, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🧮 命盘计算器</h1>
          <p style={{ fontSize: '1.1rem', color: theme.colors.textSecondary }}>
            输入您的出生日期时间，获得八字、紫微、奇门等术数域的完整命盘
          </p>
        </div>

        {/* 输入区域 */}
        <div style={{
          backgroundColor: theme.colors.surface,
          padding: '2rem',
          borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
          marginBottom: '2rem',
        }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1.25rem' }}>📝 个人信息</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1.25rem',
            marginBottom: '1.5rem',
          }}>
            <div>
              <label style={{ display: 'block', fontWeight: 500, marginBottom: '0.5rem' }}>
                出生日期
              </label>
              <input
                type="date"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.625rem 0.875rem',
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: '0.5rem',
                  backgroundColor: theme.colors.background,
                  color: theme.colors.text,
                  fontSize: '1rem',
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontWeight: 500, marginBottom: '0.5rem' }}>
                出生时间
              </label>
              <input
                type="time"
                value={birthTime}
                onChange={(e) => setBirthTime(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.625rem 0.875rem',
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: '0.5rem',
                  backgroundColor: theme.colors.background,
                  color: theme.colors.text,
                  fontSize: '1rem',
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontWeight: 500, marginBottom: '0.5rem' }}>
                性别
              </label>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.625rem 0.875rem',
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: '0.5rem',
                  backgroundColor: theme.colors.background,
                  color: theme.colors.text,
                  fontSize: '1rem',
                }}
              >
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>

          <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem', color: theme.colors.textSecondary }}>
            选择术数域
          </h3>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '0.75rem',
            marginBottom: '1.5rem',
          }}>
            {DOMAINS.map((domain) => (
              <button
                key={domain.id}
                onClick={() => toggleDomain(domain.id)}
                style={{
                  padding: '0.5rem 1.25rem',
                  borderRadius: '2rem',
                  fontSize: '0.9rem',
                  cursor: 'pointer',
                  backgroundColor: activeDomains.includes(domain.id)
                    ? theme.colors.primary
                    : theme.colors.background,
                  color: activeDomains.includes(domain.id) ? 'white' : theme.colors.text,
                  border: `1px solid ${activeDomains.includes(domain.id)
                    ? theme.colors.primary
                    : theme.colors.border}`,
                  transition: 'all 0.2s ease',
                  fontWeight: 500,
                }}
              >
                {domain.name}
              </button>
            ))}
          </div>

          <button
            onClick={handleCalculate}
            disabled={activeDomains.length === 0 || Object.values(loading).some(Boolean)}
            style={{
              width: '100%',
              padding: '1rem',
              borderRadius: '0.5rem',
              backgroundColor: activeDomains.length === 0 || Object.values(loading).some(Boolean)
                ? theme.colors.textSecondary
                : theme.colors.primary,
              color: 'white',
              fontSize: '1.1rem',
              fontWeight: 600,
              cursor: activeDomains.length === 0 || Object.values(loading).some(Boolean)
                ? 'not-allowed'
                : 'pointer',
              border: 'none',
              transition: 'all 0.2s ease',
            }}
          >
            {Object.values(loading).some(Boolean) ? '计算中...' : `开始排盘 (${activeDomains.length} 个术数域)`}
          </button>
        </div>

        {/* 结果展示 */}
        {Object.keys(results).length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {activeDomains.map((domain) => {
              const result = results[domain];
              if (!result) return null;
              const domainInfo = DOMAINS.find((d) => d.id === domain);
              return (
                <div key={domain} style={{
                  backgroundColor: theme.colors.surface,
                  padding: '1.5rem',
                  borderRadius: '1rem',
                  border: `1px solid ${theme.colors.border}`,
                }}>
                  {loading[domain] ? (
                    <div style={{
                      padding: '2rem',
                      textAlign: 'center',
                      color: theme.colors.textSecondary,
                    }}>
                      <div style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>⏳</div>
                      {domainInfo?.name} 排盘中...
                    </div>
                  ) : result.success ? (
                    <>
                      <DomainChart domain={domain} result={result.result!} />
                      {result.confidence !== undefined && (
                        <div style={{
                          marginTop: '1.5rem',
                          padding: '0.75rem 1rem',
                          backgroundColor: theme.colors.background,
                          borderRadius: '0.5rem',
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          fontSize: '0.9rem',
                          color: theme.colors.textSecondary,
                        }}>
                          <span>计算置信度</span>
                          <span style={{ fontWeight: 600, color: theme.colors.text }}>
                            {(result.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                    </>
                  ) : (
                    <div style={{
                      color: theme.colors.error,
                      textAlign: 'center',
                      padding: '2rem',
                    }}>
                      {result.error || '计算失败'}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {Object.keys(results).length === 0 && !Object.values(loading).some(Boolean) && (
          <div style={{
            textAlign: 'center',
            padding: '3rem',
            backgroundColor: theme.colors.surface,
            borderRadius: '1rem',
            border: `1px solid ${theme.colors.border}`,
            color: theme.colors.textSecondary,
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔮</div>
            <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>
              填写您的信息，点击"开始排盘"进行命盘计算
            </p>
            <p style={{ fontSize: '0.95rem' }}>
              支持同时计算多个术数域
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
