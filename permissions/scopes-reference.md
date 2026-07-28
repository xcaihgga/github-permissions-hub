# GitHub Scopes & Permissions 完整参考

## Classic PAT Scopes

### 仓库相关
| Scope | 权限说明 |
|-------|----------|
| `repo` | 完全控制私有和公共仓库 |
| `repo:status` | 读写提交状态 |
| `repo_deployment` | 读写部署状态 |
| `public_repo` | 仅控制公共仓库 |
| `repo:invite` | 接受仓库邀请 |
| `security_events` | 读写安全事件 |

### 工作流相关
| Scope | 权限说明 |
|-------|----------|
| `workflow` | 更新 GitHub Actions 工作流文件 |

### 包管理
| Scope | 权限说明 |
|-------|----------|
| `write:packages` | 上传包到 GitHub Packages |
| `read:packages` | 下载包 |
| `delete:packages` | 删除包 |

### 组织相关
| Scope | 权限说明 |
|-------|----------|
| `read:org` | 读取组织成员信息 |
| `manage_runners:org` | 管理组织级 Runner |

### 用户相关
| Scope | 权限说明 |
|-------|----------|
| `read:user` | 读取用户个人信息 |
| `user:email` | 读取用户邮箱 |
| `user:follow` | 关注/取消关注用户 |

### 讨论区
| Scope | 权限说明 |
|-------|----------|
| `write:discussion` | 读写 Discussion |
| `read:discussion` | 读取 Discussion |

### 管理级
| Scope | 权限说明 |
|-------|----------|
| `admin:org` | 完全管理组织 |
| `admin:public_key` | 管理公钥 |
| `admin:repo_hook` | 管理仓库 Webhook |
| `admin:org_hook` | 管理组织 Webhook |
| `gist` | 管理 Gist |
| `notifications` | 读取通知 |
| `delete_repo` | 删除仓库 |

## Fine-grained PAT / GitHub App Permissions

### 仓库权限
| Permission | 读 | 写 | 说明 |
|------------|----|----|------|
| Actions | ✅ | ✅ | GitHub Actions |
| Administration | ✅ | ✅ | 仓库管理设置 |
| Checks | ✅ | ✅ | 检查运行 |
| Code scanning alerts | ✅ | ✅ | 代码扫描结果 |
| Codespaces | ✅ | ✅ | 代码空间管理 |
| Commit statuses | ✅ | ✅ | 提交状态 |
| Contents | ✅ | ✅ | 代码内容 |
| Dependabot alerts | ✅ | - | 依赖警报 |
| Deployments | ✅ | ✅ | 部署管理 |
| Discussions | ✅ | ✅ | Discussion |
| Environments | ✅ | ✅ | 部署环境 |
| Issues | ✅ | ✅ | Issue |
| Merge queues | ✅ | ✅ | 合并队列 |
| Metadata | ✅ | - | 基础元数据（必需） |
| Packages | ✅ | ✅ | GitHub Packages |
| Pages | ✅ | ✅ | GitHub Pages |
| Pull requests | ✅ | ✅ | PR |
| Repository advisories | ✅ | ✅ | 安全公告 |
| Secret scanning alerts | ✅ | - | 密钥扫描 |
| Secrets | ✅ | ✅ | Actions 密钥 |
| Security events | ✅ | ✅ | 安全事件 |
| Single file | ✅ | - | 单个文件（需路径） |
| Variables | ✅ | ✅ | Actions 变量 |
| Webhooks | ✅ | ✅ | 仓库 Webhook |
| Workflows | ✅ | ✅ | 工作流文件 |

### 组织权限
| Permission | 读 | 写 | 说明 |
|------------|----|----|------|
| Blocking users | ✅ | ✅ | 阻止用户 |
| Events | ✅ | - | 组织事件 |
| Members | ✅ | ✅ | 成员管理 |
| Organization codespaces | ✅ | ✅ | 组织代码空间设置 |
| Organization codespaces secrets | ✅ | ✅ | 代码空间密钥 |
| Organization codespaces settings | ✅ | ✅ | 代码空间设置 |
| Plan | ✅ | - | 计划信息 |
| Projects | ✅ | ✅ | 组织项目 |
| Secrets | ✅ | ✅ | Actions 组织密钥 |
| Self-hosted runners | ✅ | ✅ | 自托管 Runner |
| Team discussions | ✅ | ✅ | 团队讨论 |
| Variables | ✅ | ✅ | Actions 组织变量 |

### 用户权限（Fine-grained PAT）
| Permission | 读 | 写 | 说明 |
|------------|----|----|------|
| Block another user | - | ✅ | 阻止用户 |
| Email addresses | ✅ | - | 用户邮箱 |
| Followers | ✅ | - | 关注者 |
| GPG keys | ✅ | ✅ | GPG 密钥 |
| Git SSH keys | ✅ | ✅ | SSH 密钥 |
| Interaction limits | - | ✅ | 交互限制 |
| Plan | ✅ | - | 用户计划 |
| Private repository invitations | ✅ | - | 私有仓库邀请 |
| Profile | ✅ | - | 用户资料 |
| Starring | ✅ | ✅ | Star 仓库 |
| Watching | ✅ | ✅ | Watch 仓库 |

## TRAE 场景速查

| 场景 | Classic Scope | Fine-grained / App Permission |
|------|---------------|------------------------------|
| 读取代码 | `repo` | `Contents: Read` |
| 提交代码 | `repo` | `Contents: Write` |
| 创建 Issue | `repo` | `Issues: Write` |
| 创建 PR | `repo` | `Pull requests: Write` |
| 触发 Actions | `workflow` | `Actions: Write` |
| 读取用户信息 | `read:user` | `Profile: Read` |
| 管理 Secrets | `repo` | `Secrets: Write` |
| 发布 Release | `repo` | `Contents: Write` |
| 推送 Docker 镜像 | `write:packages` | `Packages: Write` |
| 代码扫描结果 | `security_events` | `Code scanning alerts: Read` |
