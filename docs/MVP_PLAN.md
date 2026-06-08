# 第十部分：MVP最小可行产品方案

## MVP定义与目标

**MVP (Minimum Viable Product)**: 最小可行产品  
**范围**: M0-M2 (3个月)  
**目标用户**: 早期采用者 (术数爱好者、学生、专业人士)  
**成功指标**:
- 用户满意度 ≥ 4.0/5.0
- 八���计算准确度 > 90%
- 系统可用性 > 95%
- 单次查询响应时间 < 5秒

---

## MVP功能范围

### ✅ 包含的功能

#### 1. 基础认证系统
- 用户注册/登录
- JWT Token管理
- 基础权限控制

#### 2. 八字计算流程 (完整)
- 支持公历/农历输入
- 十天干十二地支排盘
- 五行分析
- 十神判断
- 大运流年计算 (基础)
- 吉凶预测 (基础)

#### 3. 知识库系统
- 导入50部古籍文本
- 基础文本分块
- 向量嵌入与索引
- 向量相似度搜索
- 基础知识检索

#### 4. 案例库系统
- 导入100+历史案例
- 案例搜索
- 案例对标

#### 5. 报告生成
- Markdown格式报告
- PDF导出
- 基础HTML报告

#### 6. API服务
- `/api/v1/auth/*` 认证端点
- `/api/v1/computations` 计算端点
- `/api/v1/knowledge/search` 知识搜索
- `/api/v1/cases/search` 案例搜索
- `/api/v1/reports/{request_id}` 报告下载

#### 7. Web用户界面
- 简洁的Web页面
- 表单输入
- 结果展示
- 报告下载

#### 8. 基础监控
- 日志收集
- 基础性能指标
- 错误追踪

### ❌ 暂不包含的功能

- 其他术数域 (紫微/奇门/六爻等) → Phase 2
- 高级推理审核 → Phase 3
- 工具系统 → Phase 3
- 多种报告格式 (DOCX/PPTX) → Phase 3
- 用户记忆与个性化 → Phase 2
- 知识库编辑管理界面 → Phase 2
- 管理后台 → Phase 2
- 移动应用 → Phase 2/3
- 企业级部署 (K8s) → Phase 4

---

## MVP技术栈

| 组件 | 选择 | 理由 |
|------|------|------|
| Web框架 | FastAPI | 轻量、快速、文档完善 |
| 数据库 | PostgreSQL | ACID、可靠、免费 |
| 缓存 | Redis | 简单、快速、消息队列 |
| 向量DB | Qdrant | 开源、易部署、功能完整 |
| LLM | Ollama + Qwen3:8B | 本地运行、免费、性能足够 |
| 前端 | HTML + Vue.js轻量版 | 简洁、快速开发 |
| 部署 | Docker Compose | 本地快速启动 |
| 文档 | Markdown + Swagger | 自动生成、易维护 |

---

## MVP架构简化版

```
┌─────────────────────────────┐
│     Web UI (HTML + Vue)     │
└────────────┬────────────────┘
             │
        ┌────▼────┐
        │ FastAPI │
        └────┬────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───▼──┐ ┌──▼───┐ ┌─▼────┐
│Authn ▼ │Calc  │ │RAG   │
└────────┴──────┴─┴──────┘
    │         │        │
┌───▼──────────▼──────▼───┐
│    PostgreSQL + Redis    │
│    + Qdrant + Ollama     │
└──────────────────────────┘
```

---

## MVP核心实现

### 1. 八字计算模块 (src/calculation/bazi/)

```python
class BaziCalculator:
    """八字排盘计算器"""
    
    def parse_birth_info(self, birth_date, birth_time, calendar_type):
        """解析出生信息，转换为农历"""
        pass
    
    def get_stems_branches(self, year, month, day, hour):
        """获取十天干十二地支"""
        pass
    
    def analyze_five_elements(self, stems_branches):
        """分析五行分布"""
        pass
    
    def calculate_ten_gods(self, day_stem, other_stems):
        """计算十神"""
        pass
    
    def generate_report(self, calculation_result):
        """生成报告"""
        pass
```

### 2. 知识检索模块 (src/rag/)

```python
class SimpleRetriever:
    """简单知识检索器"""
    
    async def embed_documents(self, documents):
        """将文档嵌入向量空间"""
        # 使用BGE-M3模型
        pass
    
    async def index_to_qdrant(self, embeddings):
        """索引到Qdrant"""
        pass
    
    async def search(self, query, top_k=5):
        """搜索相关知识"""
        # 1. 嵌入查询
        # 2. 向量搜索
        # 3. 返回Top-K结果
        pass
```

