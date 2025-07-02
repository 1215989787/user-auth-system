import 'package:local_auth/local_auth.dart';
import 'package:fluwx/fluwx.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';
import '../models/user.dart';

class AuthService {
  final ApiService _apiService = ApiService();
  final LocalAuthentication _localAuth = LocalAuthentication();

  // 生物识别相关
  Future<bool> isBiometricAvailable() async {
    try {
      final isAvailable = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      return isAvailable && isDeviceSupported;
    } catch (e) {
      return false;
    }
  }

  Future<List<BiometricType>> getAvailableBiometrics() async {
    try {
      return await _localAuth.getAvailableBiometrics();
    } catch (e) {
      return [];
    }
  }

  Future<bool> authenticateWithBiometrics() async {
    try {
      return await _localAuth.authenticate(
        localizedReason: '请使用生物识别解锁应用',
        options: const AuthenticationOptions(
          biometricOnly: true,
          stickyAuth: true,
        ),
      );
    } catch (e) {
      return false;
    }
  }

  // 微信登录相关
  Future<void> initWechat() async {
    // TODO: 实现微信API初始化
    // await registerWxApi(
    //   appId: "your_wechat_app_id", // 需要替换为实际的微信AppID
    //   doOnAndroid: true,
    //   doOnIOS: true,
    // );
  }

  Future<String?> getWechatAuthCode() async {
    try {
      // TODO: 实现微信授权
      // final result = await sendWeChatAuth(
      //   scope: "snsapi_userinfo",
      //   state: "wechat_auth",
      // );

      // if (result.errCode == 0) {
      //   return result.code;
      // }
      return null;
    } catch (e) {
      return null;
    }
  }

  // 验证码相关
  Future<bool> sendSmsCode(String phone, String type) async {
    try {
      final result = await _apiService.sendVerificationCode(
        phone: phone,
        type: type,
      );
      return result['message'] != null;
    } catch (e) {
      return false;
    }
  }

  Future<bool> sendEmailCode(String email, String type) async {
    try {
      final result = await _apiService.sendVerificationCode(
        email: email,
        type: type,
      );
      return result['message'] != null;
    } catch (e) {
      return false;
    }
  }

  // 用户注册
  Future<LoginResponse?> registerWithPassword({
    required String username,
    required String password,
  }) async {
    try {
      return await _apiService.register(
        username: username,
        password: password,
        loginType: 'password',
      );
    } catch (e) {
      return null;
    }
  }

  Future<LoginResponse?> registerWithSms({
    required String phone,
    required String verificationCode,
  }) async {
    try {
      return await _apiService.register(
        phone: phone,
        verificationCode: verificationCode,
        loginType: 'sms',
      );
    } catch (e) {
      return null;
    }
  }

  // 用户登录
  Future<LoginResponse?> loginWithPassword({
    required String username,
    required String password,
  }) async {
    try {
      return await _apiService.login(
        username: username,
        password: password,
        loginType: 'password',
      );
    } catch (e) {
      return null;
    }
  }

  Future<LoginResponse?> loginWithSms({
    required String phone,
    required String verificationCode,
  }) async {
    try {
      return await _apiService.login(
        phone: phone,
        verificationCode: verificationCode,
        loginType: 'sms',
      );
    } catch (e) {
      return null;
    }
  }

  Future<LoginResponse?> loginWithWechat() async {
    try {
      final code = await getWechatAuthCode();
      if (code != null) {
        return await _apiService.wechatLogin(code: code);
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  // 用户登出
  Future<bool> logout() async {
    try {
      await _apiService.logout();
      return true;
    } catch (e) {
      return false;
    }
  }

  // 检查登录状态
  Future<bool> isLoggedIn() async {
    return await _apiService.isLoggedIn();
  }

  // 获取当前用户信息
  Future<User?> getCurrentUser() async {
    try {
      return await _apiService.getUserProfile();
    } catch (e) {
      return null;
    }
  }

  // 保存生物识别设置
  Future<void> saveBiometricEnabled(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('biometric_enabled', enabled);
  }

  // 获取生物识别设置
  Future<bool> isBiometricEnabled() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('biometric_enabled') ?? false;
  }
}
