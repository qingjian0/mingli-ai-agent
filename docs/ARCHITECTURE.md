# MingLi-AI-Agent 系统架构设计

**版本**: v1.0.0  
**最后更新**: 2026-06-08  
**作者**: Team MingLi

---

## 📐 架构总览

### 系统分层

```
┌─────────────────────────────────────────────────────────────┐
│                      用户交互层 (UI Layer)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Web Frontend (React/Vue)                            │   │
│  │  - Chat 界面 + 输入表单                             │   │
│  │  - 命盘渲染 (2D/3D)                                 │   │
│  │  - 推理链可视化                                      │   │
│  │  - 历史名人查询                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                    API 网关层 (Gateway)                      │
│  - 请求路由 & 速率限制                                       │
│  - 认证与授权                                                 │
│  - 请求/响应日志                                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    业务逻辑层 (Service)                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Agent 协调层                                      │     │
│  │  ├── BaZi Agent (八字推理)                        │     │
│  │  ├── ZiWei Agent (紫微推理)                       │     │
│  │  ├── Analysis Agent (综合分析)                    │     │
│  │  └── LLM Interpreter (解释生成)                   │     │
│  └────────────────────────────────────────────────────┘     │
│                       ↓                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  推理链管理 (Reasoning Chain Manager)             │     │
│  │  - 追踪每一步规则应用                              │     │
│  │  - 生成结构化推理链 JSON                          │     │
│  │  - 版本控制与审计日志                             │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 规则推理引擎层 (Engines)                     │
│  ┌──────────────┬──────────────┬────────────────────┐       │
│  │  BaZi        │  ZiWei       │  QiMen / ...      │       │
│  │  引擎        │  引擎        │  引擎              │       │
│  ├──────────────┼──────────────┼────────────────────┤       │
│  │ • 排盘       │ • 星盘生成   │ • 局数计算         │       │
│  │ • 十神推导   │ • 化忌分析   │ • 符号解读         │       │
│  │ • 流年运势   │ • 宫位解读   │ • 预测推演         │       │
│  └──────────────┴──────────────┴────────────────────┘       │
│                       ↓                                      │
│  ┌──────────────────────────────────────────────────┐       │
│  │  规则执行引擎 (Rule Execution Engine)           │       │
│  │  - 规则加载与评估                                │       │
│  │  - 版本管理与切换                                │       │
│  │  - 流派多版本支持                                │       │
│  │  - 规则缓存与性能优化                            │       │
│  └──────────────────────────────────────────────────┘       │
│                       ↓                                      │
│  ┌──────────────────────────────────────────────────┐       │
│  │  计算工具库 (Calculation Toolkit)               │       │
│  │  - 历法工具 (阴阳历转换、干支计算)              │       │
│  │  - 天文工具 (节气边界、时区处理)                │       │
│  │  - 数学工具 (纳音、五行、八卦算法)              │       │
│  └──────────────────────────────────────────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    数据持久层 (Data)                        │
│  ┌──────────────┬─────────────┬───────────────────┐         │
│  │  规则库      │  历史案例   │  用户数据          │         │
│  │  (版本管理)  │  (≥50验证)  │  (持久化)          │         │
│  ├──────────────┼─────────────┼───────────────────┤         │
│  │ • 规则 JSON  │ • 名人案例  │ • 用户查询历史    │         │
│  │ • 版本记录   │ • 验证断言  │ • 订阅信息         │         │
│  │ • 审计日志   │ • 回归测试  │ • 计费记录         │         │
│  └──────────────┴─────────────┴───────────────────┘         │
│                       ↓                                      │
│  • PostgreSQL (主数据库)                                    │
│  • Redis (缓存层)                                           │
│  • MongoDB (日志与文档存储)                                │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔌 核心组件详解

### 1. 推理引擎（Reasoning Engines）

#### 1.1 八字引擎 (BaZi Engine)

```python
class BaZiEngine(BaseEngine):
    """
    八字推理引擎
    - 支持多流派（月令派、从旺派等）
    - 完整推理链追踪
    """
    
    def calculate(self, person_info: PersonInfo) -> BaZiResult:
        """
        计算八字命盘
        
        流程:
        1. 时间转换 (公历→农历→八字)
        2. 排盘 (生成四柱八字)
        3. 十神推导 (计算十神关系)
        4. 格局分析 (判断命格)
        5. 大运流年 (推算流年运势)
        """
        pass
    
    def get_reasoning_chain(self) -> ReasoningChain:
        """返回完整推理链"""
        pass
