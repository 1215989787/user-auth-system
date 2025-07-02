# 用户认证系统 - Flutter前端

## 项目简介

这是一个基于Flutter开发的多功能用户认证系统前端，支持多种登录方式：

- 账号密码登录
- 手机号验证码登录  
- 微信跳转登录
- 生物识别解锁（面容ID/TouchID）

## 功能特性

- 🎨 现代化UI设计，支持深色/浅色主题
- 🔐 多种安全登录方式
- 📱 响应式设计，支持移动端和Web端
- 🔒 生物识别认证
- 👤 个人资料管理
- 💎 VIP会员管理
- 🖼️ 头像上传功能

## 技术栈

- **框架**: Flutter 3.x
- **状态管理**: Provider
- **网络请求**: HTTP
- **本地存储**: SharedPreferences
- **数据库**: SQLite
- **生物识别**: local_auth
- **图片选择**: image_picker
- **微信登录**: fluwx

## 快速开始

### 环境要求

- Flutter 3.x
- Dart 3.x
- Android Studio / VS Code
- Chrome浏览器（Web端）

### 安装依赖

```bash
flutter pub get
```

### 运行应用

#### Web端（推荐）
```bash
flutter run -d chrome --web-port 3000
```

#### iOS模拟器
```bash
flutter run -d ios
```

#### Android模拟器
```bash
flutter run -d android
```

### 访问应用

- **Web端**: http://localhost:3000
- **移动端**: 应用会自动在模拟器中打开

## 项目结构

```
lib/
├── main.dart              # 应用入口
├── models/
│   └── user.dart          # 用户模型
├── screens/
│   └── login_screen.dart  # 登录页面
└── services/
    ├── api_service.dart   # API服务
    └── auth_service.dart  # 认证服务
```

## 后端API

确保后端服务在 http://localhost:8000 运行，提供以下API端点：

- `POST /api/v1/auth/login` - 密码登录
- `POST /api/v1/auth/sms-login` - 短信登录
- `POST /api/v1/auth/wechat-login` - 微信登录
- `GET /api/v1/users/profile` - 获取用户资料
- `PUT /api/v1/users/profile` - 更新用户资料

## 开发说明

### 添加新页面

1. 在 `lib/screens/` 目录下创建新的页面文件
2. 在 `lib/main.dart` 中添加路由配置
3. 更新导航逻辑

### 修改样式

- 主题配置在 `lib/main.dart` 中的 `MaterialApp` 部分
- 颜色和字体在 `lib/theme/` 目录下配置

### 添加新功能

1. 在 `lib/services/` 中添加相应的服务类
2. 在 `lib/models/` 中添加数据模型
3. 在对应的页面中集成新功能

## 部署

### Web端部署

```bash
flutter build web
```

构建完成后，将 `build/web` 目录部署到Web服务器。

### 移动端打包

#### Android
```bash
flutter build apk --release
```

#### iOS
```bash
flutter build ios --release
```

## 常见问题

### 1. 端口被占用
如果3000端口被占用，可以使用其他端口：
```bash
flutter run -d chrome --web-port 3001
```

### 2. 依赖安装失败
清理缓存后重新安装：
```bash
flutter clean
flutter pub get
```

### 3. 后端连接失败
确保后端服务正在运行：
```bash
cd ../backend
python main.py
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
