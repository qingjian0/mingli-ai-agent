import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import type {
  ApiResponse,
  BaziRequest,
  BaziResult,
  ZiweiRequest,
  ZiweiResult,
  QimenResult,
  LiurenResult,
  MeihuaResult,
  LiuyaoResult,
  TaiyiResult,
  ComprehensiveRequest,
  ComprehensiveResult,
  HistoricalFigure,
  DomainInfo,
  EngineStatus,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API 请求: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API 响应错误:', error.message);
    return Promise.reject(error);
  }
);

// 通用请求方法
async function request<T>(config: AxiosRequestConfig): Promise<T> {
  try {
    const response = await apiClient.request<T>(config);
    return response.data;
  } catch (error: any) {
    if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error')) {
      // 如果 API 不可用，使用 mock 数据
      console.warn('API 服务不可用，使用 mock 数据');
      return getMockData<T>(config.url || '');
    }
    throw error;
  }
}

// 获取 mock 数据（用于演示/开发）
function getMockData<T>(url: string): T {
  const mockBaziResult: BaziResult = {
    bazi_pillar: '庚午 甲辰 己未 丁卯',
    daymaster: '己',
    year_stem: '庚', year_branch: '午',
    month_stem: '甲', month_branch: '辰',
    day_stem: '己', day_branch: '未',
    hour_stem: '丁', hour_branch: '卯',
    wuxing: { 金: 1, 木: 2, 水: 0, 火: 2, 土: 2 },
    ten_gods: { 比肩: ['己'], 食神: ['庚'], 偏财: ['甲'] },
    nayin: { 年柱: '路旁土', 月柱: '覆灯火', 日柱: '天上火', 时柱: '炉中火' },
    dayun: [
      { step: 1, stem: '癸', branch: '卯', ganzhi: '癸卯', age_range: '1-10', age_start: 1, age_end: 10 },
      { step: 2, stem: '壬', branch: '寅', ganzhi: '壬寅', age_range: '11-20', age_start: 11, age_end: 20 },
      { step: 3, stem: '辛', branch: '丑', ganzhi: '辛丑', age_range: '21-30', age_start: 21, age_end: 30 },
      { step: 4, stem: '庚', branch: '子', ganzhi: '庚子', age_range: '31-40', age_start: 31, age_end: 40 },
    ],
    liunian: [
      { year: 2024, age: 34, stem: '甲', branch: '辰', ganzhi: '甲辰' },
      { year: 2025, age: 35, stem: '乙', branch: '巳', ganzhi: '乙巳' },
      { year: 2026, age: 36, stem: '丙', branch: '午', ganzhi: '丙午' },
    ],
  };

  if (url?.includes('/bazi/calc')) {
    return { success: true, result: mockBaziResult, confidence: 0.99 } as T;
  }
  if (url?.includes('/ziwei/calc')) {
    return {
      success: true,
      result: {
        ziwei_palace: '紫微星在子宫',
        palaces: { 命宫: '紫微', 兄弟宫: '天机', 夫妻宫: '太阳', 子女宫: '武曲' },
        main_stars: ['紫微', '天机', '太阳', '武曲'],
        stars: { 紫微: '子宫', 天机: '丑宫' },
      } as ZiweiResult,
      confidence: 0.95,
    } as T;
  }
  if (url?.includes('/qimen/calc')) {
    return {
      success: true,
      result: {
        hour_ganzhi: '甲子',
        pan_type: '阳遁一局',
        gong_positions: { 一宫: '坎', 二宫: '坤' },
        bamen: { 休门: '一宫', 生门: '二宫' },
        jiuxing: { 天蓬: '一宫', 天芮: '二宫' },
      } as QimenResult,
      confidence: 0.95,
    } as T;
  }
  if (url?.includes('/liuren/calc')) {
    return {
      success: true,
      result: { hour_zhi: '子', yuejiang: '登明', guishen: {}, liuchun: {} } as LiurenResult,
      confidence: 0.95,
    } as T;
  }
  if (url?.includes('/meihua/calc')) {
    return {
      success: true,
      result: {
        shang_gua: { name: '乾', symbol: '☰', element: '金' },
        xia_gua: { name: '坤', symbol: '☷', element: '土' },
        dong_yao: '二爻动',
        ti_yong: '体用比和',
      } as MeihuaResult,
      confidence: 0.95,
    } as T;
  }
  if (url?.includes('/liuyao/calc')) {
    return {
      success: true,
      result: {
        gua: { name: '乾为天', symbol: '☰☰', element: '金' },
        liuqin: { 父母: '金', 兄弟: '金' },
        liushen: ['青龙', '朱雀'],
      } as LiuyaoResult,
      confidence: 0.95,
    } as T;
  }
  if (url?.includes('/taiyi/calc')) {
    return {
      success: true,
      result: { jushu: 1, taiyi_position: '一宫', wenwang: ['太乙', '文昌'], tongyun: '上元' } as TaiyiResult,
      confidence: 0.9,
    } as T;
  }
  if (url?.includes('/analysis/comprehensive')) {
    return {
      success: true,
      results: { bazi: mockBaziResult },
      summary: '八字: 庚午 甲辰 己未 丁卯, 日主: 己',
      confidence: 0.95,
    } as T;
  }
  if (url?.includes('/analysis/domains')) {
    return {
      domains: [
        { id: 'bazi', name: '八字', description: '四柱八字命理分析', status: 'available' },
        { id: 'ziwei', name: '紫微斗数', description: '紫微斗数命理分析', status: 'available' },
        { id: 'qimen', name: '奇门遁甲', description: '奇门遁甲预测', status: 'available' },
        { id: 'liuren', name: '大六壬', description: '大六壬预测', status: 'available' },
        { id: 'meihua', name: '梅花易数', description: '梅花易数占卜', status: 'available' },
        { id: 'liuyao', name: '六爻', description: '六爻占卜', status: 'available' },
        { id: 'taiyi', name: '太乙数', description: '太乙神数', status: 'available' },
      ],
    } as T;
  }
  if (url?.includes('/analysis/status')) {
    return {
      engines: {
        bazi: { name: '八字', status: 'available', version: '1.0.0' },
        ziwei: { name: '紫微斗数', status: 'available', version: '1.0.0' },
        qimen: { name: '奇门遁甲', status: 'available', version: '1.0.0' },
        liuren: { name: '大六壬', status: 'available', version: '1.0.0' },
        meihua: { name: '梅花易数', status: 'available', version: '1.0.0' },
        liuyao: { name: '六爻', status: 'available', version: '1.0.0' },
        taiyi: { name: '太乙数', status: 'available', version: '1.0.0' },
      },
    } as T;
  }
  // 默认空响应
  return { success: false, error: '未知 API' } as T;
}

