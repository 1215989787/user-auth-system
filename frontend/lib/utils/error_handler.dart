import 'package:dio/dio.dart';

class ErrorHandler {
  /// 解析API错误信息
  static String parseApiError(dynamic error) {
    if (error is DioException) {
      final data = error.response?.data;
      if (data != null && data['detail'] != null) {
        if (data['detail'] is Map && data['detail']['msg'] != null) {
          return data['detail']['msg'];
        } else if (data['detail'] is String) {
          return data['detail'];
        }
      }

      // 根据状态码返回友好提示
      switch (error.response?.statusCode) {
        case 400:
          return '请求参数错误';
        case 401:
          return '未授权，请重新登录';
        case 403:
          return '权限不足';
        case 404:
          return '请求的资源不存在';
        case 409:
          return '数据冲突';
        case 500:
          return '服务器内部错误';
        default:
          return '网络请求失败，请检查网络连接';
      }
    }

    return error.toString();
  }

  /// 获取错误类型
  static String getErrorType(dynamic error) {
    if (error is DioException) {
      final data = error.response?.data;
      if (data != null && data['detail'] != null && data['detail'] is Map) {
        return data['detail']['code'] ?? 'UNKNOWN_ERROR';
      }
    }
    return 'UNKNOWN_ERROR';
  }
}
