import torch
import numpy as np
from PIL import Image
import os

class CropImageByMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop_by_mask"
    CATEGORY = "image"

    def crop_by_mask(self, image, mask):
        # 确保输入是numpy数组
        image_np = image.cpu().numpy()
        mask_np = mask.cpu().numpy()

        # 获取图像尺寸
        b, h, w, c = image_np.shape
        
        # 确保mask和image的数量匹配
        if len(mask_np) != b:
            raise ValueError(f"Number of masks ({len(mask_np)}) must match number of images ({b})")

        # 创建结果数组，添加alpha通道
        result = np.zeros((b, h, w, 4), dtype=np.float32)
        
        # 处理每一张图片
        for i in range(b):
            # 将mask扩展到3通道
            mask_3d = np.stack([mask_np[i]] * 3, axis=-1)
            
            # 复制原始图像到RGB通道
            result[i, :, :, :3] = image_np[i]
            
            # 将mask值复制到alpha通道
            result[i, :, :, 3] = mask_np[i]

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "CropImageByMask": CropImageByMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CropImageByMask": "Crop Image By Mask (Linhao)"
} 