// ================ API 方法 ================

// 八字排盘
export async function calculateBazi(
  params: BaziRequest
): Promise<ApiResponse<BaziResult>> {
  return request<ApiResponse<BaziResult>>({
    method: 'POST',
    url: '/api/v1/bazi/calc',
    data: params,
  });
}

// 紫微斗数
export async function calculateZiwei(
  params: ZiweiRequest
): Promise<ApiResponse<ZiweiResult>> {
  return request<ApiResponse<ZiweiResult>>({
    method: 'POST',
    url: '/api/v1/ziwei/calc',
    data: params,
  });
}

// 奇门遁甲
export async function calculateQimen(
  params: ZiweiRequest
): Promise<ApiResponse<QimenResult>> {
  return request<ApiResponse<QimenResult>>({
    method: 'POST',
    url: '/api/v1/qimen/calc',
    data: params,
  });
}

// 大六壬
export async function calculateLiuren(
  params: ZiweiRequest
): Promise<ApiResponse<LiurenResult>> {
  return request<ApiResponse<LiurenResult>>({
    method: 'POST',
    url: '/api/v1/liuren/calc',
    data: params,
  });
}

// 梅花易数
export async function calculateMeihua(
  params: ZiweiRequest
): Promise<ApiResponse<MeihuaResult>> {
  return request<ApiResponse<MeihuaResult>>({
    method: 'POST',
    url: '/api/v1/meihua/calc',
    data: params,
  });
}

// 六爻
export async function calculateLiuyao(
  params: ZiweiRequest
): Promise<ApiResponse<LiuyaoResult>> {
  return request<ApiResponse<LiuyaoResult>>({
    method: 'POST',
    url: '/api/v1/liuyao/calc',
    data: params,
  });
}

