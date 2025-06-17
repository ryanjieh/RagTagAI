from transformers import CLIPProcessor, CLIPModel, AutoProcessor, AutoModelForImageTextToText
import torch
from safetensors import safe_open

clip_model_id = "patrickjohncyh/fashion-clip"
clip_model = CLIPModel.from_pretrained(clip_model_id)
clip_processor = CLIPProcessor.from_pretrained(clip_model_id)

clip_device = torch.device(
    "mps" if torch.backends.mps.is_available()
    else 0 if torch.cuda.is_available() 
    else "cpu"
    )
clip_model = clip_model.to(clip_device)

blip_model_id = "Salesforce/blip-image-captioning-base"
blip_processor = AutoProcessor.from_pretrained(blip_model_id)
blip_model = AutoModelForImageTextToText.from_pretrained(blip_model_id)

with safe_open("./blip-finetuned/model.safetensors", framework="pt", device="cpu") as f:
    for key in f.keys():
        tensor = f.get_tensor(key)
        blip_model.state_dict()[key].copy_(tensor)  # Load weights into the model

blip_device = torch.device(
    0 if torch.cuda.is_available()
    else "cpu"
)
blip_model = blip_model.to(blip_device)

def generate_caption(image):
    prompt = "Full outfit: "
    input = blip_processor(
        text=prompt,
        images=image,
        return_tensors="pt",
    ).to(blip_device)
    
    with torch.no_grad():
        output = blip_model.generate(
            **input,
            max_new_tokens = 50,
            num_beams = 3,
            early_stopping = True
        )
    caption = blip_processor.batch_decode(output, skip_special_tokens=True)[0]
    return caption[14:]

def embed_user_input(image, caption):
    input = clip_processor(
        text=caption,
        images=image,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=77
    ).to(clip_device)
    
    with torch.no_grad():
        outputs = clip_model(**input)

    image_embed = outputs.image_embeds
    text_embed = outputs.text_embeds
    
    image_embed = torch.nn.functional.normalize(image_embed)
    text_embed = torch.nn.functional.normalize(text_embed)
    return image_embed, text_embed

def combine_embeddings(image_embeds, text_embeds):
    return 0.5 * image_embeds + 0.5 * text_embeds

def main():
    return
    
if __name__ == "__main__":
    main()