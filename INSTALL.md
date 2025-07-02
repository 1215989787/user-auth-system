# 多功能用户认证系统安装指南

## 系统要求

### 后端要求
- Python 3.9+
- MongoDB 6.x
- pip3
- 推荐使用虚拟环境

### 前端要求
- Flutter 3.0+
- Android Studio / Xcode (用于移动端开发)
- Chrome / Edge (用于Web端开发)

## 快速开始

### 1. 克隆项目
```bash
git clone <项目地址>
cd userpeofile0701
```

### 2. 安装和启动MongoDB

#### macOS (使用Homebrew)
```bash
# 安装MongoDB
brew tap mongodb/brew
brew install mongodb-community

# 启动MongoDB服务
brew services start mongodb-community

# 或者手动启动
mongod --dbpath /usr/local/var/mongodb
```

#### Linux (Ubuntu/Debian)
```bash
# 安装MongoDB
sudo apt update
sudo apt install mongodb

# 启动MongoDB服务
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### Windows
1. 从 [MongoDB官网](https://www.mongodb.com/try/download/community) 下载安装包
2. 安装后启动MongoDB服务

### 3. 启动后端

#### 方法一：手动启动（推荐）
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### 方法二：使用uvicorn（开发模式）
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动前端

#### 方法一：Web端启动
```bash
cd frontend
flutter pub get
flutter run -d chrome --web-port 3000
```

#### 方法二：移动端启动
```bash
cd frontend
flutter pub get
flutter run
```

### 5. 验证安装

#### 测试后端API
```bash
# 在项目根目录执行
python test_api.py
```

#### 测试前端功能
1. 访问 http://localhost:3000
2. 尝试注册新用户
3. 使用注册的账号登录
4. 测试各种功能

## 功能特性

### 后端功能
- ✅ **用户注册/登录**：账号密码、手机验证码、微信登录
- ✅ **JWT Token认证**：支持token刷新和自动续期
- ✅ **用户资料管理**：昵称、头像、性别、生日、简介等
- ✅ **VIP会员管理**：等级、到期时间、余额、特权
- ✅ **MongoDB异步驱动**：使用Motor实现高性能数据库操作
- ✅ **智能错误处理**：409冲突状态码，结构化错误响应
- ✅ **Pydantic v2兼容**：完全适配最新版本
- ✅ **API文档自动生成**：Swagger UI和ReDoc
- ✅ **真实密码验证**：错误密码会正确报错
- ✅ **完整API集成**：所有功能都调用真实后端API

### 前端功能
- ✅ **现代化UI设计**：渐变背景、卡片式布局
- ✅ **多种登录方式**：密码登录、短信登录、微信登录
- ✅ **智能错误提示**：友好的用户错误信息显示
- ✅ **用户资料管理**：完整的个人资料编辑功能
- ✅ **VIP会员管理**：会员状态展示和管理
- ✅ **响应式设计**：支持Web和移动端
- ✅ **真实API调用**：所有功能都调用真实后端API，无模拟延迟
- 🔄 **生物识别解锁**：预留接口，需要配置
- 🔄 **微信登录**：需要配置微信开发参数

## API文档

启动后端后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 配置说明

### 后端配置

编辑 `backend/app/core/config.py` 文件：

```python
# MongoDB配置
mongodb_url = "mongodb://localhost:27017"
mongodb_database = "user_auth_system"

# JWT配置
secret_key = "your-secret-key-here"
algorithm = "HS256"
access_token_expire_minutes = 30
refresh_token_expire_days = 7

# 微信配置
wechat_app_id = "your_wechat_app_id"
wechat_app_secret = "your_wechat_app_secret"

# 短信配置（可选）
sms_api_key = "your_sms_api_key"
sms_api_secret = "your_sms_api_secret"

# 邮件配置（可选）
smtp_username = "your_email@gmail.com"
smtp_password = "your_email_password"
```

### 前端配置

编辑 `frontend/lib/services/api_service.dart` 文件：

```dart
class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  // 如果后端运行在不同端口，请修改这里
}
```

## 数据库

系统使用MongoDB数据库：

### 数据库结构
- **users**：用户基本信息、认证信息、VIP信息
- **verification_codes**：验证码记录
- **user_sessions**：用户会话信息
- **vip_subscriptions**：VIP订阅记录

### 查看数据
```bash
# 使用mongosh连接数据库
mongosh user_auth_system

