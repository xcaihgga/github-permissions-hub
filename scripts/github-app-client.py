#!/usr/bin/env python3
"""
GitHub App 认证客户端
支持 JWT 生成和 Installation Token 获取
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# 需要 PyJWT 和 cryptography
# pip install PyJWT cryptography


def generate_jwt(app_id: str, private_key_path: str) -> str:
    """
    生成 GitHub App JWT

    Args:
        app_id: GitHub App ID
        private_key_path: .pem 私钥文件路径
    """
    try:
        import jwt
    except ImportError:
        raise ImportError("请安装依赖: pip install PyJWT cryptography")

    with open(private_key_path, "r") as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        "iat": now - 60,  # 签发时间（提前 60 秒防止时钟偏差）
        "exp": now + 600,  # 过期时间（10 分钟）
        "iss": app_id
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token(jwt_token: str, installation_id: str) -> dict:
    """
    使用 JWT 获取 Installation Access Token

    Returns:
        {"token": "ghs_xxx", "expires_at": "2024-01-01T00:00:00Z"}
    """
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", f"Bearer {jwt_token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def list_installations(jwt_token: str) -> list:
    """列出当前 App 的所有安装"""
    url = "https://api.github.com/app/installations"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {jwt_token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def get_app_info(jwt_token: str) -> dict:
    """获取 GitHub App 信息"""
    url = "https://api.github.com/app"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {jwt_token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


class GitHubAppClient:
    """GitHub App 客户端"""

    def __init__(self, app_id: str, private_key_path: str):
        self.app_id = app_id
        self.private_key_path = private_key_path
        self._jwt = None
        self._jwt_expires = 0

    def _get_jwt(self) -> str:
        """获取或刷新 JWT"""
        now = time.time()
        if not self._jwt or now >= self._jwt_expires - 60:
            self._jwt = generate_jwt(self.app_id, self.private_key_path)
            self._jwt_expires = now + 600
        return self._jwt

    def get_installation_token(self, installation_id: str) -> str:
        """获取 Installation Access Token"""
        jwt_token = self._get_jwt()
        result = get_installation_token(jwt_token, installation_id)
        return result["token"]

    def list_installations(self) -> list:
        """列出所有安装"""
        jwt_token = self._get_jwt()
        return list_installations(jwt_token)

    def get_app_info(self) -> dict:
        """获取 App 信息"""
        jwt_token = self._get_jwt()
        return get_app_info(jwt_token)


def main():
    parser = argparse.ArgumentParser(description="GitHub App 认证工具")
    parser.add_argument("--app-id", required=True, help="GitHub App ID")
    parser.add_argument("--private-key", required=True, help="私钥 .pem 文件路径")
    parser.add_argument("--action", choices=["jwt", "token", "installations", "info"],
                        default="info", help="操作类型")
    parser.add_argument("--installation-id", help="Installation ID（获取 token 时需要）")
    parser.add_argument("--pretty", action="store_true", help="格式化输出")

    args = parser.parse_args()

    if not Path(args.private_key).exists():
        print(f"错误: 私钥文件不存在: {args.private_key}")
        sys.exit(1)

    try:
        if args.action == "jwt":
            jwt_token = generate_jwt(args.app_id, args.private_key)
            print(jwt_token)

        elif args.action == "token":
            if not args.installation_id:
                print("错误: --installation-id 是必需的")
                sys.exit(1)
            jwt_token = generate_jwt(args.app_id, args.private_key)
            result = get_installation_token(jwt_token, args.installation_id)
            print(json.dumps(result, indent=2 if args.pretty else None))

        elif args.action == "installations":
            jwt_token = generate_jwt(args.app_id, args.private_key)
            result = list_installations(jwt_token)
            print(json.dumps(result, indent=2 if args.pretty else None))

        elif args.action == "info":
            jwt_token = generate_jwt(args.app_id, args.private_key)
            result = get_app_info(jwt_token)
            print(json.dumps(result, indent=2 if args.pretty else None))

    except ImportError as e:
        print(f"依赖缺失: {e}")
        print("请运行: pip install PyJWT cryptography")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
