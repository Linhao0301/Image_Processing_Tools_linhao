import torch
import numpy as np

class ImageRemoveAlpha:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "background_color": (["white", "black", "custom"], {"default": "white"}),
                "custom_color": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove_alpha"
    CATEGORY = "image"

    def hex_to_rgb(self, hex_color):
        # 移除可能的 # 前缀
        hex_color = hex_color.lstrip('#')
        # 转换为RGB值（0-1范围）
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def remove_alpha(self, image, background_color, custom_color):
        # 转换为numpy数组
        img = image.cpu().numpy()
        
        # 获取图片的尺寸
        b, h, w, c = img.shape

        # 创建结果数组（三通道）
        result = np.zeros((b, h, w, 3), dtype=np.float32)
        
        # 设置背景颜色
        if background_color == "white":
            bg_color = np.array([1.0, 1.0, 1.0])
        elif background_color == "black":
            bg_color = np.array([0.0, 0.0, 0.0])
        else:  # custom
            bg_color = np.array(self.hex_to_rgb(custom_color))
        
        # 处理每一张图片
        for i in range(b):
            if img[i].shape[-1] == 4:
                # 获取alpha通道
                alpha = img[i, :, :, 3:4]
                # 获取RGB通道
                rgb = img[i, :, :, :3]
                # 使用alpha通道混合RGB和背景色
                result[i] = rgb * alpha + bg_color * (1 - alpha)
            else:
                # 如果不是四通道图像，直接复制RGB通道
                result[i] = img[i, :, :, :3]

        return (torch.from_numpy(result),)

NODE_CLASS_MAPPINGS = {
    "ImageRemoveAlpha": ImageRemoveAlpha
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRemoveAlpha": "Image Remove Alpha(linhao)"
} 