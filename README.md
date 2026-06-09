
# MingLi-AI-Agent 术数推理命理智能体

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Next.js](https://img.shields.io/badge/Next.js-14+-black)
![Status](https://img.shields.io/badge/status-MVP-yellow)

## 🎯 项目简介

**MingLi-AI-Agent** 是一个企业级术数推理命理智能体平台，支持全7大术数域的综合分析与推演。通过结合传统命理规则引擎与现代AI技术，为用户提供可解释、可验证的命理分析服务。

### 核心功能

- ✅ **完整命盘生成**：输入出生时间 → 获得八字+紫微+奇门等所有术数命盘
- ✅ **历史名人查询**：查询历史名人的完整命理分析与验证
- ✅ **推理链可视化**：每步计算过程完整可追踪、可审核
- ✅ **智能问答**：AI 对话式解读命理信息
- ✅ **多主题切换**：现代简约 / 传统中式 / 深色数据可视化
- ✅ **Web UI**：完整的前端交互界面
- ✅ **RESTful API**：完整的API接口，支持第三方集成

### 支持的术数域（7大）

| 术数 | 优先级 | 典籍来源 | 流派支持 | 状态 |
|------|--------|----------|----------|------|
| 八字（四柱） | ⭐⭐⭐ | 《渊海子平》《滴天髓》 | 月令派、从旺派等 | ✅ 开发完成 |
| 紫微斗数 | ⭐⭐⭐ | 《紫微斗数全书》 | 南派、北派、现代派 | ✅ 开发完成 |
| 奇门遁甲 | ⭐⭐ | 《奇门遁甲》《烟壤经》 | 九星流、天干流 | ✅ 开发完成 |
| 大六壬 | ⭐⭐ | 《大六壬指南》 | 古法、现代 | ✅ 开发完成 |
| 梅花易数 | ⭐⭐ | 《梅花易数》 | 经典分类法 | ✅ 开发完成 |
| 六爻 | ⭐⭐ | 《周易》《爻辞详解》 | 动爻、变爻解读 | ✅ 开发完成 |
| 太乙数 | ⭐ | 《太乙数精义》 | 传统推演 | ✅ 开发完成 |

---

## 🏗️ 项目架构

```
mingli-ai-agent/
├── src/                    # 后端源代码 (Python)
│   ├── engines/            # 推理引擎（7个）
│   ├── utils/              # 工具函数
│   ├── api/                # FastAPI 服务
│   └── cli/                # 命令行工具
├── frontend/               # 前端 Web UI (Next.js + React)
│   ├── pages/              # 页面组件
│   │   ├── index.tsx       # 首页/仪表盘
│   │   ├── calculator.tsx  # 命盘计算器
│   │   ├── figures.tsx     # 历史名人库
│   │   ├── chat.tsx        # 智能问答
│   │   ├── reasoning.tsx   # 推理链
│   │   └── settings.tsx    # 主题设置
│   ├── components/         # 通用组件
│   │   ├── Layout.tsx      # 主布局
│   │   ├── Navbar.tsx      # 导航栏
│   │   ├── Footer.tsx      # 页脚
│   │   ├── Charts.tsx      # 命盘可视化组件
│   │   └── BaziChart.tsx   # 八字命盘
│   ├── lib/                # 工具库
│   │   ├── themes.ts       # 主题定义（3套主题）
│   │   ├── ThemeContext.tsx# 主题上下文
│   │   ├── types.ts        # TypeScript 类型定义
│   │   └── api.ts          # API 客户端
│   └── styles/             # 样式
│       └── globals.css
├── rules/                  # 规则库（数据）
├── data/                   # 数据库/历史数据
├── tests/                  # 测试
├── docker/                 # Docker 配置
└── docs/                   # 文档
```

### 技术栈

**后端**
- Python 3.9+
- FastAPI（高性能异步 API 框架）
- 规则引擎（自定义实现）
- 历法转换工具

**前端**
- Next.js 14+（React 框架）
- React 18+（UI 库）
- TypeScript（类型安全）
- 3 套可切换主题（现代简约 / 传统中式 / 深色数据）

---

## 🚀 快速开始

### 方式一：启动后端 API 服务

```bash
# 1. 克隆仓库
git clone https://github.com/qingjian0/mingli-ai-agent.git
cd mingli-ai-agent

# 2. 创建虚拟环境并安装依赖
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 启动 API 服务 (端口 8000)
PYTHONPATH=/workspace uvicorn src.api.main:app --reload

# 4. 查看 API 文档
# 浏览器访问: http://localhost:8000/docs
```

### 方式二：启动前端 Web UI

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install
# 或使用 yarn
# yarn install

# 3. 启动开发服务器
npm run dev
# 浏览器访问: http://localhost:3000

# 生产构建
npm run build
npm start
```

### 方式三：使用命令行工具 (CLI)

```bash
# 八字排盘
python -m src.cli.main bazi -d 1990-05-15 -t 10:30

# 紫微斗数
python -m src.cli.main ziwei -d 1990-05-15 -t 10:30

# 综合分析（多个术数域）
python -m src.cli.main analyze -d 1990-05-15 -t 10:30 --domains bazi,ziwei,qimen

# 查看帮助
python -m src.cli.main --help
```

### 方式四：Docker 部署

```bash
# 构建并启动
docker-compose up -d --build

# 访问
# API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

---

## 🖥️ 前端页面说明

| 页面 | 路径 | 功能 |
|------|------|------|
| **首页** | `/` | 项目介绍、快速入口、七大术数域说明 |
| **命盘计算器** | `/calculator` | 输入出生日期时间 → 计算命盘（支持多术数域同时计算）|
| **历史名人库** | `/figures` | 浏览和查询历史名人的命理信息 |
| **智能问答** | `/chat` | AI 对话式解读，支持命理相关问题 |
| **推理链** | `/reasoning` | 展示命盘计算的完整推理过程 |
| **主题设置** | `/settings` | 切换 UI 主题（现代/传统/深色） |

---

## 🎨 三套主题

| 主题 | 特点 | 适用场景 |
|------|------|---------|
| 现代简约 | 白底深色，简洁现代 | 默认推荐 |
| 传统中式 | 红木色调，古典边框 | 传统文化爱好者 |
| 数据可视化 | 深色主题，适合图表 | 数据分析师 |

在任意页面右上角点击切换按钮，或进入 `/settings` 页面选择。

---

## 📋 API 接口

### 八字排盘
```bash
POST /api/v1/bazi/calc
Content-Type: application/json

{
  "birth_date": "1990-05-15",
  "birth_time": "10:30",
  "timezone": "UTC+8",
  "location": "北京",
  "gender": "男"
}
```

### 其他术数域
- `POST /api/v1/ziwei/calc` - 紫微斗数
- `POST /api/v1/qimen/calc` - 奇门遁甲
- `POST /api/v1/liuren/calc` - 大六壬
- `POST /api/v1/meihua/calc` - 梅花易数
- `POST /api/v1/liuyao/calc` - 六爻
- `POST /api/v1/taiyi/calc` - 太乙数

### 综合分析
```bash
POST /api/v1/analysis/comprehensive
Content-Type: application/json

{
  "birth_date": "1990-05-15",
  "birth_time": "10:30",
  "domains": ["bazi", "ziwei", "qimen"]
}
```

完整 API 文档请访问：`http://localhost:8000/docs`

---

## 🧪 测试

```bash
# 单元测试
PYTHONPATH=/workspace pytest tests/unit/ -v

# 集成测试
PYTHONPATH=/workspace pytest tests/integration/ -v

# 查看覆盖率
PYTHONPATH=/workspace pytest --cov=src --cov-report=html
```

### 测试覆盖
- ✅ 八字引擎单元测试
- ✅ 紫微斗数引擎单元测试
- ✅ 奇门遁甲引擎单元测试
- ✅ 大六壬引擎单元测试
- ✅ 梅花易数引擎单元测试
- ✅ 六爻引擎单元测试
- ✅ 太乙数引擎单元测试
- ✅ 工具函数测试
- ✅ API 路由测试
- ✅ 历史案例回归测试

---

## 📚 核心模块说明

### 1. 八字引擎 (`src/engines/bazi_engine.py`)
- 天干地支计算（五虎遁、五鼠遁）
- 五行分布统计
- 纳音五行
- 大运流年推演
- 十神关系分析

### 2. 紫微斗数引擎 (`src/engines/ziwei_engine.py`)
- 主星排布
- 12宫安星
- 星曜组合分析

### 3. 其他术数引擎
- 奇门遁甲：九宫、八门、九星排局
- 大六壬：三传四课、十二月将
- 梅花易数：先天起卦、体用分析
- 六爻：六亲、六神、世应关系
- 太乙数：局数、太乙位置、统运分析

### 4. 前端可视化
- 八字四柱可视化（五行着色）
- 五行分布柱状图
- 紫微12宫图表
- 奇门九宫布局
- 完整推理链展示

---

## 📖 文档

- `docs/ARCHITECTURE.md` - 系统架构设计
- `docs/API_DESIGN.md` - API 接口设计
- `docs/BUSINESS_ROADMAP.md` - 商业路线图
- `docs/MVP_PLAN.md` - MVP 计划
- `docs/ROADMAP.md` - 完整路线图

---

## 🛠️ 开发指南

### 开发环境
- **Python**: 3.9+
- **Node.js**: 18+（前端开发）
- **操作系统**: macOS / Linux / Windows

### 目录规范
```
src/                # Python 后端
  engines/          # 新增术数引擎放这里
  utils/            # 工具函数
  api/routes/       # API 路由
frontend/           # Next.js 前端
  pages/            # 页面
  components/       # 通用组件
  lib/              # 工具库
rules/              # 规则 JSON 数据
tests/              # 测试用例
```

### 贡献代码
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## ⚠️ 免责声明

- 本项目仅供学习研究使用，不得用于商业目的
- 传统命理学是中国传统文化的重要组成部分，请理性看待、科学理解
- 本项目计算结果仅供参考，不构成任何决策建议

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

核心引擎开源，商用解释服务需另行授权。

---

## 📞 联系方式

- 问题反馈：GitHub Issues
- 技术交流：欢迎提交 PR

---

## 🙏 致谢

感谢所有参与本项目的贡献者与术数研究者。

