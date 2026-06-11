# MingLi AI Agent

企业级术数推理命理智能体引擎，支持全7大术数域（八字、紫微斗数、奇门遁甲、大六壬、梅花易数、六爻、太乙数）。

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green)](https://fastapi.tiangolo.com/)

## 🌐 多语言支持 / Multi-language Support

- [中文](#mingli-ai-agent)
- [English](#mingli-ai-agent-english)

---

## 功能特性

### 核心功能
- ✅ **八字排盘** - 精确计算八字命盘，包含十神、五行、纳音等
- ✅ **紫微斗数** - 完整的紫微斗数排盘和星曜分析
- ✅ **奇门遁甲** - 奇门排盘和格局分析
- ✅ **大六壬** - 六壬排盘和四课三传
- ✅ **梅花易数** - 梅花起卦和断卦
- ✅ **六爻** - 六爻纳甲排盘
- ✅ **太乙数** - 太乙神数排盘

### 技术特性
- 🎯 **高精度计算** - 八字排盘准确率≥99%
- 🧠 **AI智能解读** - 集成LLM进行自然语言命理解释
- 🔐 **安全认证** - JWT认证和密码加密
- 📊 **推理链记录** - 完整的计算过程追踪
- ⚡ **高性能** - 支持批量计算和缓存

---

## 技术栈

### 后端
- **框架**: FastAPI 0.115+
- **语言**: Python 3.10+
- **数据库**: SQLite / PostgreSQL
- **认证**: JWT + BCrypt
- **LLM**: OpenAI API

### 前端
- **框架**: Next.js 14
- **语言**: TypeScript
- **样式**: CSS3

---

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+

### 安装依赖

```bash
# 后端依赖
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

### 配置环境变量

创建 `.env` 文件：

```env
APP_NAME=MingLi-AI-Agent
APP_VERSION=0.1.0
ENVIRONMENT=development
DEBUG=true

API_HOST=0.0.0.0
API_PORT=8000

DATABASE_URL=sqlite:///./mingli.db

OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o-mini

SECRET_KEY=your-secret-key
```

### 启动服务

```bash
# 启动后端服务
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# 启动前端服务 (新开终端)
cd frontend
npm run dev
```

### 访问地址

- API文档: http://localhost:8000/docs
- 前端页面: http://localhost:3000

---

## API 使用示例

### 八字排盘

```bash
curl -X POST http://localhost:8000/api/v1/bazi/calc \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-01-15",
    "birth_time": "14:30",
    "timezone": "UTC+8",
    "location": "北京"
  }'
```

### 用户注册

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "测试用户"
  }'
```

### 用户登录

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

---

## 项目结构

```
mingli-ai-agent/
├── src/                      # 后端源码
│   ├── api/                  # API层
│   │   ├── routes/           # 路由定义
│   │   └── main.py           # 应用入口
│   ├── engines/              # 术数引擎
│   │   ├── bazi_engine.py    # 八字引擎
│   │   ├── ziwei_engine.py   # 紫微斗数引擎
│   │   └── ...
│   ├── services/             # 服务层
│   ├── persistence/          # 持久化层
│   ├── core/                 # 核心模块
│   ├── agents/               # Agent框架
│   └── llm/                  # LLM服务
├── frontend/                 # 前端源码
├── tests/                    # 测试用例
├── docs/                     # 文档
└── config/                   # 配置文件
```

---

## 开发指南

### 添加新术数引擎

1. 创建引擎类继承 `BaseEngine`
2. 实现 `calculate` 方法
3. 在 `src/api/routes/` 添加路由
4. 在 `src/services/computation_service.py` 注册引擎

### 测试

```bash
# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行所有测试
pytest
```

---

## 部署

### Docker 部署

```bash
docker-compose up -d
```

### 生产环境

```bash
# 使用 Gunicorn
pip install gunicorn
gunicorn -w 4 src.api.main:app -k uvicorn.workers.UvicornWorker
```

---

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 联系方式

如有问题或建议，请通过以下方式联系：

- 邮箱: contact@mingli-ai.com
- GitHub: [https://github.com/mingli-ai/mingli-ai-agent](https://github.com/mingli-ai/mingli-ai-agent)

---

---

## MingLi AI Agent (English)

An enterprise-level Chinese metaphysics reasoning engine supporting all 7 major divination systems: Bazi, Ziwei Dou Shu, Qimen Dunjia, Liuren, Meihua Yishu, Liuyao, and Taiyi.

## Features

### Core Functions
- ✅ **Bazi Calculation** - Accurate Bazi chart calculation
- ✅ **Ziwei Dou Shu** - Complete Purple Star Astrology
- ✅ **Qimen Dunjia** - Qimen divination analysis
- ✅ **Liuren** - Six Ren divination
- ✅ **Meihua Yishu** - Plum Blossom Divination
- ✅ **Liuyao** - Six Lines divination
- ✅ **Taiyi** - Taiyi divine calculation

### Technical Features
- 🎯 **High Precision** - Bazi calculation accuracy ≥99%
- 🧠 **AI Interpretation** - LLM-powered natural language explanations
- 🔐 **Security** - JWT authentication and password encryption
- 📊 **Reasoning Chain** - Complete calculation tracking
- ⚡ **High Performance** - Batch calculation support

## Tech Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.10+
- **Database**: SQLite / PostgreSQL
- **Authentication**: JWT + BCrypt
- **LLM**: OpenAI API

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript

## Quick Start

### Installation

```bash
pip install -r requirements.txt
cd frontend && npm install
```

### Configuration

Create `.env` file:

```env
DATABASE_URL=sqlite:///./mingli.db
OPENAI_API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

### Running

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
cd frontend && npm run dev
```

### API Documentation

Access Swagger UI at: http://localhost:8000/docs

## API Examples

### Bazi Calculation

```bash
curl -X POST http://localhost:8000/api/v1/bazi/calc \
  -H "Content-Type: application/json" \
  -d '{"birth_date": "1990-01-15", "birth_time": "14:30", "timezone": "UTC+8", "location": "Beijing"}'
```

## Project Structure

```
mingli-ai-agent/
├── src/
│   ├── api/           # API layer
│   ├── engines/       # Divination engines
│   ├── services/      # Business services
│   ├── persistence/   # Database models
│   ├── core/          # Core utilities
│   ├── agents/        # Agent framework
│   └── llm/           # LLM integration
├── frontend/          # React frontend
├── tests/             # Test cases
└── docs/              # Documentation
```

## License

MIT License

## Contributing

Contributions are welcome! Please fork the project and submit a pull request.