
# MingLi AI Agent - 前端 Web UI

基于 Next.js 14 + React 18 构建的术数推理命理智能体前端界面。

## 📁 目录结构

```
frontend/
├── pages/                    # 页面组件
│   ├── _app.tsx           # 应用入口（主题 Provider）
│   ├── index.tsx          # 首页
│   ├── calculator.tsx     # 命盘计算器
│   ├── figures.tsx      # 历史名人库
│   ├── chat.tsx         # 智能问答
│   ├── reasoning.tsx    # 推理链
│   └── settings.tsx     # 主题设置
├── components/               # 通用组件
│   ├── Layout.tsx         # 主布局（导航 + 内容 + 页脚）
│   ├── Navbar.tsx         # 顶部导航栏
│   ├── Footer.tsx         # 页脚
│   ├── Charts.tsx         # 命盘可视化（八字/紫微/奇门/梅花）
│   └── BaziChart.tsx    # 八字命盘（备用）
├── lib/                      # 工具库
│   ├── themes.ts          # 3套主题定义
│   ├── ThemeContext.tsx  # React Context（主题状态管理）
│   ├── types.ts         # TypeScript 类型
│   └── api.ts           # API 客户端
├── styles/                   # 样式
│   └── globals.css       # 全局 CSS 变量
├── package.json             # 依赖
├── next.config.js          # Next.js 配置（API 代理）
└── tsconfig.json           # TypeScript 配置
```

## 🚀 快速启动

```bash
# 1. 安装依赖
cd frontend
npm install

# 2. 启动开发服务器（端口 3000）
npm run dev

# 3. 生产构建
npm run build
npm start
```

浏览器访问: http://localhost:3000

## 🎯 页面功能

### 首页 (`/`)
- 项目介绍与快速入口
- 七大术数域说明
- 多主题支持

### 命盘计算器 (`/calculator`)
- 输入出生日期时间
- 多术数域选择（八字/紫微/奇门/大六壬/梅花/六爻/太乙）
- 可视化命盘展示
- 五行分布图表
- 置信度显示

### 历史名人库 (`/figures`)
- 历史名人案例浏览
- 搜索查询
- 详细信息弹窗

### 智能问答 (`/chat`)
- AI 对话式交互
- 命理问题智能解读
- 快速问题按钮

### 推理链 (`/reasoning`)
- 完整推理步骤展示
- 可展开查看输入输出
- 规则 ID 追踪

### 主题设置 (`/settings`)
- 3 套主题切换
  - 现代简约（白底深色）
  - 传统中式（红木色调）
  - 数据可视化（深色主题）
- 主题偏好本地存储

## 🎨 主题系统

三套主题通过 CSS 动态切换。

**技术实现：
- `lib/themes.ts` - 主题定义
- `lib/ThemeContext.tsx` - React Context
- 所有颜色通过 CSS 变量注入到 `:root`

## 🔌 API 集成

前端通过 `lib/api.ts` 中的 API 客户端与后端 FastAPI 服务通信。

**API 路由配置**：
- `next.config.js` 中配置 `/api/*` → `http://localhost:8000/api/*`

**支持的 API 方法**：
```typescript
calculateBazi()     // 八字
calculateZiwei()    // 紫微
calculateQimen()    // 奇门
calculateLiuren()   // 大六壬
calculateMeihua()   // 梅花易数
calculateLiuyao()   // 六爻
calculateTaiyi()    // 太乙数
```

**如果后端 API 不可用时，内置 mock 数据确保前端仍可演示运行。

## 📦 技术栈

- **框架**: Next.js 14 (Pages Router)
- **UI**: React 18 + 内联样式（无第三方 UI 库依赖）
- **语言**: TypeScript
- **状态管理**: React Context（主题）
- **数据请求**: axios
- **主题**: 3 套主题（CSS 变量）

## 🔧 自定义

**添加新主题**：
1. 在 `lib/themes.ts` 的 `themes` 中添加新条目
2. 在 `lib/themes.ts` 的 `themes` 对象中添加新的配置

**添加新术数域可视化**：
1. 在 `components/Charts.tsx` 中添加对应的 chart 组件
2. 在 `DomainChart` 中添加 `domain` →  扩展 对应 case

**添加新页面**：
1. 在 `pages/` 下创建新文件
2. 页面使用 `<Layout>` 包裹

## 📝 注意事项

- 前端完全独立，无需后端也能运行（内置 mock 数据）
- 主题切换持久化到 localStorage
- 响应式设计，支持移动端
- 无第三方 UI 库，轻量可扩展
