#!/usr/bin/env python3
"""
Vercel API 客户端 - 统一管理 Vercel 部署和项目操作
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

BASE_URL = "https://api.vercel.com"

def api_call(token, endpoint, method="GET", data=None):
    """调用 Vercel API"""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        return {"error": f"HTTP {e.code}", "message": err_body}

def get_token():
    """从环境变量获取 Token"""
    token = os.environ.get("VERCEL_TOKEN")
    if not token:
        print("错误: 请设置 VERCEL_TOKEN 环境变量", file=sys.stderr)
        sys.exit(1)
    return token

def cmd_user(args):
    """获取用户信息"""
    data = api_call(get_token(), "/v2/user")
    if "user" in data:
        u = data["user"]
        print(f"用户: {u.get('username')}")
        print(f"邮箱: {u.get('email')}")
        print(f"ID: {u.get('id')}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

def cmd_projects(args):
    """列出所有项目"""
    data = api_call(get_token(), "/v9/projects")
    projects = data.get("projects", [])
    print(f"项目数: {len(projects)}")
    print()
    for p in projects:
        url = p.get("targets", {}).get("production", {}).get("url", "-")
        print(f"  {p['name']:30s} {p.get('framework', '-'):15s} https://{url}")

def cmd_deployments(args):
    """列出部署记录"""
    data = api_call(get_token(), "/v6/deployments?limit=10")
    deploys = data.get("deployments", [])
    print(f"最近 {len(deploys)} 次部署:")
    for d in deploys:
        state = d.get("state", "-")
        name = d.get("name", "-")
        url = d.get("url", "-")
        print(f"  [{state:10s}] {name:20s} https://{url}")

def cmd_api(args):
    """直接调用任意 API"""
    data = api_call(get_token(), args.endpoint, method=args.method)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="Vercel API 客户端")
    parser.add_argument("--token", help="Vercel Token (也可通过 VERCEL_TOKEN 环境变量)")
    sub = parser.add_subparsers(dest="command")
    
    sub.add_parser("user", help="获取用户信息").set_defaults(func=cmd_user)
    sub.add_parser("projects", help="列出项目").set_defaults(func=cmd_projects)
    sub.add_parser("deployments", help="列出部署记录").set_defaults(func=cmd_deployments)
    
    api_p = sub.add_parser("api", help="调用任意 API")
    api_p.add_argument("--endpoint", required=True, help="API 端点，如 /v2/user")
    api_p.add_argument("--method", default="GET", help="HTTP 方法")
    api_p.set_defaults(func=cmd_api)
    
    args = parser.parse_args()
    
    if args.token:
        os.environ["VERCEL_TOKEN"] = args.token
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)

if __name__ == "__main__":
    main()
