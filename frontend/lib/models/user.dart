class User {
  final String id;
  final String? username;
  final String? email;
  final String? phone;
  final String? nickname;
  final String? avatar;
  final String? gender;
  final String? bio;
  final bool isActive;
  final bool isVerified;
  final bool emailVerified;
  final bool phoneVerified;
  final bool isVip;
  final int vipLevel;
  final String? vipExpireTime;
  final double vipBalance;
  final String? createdAt;
  final String? lastLogin;

  User({
    required this.id,
    this.username,
    this.email,
    this.phone,
    this.nickname,
    this.avatar,
    this.gender,
    this.bio,
    required this.isActive,
    required this.isVerified,
    required this.emailVerified,
    required this.phoneVerified,
    required this.isVip,
    required this.vipLevel,
    this.vipExpireTime,
    required this.vipBalance,
    this.createdAt,
    this.lastLogin,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      username: json['username'] as String?,
      email: json['email'] as String?,
      phone: json['phone'] as String?,
      nickname: json['nickname'] as String?,
      avatar: json['avatar'] as String?,
      gender: json['gender'] as String?,
      bio: json['bio'] as String?,
      isActive: json['is_active'] as bool,
      isVerified: json['is_verified'] as bool,
      emailVerified: json['email_verified'] as bool,
      phoneVerified: json['phone_verified'] as bool,
      isVip: json['is_vip'] as bool,
      vipLevel: json['vip_level'] as int,
      vipExpireTime: json['vip_expire_time'] as String?,
      vipBalance: (json['vip_balance'] as num).toDouble(),
      createdAt: json['created_at'] as String?,
      lastLogin: json['last_login'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'phone': phone,
      'nickname': nickname,
      'avatar': avatar,
      'gender': gender,
      'bio': bio,
      'is_active': isActive,
      'is_verified': isVerified,
      'email_verified': emailVerified,
      'phone_verified': phoneVerified,
      'is_vip': isVip,
      'vip_level': vipLevel,
      'vip_expire_time': vipExpireTime,
      'vip_balance': vipBalance,
      'created_at': createdAt,
      'last_login': lastLogin,
    };
  }

  User copyWith({
    String? id,
    String? username,
    String? email,
    String? phone,
    String? nickname,
    String? avatar,
    String? gender,
    String? bio,
    bool? isActive,
    bool? isVerified,
    bool? emailVerified,
    bool? phoneVerified,
    bool? isVip,
    int? vipLevel,
    String? vipExpireTime,
    double? vipBalance,
    String? createdAt,
    String? lastLogin,
  }) {
    return User(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      nickname: nickname ?? this.nickname,
      avatar: avatar ?? this.avatar,
      gender: gender ?? this.gender,
      bio: bio ?? this.bio,
      isActive: isActive ?? this.isActive,
      isVerified: isVerified ?? this.isVerified,
      emailVerified: emailVerified ?? this.emailVerified,
      phoneVerified: phoneVerified ?? this.phoneVerified,
      isVip: isVip ?? this.isVip,
      vipLevel: vipLevel ?? this.vipLevel,
      vipExpireTime: vipExpireTime ?? this.vipExpireTime,
      vipBalance: vipBalance ?? this.vipBalance,
      createdAt: createdAt ?? this.createdAt,
      lastLogin: lastLogin ?? this.lastLogin,
    );
  }
}

class LoginResponse {
  final String accessToken;
  final String refreshToken;
  final String tokenType;
  final User user;

  LoginResponse({
    required this.accessToken,
    required this.refreshToken,
    required this.tokenType,
    required this.user,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      accessToken: json['access_token'],
      refreshToken: json['refresh_token'],
      tokenType: json['token_type'],
      user: User.fromJson(json['user']),
    );
  }
}

class VIPSubscription {
  final String id;
  final String userId;
  final String planType;
  final double amount;
  final String currency;
  final String status;
  final DateTime startDate;
  final DateTime endDate;
  final String? paymentMethod;
  final String? transactionId;
  final DateTime createdAt;

  VIPSubscription({
    required this.id,
    required this.userId,
    required this.planType,
    required this.amount,
    required this.currency,
    required this.status,
    required this.startDate,
    required this.endDate,
    this.paymentMethod,
    this.transactionId,
    required this.createdAt,
  });

  factory VIPSubscription.fromJson(Map<String, dynamic> json) {
    return VIPSubscription(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      planType: json['plan_type'],
      amount: json['amount']?.toDouble() ?? 0.0,
      currency: json['currency'],
      status: json['status'],
      startDate: DateTime.parse(json['start_date']),
      endDate: DateTime.parse(json['end_date']),
      paymentMethod: json['payment_method'],
      transactionId: json['transaction_id'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
