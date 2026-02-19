import os
import torch
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
from huggingface_hub import login

# Load .env file
load_dotenv()

# Login using token from .env
login(os.getenv("HF_TOKEN"))

model_id = "runwayml/stable-diffusion-v1-5"

# Load pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32
)

pipe = pipe.to("cpu")

prompt = "Indian Prime Minister Narendra Modi"

image = pipe(prompt).images[0]
image.save("output.png")

print("Image saved as output.png")
