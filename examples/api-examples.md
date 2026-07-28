# API 调用示例

> 使用项目内 `scripts/api-client.py` 的常用操作示例

## 前置准备

```bash
# 设置 Token 环境变量
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# 或者直接在命令中指定 --token
```

---

## 用户信息

```bash
# 获取当前用户信息
python scripts/api-client.py --api user --pretty

# 获取指定用户信息
python scripts/api-client.py --api users/octocat --pretty
```

---

## 仓库操作

```bash
# 列出当前用户的仓库
python scripts/api-client.py --api user/repos --pretty

# 列出指定用户的仓库
python scripts/api-client.py --api users/octocat/repos --pretty

# 获取仓库详情
python scripts/api-client.py --api repos/microsoft/vscode --pretty

# 列出仓库分支
python scripts/api-client.py --api repos/microsoft/vscode/branches --pretty
```

---

## Issue 操作

```bash
# 列出仓库 Issues
python scripts/api-client.py --api repos/owner/repo/issues --pretty

# 创建 Issue
python scripts/api-client.py \
  --method POST \
  --api repos/owner/repo/issues \
  --data '{"title":"新功能建议","body":"描述一下你的建议..."}' \
  --pretty

# 更新 Issue
python scripts/api-client.py \
  --method PATCH \
  --api repos/owner/repo/issues/1 \
  --data '{"state":"closed"}' \
  --pretty
```

---

## Pull Request 操作

```bash
# 列出 PR
python scripts/api-client.py --api repos/owner/repo/pulls --pretty

# 获取 PR 详情
python scripts/api-client.py --api repos/owner/repo/pulls/42 --pretty

# 列出 PR 的提交
python scripts/api-client.py --api repos/owner/repo/pulls/42/commits --pretty

# 列出 PR 的文件变更
python scripts/api-client.py --api repos/owner/repo/pulls/42/files --pretty
```

---

## 代码内容

```bash
# 获取文件内容（返回 base64 编码，脚本会自动解码）
# 需要直接使用 Python 脚本中的 get_file_content 方法

# 或者通过 API 获取原始内容信息
python scripts/api-client.py --api repos/owner/repo/contents/README.md --pretty
```

---

## Actions 工作流

```bash
# 列出工作流
python scripts/api-client.py --api repos/owner/repo/actions/workflows --pretty

# 触发工作流
python scripts/api-client.py \
  --method POST \
  --api repos/owner/repo/actions/workflows/ci.yml/dispatches \
  --data '{"ref":"main"}'

# 列出工作流运行记录
python scripts/api-client.py --api repos/owner/repo/actions/runs --pretty

# 获取运行日志
python scripts/api-client.py --api repos/owner/repo/actions/runs/1234567890/logs
```

---

## Release

```bash
# 列出 Releases
python scripts/api-client.py --api repos/owner/repo/releases --pretty

# 创建 Release
python scripts/api-client.py \
  --method POST \
  --api repos/owner/repo/releases \
  --data '{
    "tag_name": "v1.0.0",
    "target_commitish": "main",
    "name": "v1.0.0",
    "body": "Release notes...",
    "draft": false,
    "prerelease": false
  }' \
  --pretty
```

---

## Search

```bash
# 搜索代码
python scripts/api-client.py \
  --api "search/code" \
  --pretty

# 注意：search API 需要 URL 编码查询参数
# 建议直接在脚本中构建 URL
```

---

## 在 Python 代码中使用

```python
import sys
sys.path.insert(0, "scripts")
from api_client import GitHubClient

client = GitHubClient(token="ghp_xxxxxxxxxxxx")

# 获取用户信息
user = client.get_user()
print(f"当前用户: {user['login']}")

# 列出仓库
repos = client.list_repos()
for repo in repos:
    print(f"- {repo['full_name']}")

# 创建 Issue
issue = client.create_issue("owner", "repo", "标题", "内容")
print(f"Issue 创建成功: #{issue['number']}")

# 读取文件内容
content = client.get_file_content("owner", "repo", "path/to/file.py", ref="main")
print(content)
```
