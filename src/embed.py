from transformers import CLIPProcessor, CLIPModel, AutoProcessor, AutoModelForImageTextToText
import torch

clip_model_id = "patrickjohncyh/fashion-clip"
clip_model = CLIPModel.from_pretrained(clip_model_id)
clip_processor = CLIPProcessor.from_pretrained(clip_model_id)

clip_device = torch.device(
    "mps" if torch.backends.mps.is_available()
    else 0 if torch.cuda.is_available() 
    else "cpu"
    )
clip_model = clip_model.to(clip_device)

blip_model_id = "sagniksengupta/blip-finetuned-facad-v2"
blip_processor = AutoProcessor.from_pretrained("sagniksengupta/blip-finetuned-facad-v2")
blip_model = AutoModelForImageTextToText.from_pretrained("sagniksengupta/blip-finetuned-facad-v2")

blip_device = torch.device(
    0 if torch.cuda.is_available()
    else "cpu"
)
blip_model = blip_model.to(blip_device)

def generate_caption(image):
    prompt = "Outfit description only WITHOUT any advertisement: "
    input = blip_processor(
        text=prompt,
        images=image,
        return_tensors="pt",
        truncation=True,
        max_length=77
    ).to(blip_device)
    
    with torch.no_grad():
        output = blip_model.generate(
            **input,
            max_new_tokens = 30,
            num_beams = 5,
            early_stopping = True
        )
    caption = blip_processor.batch_decode(output, skip_special_tokens=True)[0]
    return caption

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