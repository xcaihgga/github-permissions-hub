# 在 TRAE 中使用指南

> 将 GitHub 权限管理中心集成到 TRAE 工作流中的最佳实践

## 目录结构建议

在你的 TRAE 工作区中，建议将此项目作为子目录或独立仓库：

```
your-trae-workspace/
├── github-permissions-hub/      # 本项目管理目录
│   ├── tokens/                  # Token 配置说明
│   ├── scripts/                 # 可复用脚本
│   └── configs/                 # 配置模板
├── your-project-1/
└── your-project-2/
```

---

## 场景一：快速验证 Token 是否可用

```bash
# 进入权限中心目录
cd github-permissions-hub

# 验证当前环境的 Token
python scripts/validate-token.py --check-rate-limit
```

---

## 场景二：TRAE 插件开发获取 GitHub 数据

```python
# 在你的 TRAE 插件代码中
import os
import sys

# 引入通用客户端
sys.path.insert(0, "/path/to/github-permissions-hub/scripts")
from api_client import GitHubClient

# 从环境变量读取 Token（推荐）
token = os.environ.get("GITHUB_TOKEN")
client = GitHubClient(token)

# 调用 API
repos = client.list_repos("microsoft")
```

---

## 场景三：不同项目使用不同 Token

```bash
# 项目 A 使用 Fine-grained PAT（仅读取权限）
export GITHUB_TOKEN_A="github_pat_11_xxxxxxxx"
python scripts/api-client.py --token $GITHUB_TOKEN_A --api user/repos

# 项目 B 使用 Classic PAT（完整权限）
export GITHUB_TOKEN_B="ghp_xxxxxxxxxxxx"
python scripts/api-client.py --token $GITHUB_TOKEN_B --api user/repos
```

---

## 场景四：GitHub App 在 TRAE 自动化中的使用

```python
import sys
sys.path.insert(0, "/path/to/github-permissions-hub/scripts")
from github_app_client import GitHubAppClient

# 初始化 App 客户端
app = GitHubAppClient(
    app_id="123456",
    private_key_path="/secrets/trae-app.pem"
)

# 获取安装令牌（有效期 1 小时，可缓存复用）
token = app.get_installation_token("78901234")

# 将 token 传递给 api-client
from api_client import GitHubClient
client = GitHubClient(token)

# 执行操作
issues = client.list_issues("owner", "repo")
```

---

## 场景五：TRAE Secrets 管理

在 TRAE 中，建议将敏感凭证存储在环境变量或 Secrets 中：

```bash
# .env 文件（已添加到 .gitignore）
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY_PATH=/home/user/.secrets/trae-app.pem
```

在 TRAE 配置中引用：

```json
{
  "env": {
    "GITHUB_TOKEN": "${secrets.GITHUB_TOKEN}",
    "GITHUB_APP_ID": "${secrets.GITHUB_APP_ID}"
  }
}
```

---

## 场景六：权限审查

定期运行验证脚本检查 Token 状态：

```bash
#!/bin/bash
# check-permissions.sh

echo "=== 检查 GitHub Token 状态 ==="
python scripts/validate-token.py --check-rate-limit

echo ""
echo "=== 检查 App 安装状态 ==="
python scripts/github-app-client.py \
  --app-id $GITHUB_APP_ID \
  --private-key $GITHUB_APP_PRIVATE_KEY_PATH \
  --action installations \
  --pretty
```

---

## 场景速查表

| TRAE 任务 | 需要的凭证 | 参考文档 |
|-----------|-----------|----------|
| 读取公开仓库代码 | 无需 Token 或任意 Token | `tokens/personal-access-tokens.md` |
| 读取私有仓库 | PAT / Fine-grained PAT | `tokens/fine-grained-pats.md` |
| 创建 Issue/PR | PAT (repo scope) / GitHub App | `permissions/permission-matrix.md` |
| 触发 CI/CD | PAT (workflow) / GitHub App | `permissions/permission-matrix.md` |
| 发布 Release | PAT (repo) / GitHub App | `examples/api-examples.md` |
| 分析仓库数据 | Fine-grained PAT | `permissions/permission-matrix.md` |
| 用户身份验证 | OAuth App | `apps/oauth-apps.md` |
| 组织级管理 | GitHub App (组织安装) | `apps/github-apps.md` |
