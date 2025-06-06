import torch
import numpy as np
from PIL import Image
import os

class ImagePaste:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "overlay_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "paste_images"
    CATEGORY = "image"

    def paste_images(self, base_image, overlay_image):
        # 确保输入是numpy数组
        base = base_image.cpu().numpy()
        overlay = overlay_image.cpu().numpy()

        # 获取基础图片的尺寸
        b, h, w, c = base.shape
        
        # 确保两张图片的尺寸相同
        if base.shape[:3] != overlay.shape[:3]:
            raise ValueError(f"Base image shape {base.shape} must match overlay image shape {overlay.shape}")

        # 创建结果图片
        result = np.zeros((b, h, w, 4), dtype=np.float32)
        
        # 处理每一张图片
        for i in range(b):
            # 复制base图片到结果
            if base[i].shape[-1] == 3:
                result[i, :, :, :3] = base[i]
                result[i, :, :, 3] = 1.0  # 设置alpha通道为1
            else:
                result[i] = base[i]

            # 如果overlay有alpha通道，进行混合
            if overlay[i].shape[-1] == 4:
                alpha = overlay[i, :, :, 3:4]
                rgb = overlay[i, :, :, :3]
                # 只替换非透明部分
                mask = alpha > 0
                result[i, :, :, :3] = np.where(mask, rgb, result[i, :, :, :3])
                result[i, :, :, 3] = np.maximum(result[i, :, :, 3], alpha[:, :, 0])
            else:
                result[i, :, :, :3] = overlay[i]
                result[i, :, :, 3] = 1.0

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImagePaste": ImagePaste
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImagePaste": "Image Paste(linhao)"
} 