# Contributing

欢迎贡献代码！请阅读以下指南。

## 代码规范

### Python 代码规范

请遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范：

- 使用 4 空格缩进
- 行长度不超过 120 字符
- 使用 snake_case 命名变量和函数
- 使用 PascalCase 命名类
- 添加适当的注释和文档字符串

### TypeScript/JavaScript 代码规范

请遵循 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)：

- 使用 2 空格缩进
- 行长度不超过 120 字符
- 使用 camelCase 命名变量和函数
- 使用 PascalCase 命名类和组件
- 使用单引号

## 提交规范

请使用 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 格式：

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### 类型说明

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试代码
- `chore`: 构建/工具更新

### 示例

```
feat(bazi): 添加十神计算功能

- 实现十神关系分析
- 添加测试用例
```

## 开发流程

1. Fork 项目到自己的仓库
2. 创建特性分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. 编写代码和测试
4. 确保测试通过：
   ```bash
   pytest
   ```
5. 提交代码：
   ```bash
   git commit -m "feat: your feature description"
   ```
6. 推送到分支：
   ```bash
   git push origin feature/your-feature-name
   ```
7. 创建 Pull Request

## Pull Request 规范

### PR 标题

使用 Conventional Commits 格式：

```
feat: 添加新功能描述
```

### PR 描述

请包含以下内容：

1. **目的**: 这个 PR 解决什么问题
2. **改动**: 修改了哪些文件
3. **测试**: 如何验证改动
4. **相关 issue**: 关联的 issue 编号

### 检查清单

提交 PR 前请确保：

- ✅ 代码通过所有测试
- ✅ 代码符合规范
- ✅ 添加了必要的测试用例
- ✅ 更新了相关文档
- ✅ 没有引入新的依赖

## 问题报告

如果发现 bug 或有功能请求，请创建 issue 并包含：

1. **描述**: 问题的详细描述
2. **复现步骤**: 如何复现问题
3. **期望行为**: 应该发生什么
4. **实际行为**: 实际发生了什么
5. **环境**: 操作系统、Python 版本、依赖版本

## 许可证

贡献代码即表示同意代码遵循 MIT 许可证。