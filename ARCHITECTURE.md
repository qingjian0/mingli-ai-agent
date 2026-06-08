# TianFu-Agent 系统架构设计文档

## 项目总体概述

**项目名称**: TianFu-Agent (天府智能体)  
**项目目标**: 打造企业级专业术数命理易学Agent平台  
**技术栈**: Python, FastAPI, PostgreSQL, Redis, Qdrant, Ollama (Qwen3:8B)  
**部署方式**: Docker + 本地/私有云  
**用户硬件**: AMD Ryzen 7 5800U, 16GB RAM, RTX3050 Laptop 4GB, WSL2

---

## 第一部分：系统总体架构

系统采用**分层架构**，从上到下包括：

### 1. 用户界面层 (UI Layer)
- Web前端 (React/Vue)
- 移动API (RESTful)
- 第三方集成接口

### 2. API网关与认证层 (Gateway & Auth)
- 请求路由与转发
- 速率限制
- 认证/授权 (RBAC)
- 审计日志

### 3. 编排与路由层 (Orchestration Layer)
- **Supervisor Agent**: 监督整个流程
- **事件驱动架构**: Event Bus用于跨Agent通信
- **Planner Agent**: 任务拆解与规划

### 4. 核心处理层 (Core Processing Layer)
- **计算引擎**: 八字/紫微/奇门/六爻/风水等
- **推理引擎**: 逻辑验证、一致性检查
- **验证引擎**: 事实检验、术数一致性

### 5. RAG与知识层 (RAG & Knowledge Layer)
- **检索系统**: 混合搜索(BM25 + Dense + KG)
- **融合引擎**: 多源知识融合、冲突检测
- **向量数据库**: Qdrant

### 6. 持久化与状态管理层 (Persistence Layer)
- PostgreSQL (关系数据)
- Redis (缓存与会话)
- Qdrant (向量数据)
- 文件系统 (文档存储)

### 7. 工具与集成层 (Tools & Integration)
- Python工具
- Web浏览器
- 文件系统
- 数据库
- API调用

### 8. LLM推理层 (LLM Inference)
- Ollama服务器
- Qwen3:8B模型
- 提示工程
- 上下文管理

### 9. 可观测性与监控 (Observability)
- 结构化日志
- 指标收集 (Prometheus)
- 分布式追踪 (Jaeger)
- 审计日志

---

## 第二部分：模块关系图

### 核心模块依赖关系

```
API Gateway
    ↓
Supervisor Agent (总指挥)
    ↓
Planner Agent (任务拆解)
    ↓
[Knowledge] [Calculation] [Research] [Memory] [Reasoning] [Review] [Report] [Tool]
    ↓
Persistence Layer (PostgreSQL + Redis + Qdrant)
    ↓
LLM + Tools (输出结果)
```

### 模块职责

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| Supervisor | 总体协调、决策 | 用户请求 | 任务分配 |
| Planner | 任务分解、DAG生成 | 原始任务 | 执行计划 |
| Knowledge | RAG检索、知识融合 | 查询 | 相关知识 |
| Calculation | 术数计算 | 出生信息 | 命盘数据 |
| Research | 网页搜索、数据获取 | 关键词 | 外部信息 |
| Memory | 用户记忆、历史追踪 | 结果数据 | 持久化结果 |
| Reasoning | 推理分析 | 原始数据 | 洞察 |
| Review | 质量检验 | 完整分析 | 审核结果 |
| Report | 报告生成 | 所有分析结果 | 多格式报告 |
| Tool | 工具调用 | 工具参数 | 工具结果 |

---

## 第三部分：Multi-Agent架构

### Agent层级结构

#### Level 1: Supervisor (主要编排器)
```python
class SupervisorAgent(BaseAgent):
    """主管理器，协调所有其他Agent"""
    
    async def process(self, request: UserRequest) -> Response:
        1. 识别用户意图
        2. 分类任务类型
        3. 分配资源
        4. 调度Planner
        5. 监控执行进度
        6. 处理错误恢复
        7. 返回最终结果
```

#### Level 2a: Planner Agent (规划者)
```python
class PlannerAgent(BaseAgent):
    """任务规划者"""
    
    async def plan(self, task: Task) -> ExecutionPlan:
        1. 任务分解 (递归)
        2. 依赖分析
        3. 生成DAG (有向无环图)
        4. 资源估计
        5. Agent分配
        6. 状态管理
```

#### Level 2b: Event Bus (事件总线)
```python
class EventBus:
    """异步事件驱动通信"""
    
    - TaskCreated
    - TaskStarted
    - TaskCompleted
    - TaskFailed
    - StepUpdated
    - KnowledgeRetrieved
    - CalculationDone
    - ReviewStarted
    - QualityIssue
    - ReportGenerated
    - MemoryUpdated
    - ErrorOccurred
```

#### Level 3: 专业Agent集群

**Knowledge Agent** (知识检索)
- RAG查询
- 文档排序
- 知识融合
- 来源引用
- 冲突检测

