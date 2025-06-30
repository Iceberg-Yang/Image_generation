import gradio as gr
import stability_sdk.client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import os
from dotenv import load_dotenv
import io
from PIL import Image
import warnings

# 加载环境变量
load_dotenv()

# 15个固定选项
OPTION_CATEGORIES = {
    "风格类": ["写实风格", "卡通风格", "水彩画风格", "油画风格", "像素艺术风格"],
    "主题类": ["自然风景", "城市建筑", "人物肖像", "动物世界", "科幻场景"],
    "色彩类": ["暖色调", "冷色调", "黑白色调", "彩虹色彩", "夜晚色调"]
}

# 将所有选项平铺为列表
ALL_OPTIONS = []
for category, options in OPTION_CATEGORIES.items():
    ALL_OPTIONS.extend(options)

class StabilityImageGenerator:
    def __init__(self):
        self.stability_api = None
        self.initialize_api()
    
    def initialize_api(self):
        """初始化 Stability AI API"""
        api_key = os.getenv('STABILITY_KEY')
        if not api_key:
            print("警告: 未找到 STABILITY_KEY 环境变量")
            return
        
        try:
            self.stability_api = stability_sdk.client.StabilityInference(
                key=api_key,
                verbose=True,
                engine="stable-diffusion-xl-1024-v1-0"
            )
            print("Stability AI API 初始化成功")
        except Exception as e:
            print(f"Stability AI API 初始化失败: {e}")
    
    def generate_image(self, selected_options):
        """根据选中的选项生成图片"""
        if not self.stability_api:
            return "错误: Stability AI API 未正确初始化，请检查您的 API 密钥"
        
        if len(selected_options) != 3:
            return "请确保选择了恰好3个选项"
        
        # 构建 prompt
        prompt = self.build_prompt(selected_options)
        print(f"生成的 prompt: {prompt}")
        
        try:
            # 调用 Stability AI API 生成图片
            answers = self.stability_api.generate(
                prompt=prompt,
                seed=992446758,  # 可以设为随机数
                steps=30,
                cfg_scale=8.0,
                width=1024,
                height=1024,
                samples=1,
                sampler=generation.SAMPLER_K_DPMPP_2M
            )
            
            # 处理返回的图片
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "您的请求激活了API的安全过滤器，请调整您的prompt后重试。"
                        )
                        return "内容被安全过滤器拦截，请尝试其他选项组合"
                    
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                        return img
            
            return "生成失败，请重试"
            
        except Exception as e:
            error_msg = f"图片生成过程中出现错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def build_prompt(self, selected_options):
        """根据选中的选项构建英文 prompt"""
        # 中文到英文的映射
        translation_map = {
            "写实风格": "realistic style",
            "卡通风格": "cartoon style",
            "水彩画风格": "watercolor painting style",
            "油画风格": "oil painting style",
            "像素艺术风格": "pixel art style",
            "自然风景": "natural landscape",
            "城市建筑": "urban architecture",
            "人物肖像": "portrait",
            "动物世界": "wildlife",
            "科幻场景": "sci-fi scene",
            "暖色调": "warm color palette",
            "冷色调": "cool color palette",
            "黑白色调": "black and white",
            "彩虹色彩": "rainbow colors",
            "夜晚色调": "night time atmosphere"
        }
        
        # 转换为英文并构建 prompt
        english_terms = [translation_map.get(option, option) or option for option in selected_options]
        prompt = ", ".join(english_terms) + ", high quality, detailed, masterpiece"
        
        return prompt

# 初始化图片生成器
generator = StabilityImageGenerator()

def generate_image_interface(opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12, opt13, opt14, opt15):
    """Gradio 界面函数"""
    # 收集所有选中的选项
    selected_options = []
    checkbox_values = [opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12, opt13, opt14, opt15]
    
    for i, is_selected in enumerate(checkbox_values):
        if is_selected:
            selected_options.append(ALL_OPTIONS[i])
    
    if len(selected_options) != 3:
        return f"请选择恰好3个选项 (当前已选择: {len(selected_options)}个)"
    
    # 生成图片
    result = generator.generate_image(selected_options)
    return result

