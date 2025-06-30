#!/usr/bin/env python3
"""
AI 文生图应用 - 设置和启动脚本
用于快速设置环境和启动应用
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖是否已安装"""
    required_packages = ['gradio', 'stability_sdk', 'dotenv', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'dotenv':
                __import__('dotenv')
            elif package == 'stability_sdk':
                __import__('stability_sdk')
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 依赖包安装完成！")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败！")
        return False

def create_env_file():
    """创建环境变量文件"""
    env_example_content = """# Stability AI API 密钥
# 在 https://platform.stability.ai/account/keys 获取您的API密钥
STABILITY_KEY=your_stability_ai_api_key_here"""
    
    # 创建 .env.example 文件
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_example_content)
        print("✅ 已创建 .env.example 文件")
    
    # 检查 .env 文件
    if not os.path.exists('.env'):
        print("\n🔑 需要配置API密钥！")
        print("请按照以下步骤操作：")
        print("1. 访问 https://platform.stability.ai/account/keys 获取API密钥")
        print("2. 复制 .env.example 文件并重命名为 .env")
        print("3. 在 .env 文件中填入您的实际API密钥")
        
        # 复制 .env.example 到 .env
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_example_content)
        
        print("\n📝 已为您创建 .env 文件模板")
        print("⚠️  请记得将 'your_stability_ai_api_key_here' 替换为您的实际API密钥！")
        
        return False
    
    return True

def main():
    print("🎨 AI 文生图应用 - 设置向导")
    print("=" * 50)
    
    # 检查依赖
    print("🔍 检查依赖包...")
    missing = check_dependencies()
    
    if missing:
        print(f"❌ 缺少以下依赖包: {', '.join(missing)}")
        install_choice = input("是否立即安装依赖包？(y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes', '是']:
            if not install_dependencies():
                print("❌ 安装失败，请手动运行: pip install -r requirements.txt")
                return
        else:
            print("❌ 请手动安装依赖包: pip install -r requirements.txt")
            return
    else:
        print("✅ 所有依赖包已安装")
    
    # 创建环境变量文件
    print("\n🔑 检查环境配置...")
    env_ready = create_env_file()
    
    if not env_ready:
        print("\n⏳ 请配置好API密钥后重新运行此脚本")
        return
    
    # 检查API密钥是否已配置
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('STABILITY_KEY')
    if not api_key or api_key == 'your_stability_ai_api_key_here':
        print("⚠️  API密钥尚未配置，应用可能无法正常工作")
        print("请在 .env 文件中设置正确的 STABILITY_KEY")
    else:
        print("✅ API密钥已配置")
    
    # 启动应用
    print("\n🚀 准备启动应用...")
    launch_choice = input("是否立即启动应用？(y/n): ").lower().strip()
    
    if launch_choice in ['y', 'yes', '是']:
        print("🌟 正在启动 AI 文生图应用...")
        print("📱 应用将在 http://localhost:7860 启动")
        print("按 Ctrl+C 停止应用")
        print("-" * 50)
        
        try:
            from main import create_interface
            interface = create_interface()
            interface.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                debug=True
            )
        except KeyboardInterrupt:
            print("\n👋 应用已停止")
        except Exception as e:
            print(f"❌ 启动失败: {e}")
    else:
        print("📝 配置完成！您可以手动运行 'python main.py' 启动应用")

if __name__ == "__main__":
    main() 