# 查看用户数据
db.users.find()

# 查看验证码数据
db.verification_codes.find()
```

### 数据库管理工具
```bash
# 清空数据库（开发环境）
python backend/clear_db.py

# 测试API功能
python test_api.py
```

### 数据库工具
- **MongoDB Compass**：图形化数据库管理工具
- **mongosh**：命令行数据库客户端

## 错误处理机制

### 后端错误响应格式
```json
{
  "detail": {
    "code": "USER_EXISTS",
    "msg": "该用户已注册"
  }
}
```

### 前端错误处理
- 使用 `ErrorHandler` 工具类统一处理API错误
- 智能解析 `detail.msg` 和 `detail` 两种格式
- 根据HTTP状态码返回友好提示

### 常见错误类型
- **409 Conflict**：用户已注册、数据冲突
- **400 Bad Request**：参数错误、验证失败
- **401 Unauthorized**：未授权、token过期
- **500 Internal Server Error**：服务器内部错误

## 常见问题解决

### 后端问题

#### 1. ModuleNotFoundError: No module named 'motor'
```bash
# 确保已激活虚拟环境
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. MongoDB连接失败
```bash
# 检查MongoDB服务状态
brew services list | grep mongodb

# 启动MongoDB服务
brew services start mongodb-community
```

#### 3. 端口占用问题
```bash
# 查找占用端口的进程
lsof -i :8000
lsof -i :27017

# 杀死进程
kill -9 <PID>
```

#### 4. Pydantic兼容问题
项目已完全适配Pydantic v2，如遇到类型错误，已修复所有ObjectId转换问题。

### 前端问题

#### 1. 依赖冲突
```bash
cd frontend
flutter clean
flutter pub get
```

#### 2. 端口占用
```bash
# 查找占用端口的进程
lsof -i :3000

# 杀死进程
kill -9 <PID>
```

#### 3. Chrome报错
- 重启Chrome浏览器
- 更换端口：`flutter run -d chrome --web-port 3001`

#### 4. 类型错误
项目已修复所有前后端类型不一致问题，ID字段统一为String类型。

## 开发调试

### 后端调试
```bash
# 启动开发模式（自动重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 查看详细日志
python main.py --debug
```

### 前端调试
```bash
# 启动调试模式
flutter run -d chrome --web-port 3000

# 查看调试信息
flutter logs
```

### API测试
```bash
# 运行完整API测试
python test_api.py

# 测试特定接口
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "123456", "login_type": "password"}'
```

## 上线准备

### 1. 环境检查清单
- ✅ 后端API测试全部通过
- ✅ 前端依赖安装完成
- ✅ 数据库连接正常
- ✅ 错误处理机制完善
- ✅ 前后端类型一致
- ✅ 真实API调用验证

### 2. 生产环境配置
```python
# backend/app/core/config.py
mongodb_url = "mongodb://production-server:27017"
secret_key = "your-production-secret-key"
access_token_expire_minutes = 30
refresh_token_expire_days = 7
```

### 3. 安全配置
- 修改默认JWT密钥
- 配置CORS策略
- 设置环境变量
- 启用HTTPS

### 4. 部署建议
- 使用Docker容器化部署
- 配置Nginx反向代理
- 设置SSL证书
- 配置监控和日志
- 数据库备份策略

## 技术支持

### 检查清单
1. 后端服务是否正常启动
2. MongoDB连接是否正常
3. 前端依赖是否安装完成
4. 网络连接是否正常
5. API测试是否通过

### 获取帮助
- 查看API文档：http://localhost:8000/docs
- 检查错误日志
- 运行测试脚本：`python test_api.py`
- 参考项目文档

### 项目状态
- **后端**：✅ 完全可用，所有API正常工作
- **前端**：✅ 完全可用，所有功能调用真实API
- **数据库**：✅ MongoDB异步驱动，高性能
- **错误处理**：✅ 智能错误提示，用户友好
- **类型安全**：✅ 前后端类型完全一致 