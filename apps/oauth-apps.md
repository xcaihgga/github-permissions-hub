# OAuth App 配置指南

> 适用于需要用户登录授权、获取用户身份信息的 TRAE 场景。

## 创建 OAuth App

1. GitHub → Settings → Developer settings → OAuth Apps → New OAuth App
2. 填写信息：
   - **Application name**: `trae-oauth-app`
   - **Homepage URL**: 应用主页
   - **Authorization callback URL**: 授权回调地址（如 `http://localhost:3000/auth/callback`）

3. 创建后获取：
   - **Client ID**
   - **Client Secret**（仅显示一次，妥善保存）

## OAuth 授权流程

### 1. 引导用户授权

```
GET https://github.com/login/oauth/authorize
  ?client_id=YOUR_CLIENT_ID
  &scope=repo,user
  &redirect_uri=http://localhost:3000/auth/callback
  &state=random_string
```

### 2. 获取 Access Token

```bash
curl -X POST https://github.com/login/oauth/access_token \
  -H "Accept: application/json" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=USER_AUTHORIZATION_CODE" \
  -d "redirect_uri=http://localhost:3000/auth/callback"
```

### 3. 使用 Token 调用 API

```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  https://api.github.com/user
```

## TRAE 常用 Scopes

| Scope | 说明 | 适用场景 |
|-------|------|----------|
| `repo` | 完整仓库访问 | 代码管理、PR 操作 |
| `repo:status` | 提交状态读写 | CI 状态上报 |
| `repo_deployment` | 部署状态 | 发布管理 |
| `public_repo` | 仅公共仓库 | 开源项目 |
| `read:org` | 读取组织成员 | 团队协作 |
| `read:user` | 读取用户信息 | 用户身份识别 |
| `user:email` | 读取用户邮箱 | 通知发送 |
| `workflow` | 管理 Actions | CI/CD 集成 |
| `write:packages` | 推送 Packages | 镜像发布 |
| `delete:packages` | 删除 Packages | 包管理 |

## 在 TRAE 中使用

```python
from scripts.oauth_client import GitHubOAuthClient

# 初始化
client = GitHubOAuthClient(
    client_id="Ov23lixxxxxxxxx",
    client_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

# 生成授权 URL
auth_url = client.get_authorization_url(
    scopes=["repo", "read:user"],
    redirect_uri="http://localhost:3000/callback"
)

# 用户授权后，用 code 换取 token
token = client.exchange_code_for_token(code="user_auth_code")

# 调用 API
user = client.get_user()
```

## 安全建议

- `state` 参数用于防止 CSRF 攻击，必须随机生成并验证
- Client Secret 不要暴露在前端代码中
- 使用 PKCE 扩展增强安全性（Public clients 必需）
- Token 过期后使用 Refresh Token 刷新（如支持）

## 配置文件

参考 `configs/oauth-config.json`
