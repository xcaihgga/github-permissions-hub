# 权限管理中心

> 专为 TRAE 环境设计的多平台权限统一管理项目，涵盖 GitHub、Vercel 等全场景认证方案。

## 项目结构

```
github-permissions-hub/
├── tokens/           # Token 管理（PAT / Fine-grained PAT）
├── apps/             # GitHub App & OAuth App 配置
├── permissions/      # 权限矩阵与 Scopes 参考
├── scripts/          # 可复用的 API 脚本和封装
├── configs/          # 配置文件模板
├── examples/         # TRAE 中使用示例
└── vercel/           # Vercel 权限管理
```

## 快速开始

### 1. 选择认证方式

| 场景 | 推荐方式 | 文件位置 |
|------|----------|----------|
| 个人脚本/自动化 | PAT (Classic) | `tokens/personal-access-tokens.md` |
| 精细化权限控制 | Fine-grained PAT | `tokens/fine-grained-pats.md` |
| TRAE 插件/集成 | GitHub App | `apps/github-apps.md` |
| 用户登录授权 | OAuth App | `apps/oauth-apps.md` |
| Vercel 部署 | Vercel Account Token | `vercel/README.md` |

### 2. 获取凭证

根据上方选择的认证方式，查看对应文档获取 `TOKEN` 或 `APP` 凭证。

### 3. 在 TRAE 中使用

```bash
# 方式一：直接设置环境变量
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# 方式二：使用项目内的 API 客户端
python scripts/api-client.py --token ghp_xxxxxxxxxxxx --api user/repos
```

## 安全规范

- **Never commit tokens** 到仓库，使用环境变量或 TRAE Secrets
- **定期轮换** Token，参考 `tokens/token-rotation-guide.md`
- **最小权限原则**，只申请必要的 Scopes

## TRAE 集成场景

| 场景 | 调用方式 | 参考文档 |
|------|----------|----------|
| 读取仓库列表 | `scripts/api-client.py` | `examples/api-examples.md` |
| 创建 Issue/PR | GitHub App 安装令牌 | `apps/github-apps.md` |
| CI/CD 触发 | GitHub Actions Token | `permissions/scopes-reference.md` |
| 代码搜索 | Fine-grained PAT | `tokens/fine-grained-pats.md` |
