// 通用 API 响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  result?: T;
  reasoning_chain?: ReasoningStep[];
  error?: string;
  confidence?: number;
}

// 推理链步骤
export interface ReasoningStep {
  rule_id: string;
  description: string;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  confidence: number;
  timestamp?: string;
}

// 八字排盘请求
export interface BaziRequest {
  birth_date: string;
  birth_time: string;
  timezone?: string;
  location?: string;
  gender?: string;
}

// 八字排盘结果
export interface BaziResult {
  bazi_pillar: string;
  daymaster: string;
  year_stem: string;
  year_branch: string;
  month_stem: string;
  month_branch: string;
  day_stem: string;
  day_branch: string;
  hour_stem: string;
  hour_branch: string;
  wuxing: Record<string, number>;
  ten_gods?: Record<string, string[]>;
  nayin?: Record<string, string>;
  dayun?: DayunInfo[];
  liunian?: LiunianInfo[];
}

// 大运信息
export interface DayunInfo {
  step: number;
  stem: string;
  branch: string;
  ganzhi: string;
  age_range: string;
  age_start: number;
  age_end: number;
}

// 流年信息
export interface LiunianInfo {
  year: number;
  age: number;
  stem: string;
  branch: string;
  ganzhi: string;
}

// 紫微斗数排盘请求
export interface ZiweiRequest {
  birth_date: string;
  birth_time: string;
  timezone?: string;
  location?: string;
}

// 紫微斗数结果
export interface ZiweiResult {
  ziwei_palace: string;
  palaces: Record<string, string>;
  main_stars: string[];
  stars: Record<string, string>;
}

// 其他术数域通用结果
export interface QimenResult {
  hour_ganzhi: string;
  pan_type: string;
  gong_positions: Record<string, string>;
  bamen: Record<string, string>;
  jiuxing: Record<string, string>;
}

export interface LiurenResult {
  hour_zhi: string;
  yuejiang: string;
  guishen: Record<string, string>;
  liuchun: Record<string, string>;
}

export interface MeihuaResult {
  shang_gua: { name: string; symbol: string; element: string };
  xia_gua: { name: string; symbol: string; element: string };
  dong_yao?: string;
  ti_yong?: string;
}

export interface LiuyaoResult {
  gua: { name: string; symbol: string; element: string };
  liuqin?: Record<string, string>;
  liushen?: string[];
}

export interface TaiyiResult {
  jushu: number;
  taiyi_position: string;
  wenwang?: string[];
  tongyun?: string;
}

// 综合分析请求
export interface ComprehensiveRequest {
  name?: string;
  birth_date: string;
  birth_time: string;
  timezone?: string;
  location?: string;
  domains: string[];
}

// 综合分析结果
export interface ComprehensiveResult {
  results: Record<string, BaziResult | ZiweiResult | QimenResult | any>;
  summary: string;
  confidence: number;
}

// 历史名人信息
export interface HistoricalFigure {
  case_id: string;
  name: string;
  birth_date: string;
  birth_time: string;
  timezone: string;
  location: string;
  source: string;
  expected_results: {
    bazi_pillar?: string;
    daymaster?: string;
    notes?: string;
  };
}

// 术数域信息
export interface DomainInfo {
  id: string;
  name: string;
  description: string;
  status: string;
}

// 引擎状态
export interface EngineStatus {
  [key: string]: {
    name: string;
    status: string;
    version: string;
  };
}

// 聊天消息类型
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  attachments?: any[];
}