# 赛博朋克风格CSS
CYBERPUNK_CSS = """
/* 全局样式 */
.gradio-container {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #000011 100%) !important;
    color: #00ffff !important;
    font-family: 'Courier New', monospace !important;
}

/* 主标题样式 */
.main-header {
    background: linear-gradient(90deg, #ff00ff, #00ffff, #ff00ff) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-size: 2.5em !important;
    font-weight: bold !important;
    text-shadow: 0 0 20px #00ffff !important;
    margin-bottom: 20px !important;
}

/* 左侧面板样式 */
.left-panel {
    background: rgba(0, 20, 40, 0.8) !important;
    border: 2px solid #00ffff !important;
    border-radius: 10px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important;
}

/* 右侧面板样式 */
.right-panel {
    background: rgba(20, 0, 40, 0.8) !important;
    border: 2px solid #ff00ff !important;
    border-radius: 10px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.3) !important;
}

/* 使用说明区域 */
.instructions-panel {
    background: rgba(0, 40, 20, 0.8) !important;
    border: 2px solid #00ff00 !important;
    border-radius: 10px !important;
    padding: 15px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.3) !important;
}

/* 生成结果区域 */
.result-panel {
    background: rgba(40, 0, 20, 0.8) !important;
    border: 2px solid #ffff00 !important;
    border-radius: 10px !important;
    padding: 15px !important;
    box-shadow: 0 0 15px rgba(255, 255, 0, 0.3) !important;
}

/* 复选框样式 */
.checkbox-item {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid #00ffff !important;
    border-radius: 5px !important;
    margin: 5px 0 !important;
    padding: 8px !important;
    transition: all 0.3s ease !important;
}

.checkbox-item:hover {
    background: rgba(0, 255, 255, 0.1) !important;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
}

/* 按钮样式 */
.generate-btn {
    background: linear-gradient(45deg, #ff00ff, #00ffff) !important;
    border: none !important;
    color: #000 !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    padding: 15px 30px !important;
    border-radius: 10px !important;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.6) !important;
    transition: all 0.3s ease !important;
}

.generate-btn:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.8) !important;
}

/* 分类标题样式 */
.category-title {
    color: #ffff00 !important;
    font-size: 1.2em !important;
    font-weight: bold !important;
    text-shadow: 0 0 10px #ffff00 !important;
    margin: 15px 0 10px 0 !important;
}

/* 文本样式 */
.cyber-text {
    color: #00ffff !important;
    text-shadow: 0 0 5px #00ffff !important;
}

.warning-text {
    color: #ff6600 !important;
    text-shadow: 0 0 5px #ff6600 !important;
}

/* 图片区域样式 */
.image-container {
    border: 2px solid #ffff00 !important;
    border-radius: 10px !important;
    background: rgba(0, 0, 0, 0.7) !important;
    box-shadow: 0 0 20px rgba(255, 255, 0, 0.4) !important;
}
"""

