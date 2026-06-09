import { useState } from 'react';
import Layout from '../components/Layout';
import { useTheme } from '../lib/ThemeContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default function ChatPage() {
  const { theme } = useTheme();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '您好！我是术数命理智能体。我可以帮助您：\n\n1. 解读八字、紫微等命盘\n2. 分析大运流年\n3. 解答命理相关问题\n4. 提供传统命理知识\n\n请告诉我您想了解什么？',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const quickQuestions = [
    '日主为己土代表什么？',
    '八字中五行缺怎么办？',
    '大运和流年有什么区别？',
    '紫微斗数命宫主星怎么看？',
    '十神中的正财偏财有什么不同？',
  ];

  const sendMessage = async (text?: string) => {
    const content = text || input;
    if (!content.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    setTimeout(() => {
      let response = '';
      if (content.includes('日主')) {
        response = '日主（又称日干）代表命主本人的核心特质。不同日干的人有不同的性格特点：\n\n• 甲木：正直、有领导力、有活力\n• 乙木：温柔、坚韧、灵活\n• 丙火：热情、光明、有创造力\n• 丁火：细腻、温暖、专注\n• 戊土：稳重、可靠、有担当\n• 己土：包容、耐心、务实\n• 庚金：刚毅、果断、行动力强\n• 辛金：精细、内敛、有原则\n• 壬水：智慧、包容、灵动\n• 癸水：温柔、深邃、有灵气\n\n您想了解哪个日主的详细解读吗？';
      } else if (content.includes('五行') || content.includes('缺')) {
        response = '关于五行缺失的理解：\n\n传统命理认为，八字中的五行应该平衡为佳，但实际上：\n\n1. 缺失的五行可能是忌神，反而是好事\n2. 可以通过地支藏干、大运流年补充\n3. 可以通过名字、穿着、方位等外部因素调整\n4. 关键是看日主与格局的配合，而非单纯看五行数量\n\n建议结合完整命盘来分析，而不是简单看五行缺什么。';
      } else if (content.includes('大运') || content.includes('流年')) {
        response = '大运与流年的区别：\n\n【大运】\n• 每10年一变\n• 影响人生的长期运势走向\n• 决定大的人生阶段\n\n【流年】\n• 每年一变\n• 在大运的基调下产生具体影响\n• 反映每年的具体事件\n\n两者关系：大运如河流走向，流年如其中的浪花。一个大运好，流年差也不会太差；大运差，流年好也会受局限。\n\n想了解您的大运走势吗？可以告诉我您的出生信息。';
      } else if (content.includes('紫微') || content.includes('命宫')) {
        response = '紫微斗数命宫解读：\n\n命宫是紫微斗数排盘中最重要的宫位，代表：\n\n• 个人的先天特质与外貌\n• 人生的主要发展方向\n• 性格的核心表现\n\n命宫主星的含义：\n• 紫微：高贵、领导力、权威\n• 天机：智慧、善变、思虑\n• 太阳：光明、热情、博爱\n• 武曲：刚毅、行动、财富\n• 天同：温和、福气、享受\n• 廉贞：才华、复杂、感性\n• 天府：稳重、积蓄、包容\n• 太阴：细腻、内敛、情感\n\n想了解更多关于紫微斗数的内容吗？';
      } else if (content.includes('十神') || content.includes('财')) {
        response = '关于十神中的正财与偏财：\n\n【正财】\n• 代表正业、稳定的收入\n• 象征辛勤工作获得的财富\n• 也代表正式的情感关系\n\n【偏财】\n• 代表意外之财、副业收入\n• 象征投机、投资、突发之财\n• 也代表非正式的情感关系\n\n在命理分析中：\n• 身强才能担财，身弱财多反为累\n• 财能生官，也能克印\n• 财星过多可能导致贪欲过盛\n\n想分析具体命盘中的财星情况吗？';
      } else {
        response = '感谢您的提问！命理学是一门博大精深的传统学问。\n\n我可以为您提供：\n• 八字排盘与解读\n• 紫微斗数分析\n• 大运流年推演\n• 五行平衡建议\n• 历史名人案例参考\n\n如果您想进行具体的命盘分析，请提供您的出生日期和时间（精确到小时）。\n\n请问您还有什么想了解的吗？';
      }

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setLoading(false);
    }, 1500);
  };

  return (
    <Layout title="智能问答" description="与 AI 命理智能体对话">
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>💬 智能问答</h1>
          <p style={{ fontSize: '1.1rem', color: theme.colors.textSecondary }}>
            与 AI 命理智能体对话，深入了解命盘含义
          </p>
        </div>

        <div style={{
          backgroundColor: theme.colors.surface, borderRadius: '1rem',
          border: `1px solid ${theme.colors.border}`, overflow: 'hidden',
          display: 'flex', flexDirection: 'column', height: 600,
        }}>
          <div style={{
            flex: 1, overflowY: 'auto', padding: '2rem',
            display: 'flex', flexDirection: 'column', gap: '1.5rem',
          }}>
            {messages.map((msg) => (
              <div key={msg.id} style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '80%',
              }}>
                <div style={{
                  fontSize: '0.75rem', color: theme.colors.textSecondary,
                  marginBottom: '0.25rem', textAlign: msg.role === 'user' ? 'right' : 'left',
                }}>
                  {msg.role === 'user' ? '您' : 'AI 智能体'}
                </div>
                <div style={{
                  padding: '1rem 1.25rem',
                  backgroundColor: msg.role === 'user' ? theme.colors.primary : theme.colors.background,
                  color: msg.role === 'user' ? 'white' : theme.colors.text,
                  borderRadius: msg.role === 'user' ? '1rem 1rem 0.25rem 1rem' : '1rem 1rem 1rem 0.25rem',
                  border: msg.role === 'assistant' ? `1px solid ${theme.colors.border}` : 'none',
                  whiteSpace: 'pre-wrap', lineHeight: 1.7,
                }}>
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div style={{ alignSelf: 'flex-start' }}>
                <div style={{ fontSize: '0.75rem', color: theme.colors.textSecondary, marginBottom: '0.25rem' }}>
                  AI 智能体
                </div>
                <div style={{
                  padding: '1rem 1.25rem', backgroundColor: theme.colors.background,
                  borderRadius: '1rem 1rem 1rem 0.25rem', border: `1px solid ${theme.colors.border}`,
                  display: 'flex', gap: '0.5rem',
                }}>
                  <span style={{
                    width: 8, height: 8, backgroundColor: theme.colors.textSecondary,
                    borderRadius: '50%', animation: 'pulse 1.4s ease-in-out infinite',
                  }} />
                  <span style={{
                    width: 8, height: 8, backgroundColor: theme.colors.textSecondary,
                    borderRadius: '50%', animation: 'pulse 1.4s ease-in-out infinite 0.2s',
                  }} />
                  <span style={{
                    width: 8, height: 8, backgroundColor: theme.colors.textSecondary,
                    borderRadius: '50%', animation: 'pulse 1.4s ease-in-out infinite 0.4s',
                  }} />
                </div>
              </div>
            )}
          </div>

          <div style={{ padding: '1rem 1.5rem', borderTop: `1px solid ${theme.colors.border}` }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1rem' }}>
              {quickQuestions.map((q, i) => (
                <button key={i} onClick={() => sendMessage(q)}
                  style={{
                    padding: '0.5rem 1rem', backgroundColor: theme.colors.background,
                    border: `1px solid ${theme.colors.border}`, borderRadius: '1rem',
                    fontSize: '0.85rem', color: theme.colors.text, cursor: 'pointer',
                  }}>
                  {q}
                </button>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendMessage())}
                placeholder="输入您的问题..."
                disabled={loading}
                style={{
                  flex: 1, padding: '0.875rem 1.25rem', fontSize: '1rem',
                  border: `1px solid ${theme.colors.border}`, borderRadius: '0.5rem',
                  backgroundColor: theme.colors.background, color: theme.colors.text,
                }}
              />
              <button onClick={() => sendMessage()} disabled={loading}
                style={{
                  padding: '0.875rem 1.5rem', backgroundColor: theme.colors.primary,
                  color: 'white', border: 'none', borderRadius: '0.5rem',
                  fontSize: '1rem', fontWeight: 500, cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.6 : 1,
                }}>发送</button>
            </div>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', color: theme.colors.textSecondary, fontSize: '0.875rem' }}>
          ⚠️ AI 回答仅供参考，命理学仅供研究与学习
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
          40% { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </Layout>
  );
}
