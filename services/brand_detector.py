# services/brand_detector.py

import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Initialize model and processor once
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b").to(device)

def load_image(image_path):
    return Image.open(image_path).convert("RGB")

def detect_brand(image_path, prompt="brand of this product?:"):
    image = load_image(image_path)
    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_new_tokens=30)
    caption = processor.decode(output[0], skip_special_tokens=True)
    clean_caption = caption.replace(prompt, "").strip()
    return clean_caption
