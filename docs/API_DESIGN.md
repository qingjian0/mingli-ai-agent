# 第八部分：API设计规范

## API整体设计

### 设计原则
- **RESTful**: 标准HTTP方法 (GET, POST, PUT, DELETE)
- **事件驱动**: 长连接 WebSocket + Server-Sent Events
- **版本控制**: `/api/v1/`, `/api/v2/` 兼容多版本
- **可观测性**: 完整的请求追踪 (X-Request-ID)
- **速率限制**: 基于用户配额的分级限制
- **幂等性**: 关键操作支持幂等密钥

---

## 1. 认证 & 授权 API

### 1.1 用户注册
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "张三"
}

Response: 201 Created
{
  "user_id": 12345,
  "username": "user123",
  "email": "user@example.com",
  "created_at": "2026-06-08T10:30:00Z",
  "verification_status": "unverified"
}
```

### 1.2 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response: 200 OK
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 3600,
  "user": {
    "user_id": 12345,
    "username": "user123",
    "roles": ["user"]
  }
}
```

### 1.3 刷新Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json
Authorization: Bearer {refresh_token}

Response: 200 OK
{
  "access_token": "eyJhbGc...",
  "expires_in": 3600
}
```

### 1.4 登出
```http
POST /api/v1/auth/logout
Authorization: Bearer {access_token}

Response: 204 No Content
```

---

## 2. 计算请求 API

### 2.1 提交计算请求
```http
POST /api/v1/computations
Content-Type: application/json
Authorization: Bearer {access_token}
X-Idempotency-Key: {uuid}

{
  "domain": "bazi",
  "query": "分析这个人的运势",
  "input_data": {
    "birth_year": 1990,
    "birth_month": 5,
    "birth_day": 15,
    "birth_hour": 14,
    "birth_minute": 30,
    "gender": "male",
    "birth_location": "北京",
    "calendar_type": "gregorian"
  },
  "options": {
    "include_historical_cases": true,
    "prediction_years": 10,
    "detail_level": "detailed"
  }
}

Response: 202 Accepted
{
  "request_id": "comp_20250608_001",
  "request_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "progress_percentage": 0,
  "created_at": "2026-06-08T10:30:00Z",
  "expires_at": "2026-06-09T10:30:00Z",
  "polling_url": "/api/v1/computations/comp_20250608_001",
  "ws_url": "wss://api.example.com/ws/computations/comp_20250608_001"
}
```

### 2.2 查询计算进度
```http
GET /api/v1/computations/{request_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "request_id": "comp_20250608_001",
  "status": "processing",
  "progress_percentage": 45,
  "current_step": "calculation_engine",
  "current_step_name": "八字排盘计算",
  "steps": [
    {
      "step_number": 1,
      "agent_type": "planner",
      "status": "completed",
      "duration_ms": 250
    },
    {
      "step_number": 2,
      "agent_type": "knowledge",
      "status": "completed",
      "duration_ms": 1200
    },
    {
      "step_number": 3,
      "agent_type": "calculation",
      "status": "running",
      "duration_ms": 800
    }
  ],
  "started_at": "2026-06-08T10:30:05Z"
}
```

### 2.3 获取计算结果
```http
GET /api/v1/computations/{request_id}/result
Authorization: Bearer {access_token}

Response: 200 OK
{
  "request_id": "comp_20250608_001",
  "status": "completed",
  "result_data": {
    "domain": "bazi",
    "birth_chart": {
      "year_stem_branch": "庚午",
      "month_stem_branch": "丙午",
      "day_stem_branch": "丁酉",
      "hour_stem_branch": "己未",
      "five_elements": ["金", "火", "火", "土"],
      "ten_gods": ["正官", "食神", "日元", "正财"]
    },
    "analysis": {
      "summary": "此人八字...",
      "five_elements_analysis": { ... },
      "lucky_elements": ["水", "木"],
      "major_luck": [ ... ],
      "predictions": [ ... ]
    },
    "related_cases": [
      {
        "case_id": 123,
        "case_name": "某历史人物",
        "similarity_score": 0.87
      }
    ]
  },
  "quality_score": 0.92,
  "confidence_score": 0.89,
  "knowledge_sources": [
    {
      "source_id": 1,
      "source_name": "古籍汇编",
      "trustworthiness": 0.95,
      "chunks_used": 15
    }
  ],
  "completed_at": "2026-06-08T10:35:20Z",
  "total_execution_time_ms": 320
}
```

### 2.4 取消计算
```http
DELETE /api/v1/computations/{request_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "request_id": "comp_20250608_001",
  "status": "cancelled",
  "cancelled_at": "2026-06-08T10:35:00Z"
}
```

---

## 3. 知识管理 API

### 3.1 知识搜索
```http
GET /api/v1/knowledge/search
Authorization: Bearer {access_token}

