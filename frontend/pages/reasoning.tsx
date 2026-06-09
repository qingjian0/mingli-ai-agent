import { useState } from 'react';
import Layout from '../components/Layout';
import { useTheme } from '../lib/ThemeContext';

interface ReasoningStep {
  rule_id: string;
  description: string;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  confidence: number;
}

const SAMPLE_CHAIN: ReasoningStep[] = [
  {
    rule_id: 'bazi.pillar.year',
    description: '计算年柱天干地支',
    input_data: { birth_year: 1990 },
    output_data: { year_stem: '庚', year_branch: '午', ganzhi: '庚午' },
    confidence: 1.0,
  },
  {
    rule_id: 'bazi.pillar.month',
    description: '计算月柱天干地支',
    input_data: { birth_date: '1990-05-15', year_stem: '庚' },
    output_data: { month_stem: '甲', month_branch: '辰', ganzhi: '甲辰' },
    confidence: 0.98,
  },
  {
    rule_id: 'bazi.pillar.day',
    description: '计算日柱天干地支',
    input_data: { birth_date: '1990-05-15' },
    output_data: { day_stem: '己', day_branch: '未', ganzhi: '己未' },
    confidence: 0.99,
  },
  {
    rule_id: 'bazi.pillar.hour',
    description: '计算时柱天干地支',
    input_data: { birth_time: '10:30', day_stem: '己' },
    output_data: { hour_stem: '丁', hour_branch: '卯', ganzhi: '丁卯' },
    confidence: 0.99,
  },
  {
    rule_id: 'bazi.daymaster',
    description: '确定日主',
    input_data: { day_stem: '己' },
    output_data: { daymaster: '己', element: '土', yin_yang: '阴' },
    confidence: 1.0,
  },
  {
    rule_id: 'bazi.wuxing',
    description: '统计五行分布',
    input_data: { pillars: ['庚午', '甲辰', '己未', '丁卯'] },
    output_data: { 金: 1, 木: 2, 水: 0, 火: 2, 土: 2 },
    confidence: 0.97,
  },
  {
    rule_id: 'bazi.ten_gods',
    description: '计算十神关系',
    input_data: { daymaster: '己', all_stems: ['庚', '甲', '己', '丁'] },
    output_data: { 比肩: ['己'], 食神: ['庚'], 正财: ['甲'], 正印: ['丁'] },
    confidence: 0.95,
  },
];

export default function ReasoningPage() {
  const { theme } = useTheme();
  const [expanded, setExpanded] = useState<number | null>(0);

  return (
    <Layout title="推理链" description="命盘计算过程的完整推理链">
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🔗 推理链展示</h1>
          <p style={{ fontSize: '1.1rem', color: theme.colors.textSecondary }}>
            命盘计算过程的完整推理步骤，每一步都可追溯、可验证
          </p>
        </div>

        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem',
          borderRadius: '1rem', border: `1px solid ${theme.colors.border}`,
          marginBottom: '2rem',
        }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>示例: 八字排盘推理链</h2>
          <div style={{ color: theme.colors.textSecondary, fontSize: '0.95rem' }}>
            出生日期: 1990年5月15日 10:30 | 置信度: 97.5%
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {SAMPLE_CHAIN.map((step, index) => (
            <div key={index} style={{
              backgroundColor: theme.colors.surface, borderRadius: '1rem',
              border: `1px solid ${theme.colors.border}`, overflow: 'hidden',
            }}>
              <div
                onClick={() => setExpanded(expanded === index ? null : index)}
                style={{
                  padding: '1.25rem 1.5rem', cursor: 'pointer',
                  display: 'flex', alignItems: 'center', gap: '1rem',
                }}>
                <div style={{
                  width: 40, height: 40, borderRadius: '50%',
                  backgroundColor: theme.colors.primary, color: 'white',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontWeight: 700, fontSize: '1rem', flexShrink: 0,
                }}>
                  {index + 1}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>{step.description}</div>
                  <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary }}>
                    {step.rule_id}
                  </div>
                </div>
                <div style={{
                  padding: '0.25rem 0.75rem', backgroundColor: theme.colors.background,
                  borderRadius: '1rem', fontSize: '0.875rem',
                  color: step.confidence > 0.95 ? theme.colors.success : theme.colors.warning,
                  fontWeight: 600,
                }}>
                  {(step.confidence * 100).toFixed(0)}%
                </div>
                <div style={{ fontSize: '1.5rem', color: theme.colors.textSecondary }}>
                  {expanded === index ? '−' : '+'}
                </div>
              </div>

              {expanded === index && (
                <div style={{
                  padding: '0 1.5rem 1.5rem', marginTop: '-0.5rem',
                }}>
                  <div style={{
                    padding: '1rem', backgroundColor: theme.colors.background,
                    borderRadius: '0.5rem', border: `1px solid ${theme.colors.border}`,
                  }}>
                    <div style={{ marginBottom: '1rem' }}>
                      <h4 style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.5rem' }}>输入</h4>
                      <pre style={{
                        whiteSpace: 'pre-wrap', fontSize: '0.85rem',
                        color: theme.colors.text, margin: 0,
                      }}>{JSON.stringify(step.input_data, null, 2)}</pre>
                    </div>
                    <div>
                      <h4 style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.5rem' }}>输出</h4>
                      <pre style={{
                        whiteSpace: 'pre-wrap', fontSize: '0.85rem',
                        color: theme.colors.text, margin: 0,
                      }}>{JSON.stringify(step.output_data, null, 2)}</pre>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div style={{
          marginTop: '3rem', padding: '1.5rem', backgroundColor: theme.colors.surface,
          borderRadius: '1rem', border: `1px solid ${theme.colors.border}`,
        }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '0.75rem' }}>📝 说明</h3>
          <div style={{ color: theme.colors.textSecondary, fontSize: '0.95rem', lineHeight: 1.8 }}>
            <p>每一个命盘计算都包含完整的推理链，记录：</p>
            <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem' }}>
              <li>规则 ID: 具体使用的规则名称</li>
              <li>输入数据: 该步骤的原始输入</li>
              <li>输出数据: 计算结果</li>
              <li>置信度: 该计算的准确率</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
}
