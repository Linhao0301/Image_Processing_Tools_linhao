import torch
import numpy as np
import cv2

class ImageConvertToRGB:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "convert_to_rgb"
    CATEGORY = "image"

    def convert_to_rgb(self, image):
        # 转换为numpy数组
        img = image.cpu().numpy()
        
        # 获取图片的尺寸和通道数
        b, h, w, c = img.shape
        
        # 创建结果数组
        result = np.zeros((b, h, w, 3), dtype=np.float32)
        
        # 处理每一张图片
        for i in range(b):
            # 分离RGB和Alpha通道（如果有的话）
            if c == 4:
                # 直接使用RGB通道，忽略Alpha通道
                result[i] = img[i, :, :, :3]
            else:
                # 如果不是4通道图片，直接复制RGB通道
                result[i] = img[i, :, :, :3]

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImageConvertToRGB": ImageConvertToRGB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageConvertToRGB": "Image Convert To RGB(linhao)"
} 