**Calculation Agent** (计算引擎)
- 八字排盘
- 紫微排盘
- 奇门排盘
- 六爻排盘
- 风水计算
- 择日算法
- 姓名分析
- 相学分析

**Research Agent** (研究助手)
- 网页搜索
- 数据获取
- 内容解析
- 数据提炼

**Memory Agent** (记忆管理)
- 长期记忆 (LTM)
- 短期记忆 (STM)
- 语义记忆 (Semantic)
- 案例档案

**Reasoning Agent** (推理分析)
- 逻辑检验
- 一致性检查
- 异常检测
- 洞察生成
- 预测评分

**Review Agent** (质量审核)
- 事实检验
- 术数一致性
- 质量评分
- 合规检查
- 批准/拒绝

**Report Agent** (报告生成)
- 模板选择
- 数据格式化
- Markdown构建
- PDF生成
- DOCX导出
- HTML格式化

**Tool Agent** (工具调用)
- 工具注册表
- 工具调用
- 错误处理
- 结果解析
- 工具链

---

## 第四部分：RAG系统架构

### 检索管道 (Retrieval Pipeline)

```
用户查询
    ↓
查询处理 (分词、规范化、纠错、实体识别)
    ↓
[并行执行]
├─ BM25 关键词搜索
├─ Dense 向量搜索 (Qdrant)
└─ Knowledge Graph 检索
    ↓
结果融合 (去重、评分合并、集成)
    ↓
多查询扩展 (生成备选查询、递归检索)
    ↓
父子文档检索 (展开上下文)
    ↓
重排序 (LLM-based、相关性评分、多样性提升)
    ↓
元数据过滤 (域、类型、质量、可信度)
    ↓
来源归因与引用生成
    ↓
返回Top-K结果
```

### Qdrant 向量数据库配置

```python
# 集合架构
Collections = {
    "knowledge_chunks": {
        "vector_dim": 768,
        "distance": "Cosine",
        "index": "HNSW",
        "payload_schema": {
            "chunk_id": int,
            "source_id": int,
            "domain": "keyword",  # 索引
            "content_type": "keyword",  # 索引
            "quality_score": "float",  # 索引
            "trustworthiness": "float",  # 索引
            "created_at": "datetime",  # 索引
            "entities": ["string"],
            "is_current": "bool"
        }
    },
    "historical_cases": { ... },
    "reference_materials": { ... },
    "computation_results_cache": { ... }
}
```

### 知识融合策略

1. **冲突检测**: 识别相互矛盾的知识
2. **信证排序**: 按权威性、可信度排序
3. **融合方法**:
   - 多数投票 (Majority Vote)
   - 权威基础 (Authority-based)
   - 专家认可 (Expert Endorsement)
   - 显式标记 (Explicit Flagging 给LLM决策)

---

## 第五部分：知识工程架构

### 知识生命周期 (8个阶段)

#### Stage 1: 获取 (Acquisition)
- 内部: 专家笔记、历史案例、计算结果
- 外部: 古籍、学术论文、权威书籍、公共数据库
- 多模态: 文本、PDF、图像、表格、视频

#### Stage 2: 摄入与验证 (Intake & Validation)
- 源注册 (元数据、权威评级、可靠性评分)
- 初始质量检查 (格式、编码、完整性、安全扫描)
- 权利与许可检查 (版权、许可证、商业使用权)

#### Stage 3: 处理与丰富 (Processing & Enrichment)
- 文本处理 (分词、POS标注、依存解析)
- 信息提取 (NER、关系提取、属性提取)
- 语义丰富 (消歧义、同义词链接、概念链接)

#### Stage 4: 分类与标记 (Classification & Tagging)
- 域分类 (8个主要域)
- 内容类型分类 (定义、理论、技术、公式、案例等)
- 质量评级 (1-5 可信度等级)
- 时间分类 (长青、季节性、热门、历史、过时)

#### Stage 5: 注解与元数据 (Annotation & Metadata)
- 手动注解 (专家评审)
- 半自动注解 (ML预处理 + 人类审核)
- 元数据Schema (源、版本、分类、链接、生命周期)

#### Stage 6: 向量化与索引 (Vectorization & Indexing)
- 嵌入生成 (BGE-M3, 768维)
- Qdrant索引构建
- BM25全文索引
- 元数据索引

#### Stage 7: 版本管理与演进 (Version Management)
- 语义版本控制 (MAJOR.MINOR.PATCH)
- 完整变更历史
- 依赖追踪
- 审计日志

#### Stage 8: 质量保证与生命周期 (QA & Lifecycle)
- 自动质量检查 (Schema验证、去重、一致性)
- 周期性审查 (季度/年度)
- 弃用与归档
- 健康监控

### 知识存储结构

```
knowledge_base/
├── domains/
│   ├── bazi/
│   │   ├── concepts.json
│   │   ├── methods.json
│   │   ├── formulas.json
│   │   ├── cases/
│   │   ├── reference/
│   │   └── metadata.json
│   ├── ziwei/
│   ├── qimen/
│   └── ...
├── entities/
│   ├── concepts.jsonl
│   ├── people.jsonl
│   └── relationships.jsonl
├── embeddings/
│   ├── model_info.json
│   └── vectors.bin
└── indices/
    ├── qdrant_config/
    ├── bm25_index/
    └── entity_index/
```

