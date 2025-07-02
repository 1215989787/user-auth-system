# 多功能用户认证系统（FastAPI + MongoDB + Flutter）

## 项目简介
本项目是一个功能完整的用户认证系统，支持多种登录方式（账号密码、手机号验证码、微信跳转登录）、个人资料管理、VIP会员管理和生物识别解锁。后端基于 FastAPI + MongoDB，前端采用 Flutter 实现，适合 Web 端和移动端快速集成。

### 🚀 最新特性
- ✅ **完整API集成**：所有前端功能都已实现真正的后端API调用，无模拟延迟
- ✅ **智能错误处理**：友好的用户提示，支持结构化错误信息解析
- ✅ **多登录方式**：用户名/邮箱、手机号验证码、微信登录
- ✅ **用户状态管理**：409冲突状态码，精确区分"用户已注册"等业务错误
- ✅ **MongoDB异步驱动**：使用Motor实现高性能异步数据库操作
- ✅ **Pydantic v2兼容**：完全适配最新版本，解决类型验证问题
- ✅ **前后端类型一致**：所有ID字段统一为String类型，避免类型转换错误
- ✅ **真实密码验证**：错误密码会正确报错，不再允许错误密码登录

---

## 技术栈说明
- **后端**：FastAPI、MongoDB、Pydantic v2、Motor（异步MongoDB驱动）
- **前端**：Flutter（支持Web/移动端）、Dio（网络请求）、Provider（状态管理）
- **数据库**：MongoDB（所有用户数据、注册、登录、资料、VIP等均存储于MongoDB）
- **错误处理**：结构化错误响应，409冲突状态码，友好用户提示

---

## 项目状态

### ✅ 已完成功能
- **用户注册/登录**：账号密码、手机验证码、微信登录（API已实现）
- **JWT Token认证**：支持token刷新和自动续期
- **用户资料管理**：昵称、头像、性别、生日、简介等
- **VIP会员管理**：等级、到期时间、余额、特权
- **智能错误处理**：409冲突状态码，结构化错误响应
- **数据库管理**：MongoDB异步驱动，支持高性能并发操作
- **API文档**：自动生成Swagger UI和ReDoc文档

### 🔄 部分实现功能
- **微信登录**：后端API已实现，前端需要配置微信开发参数
- **生物识别解锁**：本地API已实现，需要设备支持

---

## 后端环境搭建与启动

### 1. 环境准备
- Python 3.9+
- MongoDB 6.x（本地或远程均可）
- 推荐使用虚拟环境（venv）

### 2. 安装依赖
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. MongoDB 启动与配置
- 确保本地 MongoDB 服务已启动，默认连接：`mongodb://localhost:27017`，数据库名：`user_auth_system`
- 如需自定义连接，修改 `backend/app/core/config.py` 中的 `mongodb_url` 和 `mongodb_database`
- 启动命令示例：
  ```bash
  mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork
  ```
- 若端口冲突或启动失败，先关闭已有 mongod 进程：
  ```bash
  lsof -i :27017
  kill -9 <PID>
  ```

### 4. 启动后端服务
```bash
cd backend
source venv/bin/activate
python main.py
```
- 访问接口文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 5. 数据库管理
```bash
# 清空数据库（开发环境）
python backend/clear_db.py

# 测试API功能
python test_api.py
```

### 6. 常见问题
- **ModuleNotFoundError: No module named 'motor'**：确认已激活虚拟环境并安装所有依赖。
- **MongoDB 端口占用**：用 `lsof -i :27017` 查找并杀死进程。
- **Pydantic 兼容问题**：已适配 v2，若遇到 `__modify_schema__` 报错，已修复为 `__get_pydantic_json_schema__`。
- **PyObjectId 类型错误**：已修复所有ObjectId类型转换问题。
- **email-validator 报错**：`pip install email-validator`

---

## 前端环境搭建与启动

### 1. 环境准备
- Flutter 3.x（建议使用最新版）
- Chrome 浏览器（Web调试）

### 2. 安装依赖
```bash
cd frontend
flutter pub get
```

