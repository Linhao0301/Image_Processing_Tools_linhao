import torch
import numpy as np
import requests
import json
import base64
from io import BytesIO
from PIL import Image

class ImageOpenRouterVision:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {
                    "default": "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",  # 请替换为您的API密钥
                    "multiline": False
                }),
                "model": ("STRING", {
                    "default": "google/gemini-2.5-flash-preview-05-20",
                    "multiline": False
                }),
                "user_prompt": ("STRING", {
                    "default": "Describe only the character's ethnicity (you must indicate the character's ethnicity; if you can't tell, just output 'white female'), skin color, features, makeup, face shape, and other appearance details. It is strictly forbidden to describe the background, dress code, or any other content.",
                    "multiline": True
                }),
                "system_prompt": ("STRING", {
                    "default": "You are a professional image analysis assistant.",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "analyze_image"
    CATEGORY = "image"

    def analyze_image(self, image, api_key, model, user_prompt, system_prompt):
        # 将图像转换为PIL Image
        img = image[0].cpu().numpy()  # 获取第一张图片
        img = (img * 255).astype(np.uint8)
        pil_image = Image.fromarray(img)
        
        # 将图像转换为base64
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # 准备API请求
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_str}"
                            }
                        }
                    ]
                }
            ]
        }

        # 发送请求到OpenRouter API
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            # 检查HTTP状态码
            if response.status_code != 200:
                error_msg = f"API请求失败 (状态码: {response.status_code})"
                try:
                    error_detail = response.json()
                    if 'error' in error_detail:
                        error_msg += f"\n错误信息: {error_detail['error']}"
                except:
                    error_msg += f"\n响应内容: {response.text}"
                raise Exception(error_msg)
            
            result = response.json()
            
            # 检查API响应格式
            if 'choices' not in result or not result['choices']:
                raise Exception("API响应格式错误：未找到choices字段")
            
            if 'message' not in result['choices'][0]:
                raise Exception("API响应格式错误：未找到message字段")
            
            if 'content' not in result['choices'][0]['message']:
                raise Exception("API响应格式错误：未找到content字段")
            
            return (result["choices"][0]["message"]["content"],)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求错误: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析错误: {str(e)}")
        except Exception as e:
            raise Exception(f"处理错误: {str(e)}")

NODE_CLASS_MAPPINGS = {
    "ImageOpenRouterVision": ImageOpenRouterVision
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOpenRouterVision": "Image Described by LLM(linhao)"
} 