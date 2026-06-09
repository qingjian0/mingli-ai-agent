import { useTheme } from '../lib/ThemeContext';
import type {
  BaziResult,
  ZiweiResult,
  QimenResult,
  LiurenResult,
  MeihuaResult,
  LiuyaoResult,
  TaiyiResult,
  DayunInfo,
  LiunianInfo,
} from '../lib/types';

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
const ELEMENT_TO_KEY: Record<string, string> = {
  金: 'jin', 木: 'mu', 水: 'shui', 火: 'huo', 土: 'tu',
};
const DEFAULT_COLORS: Record<string, string> = {
  金: '#9ca3af', 木: '#22c55e', 水: '#3b82f6', 火: '#ef4444', 土: '#f59e0b',
};

function getElementColor(element: string, theme: any): string {
  const key = ELEMENT_TO_KEY[element];
  if (key && theme.colors.wuxing && (theme.colors.wuxing as any)[key]) {
    return (theme.colors.wuxing as any)[key];
  }
  return DEFAULT_COLORS[element] || theme.colors.text;
}

// ============ 八字命盘 ============
interface BaziChartProps { result: BaziResult; }
export function BaziChart({ result }: BaziChartProps) {
  const { theme } = useTheme();
  const pillars = [
    { label: '年柱', stem: result.year_stem, branch: result.year_branch },
    { label: '月柱', stem: result.month_stem, branch: result.month_branch },
    { label: '日柱', stem: result.day_stem, branch: result.day_branch },
    { label: '时柱', stem: result.hour_stem, branch: result.hour_branch },
  ];

  return (
    <div className="fade-in">
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>八字四柱</h2>
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem',
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
        }}>
          {pillars.map((pillar, i) => (
            <div key={i} style={{
              display: 'flex', flexDirection: 'column', alignItems: 'center',
              padding: '1.5rem 1rem', borderRadius: '0.75rem',
              border: `2px solid ${theme.colors.border}`, backgroundColor: theme.colors.background,
            }}>
              <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.75rem' }}>
                {pillar.label}
              </div>
              <div style={{
                fontSize: '2.5rem', fontWeight: 700,
                color: getElementColor(STEM_ELEMENTS[pillar.stem], theme),
                marginBottom: '0.25rem',
              }}>{pillar.stem}</div>
              <div style={{
                fontSize: '2.5rem', fontWeight: 700,
                color: getElementColor(BRANCH_ELEMENTS[pillar.branch], theme),
              }}>{pillar.branch}</div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.5rem', color: theme.colors.textSecondary }}>
                {STEM_ELEMENTS[pillar.stem]} / {BRANCH_ELEMENTS[pillar.branch]}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div style={{
        backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
        border: `1px solid ${theme.colors.border}`, marginBottom: '2rem',
      }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>日主信息</h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
          <div style={{
            width: 80, height: 80, borderRadius: '50%',
            backgroundColor: getElementColor(STEM_ELEMENTS[result.daymaster], theme),
            color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '2.5rem', fontWeight: 700,
          }}>{result.daymaster}</div>
          <div>
            <div style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.25rem' }}>日主（日柱天干）</div>
            <div style={{ color: theme.colors.textSecondary }}>五行属性: {STEM_ELEMENTS[result.daymaster]}</div>
            <div style={{ color: theme.colors.textSecondary, marginTop: '0.25rem' }}>
              命主代表自身，代表个人的性格、特质与命运走向
            </div>
          </div>
        </div>
      </div>

      <div style={{
        backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
        border: `1px solid ${theme.colors.border}`, marginBottom: '2rem',
      }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>五行分布</h3>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'flex-end' }}>
          {Object.entries(result.wuxing).map(([element, count]) => (
            <div key={element} style={{
              flex: 1, minWidth: 80, display: 'flex', flexDirection: 'column',
              alignItems: 'center', gap: '0.5rem',
            }}>
              <div style={{
                width: '100%', height: 100 + (Number(count) * 30),
                backgroundColor: getElementColor(element, theme), borderRadius: '0.5rem',
                opacity: 0.8, minHeight: 60,
              }} />
              <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary }}>{element}</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700 }}>{count}</div>
            </div>
          ))}
        </div>
      </div>

      {result.ten_gods && (
        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`, marginBottom: '2rem',
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>十神</h3>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '1rem',
          }}>
            {Object.entries(result.ten_gods).map(([godName, stems]) => (
              <div key={godName} style={{
                padding: '1rem', backgroundColor: theme.colors.background, borderRadius: '0.5rem',
                border: `1px solid ${theme.colors.border}`, textAlign: 'center',
              }}>
                <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>{godName}</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{stems.join(' ')}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {result.dayun && result.dayun.length > 0 && (
        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`, marginBottom: '2rem',
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>大运</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {result.dayun.map((dayun: DayunInfo) => (
              <div key={dayun.step} style={{
                display: 'flex', alignItems: 'center', padding: '0.75rem 1rem',
                backgroundColor: theme.colors.background, borderRadius: '0.5rem',
                border: `1px solid ${theme.colors.border}`, gap: '1rem',
              }}>
                <div style={{ width: 60, color: theme.colors.textSecondary, fontSize: '0.875rem' }}>
                  第{dayun.step}步
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>{dayun.ganzhi}</div>
                <div style={{ color: theme.colors.textSecondary, marginLeft: 'auto' }}>{dayun.age_range}岁</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {result.liunian && result.liunian.length > 0 && (
        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>流年</h3>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '1rem',
          }}>
            {result.liunian.map((liunian: LiunianInfo, index: number) => (
              <div key={index} style={{
                padding: '1rem', backgroundColor: theme.colors.background, borderRadius: '0.5rem',
                border: `1px solid ${theme.colors.border}`, textAlign: 'center',
              }}>
                <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>
                  {liunian.year}年 ({liunian.age}岁)
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>{liunian.ganzhi}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============ 紫微斗数命盘 ============
interface ZiweiChartProps { result: ZiweiResult; }
export function ZiweiChart({ result }: ZiweiChartProps) {
  const { theme } = useTheme();
  const palaces = [
    { name: '命宫', content: result.palaces['命宫'] || '', note: '主命运' },
    { name: '兄弟宫', content: result.palaces['兄弟宫'] || '', note: '主兄弟' },
    { name: '夫妻宫', content: result.palaces['夫妻宫'] || '', note: '主婚姻' },
    { name: '子女宫', content: result.palaces['子女宫'] || '', note: '主子息' },
    { name: '财帛宫', content: result.palaces['财帛宫'] || '', note: '主财运' },
    { name: '疾厄宫', content: result.palaces['疾厄宫'] || '', note: '主健康' },
    { name: '迁移宫', content: result.palaces['迁移宫'] || '', note: '主外出' },
    { name: '交友宫', content: result.palaces['交友宫'] || '', note: '主人际' },
    { name: '官禄宫', content: result.palaces['官禄宫'] || '', note: '主事业' },
    { name: '田宅宫', content: result.palaces['田宅宫'] || '', note: '主房产' },
    { name: '福德宫', content: result.palaces['福德宫'] || '', note: '主福气' },
    { name: '父母宫', content: result.palaces['父母宫'] || '', note: '主长辈' },
  ];

  return (
    <div className="fade-in">
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>紫微斗数命盘</h2>
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem',
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `2px solid ${theme.colors.primary}`,
        }}>
          {palaces.map((p, i) => (
            <div key={i} style={{
              aspectRatio: '1', padding: '0.75rem', borderRadius: '0.5rem',
              border: `1px solid ${theme.colors.border}`, backgroundColor: theme.colors.background,
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
              minHeight: 120,
            }}>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, color: theme.colors.primary, marginBottom: '0.5rem' }}>
                {p.name}
              </div>
              <div style={{ fontSize: '1rem', color: theme.colors.text, textAlign: 'center' }}>
                {p.content || '—'}
              </div>
              <div style={{ fontSize: '0.7rem', color: theme.colors.textSecondary, marginTop: '0.25rem' }}>
                {p.note}
              </div>
            </div>
          ))}
        </div>
      </div>

      {result.main_stars && result.main_stars.length > 0 && (
        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`, marginBottom: '2rem',
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>主星</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
            {result.main_stars.map((star: string, i: number) => (
              <div key={i} style={{
                padding: '0.5rem 1rem', backgroundColor: theme.colors.primary, color: 'white',
                borderRadius: '2rem', fontSize: '0.9rem', fontWeight: 500,
              }}>{star}</div>
            ))}
          </div>
        </div>
      )}

      {Object.keys(result.stars || {}).length > 0 && (
        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>其他星曜</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
            {Object.entries(result.stars).map(([name, position]) => (
              <div key={name} style={{
                padding: '0.5rem 1rem', backgroundColor: theme.colors.background,
                border: `1px solid ${theme.colors.border}`, borderRadius: '2rem', fontSize: '0.9rem',
              }}>
                <span style={{ fontWeight: 500 }}>{name}</span>
                <span style={{ color: theme.colors.textSecondary, marginLeft: '0.5rem' }}>{position}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============ 奇门遁甲 ============
interface QimenChartProps { result: QimenResult; }
export function QimenChart({ result }: QimenChartProps) {
  const { theme } = useTheme();
  const bamenItems = Object.entries(result.bamen || {});
  const jiuxingItems = Object.entries(result.jiuxing || {});

  return (
    <div className="fade-in">
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>奇门遁甲排盘</h2>
        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`,
        }}>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.75rem',
            marginBottom: '1.5rem',
          }}>
            {Object.entries(result.gong_positions || {}).map(([gong, content], i) => (
              <div key={i} style={{
                padding: '1rem', backgroundColor: theme.colors.background, borderRadius: '0.5rem',
                border: `1px solid ${theme.colors.border}`, textAlign: 'center',
              }}>
                <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>{gong}</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>{content || '—'}</div>
              </div>
            ))}
          </div>

          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem',
          }}>
            <div>
              <h3 style={{ marginBottom: '0.75rem', fontSize: '1.1rem' }}>八门</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {bamenItems.length > 0 ? bamenItems.map(([name, position], i) => (
                  <div key={i} style={{
                    display: 'flex', justifyContent: 'space-between', padding: '0.5rem 1rem',
                    backgroundColor: theme.colors.background, borderRadius: '0.375rem',
                    border: `1px solid ${theme.colors.border}`,
                  }}>
                    <span style={{ fontWeight: 500 }}>{name}</span>
                    <span style={{ color: theme.colors.textSecondary }}>{position}</span>
                  </div>
                )) : (
                  <div style={{ color: theme.colors.textSecondary, fontSize: '0.9rem' }}>暂无数据</div>
                )}
              </div>
            </div>
            <div>
              <h3 style={{ marginBottom: '0.75rem', fontSize: '1.1rem' }}>九星</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {jiuxingItems.length > 0 ? jiuxingItems.map(([name, position], i) => (
                  <div key={i} style={{
                    display: 'flex', justifyContent: 'space-between', padding: '0.5rem 1rem',
                    backgroundColor: theme.colors.background, borderRadius: '0.375rem',
                    border: `1px solid ${theme.colors.border}`,
                  }}>
                    <span style={{ fontWeight: 500 }}>{name}</span>
                    <span style={{ color: theme.colors.textSecondary }}>{position}</span>
                  </div>
                )) : (
                  <div style={{ color: theme.colors.textSecondary, fontSize: '0.9rem' }}>暂无数据</div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{
        backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
        border: `1px solid ${theme.colors.border}`,
      }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>基本信息</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{
            padding: '0.75rem 1.5rem', backgroundColor: theme.colors.background,
            borderRadius: '0.5rem', border: `1px solid ${theme.colors.border}`,
          }}>
            <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary }}>时辰干支</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>{result.hour_ganzhi}</div>
          </div>
          <div style={{
            padding: '0.75rem 1.5rem', backgroundColor: theme.colors.background,
            borderRadius: '0.5rem', border: `1px solid ${theme.colors.border}`,
          }}>
            <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary }}>局数类型</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>{result.pan_type}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============ 梅花易数 ============