### 3. 启动前端（Web端）
```bash
flutter run -d chrome --web-port 3000
```
- 默认访问：http://localhost:3000
- 如端口被占用，先查找并杀死进程：
  ```bash
  lsof -i :3000
  kill -9 <PID>
  ```

### 4. 常见问题
- **依赖冲突**：升级/降级依赖后务必 `flutter pub get`。
- **fluwx 兼容问题**：已升级到 5.6.0。
- **资源/字体缺失**：可临时注释 `pubspec.yaml` 中的 assets/fonts 配置。
- **Chrome 报错**：重启 Chrome 或更换端口。

---

## 主要功能说明

### 1. 多方式登录/注册
- **账号密码登录/注册**：支持用户名或邮箱格式，真实密码验证
- **手机号+验证码登录/注册**：完整的验证码发送和验证流程
- **微信跳转登录**：后端API已实现，前端需要配置微信开发参数

### 2. 智能错误处理
- **结构化错误响应**：后端返回 `{"code": "USER_EXISTS", "msg": "该用户已注册"}`
- **409冲突状态码**：精确区分业务错误类型
- **友好用户提示**：前端智能解析错误信息，显示用户友好的提示

### 3. 个人资料管理
- 支持查看、编辑昵称、头像、性别、生日、简介等
- 实时数据同步和验证

### 4. VIP会员管理
- VIP等级、到期时间、余额、特权展示
- 支持订阅、取消、历史查询

### 5. 生物识别解锁
- 预留接口，支持后续集成指纹/面容ID

### 6. 安全退出
- 支持一键安全退出，调用后端API清除会话

---

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

---

## 数据存储说明
- 所有用户数据（注册、登录、资料、VIP等）均存储于 MongoDB 数据库
- 使用Motor异步驱动，支持高性能并发操作
- 可用 `mongosh` 或 MongoDB Compass 工具查看数据
- 数据库配置详见 `backend/app/core/config.py`

---

## API接口说明

### 认证相关接口
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/wechat/login` - 微信登录
- `POST /api/v1/auth/verification-code` - 发送验证码
- `POST /api/v1/auth/refresh` - 刷新token
- `POST /api/v1/auth/logout` - 用户登出
- `GET /api/v1/auth/me` - 获取当前用户信息

### 用户相关接口
- `GET /api/v1/users/profile` - 获取用户资料
- `PUT /api/v1/users/profile` - 更新用户资料
- `POST /api/v1/users/change-password` - 修改密码
- `GET /api/v1/users/vip/info` - 获取VIP信息

---

## 项目结构
```
userpeofile0701/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/v1/         # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # 数据验证
│   │   └── services/       # 业务逻辑
│   ├── main.py             # 启动文件
│   ├── requirements.txt    # 依赖列表
│   └── clear_db.py         # 数据库清理工具
├── frontend/               # 前端应用
│   ├── lib/
│   │   ├── screens/        # 页面组件
│   │   ├── services/       # API服务
│   │   ├── models/         # 数据模型
│   │   └── utils/          # 工具类
│   ├── main.dart           # 入口文件
│   └── pubspec.yaml        # 依赖配置
├── test_api.py             # API测试脚本
├── README.md               # 项目说明
└── INSTALL.md              # 安装指南
```

---

## 上线准备

### 1. 环境检查
- ✅ 后端API测试全部通过
- ✅ 前端依赖安装完成
- ✅ 数据库连接正常
- ✅ 错误处理机制完善

### 2. 配置调整
- 修改生产环境数据库连接
- 配置JWT密钥
- 设置CORS策略
- 配置日志记录

### 3. 部署建议
- 使用Docker容器化部署
- 配置Nginx反向代理
- 设置SSL证书
- 配置监控和日志

---

## 技术支持

如有问题，请检查：
1. 后端服务是否正常启动
2. MongoDB连接是否正常
3. 前端依赖是否安装完成
4. 网络连接是否正常

更多详细信息请参考 `INSTALL.md` 文件。

---

## 联系方式/致谢
- 作者：Ruilin Zhang & AI助手
- 技术交流/问题反馈：请通过issue或邮箱联系
- 致谢：感谢所有开源依赖和社区支持

---

祝你开发顺利，欢迎Star和反馈建议！ 🚀 