import torch
import numpy as np
import cv2

class ImageGaussianBlur:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "kernel_size": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 31,
                    "step": 2
                }),
                "sigma_x": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "gaussian_blur"
    CATEGORY = "image"

    def gaussian_blur(self, image, kernel_size, sigma_x):
        # 确保kernel_size是奇数
        if kernel_size % 2 == 0:
            kernel_size += 1

        # 转换为numpy数组
        img = image.cpu().numpy()
        
        # 获取图片的尺寸
        b, h, w, c = img.shape

        # 创建结果数组
        result = np.zeros_like(img)
        
        # 处理每一张图片
        for i in range(b):
            # 将图像转换为uint8格式
            img_uint8 = (img[i] * 255).astype(np.uint8)
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(img_uint8, (kernel_size, kernel_size), sigma_x)
            
            # 转回float32格式
            result[i] = blurred.astype(np.float32) / 255.0

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImageGaussianBlur": ImageGaussianBlur
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageGaussianBlur": "Image Gaussian Blur(linhao)"
} 