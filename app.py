import base64
import os

import requests
from flask import Flask
from openai import OpenAI
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO



load_dotenv()

app = Flask(__name__)

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


cell_image = "images/bwcell.jpg"
dig_image = "images/img_4.png"

base64_image = encode_image(dig_image)

openai_key = os.getenv("OPENAI_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_key}"
}

payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "# Guidelines"
                            "-Create a thorough description of this image. Just describe what is visible in the image. "
                            "-Do not add any additional details regarding the functions or facts about what is present in the image, just make a visual description."
                            "# Considerations"
                            "-This description will be passed on to the DALL-E 3 model. Make sure the description is suitable for DALL-E 3 to completely understand"

                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300
}
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

answer = response.json()
content = answer['choices'][0]['message']['content']
print(content)


#DALL-E 3

def get_image_from_DALL_E_3_API(user_prompt,
                                image_dimension="1024x1024",
                                image_quality="hd",
                                model="dall-e-3",
                                nb_final_image=1):
    dalle_response = client.images.generate(
        model=model,
        prompt=user_prompt,
        size=image_dimension,
        quality=image_quality,
        n=nb_final_image,
    )

    image_url = dalle_response.data[0].url

    # Download the image
    image_response = requests.get(image_url)

    # Check if the request was successful
    if image_response.status_code == 200:
        # Open the image with PIL
        img = Image.open(BytesIO(image_response.content))

        # Save the image locally
        img.save("generated_image.png")

        # Display the image
        img.show()
    else:
        print("Failed to retrieve the image")

cell_prompt = f"Create an image with this description: {content}. Make sure you include everything that is present in the description. The image must be colored and it has to be understandable for kids in elementary school. If there are any labels, they must be written in spanish, and it is mandatory to write in that language and to make sure there are no grammar mistakes and that those words exist in spanish."
get_image_from_DALL_E_3_API(cell_prompt)

dig_prompt = f"Create an image with this description: {content}. Make sure you include everything that is present in the description. The image must be colored and it has to be understandable for kids in elementary school. If there are any labels, they must be written in spanish, and it is mandatory to write in that language and to make sure there are no grammar mistakes and that those words exist in spanish."