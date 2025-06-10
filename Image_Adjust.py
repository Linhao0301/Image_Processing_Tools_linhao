import torch
import numpy as np
import cv2

class ImageAdjust:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness": ("FLOAT", {
                    "default": 0.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "gamma": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust_image"
    CATEGORY = "image"

    def adjust_image(self, image, brightness, contrast, gamma):
        # 转换为numpy数组
        img = image.cpu().numpy()
        
        # 获取图片的尺寸和通道数
        b, h, w, c = img.shape
        
        # 创建结果数组
        result = np.zeros_like(img)
        
        # 处理每一张图片
        for i in range(b):
            # 分离RGB和Alpha通道（如果有的话）
            if c == 4:
                rgb = img[i, :, :, :3]
                alpha = img[i, :, :, 3:4]
            else:
                rgb = img[i]
                alpha = None
            
            # 将图像转换为uint8格式进行处理
            rgb_uint8 = (rgb * 255).astype(np.uint8)
            
            # 应用亮度调整
            if brightness != 0:
                rgb_uint8 = cv2.add(rgb_uint8, int(brightness * 255))
            
            # 应用对比度调整
            if contrast != 1.0:
                rgb_uint8 = cv2.convertScaleAbs(rgb_uint8, alpha=contrast, beta=0)
            
            # 应用伽马校正
            if gamma != 1.0:
                # 创建查找表
                lookup_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
                                       for i in np.arange(0, 256)]).astype("uint8")
                # 应用查找表
                rgb_uint8 = cv2.LUT(rgb_uint8, lookup_table)
            
            # 转回float32格式
            rgb_float = rgb_uint8.astype(np.float32) / 255.0
            
            # 重新组合通道
            if c == 4:
                result[i, :, :, :3] = rgb_float
                result[i, :, :, 3:4] = alpha
            else:
                result[i] = rgb_float

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImageAdjust": ImageAdjust
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageAdjust": "Image Adjust(linhao)"
} 