```

**关键方法：**
- `calculate()` - 核心计算
- `get_ten_gods()` - 十神推导
- `analyze_pattern()` - 格局分析
- `predict_fortune()` - 大运流年推算

**输入参数：**
```json
{
  "name": "person_name",
  "birth_date": "YYYY-MM-DD",
  "birth_time": "HH:MM",
  "timezone": "UTC+8",
  "location": "city",
  "sectarian_school": "月令派" 
}
```

**输出结果：**
```json
{
  "bazi_pillar": "甲寅 乙巳 丙午 子時",
  "ten_gods": {
    "year": "...",
    "month": "...",
    "day": "...",
    "hour": "..."
  },
  "pattern": "正财格",
  "major_fortune": {...},
  "yearly_fortune": {...},
  "reasoning_chain": [
    {
      "step": 1,
      "description": "计算农历日期",
      "rule_id": "calendar.gregorian_to_lunar",
      "input": {...},
      "output": {...},
      "confidence": 0.99
    },
    ...
  ]
}
```

#### 1.2 紫微引擎 (ZiWei Engine)

```python
class ZiWeiEngine(BaseEngine):
    """
    紫微斗数推理引擎
    - 14主星 + 12杂曜
    - 化忌链分析
    - 多宫位解读
    """
    
    def calculate(self, person_info: PersonInfo) -> ZiWeiResult:
        """
        计算紫微命盘
        
        流程:
        1. 转换时间到农历
        2. 计算命宫 (定位14主星)
        3. 推导杂曜 (12杂曜分布)
        4. 分析化忌链 (星曜相互作用)
        5. 解读命运 (综合分析)
        """
        pass
```

**关键方法：**
- `calculate()` - 核心计算
- `get_major_stars()` - 14主星定位
- `get_minor_stars()` - 杂曜推导
- `analyze_transformation_chain()` - 化忌链分析

---

### 2. 规则执行引擎 (Rule Execution Engine)

```python
class RuleExecutionEngine:
    """
    通用规则执行引擎
    - 加载规则库
    - 版本管理
    - 规则评估与执行
    """
    
    def load_rules(self, engine_type: str, version: str = "latest"):
        """加载指定术数的规则库"""
        pass
    
    def execute_rule(self, rule_id: str, context: Dict) -> RuleResult:
        """执行单条规则"""
        pass
    
    def apply_rules(self, rules: List[str], context: Dict) -> List[RuleResult]:
        """批量执行规则"""
        pass
    
    def switch_sectarian_school(self, school: str):
        """切换流派 (支持多版本并存)"""
        pass
```

**规则库结构：**
```
rules/
├── schema/
│   └── rule_schema.json          # 规则定义模式
├── bazi/
│   ├── v1.0-月令派/
│   │   ├── base_rules.json
│   │   ├── heaven_stems.json
│   │   ├── earth_branches.json
│   │   └── ten_gods.json
│   ├── v1.0-从旺派/
│   └── versions.json             # 版本索引
├── ziwei/
│   ├── v1.0-南派/
│   ├── v1.0-北派/
│   └── versions.json
└── qimen/
    └── ...
```

---

### 3. Agent 协调层 (Agent Framework)

使用 LangChain/AutoGen 实现多 Agent 协调：

```python
class MingLiAgentFramework:
    """
    多 Agent 协调框架
    - BaZi Agent: 八字专用
    - ZiWei Agent: 紫微专用
    - Analysis Agent: 综合分析
    - Interpreter Agent: 自然语言解释
    """
    
    def process_query(self, user_query: str, person_info: PersonInfo):
        """
        多 Agent 协调查询处理
        
        流程:
        1. NLU Agent: 理解用户意图
        2. Routing Agent: 确定需要调用哪些计算引擎
        3. Calculation Agents: 并行执行八字、紫微等计算
        4. Analysis Agent: 综合多个结果进行分析
        5. Interpreter Agent: 用自然语言解释结果
        """
        pass
    
    def track_reasoning_chain(self):
        """追踪并记录完整推理链"""
        pass
```

---

### 4. 推理链管理 (Reasoning Chain Manager)

```python
class ReasoningChainManager:
    """
    推理链追踪与管理
    - 记录每一步的规则应用
    - 生成可视化数据结构
    - 支持审计与回溯
    """
    
    def start_chain(self, query_id: str):
        """开始一个新的推理链"""
        pass
    
    def add_step(self, 
                 step_id: str,
                 rule_id: str,
                 description: str,
                 inputs: Dict,
                 outputs: Dict,
                 confidence: float):
        """添加推理步骤"""
        pass
    
    def finalize_chain(self) -> ReasoningChain:
        """完成推理链并返回"""
        pass
    
    def to_json(self) -> str:
        """导出为 JSON 格式"""
        pass
    
    def to_visualization(self) -> Dict:
        """转换为前端可视化数据"""
        pass