Query Parameters:
  q: "八字格局"                          # 搜索关键词
  domain: "bazi"                         # 可选：限制域
  content_type: "definition,example"     # 可选：内容类型
  quality_min: 0.7                       # 可选：最低质量
  trustworthiness_min: 0.8               # 可选：最低可信度
  limit: 20                              # 可选：返回数量
  offset: 0                              # 可选：分页偏移

Response: 200 OK
{
  "query": "八字格局",
  "total_results": 156,
  "results": [
    {
      "chunk_id": 4521,
      "source_id": 12,
      "source_name": "古籍汇编",
      "domain": "bazi",
      "content_type": "definition",
      "content": "八字格局是指根据十天干...",
      "content_preview": "八字格局是指根据十天干与十二地支的组合...",
      "quality_score": 0.95,
      "trustworthiness": 0.95,
      "authority_level": "authoritative",
      "similarity_score": 0.92,
      "rerank_score": 0.91,
      "cited_count": 245,
      "related_chunks": [4522, 4523, 4524],
      "entities": ["日主", "天干", "地支"],
      "created_at": "2025-01-15T00:00:00Z",
      "updated_at": "2026-05-20T10:00:00Z"
    }
  ],
  "facets": {
    "domain": {
      "bazi": 120,
      "ziwei": 25,
      "qimen": 11
    },
    "content_type": {
      "definition": 80,
      "example": 45,
      "formula": 31
    },
    "quality_range": {
      "0.9-1.0": 95,
      "0.7-0.9": 45,
      "0.5-0.7": 16
    }
  }
}
```

### 3.2 知识详情
```http
GET /api/v1/knowledge/chunks/{chunk_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "chunk_id": 4521,
  "source_id": 12,
  "source": {
    "source_id": 12,
    "source_name": "古籍汇编",
    "author": "未知",
    "publication_date": "2020-01-01",
    "authority_level": "authoritative",
    "trustworthiness": 0.95,
    "url": "https://..."
  },
  "content": "八字格局是指根据十天干与十二地支的组合...",
  "domain": "bazi",
  "content_type": "definition",
  "difficulty_level": 2,
  "quality_score": 0.95,
  "completeness_score": 0.92,
  "clarity_score": 0.97,
  "section_title": "第一章 基础概念",
  "hierarchical_position": "1.2.3",
  "page_number": 15,
  "parent_chunk_id": 4520,
  "child_chunks": [4522, 4523, 4524],
  "related_chunks": [4525, 4526],
  "entities": [
    {
      "entity_type": "concept",
      "entity_name": "日主",
      "canonical_form": "日干",
      "description": "八字中代表本人的天干"
    }
  ],
  "created_at": "2025-01-15T00:00:00Z",
  "version": 2,
  "version_history": [
    {
      "version": 1,
      "updated_at": "2025-01-15T00:00:00Z",
      "updated_by": "admin",
      "change_summary": "初始创建"
    }
  ]
}
```

### 3.3 上传知识源
```http
POST /api/v1/knowledge/sources
Content-Type: multipart/form-data
Authorization: Bearer {access_token}

form_data:
  file: <PDF file>
  source_name: "新增古籍"
  source_type: "book"
  author: "某某"
  publication_date: "2026-01-01"
  authority_level: "reliable"
  license_type: "open"

Response: 202 Accepted
{
  "source_id": 145,
  "source_name": "新增古籍",
  "status": "processing",
  "upload_id": "upload_20250608_001",
  "progress_url": "/api/v1/knowledge/sources/145/processing-progress",
  "message": "知识源已提交处理，将进行抽取、分块、分类、嵌入等处理"
}
```

---

## 4. 案例库 API

### 4.1 搜索历史案例
```http
GET /api/v1/cases/search
Authorization: Bearer {access_token}

Query Parameters:
  domain: "bazi"
  subject_birth_year_min: 1900
  subject_birth_year_max: 2000
  verification_status: "verified"
  quality_min: 0.8
  limit: 20

