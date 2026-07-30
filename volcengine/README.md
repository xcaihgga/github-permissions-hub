# 火山引擎权限管理

火山引擎 AK/SK 管理与 API 调用指南。

## AK/SK 信息

- **Access Key ID (AK)**: `YOUR_ACCESS_KEY_ID`
- **Secret Access Key (SK)**: `YOUR_SECRET_ACCESS_KEY`
- **账号状态**: 有效
- **获取地址**: https://console.volcengine.com/iam/keymanage
- **地域默认**: cn-north-1

## 签名机制

火山引擎使用 HMAC-SHA256 签名鉴权（类似 AWS Signature Version 4），每个请求的签名都是独立且临时的。

**签名参数：**
- `X-Date`: UTC 时间，格式 `YYYYMMDD'T'HHMMSS'Z'`
- `Authorization`: `HMAC-SHA256 Credential={AK}/{ShortDate}/{Region}/{Service}/request, SignedHeaders={SignedHeaders}, Signature={Signature}`

## 常用 API

```python
# 使用 volcengine SDK（推荐）
pip install volcengine

# 通用签名调用示例
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials

def volcengine_api_call(ak, sk, service, action, version, region="cn-north-1", method="GET", query=None, body=None):
    r = Request()
    r.set_shema("https")
    r.set_method(method)
    r.set_host(f"open.volcengineapi.com")
    r.set_path("/")
    if query:
        r.set_query(query)
    r.set_headers({
        "Accept": "application/json",
        "Content-Type": "application/json" if body else "application/x-www-form-urlencoded"
    })
    if body:
        r.set_body(json.dumps(body))
    
    credentials = Credentials(ak, sk, service, region)
    SignerV4.sign(r, credentials)
    
    # 发送请求...
    return r
```

## 使用场景

| 场景 | 服务名 | 说明 |
|------|--------|------|
| IAM 用户管理 | iam | 管理子用户、权限策略 |
| 对象存储 TOS | tos | 文件上传下载 |
| 云服务器 ECS | ecs | 实例管理 |
| 容器服务 VKE | vke | Kubernetes 集群 |
| 数据库服务 | rds | 数据库实例管理 |
| CDN | cdn | 内容分发 |
| AI 服务 | ark/视觉/语音 | 大模型、图像、语音等 |

## 安全建议

- AK/SK 是敏感信息，不要提交到 Git 仓库
- 使用子账号 AK/SK 而非主账号，遵循最小权限原则
- 定期轮换密钥
- 在 TRAE 中使用环境变量：`VOLCENGINE_AK` 和 `VOLCENGINE_SK`