```

**推理链 JSON 结构：**
```json
{
  "chain_id": "query_12345",
  "timestamp": "2026-06-08T10:00:00Z",
  "query": "输入出生时间 → 获得八字命盘",
  "total_steps": 5,
  "steps": [
    {
      "step_id": 1,
      "rule_id": "calendar.gregorian_to_lunar",
      "rule_name": "公历转农历",
      "rule_source": "万年历",
      "rule_version": "v1.0",
      "description": "将公历日期转换为农历",
      "input": {
        "gregorian_date": "1654-05-04",
        "gregorian_time": "23:30",
        "timezone": "UTC+8"
      },
      "output": {
        "lunar_date": "甲寅年 四月 初二",
        "lunar_time": "亥時"
      },
      "confidence": 0.99,
      "provenance": "《万年历》官方数据"
    },
    {
      "step_id": 2,
      "rule_id": "bazi.heavenly_stem_calculation",
      "rule_name": "天干计算",
      "description": "根据农历日期计算天干",
      "input": {
        "lunar_year": "甲寅",
        "lunar_month": "四月",
        "lunar_day": "初二"
      },
      "output": {
        "year_stem": "甲",
        "month_stem": "乙",
        "day_stem": "丙"
      },
      "confidence": 0.99,
      "provenance": "《滴天髓》"
    },
    ...
  ],
  "metadata": {
    "engine_used": ["bazi", "calendar"],
    "execution_time_ms": 245,
    "cached": false,
    "audit_log": [...]
  }
}
```

---

### 5. 历法工具库 (Calendar Toolkit)

```python
class CalendarToolkit:
    """
    历法计算工具
    - 阴阳历转换
    - 节气边界判断
    - 时区处理
    """
    
    def gregorian_to_lunar(self, date: datetime, tz: str) -> LunarDate:
        """公历 → 农历转换"""
        pass
    
    def lunar_to_gregorian(self, lunar_date: LunarDate) -> datetime:
        """农历 → 公历转换"""
        pass
    
    def get_solar_term(self, gregorian_date: datetime) -> str:
        """获取节气"""
        pass
    
    def is_leap_month(self, lunar_year: int) -> bool:
        """判断是否为闰月"""
        pass
    
    def handle_timezone(self, time: str, tz: str) -> datetime:
        """处理时区转换"""
        pass
```

---

### 6. 数据模型 (Data Models)

#### Person Model
```python
class PersonInfo:
    """
    人物基本信息
    """
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    timezone: str    # UTC±X
    location: str    # 城市/地点
    gender: str      # M/F
    notes: str       # 备注
```

#### BaZiResult Model
```python
class BaZiResult:
    """
    八字计算结果
    """
    bazi_pillar: str              # 四柱八字字符串
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    ten_gods: Dict[str, str]      # 十神分配
    pattern: str                  # 格局
    major_fortune: Dict           # 大运
    yearly_fortune: Dict          # 流年
    reasoning_chain: List[Dict]   # 推理链
```

#### ZiWeiResult Model
```python
class ZiWeiResult:
    """
    紫微计算结果
    """
    major_stars: Dict[str, Star]  # 14主星
    minor_stars: Dict[str, Star]  # 杂曜
    transformation_chain: List    # 化忌链
    palace_analysis: Dict         # 12宫分析
    reasoning_chain: List[Dict]   # 推理链
```

---

## 🔄 请求流程

### 典型请求流程（从输入到输出）

```
1. 用户输入
   ↓ (Web UI 或 API)
2. API Gateway
   ├── 请求验证
   ├── 认证检查
   └── 速率限制
   ↓
3. Agent 协调层
   ├── NLU: 理解用户意图
   ├── Routing: 决定调用哪些引擎
   └── Orchestration: 并行执行
   ↓
4. 推理引擎（可并行）
   ├── BaZi Engine: 八字排盘
   │   ├── 时间转换
   │   ├── 四柱排列
   │   ├── 十神推导
   │   └── 格局分析
   │
   ├── ZiWei Engine: 紫微排盘
   │   ├── 命宫定位
   │   ├── 主星分布
   │   ├── 化忌分析
   │   └── 宫位解读
   │
   └── Calendar Toolkit
       ├── 时间转换
       ├── 节气判断
       └── 时区处理
   ↓
5. 推理链管理
   ├── 记录每步计算
   ├── 追踪规则应用
   └── 生成结构化链
   ↓
6. 分析 Agent
   ├── 综合多个结果
   ├── 生成洞察
   └── 准备输出
   ↓
7. 解释 Agent (LLM)
   ├── 转换为自然语言
   ├── 格式化输出
   └── 生成建议
   ↓
8. 响应返回
   ├── 命盘数据
   ├── 推理链
   ├── 自然语言解释
   └── 置信度指标
   ↓
