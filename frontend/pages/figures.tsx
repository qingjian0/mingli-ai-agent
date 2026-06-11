import { useState } from 'react';
import Layout from '../components/Layout';
import { useTheme } from '../lib/ThemeContext';
import type { HistoricalFigure } from '../lib/types';

const SAMPLE_FIGURES: HistoricalFigure[] = [
  { case_id: '001', name: '康熙帝', birth_date: '1654-05-04', birth_time: '23:30', timezone: 'UTC+8', location: '北京', source: '《康熙起居注》', expected_results: { bazi_pillar: '甲午 戊辰 戊申 壬子', daymaster: '戊', notes: '在位61年，开创康乾盛世' } },
  { case_id: '002', name: '乾隆帝', birth_date: '1711-09-25', birth_time: '02:00', timezone: 'UTC+8', location: '北京', source: '《清实录》', expected_results: { bazi_pillar: '辛卯 丁酉 庚午 丙子', daymaster: '庚', notes: '在位60年，文治武功' } },
  { case_id: '003', name: '曾国藩', birth_date: '1811-11-26', birth_time: '20:00', timezone: 'UTC+8', location: '湖南湘乡', source: '《曾国藩年谱》', expected_results: { bazi_pillar: '辛未 己亥 丙辰 戊戌', daymaster: '丙', notes: '晚清名臣，湘军统帅' } },
  { case_id: '004', name: '毛泽东', birth_date: '1893-12-26', birth_time: '06:00', timezone: 'UTC+8', location: '湖南湘潭', source: '官方资料', expected_results: { bazi_pillar: '癸巳 甲子 丁酉 癸卯', daymaster: '丁', notes: '中华人民共和国缔造者' } },
  { case_id: '005', name: '诸葛亮', birth_date: '181-07-23', birth_time: '04:00', timezone: 'UTC+8', location: '琅琊阳都', source: '《三国志》', expected_results: { daymaster: '癸', notes: '蜀汉丞相，卧龙先生' } },
  { case_id: '006', name: '李白', birth_date: '701-02-28', birth_time: '05:00', timezone: 'UTC+8', location: '碎叶城', source: '《旧唐书》', expected_results: { daymaster: '癸', notes: '诗仙，唐代著名诗人' } },
  { case_id: '007', name: '苏轼', birth_date: '1037-01-08', birth_time: '10:00', timezone: 'UTC+8', location: '眉山', source: '《宋史》', expected_results: { daymaster: '癸', notes: '东坡居士，豪放派词人' } },
  { case_id: '008', name: '钱学森', birth_date: '1911-12-11', birth_time: '08:00', timezone: 'UTC+8', location: '上海', source: '官方资料', expected_results: { daymaster: '壬', notes: '中国航天之父' } },
  { case_id: '009', name: '屠呦呦', birth_date: '1930-12-30', birth_time: '10:00', timezone: 'UTC+8', location: '宁波', source: '官方资料', expected_results: { daymaster: '癸', notes: '青蒿素发现者，诺贝尔奖' } },
  { case_id: '010', name: '杨振宁', birth_date: '1922-10-01', birth_time: '08:00', timezone: 'UTC+8', location: '合肥', source: '官方资料', expected_results: { daymaster: '壬', notes: '物理学家，诺贝尔奖' } },
];

