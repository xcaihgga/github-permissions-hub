#!/usr/bin/env python3
"""
火山引擎 API 客户端 - 统一管理火山引擎各服务调用
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials


def get_credentials():
    """从环境变量获取 AK/SK"""
    ak = os.environ.get("VOLCENGINE_AK")
    sk = os.environ.get("VOLCENGINE_SK")
    if not ak or not sk:
        print("错误: 请设置 VOLCENGINE_AK 和 VOLCENGINE_SK 环境变量", file=sys.stderr)
        sys.exit(1)
    return ak, sk


def api_call(ak, sk, service, action, version, region="cn-north-1", method="GET", query=None, body=None):
    """调用火山引擎 API"""
    if query is None:
        query = {}
    query["Action"] = action
    query["Version"] = version
    
    r = Request()
    r.set_shema("https")
    r.set_method(method.upper())
    r.set_connection_timeout(30)
    r.set_socket_timeout(30)
    r.set_host("open.volcengineapi.com")
    r.set_path("/")
    r.set_query(query)
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json" if body else "application/x-www-form-urlencoded"
    }
    r.set_headers(headers)
    if body:
        r.set_body(json.dumps(body))
    
    credentials = Credentials(ak, sk, service, region)
    SignerV4.sign(r, credentials)
    
    query_str = urllib.parse.urlencode(sorted(query.items()))
    url = f"https://{r.host}{r.path}?{query_str}"
    
    req = urllib.request.Request(url, method=r.method)
    for k, v in r.headers.items():
        req.add_header(k, v)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read())
        except:
            return {"error": f"HTTP {e.code}", "message": str(e)}


def cmd_iam_users(args):
    """列出 IAM 用户"""
    ak, sk = get_credentials()
    data = api_call(ak, sk, "iam", "ListUsers", "2018-01-01", query={"PageSize": "100"})
    if "Result" in data:
        users = data["Result"].get("UserMetadata", [])
        print(f"用户总数: {data['Result'].get('Total', 0)}")
        for u in users:
            print(f"  - {u.get('UserName', 'N/A')} (ID: {u.get('UserId', 'N/A')})")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_api(args):
    """调用任意 API"""
    ak, sk = get_credentials()
    query = {}
    if args.query:
        for item in args.query:
            k, v = item.split("=", 1)
            query[k] = v
    body = json.loads(args.body) if args.body else None
    data = api_call(ak, sk, args.service, args.action, args.version, args.region, args.method, query, body)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="火山引擎 API 客户端")
    parser.add_argument("--ak", help="Access Key ID (也可通过 VOLCENGINE_AK 环境变量)")
    parser.add_argument("--sk", help="Secret Access Key (也可通过 VOLCENGINE_SK 环境变量)")
    sub = parser.add_subparsers(dest="command")
    
    sub.add_parser("iam-users", help="列出 IAM 用户").set_defaults(func=cmd_iam_users)
    
    api_p = sub.add_parser("api", help="调用任意 API")
    api_p.add_argument("--service", required=True, help="服务名，如 iam, ecs, tos")
    api_p.add_argument("--action", required=True, help="接口名，如 ListUsers")
    api_p.add_argument("--version", default="2018-01-01", help="API 版本")
    api_p.add_argument("--region", default="cn-north-1", help="地域")
    api_p.add_argument("--method", default="GET", help="HTTP 方法")
    api_p.add_argument("--query", nargs="*", help="查询参数，如 Key=Value")
    api_p.add_argument("--body", help="请求体 JSON 字符串")
    api_p.set_defaults(func=cmd_api)
    
    args = parser.parse_args()
    
    if args.ak:
        os.environ["VOLCENGINE_AK"] = args.ak
    if args.sk:
        os.environ["VOLCENGINE_SK"] = args.sk
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
