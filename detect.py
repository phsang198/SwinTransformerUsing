import torch
import detectron2
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2

# Thiết lập config
cfg = get_cfg()
cfg.merge_from_file("mask_rcnn_swint_T_FPN_3x.yaml")  # Thay thế path đến config file
cfg.MODEL.WEIGHTS = "mask_rcnn_swint_T_coco17.pth"   # Thay thế path đến weights file
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Ngưỡng confidence threshold
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Tạo predictor
predictor = DefaultPredictor(cfg)

# Đọc hình ảnh
image = cv2.imread("D:\Study\CHK34\AD AI\img.jpg")

# Thực hiện dự đoán
outputs = predictor(image)

# Hiển thị kết quả
v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2.imshow("Result", v.get_image()[:, :, ::-1])
cv2.waitKey(0)
cv2.imwrite("result.jpg", v.get_image()[:, :, ::-1])