import tkinter as tk
from tkinter import filedialog
import torch
import cv2
import numpy as np
from PIL import Image, ImageTk
from mmdet.apis import init_detector, inference_detector
import mmcv

# Cấu hình MMDetection với Swin Transformer
config_file = 'configs/swin/mask_rcnn_swin-t-p4-w7_fpn_1x_coco.py'
checkpoint_file = 'https://download.openmmlab.com/mmdetection/v2.0/swin/mask_rcnn_swin-t-p4-w7_fpn_1x_coco/mask_rcnn_swin-t-p4-w7_fpn_1x_coco.pth'

model = init_detector(config_file, checkpoint_file, device='cuda' if torch.cuda.is_available() else 'cpu')

# Xử lý ảnh và phát hiện object
def detect_object():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    image = mmcv.imread(file_path)
    result = inference_detector(model, image)
    
    # Vẽ bounding box
    image = model.show_result(image, result, score_thr=0.3, show=False)
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img.thumbnail((600, 600))
    img_tk = ImageTk.PhotoImage(img)
    
    img_label.config(image=img_tk)
    img_label.image = img_tk

# Giao diện Tkinter
root = tk.Tk()
root.title("Swin Transformer Object Detection (MMDetection)")

btn_select = tk.Button(root, text="Chọn ảnh", command=detect_object)
btn_select.pack()

img_label = tk.Label(root)
img_label.pack()

root.mainloop()
