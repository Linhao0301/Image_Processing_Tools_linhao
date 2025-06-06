import torch
import numpy as np
from PIL import Image
import os

class ImagePasteByBbox:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "overlay_image": ("IMAGE",),
                "bbox_format": (["xywh", "xyxy"], {"default": "xywh"}),
                "bbox": ("BBOX",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "paste_images"
    CATEGORY = "image"

    def paste_images(self, base_image, overlay_image, bbox_format, bbox):
        # 确保输入是numpy数组
        base = base_image.cpu().numpy()
        overlay = overlay_image.cpu().numpy()

        # 获取基础图片的尺寸
        b, h, w, c = base.shape
        
        # 确保overlay_image和bbox的数量匹配
        if len(overlay) != len(bbox):
            raise ValueError(f"Number of overlay images ({len(overlay)}) must match number of bboxes ({len(bbox)})")

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

            # 根据bbox格式计算实际的位置和尺寸
            if bbox_format == "xywh":
                x1, y1 = int(bbox[i][0]), int(bbox[i][1])
                x2, y2 = int(bbox[i][0] + bbox[i][2]), int(bbox[i][1] + bbox[i][3])
            else:  # xyxy
                x1, y1 = int(bbox[i][0]), int(bbox[i][1])
                x2, y2 = int(bbox[i][2]), int(bbox[i][3])

            # 确保坐标在有效范围内
            x1 = max(0, min(x1, w-1))
            y1 = max(0, min(y1, h-1))
            x2 = max(0, min(x2, w))
            y2 = max(0, min(y2, h))

            # 确保目标区域有效
            if x2 <= x1 or y2 <= y1:
                continue

            target_width = x2 - x1
            target_height = y2 - y1

            # 将overlay图片转换为PIL图像，使用float32保持精度
            overlay_img = Image.fromarray((overlay[i] * 255).astype(np.uint8))
            # 调整大小以匹配目标区域，使用高质量的缩放方法
            resized = overlay_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            # 转回numpy数组，保持float32精度
            resized_overlay = np.array(resized).astype(np.float32) / 255.0

            # 确保resized_overlay的通道数正确
            if resized_overlay.shape[-1] == 3:
                resized_overlay = np.concatenate([resized_overlay, np.ones((target_height, target_width, 1))], axis=-1)
            
            # 提取alpha通道和RGB通道
            alpha = resized_overlay[:, :, 3:4]  # 上面图片的alpha通道
            rgb = resized_overlay[:, :, :3]     # 上面图片的RGB通道
            
            # 确保目标区域在base图片范围内
            if x1 < w and y1 < h and x2 > 0 and y2 > 0:
                # 计算实际可用的区域
                valid_x1 = max(0, x1)
                valid_y1 = max(0, y1)
                valid_x2 = min(w, x2)
                valid_y2 = min(h, y2)
                
                # 计算在resized_overlay中对应的区域
                overlay_x1 = valid_x1 - x1
                overlay_y1 = valid_y1 - y1
                overlay_x2 = overlay_x1 + (valid_x2 - valid_x1)
                overlay_y2 = overlay_y1 + (valid_y2 - valid_y1)
                
                # 获取当前区域的alpha和RGB
                current_alpha = alpha[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
                current_rgb = rgb[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
                current_base = result[i, valid_y1:valid_y2, valid_x1:valid_x2, :3]
                
                # 只替换非透明部分
                mask = current_alpha > 0
                result[i, valid_y1:valid_y2, valid_x1:valid_x2, :3] = np.where(
                    mask,
                    current_rgb,
                    current_base
                )
                result[i, valid_y1:valid_y2, valid_x1:valid_x2, 3] = np.maximum(
                    result[i, valid_y1:valid_y2, valid_x1:valid_x2, 3],
                    current_alpha[:, :, 0]
                )

        # 将四通道转换为三通道输出
        result = result[:, :, :, :3]

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImagePasteByBbox": ImagePasteByBbox
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImagePasteByBbox": "Image Paste By Bbox(linhao)"
} 