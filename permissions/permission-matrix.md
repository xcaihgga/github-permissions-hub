# TRAE 场景权限矩阵

> 按 TRAE 实际使用场景整理的最小权限配置，遵循最小权限原则。

## 场景一：代码检索与分析

**需求**：搜索代码、读取文件内容、分析仓库结构

**推荐认证**：Fine-grained PAT

```yaml
Repository permissions:
  Contents: Read-only
  Metadata: Read-only

Account permissions:
  None
```

**脚本调用**：
```bash
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --method GET \
  --api repos/{owner}/{repo}/contents/{path}
```

---

## 场景二：Issue / PR 管理

**需求**：创建、更新、查询 Issue 和 Pull Request

**推荐认证**：GitHub App 或 Fine-grained PAT

```yaml
Repository permissions:
  Issues: Read and write
  Pull requests: Read and write
  Contents: Read-only    # 如需读取 PR 代码
  Metadata: Read-only
```

**脚本调用**：
```bash
# 创建 Issue
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --method POST \
  --api repos/{owner}/{repo}/issues \
  --data '{"title":"Bug report","body":"..."}'

# 列出 PR
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --api repos/{owner}/{repo}/pulls
```

---

## 场景三：自动化发布

**需求**：创建 Release、上传附件、管理版本

**推荐认证**：Fine-grained PAT 或 GitHub App

```yaml
Repository permissions:
  Contents: Read and write
  Metadata: Read-only
```

**脚本调用**：
```bash
# 创建 Release
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --method POST \
  --api repos/{owner}/{repo}/releases \
  --data '{
    "tag_name": "v1.0.0",
    "name": "Release v1.0.0",
    "body": "Release notes..."
  }'
```

---

## 场景四：CI/CD 集成

**需求**：触发工作流、管理 Secrets、读取运行日志

**推荐认证**：GitHub App（推荐）或 PAT

```yaml
Repository permissions:
  Actions: Read and write
  Secrets: Read and write
  Variables: Read and write
  Contents: Read-only
  Metadata: Read-only
```

**脚本调用**：
```bash
# 触发工作流
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --method POST \
  --api repos/{owner}/{repo}/actions/workflows/ci.yml/dispatches \
  --data '{"ref":"main"}'

# 读取运行日志
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --api repos/{owner}/{repo}/actions/runs/{run_id}/logs
```

---

## 场景五：组织级管理

**需求**：管理组织成员、仓库权限、团队设置

**推荐认证**：GitHub App（组织级安装）

```yaml
Repository permissions:
  Administration: Read and write
  Members: Read and write
  Metadata: Read-only

Organization permissions:
  Members: Read and write
```

---

## 场景六：安全审计

**需求**：读取 Dependabot 警报、密钥扫描结果

**推荐认证**：GitHub App 或 Fine-grained PAT

```yaml
Repository permissions:
  Dependabot alerts: Read
  Secret scanning alerts: Read
  Code scanning alerts: Read
  Security events: Read
  Metadata: Read-only
```

---

## 场景七：Packages / Container 管理

**需求**：推送、拉取 Docker 镜像或 npm 包

**推荐认证**：Fine-grained PAT

```yaml
Repository permissions:
  Packages: Read and write
  Metadata: Read-only
```

**脚本调用**：
```bash
# 列出包版本
python scripts/api-client.py \
  --token $GITHUB_TOKEN \
  --api users/{owner}/packages/container/{package_name}/versions
```

---

## 多场景组合配置

如果需要在 TRAE 中同时处理多个场景，建议使用 **GitHub App** 并组合以下权限：

```yaml
Repository permissions:
  Actions: Read and write
  Checks: Read and write
  Contents: Read and write
  Issues: Read and write
  Metadata: Read-only
  Packages: Read and write
  Pull requests: Read and write
  Secrets: Read and write
  Variables: Read and write
  Workflows: Read and write

Organization permissions:
  Members: Read-only
```

> 注意：实际使用时请根据具体需求裁剪，不要一次性给予所有权限。
