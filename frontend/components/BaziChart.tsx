import { useTheme } from '../lib/ThemeContext';
import type { BaziResult, DayunInfo, LiunianInfo } from '../lib/types';

interface BaziChartProps {
  result: BaziResult;
  showDetails?: boolean;
}

// 天干地支的五行属性
const STEM_ELEMENTS: Record<string, string> = {
  甲: '木', 乙: '木', 丙: '火', 丁: '火',
  戊: '土', 己: '土', 庚: '金', 辛: '金',
  壬: '水', 癸: '水',
};

const BRANCH_ELEMENTS: Record<string, string> = {
  子: '水', 丑: '土', 寅: '木', 卯: '木',
  辰: '土', 巳: '火', 午: '火', 未: '土',
  申: '金', 酉: '金', 戌: '土', 亥: '水',
};

// 五行对应的颜色
const ELEMENT_COLORS: Record<string, string> = {
  金: '#9ca3af',
  木: '#22c55e',
  水: '#3b82f6',
  火: '#ef4444',
  土: '#f59e0b',
};

export default function BaziChart({ result, showDetails = true }: BaziChartProps) {
  const { theme } = useTheme();

  const pillars = [
    { label: '年柱', stem: result.year_stem, branch: result.year_branch },
    { label: '月柱', stem: result.month_stem, branch: result.month_branch },
    { label: '日柱', stem: result.day_stem, branch: result.day_branch },
    { label: '时柱', stem: result.hour_stem, branch: result.hour_branch },
  ];

  return (
    <div className="fade-in">
      {/* 八字四柱 */}
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>八字四柱</h2>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '1rem',
            backgroundColor: theme.colors.surface,
            padding: '1.5rem',
            borderRadius: '1rem',
            border: `1px solid ${theme.colors.border}`,
          }}
        >
          {pillars.map((pillar, index) => (
            <div
              key={index}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                padding: '1.5rem 1rem',
                borderRadius: '0.75rem',
                border: `2px solid ${theme.colors.border}`,
                backgroundColor: theme.colors.background,
              }}
            >
              <div
                style={{
                  fontSize: '0.875rem',
                  color: theme.colors.textSecondary,
                  marginBottom: '0.75rem',
                }}
              >
                {pillar.label}
              </div>
              <div
                style={{
                  fontSize: '2.5rem',
                  fontWeight: 700,
                  color: ELEMENT_COLORS[STEM_ELEMENTS[pillar.stem]] || theme.colors.text,
                  marginBottom: '0.25rem',
                }}
              >
                {pillar.stem}
              </div>
              <div
                style={{
                  fontSize: '2.5rem',
                  fontWeight: 700,
                  color: ELEMENT_COLORS[BRANCH_ELEMENTS[pillar.branch]] || theme.colors.text,
                }}
              >
                {pillar.branch}
              </div>
              {showDetails && (
                <div style={{ fontSize: '0.75rem', marginTop: '0.5rem', color: theme.colors.textSecondary }}>
                  {STEM_ELEMENTS[pillar.stem]} / {BRANCH_ELEMENTS[pillar.branch]}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 日主信息 */}
      <div
        style={{
          backgroundColor: theme.colors.surface,
          padding: '1.5rem',
          borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
          marginBottom: '2rem',
        }}
      >
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>日主信息</h3>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '1.5rem',
            flexWrap: 'wrap',
          }}
        >
          <div
            style={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              backgroundColor: theme.colors.primary,
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2.5rem',
              fontWeight: 700,
            }}
          >
            {result.daymaster}
          </div>
          <div>
            <div style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.25rem' }}>
              日主（日柱天干）
            </div>
            <div style={{ color: theme.colors.textSecondary }}>
              五行属性: {STEM_ELEMENTS[result.daymaster]}
            </div>
            <div style={{ color: theme.colors.textSecondary, marginTop: '0.25rem' }}>
              命主代表自身，代表个人的性格、特质与命运走向
            </div>
          </div>
        </div>
      </div>

      {/* 五行分布 */}
      <div
        style={{
          backgroundColor: theme.colors.surface,
          padding: '1.5rem',
          borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
          marginBottom: '2rem',
        }}
      >
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>五行分布</h3>
        <div
          style={{
            display: 'flex',
            gap: '1rem',
            flexWrap: 'wrap',
            alignItems: 'flex-end',
          }}
        >
          {Object.entries(result.wuxing).map(([element, count]) => (
            <div
              key={element}
              style={{
                flex: 1,
                minWidth: 80,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              <div
                style={{
                  width: '100%',
                  height: 100 + count * 30,
                  backgroundColor: ELEMENT_COLORS[element],
                  borderRadius: '0.5rem',
                  opacity: 0.8,
                  minHeight: 60,
                }}
              />
              <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary }}>
                {element}
              </div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700 }}>
                {count}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 纳音 */}
      {showDetails && result.nayin && (
        <div
          style={{
            backgroundColor: theme.colors.surface,
            padding: '1.5rem',
            borderRadius: '1rem',
            border: `1px solid ${theme.colors.border}`,
            marginBottom: '2rem',
          }}
        >
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>纳音</h3>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '1rem',
            }}
          >
            {Object.entries(result.nayin).map(([pillar, value]) => (
              <div
                key={pillar}
                style={{
                  padding: '1rem',
                  backgroundColor: theme.colors.background,
                  borderRadius: '0.5rem',
                  border: `1px solid ${theme.colors.border}`,
                }}
              >
                <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>
                  {pillar}
                </div>
                <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>{value}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 十神 */}
      {showDetails && result.ten_gods && (
        <div
          style={{
            backgroundColor: theme.colors.surface,
            padding: '1.5rem',
            borderRadius: '1rem',
            border: `1px solid ${theme.colors.border}`,
            marginBottom: '2rem',
          }}
        >
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>十神</h3>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '1rem',
            }}
          >
            {Object.entries(result.ten_gods).map(([godName, stems]) => (
              <div
                key={godName}
                style={{
                  padding: '1rem',
                  backgroundColor: theme.colors.background,
                  borderRadius: '0.5rem',
                  border: `1px solid ${theme.colors.border}`,
                  textAlign: 'center',
                }}
              >
                <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>
                  {godName}
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>
                  {stems.join(' ')}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 大运 */}
      {showDetails && result.dayun && result.dayun.length > 0 && (
        <div
          style={{
            backgroundColor: theme.colors.surface,
            padding: '1.5rem',
            borderRadius: '1rem',
            border: `1px solid ${theme.colors.border}`,
            marginBottom: '2rem',
          }}
        >
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>大运</h3>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '0.5rem',
            }}
          >
            {result.dayun.map((dayun: DayunInfo) => (
              <div
                key={dayun.step}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  padding: '0.75rem 1rem',
                  backgroundColor: theme.colors.background,
                  borderRadius: '0.5rem',
                  border: `1px solid ${theme.colors.border}`,
                  gap: '1rem',
                }}
              >
                <div style={{ width: 60, color: theme.colors.textSecondary, fontSize: '0.875rem' }}>
                  第{dayun.step}步
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>
                  {dayun.ganzhi}
                </div>
                <div style={{ color: theme.colors.textSecondary, marginLeft: 'auto' }}>
                  {dayun.age_range}岁
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 流年 */}
      {showDetails && result.liunian && result.liunian.length > 0 && (
        <div
          style={{
            backgroundColor: theme.colors.surface,
            padding: '1.5rem',
            borderRadius: '1rem',
            border: `1px solid ${theme.colors.border}`,
          }}
        >
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>流年</h3>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '1rem',
            }}
          >
            {result.liunian.map((liunian: LiunianInfo, index: number) => (
              <div
                key={index}
                style={{
                  padding: '1rem',
                  backgroundColor: theme.colors.background,
                  borderRadius: '0.5rem',
                  border: `1px solid ${theme.colors.border}`,
                  textAlign: 'center',
                }}
              >
                <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>
                  {liunian.year}年 ({liunian.age}岁)
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>
                  {liunian.ganzhi}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