# 创建 Gradio 界面
def create_interface():
    with gr.Blocks(
        title="🌐 CYBER AI 文生图实验室", 
        theme=gr.themes.Base().set(
            body_background_fill="*neutral_950",
            body_text_color="*cyan_500",
            button_primary_background_fill="*pink_500",
            button_primary_text_color="*neutral_50"
        ),
        css=CYBERPUNK_CSS
    ) as interface:
        
        # 主标题
        gr.HTML("""
            <div class="main-header">
                ⚡ CYBER AI 文生图实验室 ⚡
            </div>
            <div style="text-align: center; color: #00ffff; font-size: 1.2em; margin-bottom: 30px; text-shadow: 0 0 10px #00ffff;">
                >> 神经网络驱动的数字艺术创造系统 <<
            </div>
        """)
        
        with gr.Row():
            # 左侧：创作元素选择面板
            with gr.Column(scale=1, elem_classes=["left-panel"]):
                gr.HTML("""
                    <div style="color: #ff00ff; font-size: 1.5em; font-weight: bold; text-align: center; 
                                text-shadow: 0 0 15px #ff00ff; margin-bottom: 20px;">
                        🎮 创作元素矩阵
                    </div>
                    <div style="color: #00ffff; text-align: center; margin-bottom: 20px; text-shadow: 0 0 5px #00ffff;">
                        >> 选择恰好 3 个元素激活生成协议 <<
                    </div>
                """)
                
                # 创建15个复选框
                checkboxes = []
                for i, option in enumerate(ALL_OPTIONS):
                    # 添加分类标题
                    if i == 0:
                        gr.HTML('<div class="category-title">🎨 风格代码矩阵</div>')
                    elif i == 5:
                        gr.HTML('<div class="category-title">🌆 主题数据库</div>')
                    elif i == 10:
                        gr.HTML('<div class="category-title">🌈 色彩光谱</div>')
                    
                    checkbox = gr.Checkbox(
                        label=f"[{i+1:02d}] {option}", 
                        value=False,
                        elem_classes=["checkbox-item"]
                    )
                    checkboxes.append(checkbox)
                
                # 生成按钮
                generate_btn = gr.Button(
                    "⚡ 启动生成序列 ⚡", 
                    variant="primary", 
                    size="lg",
                    elem_classes=["generate-btn"]
                )
                
                # 系统提示
                gr.HTML("""
                    <div style="margin-top: 20px; padding: 15px; background: rgba(0, 0, 0, 0.6); 
                                border: 1px solid #00ff00; border-radius: 10px;">
                        <div style="color: #00ff00; font-weight: bold; text-shadow: 0 0 5px #00ff00; margin-bottom: 10px;">
                            💡 系统提示
                        </div>
                        <div style="color: #00ffff; font-size: 0.9em; line-height: 1.5;">
                            • 风格代码：定义输出的视觉渲染模式<br>
                            • 主题数据：确定生成内容的核心对象<br>
                            • 色彩光谱：控制像素的色彩映射算法<br><br>
                            <span style="color: #ffff00;">建议：从三个不同矩阵中各选择一个元素以获得最佳生成效果</span>
                        </div>
                    </div>
                """)
            
            # 右侧：使用说明和生成结果
            with gr.Column(scale=2, elem_classes=["right-panel"]):
                # 上半部分：使用说明
                with gr.Column(elem_classes=["instructions-panel"]):
                    gr.HTML("""
                        <div style="color: #00ff00; font-size: 1.4em; font-weight: bold; text-align: center; 
                                    text-shadow: 0 0 15px #00ff00; margin-bottom: 15px;">
                            📡 操作协议
                        </div>
                    """)
                    
                    gr.HTML("""
                        <div style="color: #00ffff; line-height: 2; font-size: 1.1em;">
                            <div style="margin-bottom: 15px;">
                                <span style="color: #ff00ff; font-weight: bold;">STEP 01:</span> 
                                从左侧元素矩阵中选择恰好 <span style="color: #ffff00; font-weight: bold;">3个元素</span>
                            </div>
                            <div style="margin-bottom: 15px;">
                                <span style="color: #ff00ff; font-weight: bold;">STEP 02:</span> 
                                点击 <span style="color: #ffff00; font-weight: bold;">"启动生成序列"</span> 按钮
                            </div>
                            <div style="margin-bottom: 15px;">
                                <span style="color: #ff00ff; font-weight: bold;">STEP 03:</span> 
                                等待神经网络处理 <span style="color: #ffff00; font-weight: bold;">(10-30秒)</span>
                            </div>
                            <div style="margin-bottom: 15px;">
                                <span style="color: #ff00ff; font-weight: bold;">STEP 04:</span> 
                                获取独特的数字艺术创作
                            </div>
                        </div>
                    """)
                    
                    gr.HTML("""
                        <div style="margin-top: 15px; padding: 10px; background: rgba(255, 102, 0, 0.1); 
                                    border: 1px solid #ff6600; border-radius: 5px;">
                            <div style="color: #ff6600; font-weight: bold; text-shadow: 0 0 5px #ff6600;">
                                ⚠️ 系统警告
                            </div>
                            <div style="color: #ffff00; font-size: 0.9em; margin-top: 5px;">
                                某些元素组合可能触发内容过滤协议，请尝试不同的组合方式
                            </div>
                        </div>
                    """)
                
                # 下半部分：生成结果
                with gr.Column(elem_classes=["result-panel"]):
                    gr.HTML("""
                        <div style="color: #ffff00; font-size: 1.4em; font-weight: bold; text-align: center; 
                                    text-shadow: 0 0 15px #ffff00; margin-bottom: 15px;">
                            🖼️ 生成结果输出
                        </div>
                    """)
                    
                    output_image = gr.Image(
                        label="", 
                        height=500,
                        elem_classes=["image-container"]
                    )
                    
                    gr.HTML("""
                        <div style="text-align: center; margin-top: 15px; color: #00ffff; font-size: 0.9em; 
                                    text-shadow: 0 0 5px #00ffff;">
                            >> 每个生成的作品都是独一无二的数字艺术品 <<
                        </div>
                    """)
        
        # 绑定生成函数
        generate_btn.click(
            fn=generate_image_interface,
            inputs=checkboxes,
            outputs=output_image
        )
    
    return interface

if __name__ == "__main__":
    # 检查环境变量
    if not os.getenv('STABILITY_KEY'):
        print("⚠️  警告: 未找到 STABILITY_KEY 环境变量")
        print("请在 .env 文件中设置您的 Stability AI API 密钥")
        print("或运行: export STABILITY_KEY='your-api-key-here'")
    
    # 启动应用
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        debug=True
    ) 