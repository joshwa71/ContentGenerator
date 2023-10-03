import requests
import os
import json
import argparse
from PIL import Image
from io import BytesIO

def main(categories, num_images, OAI_api_key, SD_api_key, engine_id):
    sd_url = 'https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image'
    
    all_data = []

    for category in categories:
        folder_name = f"./{category}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        json_file_path = f"{folder_name}/{category}_products.json"
        
        for i in range(num_images):
            scene_prompt = f"Generate a scene idea related to {category}, describe this scene concisely (no more than 20 words) so that it will create good results when passed to a text-to-image AI like Dalle."
            seo_description_prompt = f"We are creating new product pages for a greetings card business. We need to generate a description for a {category} card. The description should be roughly 100 words long and contain the keywords words {category}, greetings card, and birthday card so that the description ranks high for searches of these keywords (e.g. rank high for '{category} birthday card'). Respond only with the description."
            
            gpt_image_response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={'Authorization': f'Bearer {OAI_api_key}'},
                json={
                    'model': 'gpt-4',
                    'messages': [{'role': 'user', 'content': scene_prompt}]
                }
            )
            gpt_description_response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={'Authorization': f'Bearer {OAI_api_key}'},
                json={
                    'model': 'gpt-4',
                    'messages': [{'role': 'user', 'content': seo_description_prompt}]
                }
            )

            scene = gpt_image_response.json()['choices'][0]['message']['content']
            seo_description = gpt_description_response.json()['choices'][0]['message']['content']

            print(scene)
            print(seo_description)

            sd_headers = {
                "Accept": "image/png",
                "Stability-Client-ID": "my-great-plugin",
                "Stability-Client-Version": "1.2.1",
                "Authorization": "Bearer " + SD_api_key,
            }

            payload = {
                "height": 1024,
                "width": 1024,
                "text_prompts": [
                    {
                        "text": scene,
                        "weight": 0.5
                    }
                ],
                "cfg_scale": 7,
                "clip_guidance_preset": "NONE",
                "sampler": "DDIM",
                "samples": 1,
                "seed": 0,
                "steps": 50,
                "extras": {}
            }

            diffusion_response = requests.post(sd_url, headers=sd_headers, json=payload)
            
            if diffusion_response.status_code == 200:
                print("Image generated successfully.")
                image = Image.open(BytesIO(diffusion_response.content))
                image.show()
            else:
                print(f"Error: {diffusion_response.status_code}")
                print(diffusion_response.text)
                        
            image_path = f"{folder_name}/image_{i}.png"
            with open(image_path, 'wb') as img_file:
                img_file.write(diffusion_response.content)
            
            product_data = {
                'Type': 'simple',
                'Name': f"{category} scene {i+1}",
                'Image Prompt': scene,
                'Categories': category,
                'Tags': '',
                'Image': image_path,
                'SEO Title': '',
                'SEO Description': seo_description
            }
            all_data.append(product_data)

        with open(json_file_path, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically generate art and descriptions for a business.")
    
    parser.add_argument("--categories", nargs="+", default=["climbing"], help="List of categories.")
    parser.add_argument("--num_images", type=int, default=2, help="Number of images to generate for each category.")
    parser.add_argument("--OAI_api_key", default="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", help="OpenAI API key.")
    parser.add_argument("--SD_api_key", default="sk-G8km1hjnY1jwHHX8vV9rUap8Jis7iWyra0Pswoezmpx4PaDH", help="Stability API key.")
    parser.add_argument("--engine_id", default="stable-diffusion-xl-1024-v1-0", help="Engine ID for Stability API.")

    args = parser.parse_args()
    
    main(
        categories=args.categories,
        num_images=args.num_images,
        OAI_api_key=args.OAI_api_key,
        SD_api_key=args.SD_api_key,
        engine_id=args.engine_id
    )