### 3. API层 (src/api/routes/computation.py)

```python
@app.post("/api/v1/computations")
async def submit_computation(
    request: ComputationRequest,
    user: User = Depends(get_current_user)
) -> ComputationResponse:
    """提交计算请求"""
    
    # 1. 验证输入
    # 2. 调用Planner拆解任务
    # 3. 调用Knowledge Agent检索相关知识
    # 4. 调用Calculation Agent进行计算
    # 5. 生成报告
    # 6. 存储结果
    # 7. 返回请求ID与链接
    pass

@app.get("/api/v1/computations/{request_id}")
async def get_computation_result(
    request_id: str,
    user: User = Depends(get_current_user)
) -> ComputationResultResponse:
    """获取计算结果"""
    pass
```

### 4. Web前端 (templates/index.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>天府AI命理分析</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div id="app">
        <h1>八字命理分析</h1>
        
        <form @submit="submitForm">
            <input v-model="form.birthYear" placeholder="出生年份" />
            <input v-model="form.birthMonth" placeholder="月份" />
            <input v-model="form.birthDay" placeholder="日期" />
            <input v-model="form.birthHour" placeholder="小时" />
            <button type="submit">分析</button>
        </form>
        
        <div v-if="loading" class="spinner">分析中...</div>
        
        <div v-if="result" class="result">
            <h2>分析结果</h2>
            <div v-html="result.content"></div>
            <a :href="result.pdf_url">下载PDF</a>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
    <script src="/static/app.js"></script>
</body>
</html>
```

---

## MVP数据流

### 完整的八字查询流程

```
1. 用户输入
   ├─ 出生年月日时
   ├─ 性别
   └─ 地点

2. API接收 (/api/v1/computations POST)
   ├─ 验证输入
   └─ 创建Computation Request

3. Supervisor Agent
   ├─ 识别意图: "八字分析"
   ├─ 分类任务: "calculation"
   └─ 分发到Planner

4. Planner Agent
   ├─ 拆解任务:
   │  ├─ Step 1: 知识检索
   │  ├─ Step 2: 八字计算
   │  └─ Step 3: 报告生成
   └─ 生成DAG

5. Orchestration 执行DAG
   │
   ├─ Step 1: Knowledge Agent
   │  ├─ 查询: "八字基础理论"
   │  ├─ 检索: [理论文本]
   │  └─ 返回: 知识上下文
   │
   ├─ Step 2: Calculation Agent
   │  ├─ 输入: 出生信息 + 知识上下文
   │  ├─ 执行: 排盘 → 五行分析 → 十神判断 → 预测
   │  └─ 返回: 计算结果
   │
   └─ Step 3: Report Agent
      ├─ 输入: 计算结果
      ├─ 生成: Markdown报告
      ├─ 转换: PDF
      └─ 返回: 报告URL

6. 存储结果
   ├─ PostgreSQL: 计算结果、步骤日志
   ├─ File System: PDF文件
   └─ Redis: 缓存 (1小时)

7. 返回给用户
   ├─ request_id: "comp_20250608_001"
   ├─ result_url: "/api/v1/computations/comp_20250608_001/result"
   └─ pdf_url: "/files/reports/comp_20250608_001.pdf"
```

---

## MVP部署方案

### 本地开发环境

#### 前置要求
```bash
- Python 3.9+
- Docker & Docker Compose
- 至少16GB RAM
- RTX3050或以上GPU (可选)
```

#### 快速启动

```bash
# 1. 克隆仓库
git clone https://github.com/qingjian0/mingli-ai-agent.git
cd mingli-ai-agent

# 2. 配置环境
cp .env.example .env

# 3. 启动服务
docker-compose -f docker-compose.dev.yml up -d

# 4. 初始化数据库
docker exec mingli-api python -m alembic upgrade head

# 5. 导入知识库
docker exec mingli-api python scripts/import_knowledge_base.py

# 6. 访问应用
# Web: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### docker-compose.dev.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: mingli
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: mingli_db
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve

  mingli-api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://mingli:dev_password@postgres:5432/mingli_db
      REDIS_URL: redis://redis:6379/0
      QDRANT_URL: http://qdrant:6333
      OLLAMA_URL: http://ollama:11434
    depends_on:
      - postgres
      - redis
      - qdrant
      - ollama
    volumes:
      - .:/app
    command: uvicorn src.api.app:app --host 0.0.0.0 --reload