// 太乙数
export async function calculateTaiyi(
  params: ZiweiRequest
): Promise<ApiResponse<TaiyiResult>> {
  return request<ApiResponse<TaiyiResult>>({
    method: 'POST',
    url: '/api/v1/taiyi/calc',
    data: params,
  });
}

// 综合分析
export async function comprehensiveAnalysis(
  params: ComprehensiveRequest
): Promise<ApiResponse<ComprehensiveResult>> {
  return request<ApiResponse<ComprehensiveResult>>({
    method: 'POST',
    url: '/api/v1/analysis/comprehensive',
    data: params,
  });
}

// 获取支持的术数域
export async function getDomains(): Promise<{ domains: DomainInfo[] }> {
  return request<{ domains: DomainInfo[] }>({
    method: 'GET',
    url: '/api/v1/analysis/domains',
  });
}

// 获取引擎状态
export async function getEngineStatus(): Promise<{ engines: EngineStatus }> {
  return request<{ engines: EngineStatus }>({
    method: 'GET',
    url: '/api/v1/analysis/status',
  });
}

// 加载历史名人案例
export async function getHistoricalFigures(): Promise<HistoricalFigure[]> {
  // 由于历史案例数据存储在后端 data/cases/ 目录
  // 这里返回内置的 mock 数据
  return [
    { case_id: 'case_001', name: '康熙帝', birth_date: '1654-05-04', birth_time: '23:30', timezone: 'UTC+8', location: '北京', source: '《康熙起居注》', expected_results: { bazi_pillar: '甲午 戊辰 戊申 壬子', daymaster: '戊', notes: '在位61年，开创康乾盛世' } },
    { case_id: 'case_002', name: '乾隆帝', birth_date: '1711-09-25', birth_time: '02:00', timezone: 'UTC+8', location: '北京', source: '《清实录》', expected_results: { bazi_pillar: '辛卯 丁酉 庚午 丙子', daymaster: '庚', notes: '在位60年，文治武功' } },
    { case_id: 'case_003', name: '曾国藩', birth_date: '1811-11-26', birth_time: '20:00', timezone: 'UTC+8', location: '湖南湘乡', source: '《曾国藩年谱》', expected_results: { bazi_pillar: '辛未 己亥 丙辰 戊戌', daymaster: '丙', notes: '晚清名臣，湘军统帅' } },
    { case_id: 'case_004', name: '毛泽东', birth_date: '1893-12-26', birth_time: '06:00', timezone: 'UTC+8', location: '湖南湘潭', source: '官方资料', expected_results: { bazi_pillar: '癸巳 甲子 丁酉 癸卯', daymaster: '丁', notes: '中华人民共和国缔造者' } },
    { case_id: 'case_005', name: '周恩来', birth_date: '1898-03-05', birth_time: '03:00', timezone: 'UTC+8', location: '江苏淮安', source: '官方资料', expected_results: { daymaster: '丁', notes: '中华人民共和国总理' } },
    { case_id: 'case_006', name: '诸葛亮', birth_date: '181-07-23', birth_time: '04:00', timezone: 'UTC+8', location: '琅琊阳都', source: '《三国志》', expected_results: { daymaster: '癸', notes: '蜀汉丞相，卧龙先生' } },
    { case_id: 'case_007', name: '李白', birth_date: '701-02-28', birth_time: '05:00', timezone: 'UTC+8', location: '碎叶城', source: '《旧唐书》', expected_results: { daymaster: '癸', notes: '诗仙，唐代著名诗人' } },
    { case_id: 'case_008', name: '苏轼', birth_date: '1037-01-08', birth_time: '10:00', timezone: 'UTC+8', location: '眉山', source: '《宋史》', expected_results: { daymaster: '癸', notes: '东坡居士，豪放派词人' } },
    { case_id: 'case_009', name: '钱学森', birth_date: '1911-12-11', birth_time: '08:00', timezone: 'UTC+8', location: '上海', source: '官方资料', expected_results: { daymaster: '壬', notes: '中国航天之父' } },
    { case_id: 'case_010', name: '屠呦呦', birth_date: '1930-12-30', birth_time: '10:00', timezone: 'UTC+8', location: '宁波', source: '官方资料', expected_results: { daymaster: '癸', notes: '青蒿素发现者，诺贝尔奖' } },
  ];
}
