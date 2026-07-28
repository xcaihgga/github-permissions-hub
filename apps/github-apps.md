# GitHub App 配置指南

> 适用于 TRAE 插件开发、机器人集成、Webhook 处理等场景。

## 创建 GitHub App

1. GitHub → Settings → Developer settings → GitHub Apps → New GitHub App
2. 填写基本信息：
   - **GitHub App name**: `trae-integration-app`
   - **Homepage URL**: 你的项目地址
   - **Webhook URL**: 接收事件的服务器地址（可选）
   - **Webhook secret**: 用于验证 Webhook 签名

3. 配置权限（Permissions & Events）：

### TRAE 推荐权限配置

#### 基础集成
```
Repository permissions:
  Contents: Read-only
  Issues: Read and write
  Pull requests: Read and write
  Metadata: Read-only

Organization permissions:
  Members: Read-only
```

#### 完整 CI/CD 集成
```
Repository permissions:
  Actions: Read and write
  Checks: Read and write
  Contents: Read and write
  Deployments: Read and write
  Issues: Read and write
  Pull requests: Read and write
  Statuses: Read and write
  Workflows: Read and write

Organization permissions:
  Members: Read-only
```

#### 安全审计
```
Repository permissions:
  Code scanning alerts: Read
  Dependabot alerts: Read
  Secret scanning alerts: Read
  Security events: Read
```

## 认证流程

### 1. 生成 Private Key
- App 创建后 → Generate a private key
- 下载 `.pem` 文件并妥善保存

### 2. 获取 App ID
- App 设置页面找到 **App ID**（数字）

### 3. 获取 Installation Access Token

```python
# 使用项目脚本获取安装令牌
python scripts/get-installation-token.py \
  --app-id 123456 \
  --private-key-path /path/to/private-key.pem \
  --installation-id 78901234
```

### JWT + Installation Token 流程

```
App Private Key → JWT → Installation Token → API Access
```

## TRAE 中使用示例

```python
from scripts.github_app_client import GitHubAppClient

# 初始化客户端
client = GitHubAppClient(
    app_id=123456,
    private_key_path="/secrets/trae-app.pem"
)

# 获取安装令牌（有效期 1 小时）
token = client.get_installation_token(installation_id=78901234)

# 调用 API
repos = client.list_installation_repos()
```

## Webhook 事件订阅

TRAE 常用事件：
- `pull_request`: PR 创建、更新、合并
- `issues`: Issue 创建、更新、关闭
- `push`: 代码推送
- `workflow_run`: Actions 工作流执行
- `release`: Release 发布

## 配置文件模板

参考 `configs/github-app-config.yml`
