# Vercel 权限管理

Vercel Token 管理与 API 调用指南。

## Token 信息

- **账号**: xcaihgga
- **邮箱**: kpjynvs64t@privaterelay.appleid.com
- **Token 前缀**: `vcp_`
- **类型**: Account Token
- **获取地址**: https://vercel.com/account/settings/tokens

## 当前项目

| 项目名 | 框架 | 生产环境 URL |
|--------|------|-------------|
| workspace | vite | https://workspace-64lr9kd2z-xcaihggas-projects.vercel.app |
| jigu-v5-ygvj | vite | https://jigu-v5-ygvj-j1eqjhg1l-xcaihggas-projects.vercel.app |
| jigu-v5 | vite | https://jigu-v5-9ihqcgigx-xcaihggas-projects.vercel.app |

## 常用 API

```bash
# 设置 Token
export VERCEL_TOKEN="vcp_xxxxxxxxxxxx"

# 获取用户信息
curl -s -X GET "https://api.vercel.com/v2/user" \
  -H "Authorization: Bearer $VERCEL_TOKEN"

# 列出所有项目
curl -s -X GET "https://api.vercel.com/v9/projects" \
  -H "Authorization: Bearer $VERCEL_TOKEN"

# 部署项目
curl -s -X POST "https://api.vercel.com/v13/deployments?forceNew=1" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "project-name",
    "files": [...]
  }'

# 获取部署列表
curl -s -X GET "https://api.vercel.com/v6/deployments" \
  -H "Authorization: Bearer $VERCEL_TOKEN"

# 列出域名
curl -s -X GET "https://api.vercel.com/v9/projects/{projectId}/domains" \
  -H "Authorization: Bearer $VERCEL_TOKEN"
```

## 使用场景

| 场景 | 所需权限 | 说明 |
|------|---------|------|
| 部署项目 | 全权限 (默认) | Vercel Account Token 默认为全权限 |
| 查看部署状态 | 全权限 | 可查所有部署记录 |
| 绑定自定义域名 | 全权限 | 管理项目域名 |
| 管理环境变量 | 全权限 | 增删改查 env vars |
| 删除项目 | 全权限 | 危险操作，谨慎使用 |

## 安全建议

- Vercel Token 没有细粒度权限控制，全量 Token 能操作一切
- 建议为不同项目创建不同 Token，命名时加上项目标识
- 定期轮换（Settings → Tokens → Revoke 旧的 → Create 新的）
- 不要提交到 Git 仓库，使用环境变量或 TRAE Secrets