9. Web UI 渲染
   ├── 命盘可视化
   ├── 推理链展示
   ├── 聊天界面
   └── 交互功能
```

---

## 🗄️ 数据库设计

### 核心表结构

#### users 表
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    username VARCHAR(100),
    subscription_tier VARCHAR(50),  -- free/pro/vip
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### queries 表
```sql
CREATE TABLE queries (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    query_text TEXT,
    person_info JSONB,
    result JSONB,
    reasoning_chain JSONB,
    created_at TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

#### rules 表
```sql
CREATE TABLE rules (
    id UUID PRIMARY KEY,
    rule_id VARCHAR(255) UNIQUE,
    engine_type VARCHAR(50),       -- bazi/ziwei/qimen/...
    sectarian_school VARCHAR(100),  -- 流派
    version VARCHAR(50),
    content JSONB,
    source VARCHAR(255),
    priority INTEGER,
    validation_status VARCHAR(50),  -- draft/approved/deprecated
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    INDEX idx_engine_type (engine_type),
    INDEX idx_version (version)
);
```

#### validation_cases 表
```sql
CREATE TABLE validation_cases (
    id UUID PRIMARY KEY,
    case_id VARCHAR(255) UNIQUE,
    name VARCHAR(100),
    birth_date DATE,
    birth_time TIME,
    timezone VARCHAR(50),
    location VARCHAR(255),
    source VARCHAR(255),
    expected_results JSONB,
    test_status VARCHAR(50),  -- passed/failed
    last_tested TIMESTAMP,
    created_at TIMESTAMP
);
```

---

## 🔐 安全与可靠性

### 安全设计

1. **API 安全**
   - JWT 认证
   - API Key 管理
   - 速率限制 (Rate Limiting)
   - CORS 配置

2. **数据安全**
   - 数据库加密 (TLS)
   - 密码加密 (bcrypt)
   - 审计日志
   - GDPR 合规

3. **规则库保护**
   - 版本控制
   - 变更审批流程
   - 自动回滚机制
   - 定期备份

### 高可用性

1. **缓存策略**
   - Redis 缓存热数据
   - 规则库缓存（TTL 24h）
   - 计算结果缓存

2. **负载均衡**
   - 多实例部署
   - 自动扩缩容
   - 健康检查

3. **容灾备份**
   - 数据库主从复制
   - 定期全量备份
   - 灾难恢复计划

---

## 📊 性能指标

| 指标 | 目标 | 说明 |
|------|------|------|
| **API 响应时间** | <500ms | p95 响应时间 |
| **吞吐量** | >1000 req/s | 每秒请求数 |
| **缓存命中率** | >70% | 热数据缓存率 |
| **系统可用性** | >99.5% | SLA 保证 |
| **规则引擎准确率** | >95% | 规则应用准确性 |

---

## 🔄 扩展性设计

### 新引擎集成流程

添加新的术数域引擎（如奇门遁甲）只需：

1. 继承 `BaseEngine`
2. 实现 `calculate()` 方法
3. 定义规则库 (JSON)
4. 编写测试用例
5. 注册到 Agent 框架

```python
class QiMenEngine(BaseEngine):
    """奇门遁甲引擎"""
    
    def calculate(self, person_info: PersonInfo) -> QiMenResult:
        pass
    
    def get_reasoning_chain(self) -> ReasoningChain:
        pass
```

---

## 🚀 部署架构

```
互联网
  ↓
CDN (静态资源)
  ↓
API Gateway (nginx)
  ↓
┌─────────────────────────────┐
│  Kubernetes 集群             │
│  ┌───────────────────────┐  │
│  │ API Pods (3+)        │  │
│  │ - FastAPI 应用       │  │
│  │ - 自动扩缩容         │  │
│  └───────────────────────┘  │
│  ┌───────────────────────┐  │
│  │ Worker Pods (2+)     │  │
│  │ - 异步任务处理       │  │
│  │ - 批量计算           │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
  ↓
┌─────────────────────────────┐
│  数据存储层                   │
│  ├─ PostgreSQL (主数据库)   │
│  ├─ Redis (缓存)            │
│  └─ MongoDB (日志)          │
└─────────────────────────────┘
```

---

## 📝 总结

MingLi-AI-Agent 的架构设计遵循以下原则：

1. **分层清晰**: 从 UI 到数据库各层职责明确
2. **规则驱动**: 核心计算完全由规则引擎驱动，不依赖 LLM
3. **可追踪**: 每步推理都被完整记录与可视化
4. **可扩展**: 支持新术数域的无缝集成
5. **高可用**: 多实例、缓存、备份等保障可靠性
6. **企业级**: 安全、审计、合规等完整覆盖

下一步将基于本架构开始具体工程实现。
