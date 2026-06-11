# Harness CI/CD Pipeline 配置

本目录包含 MingLi-AI-Agent 项目的 Harness 平台 CI/CD Pipeline as Code 配置。

## 目录结构

```
.harness/
├── README.md                         # 本文件 — 设置指南
├── ci-pipeline.yaml                  # 主 CI Pipeline（多阶段）
├── connectors/
│   ├── github-connector.yaml         # GitHub 代码库连接器
│   └── dockerhub-connector.yaml      # Docker Hub 镜像仓库连接器
└── secrets/
    └── dockerhubPAT.yaml             # Docker Hub 访问令牌（占位配置）
```

## 快速开始

### 前提条件

1. **注册 Harness 账号**：访问 [app.harness.io](https://app.harness.io) 免费注册
2. **安装 Harness CLI**（可选，用于命令行管理）：
   ```bash
   # macOS
   brew install harness-cli/harness-cli/harness

   # Linux
   curl -LO https://release.harness.io/latest/harness-cli-linux-amd64
   chmod +x harness-cli-linux-amd64
   sudo mv harness-cli-linux-amd64 /usr/local/bin/harness
   ```
3. **GitHub Personal Access Token**（需要 `repo` 和 `read:packages` 权限）
4. **Docker Hub Access Token**（用于推送镜像）

### 步骤 1：创建 GitHub Connector

在 Harness UI 中：
1. 进入 **Project Setup** → **Connectors** → **New Connector**
2. 选择 **Code Repositories** → **GitHub**
3. 或直接在 UI 中导入 [connectors/github-connector.yaml](connectors/github-connector.yaml)

```bash
# 使用 Harness CLI
harness connector --file connectors/github-connector.yaml apply
```

### 步骤 2：创建 Docker Hub Connector

```bash
harness connector --file connectors/dockerhub-connector.yaml apply
```

### 步骤 3：配置 Secrets

在 Harness UI 中创建以下 Secret（Project Setup → Secrets）：
- `dockerhub_pat` — Docker Hub Personal Access Token
- `dockerhub_username` — Docker Hub 用户名
- `github_pat` — GitHub Personal Access Token

或使用 CLI：
```bash
harness secret apply --token YOUR_DOCKERHUB_PAT --secret-name "dockerhub_pat"
harness secret apply --token YOUR_DOCKERHUB_USERNAME --secret-name "dockerhub_username"
```

### 步骤 4：创建/导入 Pipeline

```bash
# 导入主 CI Pipeline
harness pipeline --file ci-pipeline.yaml apply
```

或在 Harness UI 中：
1. 进入 **Pipelines** → **Create Pipeline** → **YAML**
2. 粘贴 [ci-pipeline.yaml](ci-pipeline.yaml) 的内容

## Pipeline 概览

[ci-pipeline.yaml](ci-pipeline.yaml) 包含以下 Stage：

| Stage | 类型 | 说明 |
|-------|------|------|
| **Backend Tests** | CI | Python 3.9/3.10/3.11 矩阵测试 + pytest |
| **Frontend Build** | CI | Node.js 20 依赖安装 + lint + build |
| **Security Scan** | CI | Python Bandit 安全扫描 |
| **Docker Build & Push** | CI | 构建并推送后端和前端 Docker 镜像 |

## 环境变量（Pipeline Variables）

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DOCKERHUB_USERNAME` | — | Docker Hub 用户名（需配置为 Secret） |
| `DOCKER_REGISTRY` | `registry.hub.docker.com` | Docker 镜像仓库地址 |
| `BACKEND_IMAGE` | `mingli-ai-agent-api` | 后端镜像名 |
| `FRONTEND_IMAGE` | `mingli-ai-agent-frontend` | 前端镜像名 |
| `PYTHON_VERSION` | `3.11` | 测试用 Python 版本 |
| `NODE_VERSION` | `20` | 构建用 Node.js 版本 |

## 与 GitHub Actions 的区别

| 特性 | GitHub Actions | Harness CI |
|------|---------------|-------------|
| 配置文件 | `.github/workflows/` | `.harness/` |
| 多 Python 版本矩阵 | ✅ 原生支持 | ✅ Build Matrix |
| Docker 构建缓存 | GHA Cache | Harness Cache + BuildKit |
| 安全扫描 | 第三方 Action | 内置 STO (Security Testing Orchestration) |
| 审批门控 | 手动 trigger | ✅ Stage Approval |
| 多集群部署 | — | ✅ CD 模块支持 |

## 文档链接

- [Harness CI 文档](https://developer.harness.io/docs/continuous-integration)
- [Harness Pipeline YAML 语法](https://developer.harness.io/docs/platform/pipelines/w_pipeline-steps-reference/yaml-reference-ci-pipeline/)
- [Harness Connectors](https://developer.harness.io/docs/platform/connectors)
- [Harness Secrets](https://developer.harness.io/docs/platform/secrets)
