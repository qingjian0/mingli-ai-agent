
# MingLi-AI-Agent 术数推理命理智能体

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Status](https://img.shields.io/badge/status-MVP-yellow)

## 🎯 项目简介

**MingLi-AI-Agent** 是一个企业级术数推理命理智能体平台，支持全7大术数域的综合分析与推演。通过结合传统命理规则引擎与现代AI技术，为用户提供可解释、可验证的命理分析服务。

### 核心功能

- ✅ **完整命盘生成**：输入出生时间 → 获得八字+紫微+奇门等所有术数命盘
- ✅ **历史名人查询**：查询历史名人的完整命理分析与验证
- ✅ **推理链可视化**：每步计算过程完整可追踪、可审核
- ✅ **多流派支持**：同一术数支持多个传统流派并存
- ✅ **RESTful API**：完整的API接口，支持第三方集成

### 支持的术数域（7大）

| 术数 | 优先级 | 典籍来源 | 流派支持 | 状态 |
|------|--------|----------|----------|------|
| 八字（四柱） | ⭐⭐⭐ | 《渊海子平》《滴天髓》 | 月令派、从旺派等 | ✅ 开发完成 |
| 紫微斗数 | ⭐⭐⭐ | 《紫微斗数全书》 | 南派、北派、现代派 | ✅ 开发完成 |
| 奇门遁甲 | ⭐⭐ | 《奇门遁甲》《烟壤经》 | 九星流、天干流 | 规划中 |
| 大六壬 | ⭐⭐ | 《大六壬指南》 | 古法、现代 | 规划中 |
| 梅花易数 | ⭐⭐ | 《梅花易数》 | 经典分类法 | 规划中 |
| 六爻 | ⭐⭐ | 《周易》《爻辞详解》 | 动爻、变爻解读 | 规划中 |
| 太乙数 | ⭐ | 《太乙数精义》 | 传统推演 | 规划中 |

---

## 🏗️ 项目架构

```
mingli-ai-agent/
├── src/                    # 源代码
│   ├── engines/            # 推理引擎
│   │   ├── base_engine.py  # 基础引擎接口
│   │   ├── bazi_engine.py  # 八字推理引擎
│   │   └── ziwei_engine.py # 紫微推理引擎
│   ├── utils/              # 工具函数
│   │   ├── calendar.py     # 历法工具
│   │   ├── bazi_utils.py   # 八字计算工具
│   │   └── ziwei_utils.py  # 紫微计算工具
│   ├── api/                # API服务
│   │   ├── main.py         # FastAPI入口
│   │   └── routes/         # API路由
│   └── __init__.py
├── rules/                  # 规则库
│   ├── bazi/               # 八字规则
│   └── ziwei/              # 紫微规则
├── data/                   # 数据
│   └── cases/              # 历史案例库
├── tests/                  # 测试
│   └── unit/               # 单元测试
├── docker/                 # Docker配置
└── docs/                   # 文档
```

---

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+ (前端)
- Docker & Docker Compose

### 本地开发

```bash
# 1. 克隆仓库
git clone https://github.com/qingjian0/mingli-ai-agent.git
cd mingli-ai-agent

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动API服务
python -m uvicorn src.api.main:app --reload

# 5. 访问API文档
# http://localhost:8000/docs
```

### Docker启动

```bash
docker-compose up -d
```

---

## 📚 核心API接口

### 八字排盘

```bash
POST /api/v1/bazi/calc
Content-Type: application/json

{
  "name": "测试用户",
  "birth_date": "2000-01-01",
  "birth_time": "12:00",
  "timezone": "UTC+8",
  "location": "北京"
}
```

### 紫微排盘

```bash
POST /api/v1/ziwei/calc
Content-Type: application/json

{
  "name": "测试用户",
  "birth_date": "2000-01-01",
  "birth_time": "12:00",
  "timezone": "UTC+8",
  "location": "北京"
}
```

### 综合分析

```bash
POST /api/v1/analysis/comprehensive
Content-Type: application/json

{
  "name": "测试用户",
  "birth_date": "2000-01-01",
  "birth_time": "12:00",
  "timezone": "UTC+8",
  "location": "北京",
  "domains": ["bazi", "ziwei"]
}
```

---

## 🧪 测试

```bash
# 单元测试
pytest tests/unit/ -v

# 运行所有测试
pytest tests/ -v
```

---

## 📦 项目阶段

| 阶段 | 时间 | 状态 |
|------|------|------|
| Phase 1: MVP | 3-4个月 | ✅ 进行中 |
| Phase 2: 扩展 | 2-3个月 | 规划中 |
| Phase 3: 商业化 | 1-2个月 | 规划中 |

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🤝 贡献

欢迎贡献！请阅读相关文档了解详情。