volumes:
  pg_data:
  redis_data:
  qdrant_data:
  ollama_data:
```

---

## MVP初始数据

### 知识库 (50+部古籍)

#### 八字相关
- 滴天髄
- 三命通会
- 渊海子平
- 八字基础理论汇编
- ... (共20部)

#### 通用参考
- 易经
- 周易正义
- 十干十二支详解
- ... (共30部)

### 历史案例库 (100+案例)

#### 历史人物 (50+案例)
- 康熙帝
- 乾隆帝
- 曾国藩
- 林则徐
- ... (50多位历史名人八字分析与验证)

#### 验证案例 (50+案例)
- 已实现的准确预测
- 性格特征匹配
- 事业运势对应
- ... (50多个实际验证案例)

### 算法与规则库
- 十天干十二地支关系表
- 五行生克制化规则
- 十神判断规则
- 大运流年计算规则
- 吉凶预测规则
- 日历转换表

---

## MVP测试计划

### 单元测试 (>80% 覆盖率)

```python
# tests/test_bazi_calculator.py
class TestBaziCalculator:
    def test_parse_birth_info(self):
        """测试出生信息解析"""
        pass
    
    def test_stems_branches_calculation(self):
        """测试十天干十二地支计算"""
        pass
    
    def test_five_elements_analysis(self):
        """测试五行分析"""
        pass
    
    def test_known_cases(self):
        """测试已知历史案例"""
        # 验证康熙帝八字计算正确性
        # 验证乾隆帝八字计算正确性
        # ...
        pass
```

### 集成测试

```python
# tests/test_integration.py
class TestComputationFlow:
    async def test_complete_bazi_flow(self):
        """测试完整的八字计算流程"""
        # 1. 提交计算请求
        # 2. 等待完成
        # 3. 验证结果正确性
        # 4. 验证报告生成
        pass
    
    async def test_knowledge_retrieval(self):
        """测试知识检索"""
        pass
    
    async def test_pdf_generation(self):
        """测试PDF生成"""
        pass
```

### 手动测试用例库

| 用例ID | 测试场景 | 预期结果 | 状态 |
|--------|---------|---------|------|
| T001 | 输入有效八字 | 成功计算并生成报告 | ✅ |
| T002 | 输入无效日期 | 显示错误提示 | ✅ |
| T003 | 并发查询10个请求 | 全部成功完成 | ✅ |
| T004 | 查询结果下载PDF | PDF文件完整 | ✅ |
| T005 | 查询历史人物八字 | 与已知结果匹配 | ✅ |

---

## MVP验收标准

### 功能验收

- [x] 用户能够注册/登录
- [x] 用户能够输入出生信息
- [x] 系统能够正确计算八字
- [x] 系统能够生成Markdown报告
- [x] 系统能够生成PDF报告
- [x] 用户能够下载报告
- [x] 知识搜索功能可用
- [x] 案例搜索功能可用

### 性能验收

- [ ] 单次查询响应时间 < 5秒 (P95)
- [ ] 系统可支持10并发用户
- [ ] 内存使用 < 8GB
- [ ] CPU使用 < 80%

### 质量验收

- [ ] 代码覆盖率 > 80%
- [ ] 八字计算准确度 > 90% (基于历史案例验证)
- [ ] 没有高危bug
- [ ] 用户满意度 > 4.0/5.0 (基于内测反馈)

### 文档验收

- [ ] API文档完整 (Swagger自动生成)
- [ ] 部署指南完整
- [ ] 开发指南完整
- [ ] 用户指南完整

---

## MVP推出计划

### 内测阶段 (M2末)
- 邀请20位内测用户
- 收集反馈
- 快速迭代修复

### 早期发布 (M2末-M3初)
- 在GitHub发布源代码
- 在社区宣传
- 邀请有兴趣的用户

### 反馈收集
- 用户反馈表单
- 问题追踪系统
- 定期改进

---

## MVP成功指标

| 指标 | 目标 | 当前 | 状态 |
|------|------|------|------|
| 用户注册数 | 100+ | - | 跟踪中 |
| 日活用户 | 20+ | - | 跟踪中 |
| 计算准确度 | > 90% | - | 测试中 |
| API响应时间 (P95) | < 5s | - | 测试中 |
| 用户满意度 | > 4.0/5.0 | - | 测试中 |
| 系统可用性 | > 95% | - | 监控中 |
