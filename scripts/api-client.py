#!/usr/bin/env python3
"""
GitHub API 通用客户端
支持 PAT (Classic / Fine-grained)、GitHub App Installation Token、OAuth Token
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


class GitHubClient:
    """GitHub API 客户端"""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str, base_url: str = BASE_URL):
        self.token = token
        self.base_url = base_url.rstrip("/")

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "trae-github-client/1.0"
        }

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        发送 HTTP 请求

        Args:
            method: HTTP 方法 (GET, POST, PUT, PATCH, DELETE)
            endpoint: API 端点 (如 "user/repos" 或 "/repos/owner/repo/issues")
            data: 请求体数据
            params: URL 查询参数
        """
        # 构建 URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query}"

        # 准备请求
        req = urllib.request.Request(url, method=method.upper())
        for key, value in self._get_headers().items():
            req.add_header(key, value)

        if data:
            req.add_header("Content-Type", "application/json")
            req.data = json.dumps(data).encode("utf-8")

        try:
            with urllib.request.urlopen(req) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_json = json.loads(error_body)
                error_msg = error_json.get("message", error_body)
            except json.JSONDecodeError:
                error_msg = error_body
            raise GitHubAPIError(e.code, error_msg)

    # 便捷方法
    def get(self, endpoint: str, params: Optional[Dict[str, str]] = None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]):
        return self.request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None):
        return self.request("PUT", endpoint, data=data)

    def patch(self, endpoint: str, data: Dict[str, Any]):
        return self.request("PATCH", endpoint, data=data)

    def delete(self, endpoint: str):
        return self.request("DELETE", endpoint)

    # 常用 API 封装
    def get_user(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self.get("user")

    def list_repos(self, owner: Optional[str] = None, type_: str = "all") -> list:
        """
        列出仓库

        Args:
            owner: 用户名/组织名，为空则列出当前用户的仓库
            type_: owner, member, all
        """
        if owner:
            return self.get(f"users/{owner}/repos", {"type": type_})
        return self.get("user/repos", {"type": type_})

    def get_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """获取仓库信息"""
        return self.get(f"repos/{owner}/{repo}")

    def list_issues(self, owner: str, repo: str, state: str = "open") -> list:
        """列出 Issues"""
        return self.get(f"repos/{owner}/{repo}/issues", {"state": state})

    def create_issue(self, owner: str, repo: str, title: str, body: str = "") -> Dict[str, Any]:
        """创建 Issue"""
        return self.post(f"repos/{owner}/{repo}/issues", {"title": title, "body": body})

    def list_pulls(self, owner: str, repo: str, state: str = "open") -> list:
        """列出 Pull Requests"""
        return self.get(f"repos/{owner}/{repo}/pulls", {"state": state})

    def get_file_content(self, owner: str, repo: str, path: str, ref: str = "main") -> str:
        """
        获取文件内容
        返回解码后的文件内容字符串
        """
        import base64
        result = self.get(f"repos/{owner}/{repo}/contents/{path}", {"ref": ref})
        content = result.get("content", "")
        return base64.b64decode(content).decode("utf-8")

    def trigger_workflow(self, owner: str, repo: str, workflow_id: str, ref: str = "main"):
        """触发 Actions 工作流"""
        return self.post(
            f"repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            {"ref": ref}
        )


class GitHubAPIError(Exception):
    """GitHub API 错误"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"GitHub API Error {status_code}: {message}")


def main():
    parser = argparse.ArgumentParser(description="GitHub API CLI 客户端")
    parser.add_argument("--token", help="GitHub Token，默认从 GITHUB_TOKEN 环境变量读取")
    parser.add_argument("--method", default="GET", help="HTTP 方法: GET, POST, PUT, PATCH, DELETE")
    parser.add_argument("--api", required=True, help="API 端点，如 'user/repos' 或 'repos/owner/repo/issues'")
    parser.add_argument("--data", help="请求体 JSON 字符串")
    parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")

    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("错误: 请提供 --token 或设置 GITHUB_TOKEN 环境变量")
        sys.exit(1)

    client = GitHubClient(token)

    data = None
    if args.data:
        data = json.loads(args.data)

    try:
        result = client.request(args.method, args.api, data=data)
        if args.pretty:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))
    except GitHubAPIError as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
