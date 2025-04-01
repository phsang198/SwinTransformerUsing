import torch
from PIL import Image
from transformers import AutoFeatureExtractor, SwinForImageClassification

feature_extractor = AutoFeatureExtractor.from_pretrained('microsoft/swin-base-patch4-window7-224')
model = SwinForImageClassification.from_pretrained('microsoft/swin-base-patch4-window7-224')

def recognize_objects(image_path):
    
    image = Image.open(image_path)

    
    inputs = feature_extractor(images=image, return_tensors="pt")

    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_class_idx = logits.argmax(-1).item()
    return model.config.id2label[predicted_class_idx]

# Example usage
#if __name__ == "__main__":
    #image_path = 'F:\\OutSource\\PYTHON\\SwinTransformerUsing\\img2.jpg'
    #predicted_class = recognize_objects(image_path)
    #print(f'Predicted class: {predicted_class}')