export default function FiguresPage() {
  const { theme } = useTheme();
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<HistoricalFigure | null>(null);
  const [figures] = useState<HistoricalFigure[]>(SAMPLE_FIGURES);

  const filtered = figures.filter(
    (f) =>
      f.name.includes(search) ||
      (f.expected_results?.notes || '').includes(search) ||
      f.location.includes(search)
  );

  return (
    <Layout title="历史名人库" description="历史名人命理案例库">
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>📜 历史名人库</h1>
          <p style={{ fontSize: '1.1rem', color: theme.colors.textSecondary }}>
            收录历代名人的出生信息与命理记录，供研究与学习参考
          </p>
        </div>

        <div style={{
          backgroundColor: theme.colors.surface, padding: '1.5rem', borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`, marginBottom: '2rem',
        }}>
          <input
            type="text"
            placeholder="搜索姓名、出生地、备注..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              width: '100%', padding: '0.875rem 1.25rem', fontSize: '1rem',
              border: `1px solid ${theme.colors.border}`, borderRadius: '0.5rem',
              backgroundColor: theme.colors.background, color: theme.colors.text,
            }}
          />
          <div style={{ marginTop: '0.75rem', color: theme.colors.textSecondary, fontSize: '0.875rem' }}>
            共 {filtered.length} 位名人
          </div>
        </div>

        {/* 列表 */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: '1rem', marginBottom: '2rem',
        }}>
          {filtered.map((figure) => (
            <div key={figure.case_id}
              onClick={() => setSelected(figure)}
              style={{
                padding: '1.5rem', backgroundColor: theme.colors.surface,
                borderRadius: '1rem', border: `1px solid ${theme.colors.border}`,
                cursor: 'pointer', transition: 'all 0.2s ease',
              }}>
              <div style={{
                fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem',
                color: theme.colors.primary,
              }}>{figure.name}</div>
              <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary, marginBottom: '0.75rem' }}>
                {figure.birth_date} {figure.birth_time}
              </div>
              <div style={{ fontSize: '0.875rem', color: theme.colors.textSecondary }}>
                📍 {figure.location}
              </div>
              {figure.expected_results?.daymaster && (
                <div style={{
                  marginTop: '0.75rem', padding: '0.375rem 0.75rem',
                  backgroundColor: theme.colors.background, borderRadius: '0.375rem',
                  fontSize: '0.875rem', color: theme.colors.text,
                  display: 'inline-block', border: `1px solid ${theme.colors.border}`,
                }}>日主: {figure.expected_results.daymaster}</div>
              )}
            </div>
          ))}
        </div>

        {/* 详情弹窗 */}
        {selected && (
          <div style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex',
            alignItems: 'center', justifyContent: 'center', padding: '1rem', zIndex: 1000,
          }} onClick={() => setSelected(null)}>
            <div style={{
              backgroundColor: theme.colors.background, borderRadius: '1.5rem',
              padding: '2rem', maxWidth: 500, width: '100%', maxHeight: '80vh',
              overflow: 'auto', border: `1px solid ${theme.colors.border}`,
            }} onClick={(e) => e.stopPropagation()}>
              <h2 style={{ fontSize: '1.75rem', marginBottom: '1rem', color: theme.colors.primary }}>
                {selected.name}
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
                <div><span style={{ color: theme.colors.textSecondary }}>出生日期: </span>
                  {selected.birth_date} {selected.birth_time}
                </div>
                <div><span style={{ color: theme.colors.textSecondary }}>出生地: </span>{selected.location}</div>
                <div><span style={{ color: theme.colors.textSecondary }}>时区: </span>{selected.timezone}</div>
                <div><span style={{ color: theme.colors.textSecondary }}>资料来源: </span>{selected.source}</div>
              </div>

              {selected.expected_results && (
                <div style={{
                  padding: '1.25rem', backgroundColor: theme.colors.surface,
                  borderRadius: '0.75rem', border: `1px solid ${theme.colors.border}`,
                }}>
                  <h3 style={{ fontSize: '1.1rem', marginBottom: '0.75rem' }}>命理信息</h3>
                  {selected.expected_results.bazi_pillar && (
                    <div style={{ marginBottom: '0.5rem' }}>
                      <span style={{ color: theme.colors.textSecondary }}>八字: </span>
                      <span style={{ fontSize: '1.15rem', fontWeight: 600 }}>{selected.expected_results.bazi_pillar}</span>
                    </div>
                  )}
                  {selected.expected_results.daymaster && (
                    <div style={{ marginBottom: '0.5rem' }}>
                      <span style={{ color: theme.colors.textSecondary }}>日主: </span>
                      <span style={{ fontWeight: 600, fontSize: '1.1rem' }}>{selected.expected_results.daymaster}</span>
                    </div>
                  )}
                  {selected.expected_results.notes && (
                    <div style={{ marginTop: '0.75rem', fontStyle: 'italic', color: theme.colors.textSecondary }}>
                      {selected.expected_results.notes}
                    </div>
                  )}
                </div>
              )}

              <button onClick={() => setSelected(null)}
                style={{
                  marginTop: '1.5rem', width: '100%', padding: '0.75rem',
                  backgroundColor: theme.colors.primary, color: 'white',
                  border: 'none', borderRadius: '0.5rem', fontSize: '1rem',
                  fontWeight: 500, cursor: 'pointer',
                }}>关闭</button>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