---

## 第六部分：数据库设计

### 数据库选型

| 数据库 | 用途 | 为什么 |
|--------|------|--------|
| PostgreSQL | 结构化业务数据 | ACID保证、复杂查询、参照完整性 |
| Redis | 缓存与会话 | 亚毫秒延迟、Pub/Sub、速率限制 |
| Qdrant | 向量搜索 | 专为语义搜索优化、元数据过滤 |
| 文件系统 | 文档存储 | 简单备份、版本控制 |

### PostgreSQL 核心表

```sql
-- 用户与认证
users (id, username, email, roles, status, ...)
user_profiles (user_id, birth_date, location, ...)
user_sessions (id, user_id, token_hash, expires_at, ...)

-- 计算请求
computation_requests (id, user_id, domain, status, input_data, result_data, ...)
computation_steps (id, request_id, agent_type, status, input_data, output_data, ...)

-- 知识存储
knowledge_sources (id, source_name, authority_level, trustworthiness_score, ...)
knowledge_chunks (id, source_id, content, domain, content_type, quality_score, ...)
knowledge_chunk_entities (id, chunk_id, entity_type, entity_name, ...)

-- 案例库
historical_cases (id, case_name, primary_domain, verification_status, ...)

-- 用户记忆
user_conversation_history (id, session_id, role, content, ...)
user_case_saved (user_id, case_id, ...)

-- 审计与合规
audit_log (id, user_id, action_type, entity_type, ...)
```

### Redis 键策略

```
session:{session_id}          # 会话数据
user:{user_id}:profile        # 用户资料缓存
rate_limit:{user_id}:{ep}     # 速率限制
queue:computations            # 计算队列
user:{uid}:conversation:{sid} # 对话历史(最近)
cache:knowledge:{chunk_id}    # 知识缓存
```

### Qdrant 集合设计

```python
Collections = {
    "knowledge_chunks": {
        "vectors": 768,
        "distance": "Cosine",
        "payloads": {
            "chunk_id", "source_id", "domain", "content_type",
            "quality_score", "trustworthiness", "created_at",
            "entities", "is_current"
        }
    },
    "historical_cases": { ... },
    "reference_materials": { ... },
    "computation_cache": { ... }
}
```

---

## 第七部分：目录结构

```
mingli-ai-agent/
├── src/
│   ├── core/                  # 核心层
│   │   ├── agent.py
│   │   ├── task.py
│   │   ├── event.py
│   │   ├── memory.py
│   │   └── exceptions.py
│   │
│   ├── orchestration/         # 编排层
│   │   ├── supervisor.py
│   │   ├── planner.py
│   │   ├── router.py
│   │   ├── dispatcher.py
│   │   ├── workflow_engine.py
│   │   └── event_bus.py
│   │
│   ├── agents/                # Agent实现
│   │   ├── knowledge_agent.py
│   │   ├── calculation_agent.py
│   │   ├── research_agent.py
│   │   ├── memory_agent.py
│   │   ├── reasoning_agent.py
│   │   ├── review_agent.py
│   │   ├── report_agent.py
│   │   └── tool_agent.py
│   │
│   ├── rag/                   # RAG系统
│   │   ├── retriever.py
│   │   ├── hybrid_search.py
│   │   ├── reranker.py
│   │   ├── fusion.py
│   │   └── citation.py
│   │
│   ├── knowledge/             # 知识工程
│   │   ├── acquisition.py
│   │   ├── ingestion.py
│   │   ├── extraction.py
│   │   ├── chunking.py
│   │   ├── classification.py
│   │   ├── annotation.py
│   │   ├── embedding.py
│   │   └── lifecycle.py
│   │
│   ├── calculation/           # 计算引擎
│   │   ├── bazi/
│   │   ├── ziwei/
│   │   ├── qimen/
│   │   ├── liuyao/
│   │   ├── feng_shui/
│   │   ├── date_selection/
│   │   ├── name_analysis/
│   │   └── physiognomy/
│   │
│   ├── reasoning/             # 推理引擎
│   ├── reporting/             # 报告生成
│   ├── tools/                 # 工具系统
│   ├── persistence/           # 持久化层
│   ├── api/                   # API层
│   ├── llm/                   # LLM层
│   └── observability/         # 可观测性
│
├── tests/                     # 测试
├── docs/                      # 文档
├── config/                    # 配置文件
├── docker/                    # Docker配置
└── scripts/                   # 脚本
```

---

## 后续部分预告

- 第八部分: API设计 (RESTful + WebSocket)
- 第九部分: 开发路线图 (12个月分阶段)
- 第十部分: MVP实施方案 (最小可行产品)
- 第十一部分: 商业化路线
- 第十二部分: 3年技术演进路线