interface MeihuaChartProps { result: MeihuaResult; }
export function MeihuaChart({ result }: MeihuaChartProps) {
  const { theme } = useTheme();

  return (
    <div className="fade-in">
      <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>梅花易数卦象</h2>
      <div style={{
        backgroundColor: theme.colors.surface, padding: '2rem', borderRadius: '1rem',
        border: `1px solid ${theme.colors.border}`, display: 'flex',
        flexDirection: 'column', alignItems: 'center', gap: '2rem',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.9rem', color: theme.colors.textSecondary, marginBottom: '0.5rem' }}>上卦</div>
          <div style={{ fontSize: '3rem', fontWeight: 700, color: getElementColor(result.shang_gua.element, theme) }}>
            {result.shang_gua.name}
          </div>
          <div style={{ fontSize: '0.9rem', color: theme.colors.textSecondary }}>五行: {result.shang_gua.element}</div>
        </div>

        <div style={{
          width: '100%', height: 2, backgroundColor: theme.colors.border, margin: '0.5rem 0',
          position: 'relative',
        }}>
          {result.dong_yao && (
            <div style={{
              position: 'absolute', left: '50%', transform: 'translateX(-50%)',
              padding: '0.25rem 1rem', backgroundColor: theme.colors.accent, color: 'white',
              borderRadius: '1rem', fontSize: '0.875rem',
            }}>动爻: {result.dong_yao}</div>
          )}
        </div>

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.9rem', color: theme.colors.textSecondary, marginBottom: '0.5rem' }}>下卦</div>
          <div style={{ fontSize: '3rem', fontWeight: 700, color: getElementColor(result.xia_gua.element, theme) }}>
            {result.xia_gua.name}
          </div>
          <div style={{ fontSize: '0.9rem', color: theme.colors.textSecondary }}>五行: {result.xia_gua.element}</div>
        </div>
      </div>

      <div style={{
        backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
        border: `1px solid ${theme.colors.border}`, marginTop: '2rem',
      }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>体用关系</h3>
        <div style={{
          padding: '1rem', backgroundColor: theme.colors.background, borderRadius: '0.5rem',
          border: `1px solid ${theme.colors.border}`,
        }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>
            {result.ti_yong || '请根据五行关系分析体用生克'}
          </div>
        </div>
      </div>
    </div>
  );
}

// ============ 通用命盘显示组件 ============
interface DomainChartProps {
  domain: string;
  result: BaziResult | ZiweiResult | QimenResult | LiurenResult | MeihuaResult | LiuyaoResult | TaiyiResult;
}
export function DomainChart({ domain, result }: DomainChartProps) {
  switch (domain) {
    case 'bazi':
      return <BaziChart result={result as BaziResult} />;
    case 'ziwei':
      return <ZiweiChart result={result as ZiweiResult} />;
    case 'qimen':
      return <QimenChart result={result as QimenResult} />;
    case 'meihua':
      return <MeihuaChart result={result as MeihuaResult} />;
    default:
      return <GenericChart domain={domain} result={result} />;
  }
}

// ============ 通用结果显示（用于六壬/六爻/太乙数）============
interface GenericChartProps { domain: string; result: any; }
function GenericChart({ domain, result }: GenericChartProps) {
  const { theme } = useTheme();
  const titles: Record<string, string> = {
    liuren: '大六壬排盘', liuyao: '六爻排盘', taiyi: '太乙数排盘',
  };

  return (
    <div className="fade-in">
      <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>{titles[domain] || '命盘排盘'}</h2>
      <div style={{
        backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
        border: `1px solid ${theme.colors.border}`,
      }}>
        <pre style={{
          whiteSpace: 'pre-wrap', wordBreak: 'break-word', fontSize: '0.95rem',
          lineHeight: 1.8, color: theme.colors.text, margin: 0,
        }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      </div>
    </div>
  );
}