Response: 200 OK
{
  "total_cases": 342,
  "cases": [
    {
      "case_id": 201,
      "case_uuid": "550e8400-e29b-41d4-a716-446655440000",
      "case_name": "某历史人物分析",
      "primary_domain": "bazi",
      "subject_name": "某某",
      "subject_birth_date": "1950-06-15",
      "subject_gender": "male",
      "subject_birth_location": "北京",
      "analysis_summary": "此人八字...",
      "verified_outcome": "预测准确度90%以上",
      "verification_status": "fully_verified",
      "quality_score": 0.95,
      "expert_endorsed": true,
      "created_at": "2024-01-10T00:00:00Z"
    }
  ]
}
```

### 4.2 案例详情
```http
GET /api/v1/cases/{case_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "case_id": 201,
  "case_name": "某历史人物分析",
  "description": "详细的案例描述",
  "subject": {
    "name": "某某",
    "birth_date": "1950-06-15",
    "gender": "male",
    "birth_location": "北京",
    "birth_time": "14:30"
  },
  "domains": ["bazi", "feng_shui"],
  "analysis": {
    "bazi_analysis": { ... },
    "predictions": [ ... ],
    "actual_outcomes": [ ... ]
  },
  "source_id": 12,
  "contributed_by": 345,
  "expert_endorsements": [
    {
      "expert_id": 678,
      "expert_name": "专家甲",
      "endorsed_at": "2024-06-20T10:00:00Z"
    }
  ],
  "verification_status": "fully_verified",
  "quality_score": 0.95
}
```

### 4.3 保存案例
```http
POST /api/v1/cases/{case_id}/save
Authorization: Bearer {access_token}

{
  "notes": "这个案例很有参考价值"
}

Response: 201 Created
{
  "saved_at": "2026-06-08T10:30:00Z"
}
```

---

## 5. 用户记忆 & 历史 API

### 5.1 获取对话历史
```http
GET /api/v1/memory/conversations/{session_id}
Authorization: Bearer {access_token}

Query Parameters:
  limit: 50
  offset: 0

Response: 200 OK
{
  "session_id": "sess_20250608_001",
  "messages": [
    {
      "message_id": 1001,
      "role": "user",
      "content": "帮我分析这个八字",
      "created_at": "2026-06-08T10:30:00Z"
    },
    {
      "message_id": 1002,
      "role": "assistant",
      "content": "好的，我来为您分析...",
      "tokens_used": 450,
      "model_used": "qwen3:8b",
      "processing_time_ms": 2100,
      "created_at": "2026-06-08T10:30:05Z"
    }
  ]
}
```

### 5.2 保存计算结果
```http
POST /api/v1/memory/saved-queries
Authorization: Bearer {access_token}

{
  "request_id": "comp_20250608_001",
  "custom_name": "母亲的运势分析",
  "notes": "用于对比2026年运势变化",
  "tags": ["family", "2026", "important"]
}

Response: 201 Created
{
  "saved_query_id": 5001,
  "saved_at": "2026-06-08T10:30:00Z"
}
```

### 5.3 获取用户统计
```http
GET /api/v1/memory/user-stats
Authorization: Bearer {access_token}

Response: 200 OK
{
  "user_id": 12345,
  "total_computations": 156,
  "successful_computations": 154,
  "total_computation_time_hours": 12.5,
  "favorite_domains": ["bazi", "ziwei", "date_selection"],
  "saved_cases": 45,
  "saved_queries": 23,
  "last_computation": {
    "request_id": "comp_20250608_001",
    "completed_at": "2026-06-08T10:35:20Z",
    "domain": "bazi"
  },
  "monthly_usage": [
    {
      "month": "2026-05",
      "computations": 25,
      "minutes_used": 120
    }
  ]
}
```

---

## 6. 管理员 API

### 6.1 审核计算结果
```http
PATCH /api/v1/admin/computations/{request_id}/review
Authorization: Bearer {admin_token}

{
  "review_status": "approved",
  "review_notes": "分析准确，质量良好",
  "quality_score": 0.95,
  "flag_for_expert": false
}

Response: 200 OK
{
  "request_id": "comp_20250608_001",
  "review_status": "approved",
  "reviewed_by": 1,
  "reviewed_at": "2026-06-08T11:00:00Z"
}
```

### 6.2 知识质量评分
```http
POST /api/v1/admin/knowledge/chunks/{chunk_id}/quality-review
Authorization: Bearer {admin_token}

