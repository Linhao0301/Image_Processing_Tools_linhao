# Image Processing Tools for ComfyUI

这是一个ComfyUI的图像处理工具集，提供了一系列用于图像处理的节点。

## 功能节点

1. **Image Alpha Blend(linhao)**
   - 使用alpha通道混合两张图片

2. **Image Alpha Blend By Bbox(linhao)**
   - 在指定边界框内使用alpha通道混合图片

3. **Image Paste(linhao)**
   - 将一张图片粘贴到另一张图片上

4. **Image Paste By Bbox(linhao)**
   - 在指定边界框内粘贴图片

5. **Image To Gray(linhao)**
   - 将图片转换为灰度图

6. **Crop Image By Mask(linhao)**
   - 使用蒙版裁剪图片

7. **Image Gaussian Blur(linhao)**
   - 对图片应用高斯模糊

## 安装方法

1. 进入ComfyUI的custom_nodes目录：
```bash
cd ComfyUI/custom_nodes
```

2. 克隆仓库：
```bash
git clone https://github.com/your-username/Image_Processing_Tools_linhao.git
```

3. 安装依赖：
```bash
pip install opencv-python
```

## 使用方法

1. 启动ComfyUI
2. 在节点列表中找到 "linhao" 分类
3. 选择需要的节点进行使用

## 依赖

- ComfyUI
- OpenCV-Python
- NumPy
- PyTorch 