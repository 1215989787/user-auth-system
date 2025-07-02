#!/usr/bin/env python3
"""
用户认证系统API测试脚本
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print("❌ 健康检查失败")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_register():
    """测试用户注册"""
    print("\n🔍 测试用户注册...")
    
    # 测试密码注册
    register_data = {
        "username": "testuser",
        "password": "123456",
        "login_type": "password"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            print("✅ 密码注册成功")
            return response.json()
        else:
            print(f"❌ 密码注册失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 注册异常: {e}")
        return None

def test_login():
    """测试用户登录"""
    print("\n🔍 测试用户登录...")
    
    login_data = {
        "username": "testuser",
        "password": "123456",
        "login_type": "password"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ 密码登录成功")
            return response.json()
        else:
            print(f"❌ 密码登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return None

def test_send_verification_code():
    """测试发送验证码"""
    print("\n🔍 测试发送验证码...")
    
    code_data = {
        "phone": "13800138000",
        "type": "login"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/verification-code", json=code_data)
        if response.status_code == 200:
            print("✅ 验证码发送成功")
            return response.json()
        else:
            print(f"❌ 验证码发送失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 验证码发送异常: {e}")
        return None

def test_user_profile(access_token):
    """测试获取用户资料"""
    print("\n🔍 测试获取用户资料...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("✅ 获取用户资料成功")
            return response.json()
        else:
            print(f"❌ 获取用户资料失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 获取用户资料异常: {e}")
        return None

def test_vip_info(access_token):
    """测试获取VIP信息"""
    print("\n🔍 测试获取VIP信息...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/vip/info", headers=headers)
        if response.status_code == 200:
            print("✅ 获取VIP信息成功")
            return response.json()
        else:
            print(f"❌ 获取VIP信息失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 获取VIP信息异常: {e}")
        return None

def test_logout(refresh_token):
    """测试用户登出"""
    print("\n🔍 测试用户登出...")
    
    logout_data = {"refresh_token": refresh_token}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/logout", json=logout_data)
        if response.status_code == 200:
            print("✅ 用户登出成功")
            return True
        else:
            print(f"❌ 用户登出失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 用户登出异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试用户认证系统API")
    print("=" * 50)
    
    # 1. 健康检查
    if not test_health_check():
        print("❌ 后端服务未启动，请先启动后端服务")
        return
    
    # 2. 测试注册
    register_result = test_register()
    if not register_result:
        print("⚠️  注册失败，可能用户已存在，继续测试登录")
    
    # 3. 测试登录
    login_result = test_login()
    if not login_result:
        print("❌ 登录失败，无法继续测试")
        return
    
    access_token = login_result["access_token"]
    refresh_token = login_result["refresh_token"]
    
    # 4. 测试发送验证码
    test_send_verification_code()
    
    # 5. 测试获取用户资料
    test_user_profile(access_token)
    
    # 6. 测试获取VIP信息
    test_vip_info(access_token)
    
    # 7. 测试登出
    test_logout(refresh_token)
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成！")
    print("\n📖 更多API文档请访问: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 