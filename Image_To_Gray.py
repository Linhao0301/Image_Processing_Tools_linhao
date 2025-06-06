import torch
import numpy as np
from PIL import Image
import os

class ImageToGray:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "to_gray"
    CATEGORY = "image"

    def to_gray(self, image):
        # 确保输入是numpy数组
        img = image.cpu().numpy()

        # 获取图片的尺寸
        b, h, w, c = img.shape

        # 创建结果图片
        result = np.zeros((b, h, w, 4), dtype=np.float32)
        
        # 处理每一张图片
        for i in range(b):
            # 转换为灰度图
            if img[i].shape[-1] == 3:
                # 使用标准的RGB到灰度转换权重
                gray = np.dot(img[i, :, :, :3], [0.299, 0.587, 0.114])
                # 将灰度值复制到RGB三个通道
                result[i, :, :, :3] = np.stack([gray] * 3, axis=-1)
                # 设置alpha通道为1
                result[i, :, :, 3] = 1.0
            elif img[i].shape[-1] == 4:
                # 如果输入是RGBA图像，保持alpha通道不变
                gray = np.dot(img[i, :, :, :3], [0.299, 0.587, 0.114])
                result[i, :, :, :3] = np.stack([gray] * 3, axis=-1)
                result[i, :, :, 3] = img[i, :, :, 3]
            else:
                # 如果输入已经是灰度图，直接复制
                result[i] = img[i]

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImageToGray": ImageToGray
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToGray": "Image To Gray(linhao)"
} 