{
  "quality_score": 0.95,
  "completeness_score": 0.92,
  "clarity_score": 0.97,
  "trustworthiness": 0.95,
  "notes": "高质量的定义，表述清晰"
}

Response: 200 OK
{
  "chunk_id": 4521,
  "quality_score": 0.95,
  "reviewed_at": "2026-06-08T11:00:00Z",
  "reviewed_by": 1
}
```

### 6.3 用户管理
```http
GET /api/v1/admin/users
Authorization: Bearer {admin_token}

Query Parameters:
  status: "active"
  subscription_tier: "pro"
  limit: 50

Response: 200 OK
{
  "total_users": 1250,
  "users": [
    {
      "user_id": 12345,
      "username": "user123",
      "email": "user@example.com",
      "status": "active",
      "roles": ["user"],
      "subscription_tier": "pro",
      "created_at": "2026-01-01T00:00:00Z",
      "last_login": "2026-06-07T15:30:00Z"
    }
  ]
}
```

---

## 7. WebSocket 实时 API

### 7.1 连接到计算实时更新
```
ws://api.example.com/ws/computations/{request_id}?token={access_token}

# 发送heartbeat保活
{ "type": "ping" }

# 接收计算更新
{
  "type": "step_update",
  "step_number": 3,
  "agent_type": "calculation",
  "status": "running",
  "progress_percentage": 45,
  "estimated_remaining_seconds": 45
}

# 接收完成消息
{
  "type": "completed",
  "request_id": "comp_20250608_001",
  "status": "completed",
  "total_execution_time_ms": 3200
}

# 接收错误消息
{
  "type": "error",
  "error_code": "CALC_001",
  "error_message": "计算引擎内部错误",
  "step_number": 3
}
```

### 7.2 连接到对话流
```
ws://api.example.com/ws/chat/{session_id}?token={access_token}

# 发送消息
{
  "type": "message",
  "content": "帮我分析这个八字"
}

# 接收流式响应
{
  "type": "stream",
  "content": "我正在为您分析...",
  "tokens_generated": 25
}

# 接收完成
{
  "type": "done",
  "total_tokens": 450,
  "computation_request_id": "comp_20250608_001"
}
```

---

## 8. 错误处理

### 标准错误响应
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求数据验证失败",
    "details": [
      {
        "field": "birth_year",
        "issue": "必须在1900-2100之间"
      }
    ],
    "request_id": "req_20250608_001",
    "timestamp": "2026-06-08T10:30:00Z"
  }
}
```

### 常见错误码
| 错误码 | HTTP状态 | 说明 |
|--------|---------|------|
| INVALID_REQUEST | 400 | 请求格式错误 |
| INVALID_AUTH | 401 | 认证失败 |
| FORBIDDEN | 403 | 无权访问 |
| NOT_FOUND | 404 | 资源不存在 |
| RATE_LIMIT_EXCEEDED | 429 | 请求过于频繁 |
| QUOTA_EXCEEDED | 429 | 配额已满 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |
| SERVICE_UNAVAILABLE | 503 | 服务不可用 |

---

## 9. 速率限制 & 配额

### 请求头
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1717944600
X-Request-ID: req_20250608_001
```

### 配额规则
- Free: 100请求/小时，10000分钟/月计算
- Basic: 500请求/小时，50000分钟/月计算
- Pro: 2000请求/小时，无限制
- Enterprise: 自定义

---

## 10. 版本控制

### 当前版本
- `/api/v1/` - 稳定版本

### 弃用策略
1. 新版本发布
2. 旧版本30天警告期
3. 60天后关闭旧版本

---

## 11. 实现技术栈

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Auth**: JWT + OAuth2
- **Cache**: Redis
- **Vector DB**: Qdrant (Python客户端)
- **WebSocket**: websockets
- **Documentation**: FastAPI自动生成 + Swagger

### 关键装饰器示例

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer

app = FastAPI()

@app.post("/api/v1/computations")
async def submit_computation(
    request: ComputationRequest,
    user: User = Depends(get_current_user),
    rate_limiter: RateLimiter = Depends(check_rate_limit),
    idempotency_key: str = Header(None)
) -> ComputationResponse:
    """
    提交计算请求
    
    - **domain**: 术数域 (bazi, ziwei, etc.)
    - **query**: 用户问题
    - **input_data**: 结构化输入
    - **options**: 计算选项
    """
    # 实现逻辑
    pass
```

