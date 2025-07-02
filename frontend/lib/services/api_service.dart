import 'dart:io';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const String tokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';

  late Dio _dio;

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
      },
    ));

    // 添加拦截器
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // 添加token到请求头
        final token = await _getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token过期，尝试刷新
          final refreshed = await _refreshToken();
          if (refreshed) {
            // 重新发送请求
            final token = await _getToken();
            error.requestOptions.headers['Authorization'] = 'Bearer $token';
            final response = await _dio.fetch(error.requestOptions);
            handler.resolve(response);
            return;
          }
        }
        handler.next(error);
      },
    ));
  }

  // 获取token
  Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(tokenKey);
  }

  // 保存token
  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(tokenKey, token);
  }

  // 保存刷新token
  Future<void> _saveRefreshToken(String refreshToken) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(refreshTokenKey, refreshToken);
  }

  // 刷新token
  Future<bool> _refreshToken() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final refreshToken = prefs.getString(refreshTokenKey);

      if (refreshToken == null) return false;

      final response = await _dio.post('/auth/refresh', data: {
        'refresh_token': refreshToken,
      });

      if (response.statusCode == 200) {
        await _saveToken(response.data['access_token']);
        return true;
      }
    } catch (e) {
      // print('刷新token失败: $e');
    }
    return false;
  }

  // 清除token
  Future<void> _clearTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(tokenKey);
    await prefs.remove(refreshTokenKey);
  }

  // 用户注册
  Future<LoginResponse> register({
    String? username,
    String? email,
    String? phone,
    String? password,
    String? verificationCode,
    required String loginType,
  }) async {
    final response = await _dio.post('/auth/register', data: {
      'username': username,
      'email': email,
      'phone': phone,
      'password': password,
      'verification_code': verificationCode,
      'login_type': loginType,
    });

    final loginResponse = LoginResponse.fromJson(response.data);
    await _saveToken(loginResponse.accessToken);
    await _saveRefreshToken(loginResponse.refreshToken);

    return loginResponse;
  }

  // 用户登录
  Future<LoginResponse> login({
    String? username,
    String? email,
    String? phone,
    String? password,
    String? verificationCode,
    required String loginType,
  }) async {
    final response = await _dio.post('/auth/login', data: {
      'username': username,
      'email': email,
      'phone': phone,
      'password': password,
      'verification_code': verificationCode,
      'login_type': loginType,
    });

    final loginResponse = LoginResponse.fromJson(response.data);
    await _saveToken(loginResponse.accessToken);
    await _saveRefreshToken(loginResponse.refreshToken);

    return loginResponse;
  }

  // 微信登录
  Future<LoginResponse> wechatLogin(
      {required String code, String? state}) async {
    final response = await _dio.post('/auth/wechat/login', data: {
      'code': code,
      'state': state,
    });

    final loginResponse = LoginResponse.fromJson(response.data);
    await _saveToken(loginResponse.accessToken);
    await _saveRefreshToken(loginResponse.refreshToken);

    return loginResponse;
  }

  // 发送验证码
  Future<Map<String, dynamic>> sendVerificationCode({
    String? phone,
    String? email,
    required String type,
  }) async {
    final response = await _dio.post('/auth/verification-code', data: {
      'phone': phone,
      'email': email,
      'type': type,
    });

    return response.data;
  }

  // 获取用户信息
  Future<User> getUserProfile() async {
    final response = await _dio.get('/users/profile');
    return User.fromJson(response.data);
  }

  // 更新用户资料
  Future<User> updateUserProfile({
    String? nickname,
    String? avatar,
    String? gender,
    DateTime? birthday,
    String? bio,
  }) async {
    final response = await _dio.put('/users/profile', data: {
      'nickname': nickname,
      'avatar': avatar,
      'gender': gender,
      'birthday': birthday?.toIso8601String(),
      'bio': bio,
    });

    return User.fromJson(response.data);
  }

  // 修改密码
  Future<Map<String, dynamic>> changePassword({
    required String oldPassword,
    required String newPassword,
  }) async {
    final response = await _dio.post('/users/change-password', data: {
      'old_password': oldPassword,
      'new_password': newPassword,
    });

    return response.data;
  }

  // 绑定手机号或邮箱
  Future<Map<String, dynamic>> bindPhoneOrEmail({
    String? phone,
    String? email,
    required String verificationCode,
  }) async {
    final response = await _dio.post('/users/bind', data: {
      'phone': phone,
      'email': email,
      'verification_code': verificationCode,
    });

    return response.data;
  }

  // 上传头像
  Future<Map<String, dynamic>> uploadAvatar(File file) async {
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(file.path),
    });

    final response = await _dio.post('/users/upload-avatar', data: formData);
    return response.data;
  }

  // 获取VIP信息
  Future<Map<String, dynamic>> getVipInfo() async {
    final response = await _dio.get('/users/vip/info');
    return response.data;
  }

  // 创建VIP订阅
  Future<VIPSubscription> createVipSubscription({
    required String planType,
    required double amount,
    String currency = 'CNY',
    String? paymentMethod,
  }) async {
    final response = await _dio.post('/users/vip/subscribe', data: {
      'plan_type': planType,
      'amount': amount,
      'currency': currency,
      'payment_method': paymentMethod,
    });

    return VIPSubscription.fromJson(response.data);
  }

  // 获取用户订阅历史
  Future<List<VIPSubscription>> getUserSubscriptions() async {
    final response = await _dio.get('/users/vip/subscriptions');
    return (response.data as List)
        .map((json) => VIPSubscription.fromJson(json))
        .toList();
  }

  // 取消VIP订阅
  Future<Map<String, dynamic>> cancelVipSubscription(int subscriptionId) async {
    final response = await _dio.post('/users/vip/cancel/$subscriptionId');
    return response.data;
  }

  // 用户登出
  Future<Map<String, dynamic>> logout() async {
    final prefs = await SharedPreferences.getInstance();
    final refreshToken = prefs.getString(refreshTokenKey);

    if (refreshToken != null) {
      await _dio.post('/auth/logout', data: {
        'refresh_token': refreshToken,
      });
    }

    await _clearTokens();
    return {'message': '登出成功'};
  }

  // 检查是否已登录
  Future<bool> isLoggedIn() async {
    final token = await _getToken();
    return token != null;
  }
}
