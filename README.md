# ContentGenerator

The ContentGenerator repository contains a script called `card_generator.py` designed to automatically generate art and SEO descriptions for a greeting card business.

## Features

- Generates images based on text prompts using the Stability Diffusion API
- Generates SEO descriptions using OpenAI's GPT-4
- Saves the generated images and SEO descriptions in a specified directory
- Creates a JSON file containing the metadata for each generated image

## Requirements

- Python 3.x
- PIL (Pillow) for image processing
- requests library for API calls

You can install the required Python packages using pip:

\`\`\`bash
pip install Pillow requests
\`\`\`

## Usage

### Command Line Arguments

The script accepts the following command-line arguments:

- `--categories`: List of categories for which you want to generate images and SEO descriptions. (default: `["climbing"]`)
- `--num_images`: Number of images to generate for each category. (default: `2`)
- `--OAI_api_key`: Your OpenAI API key.
- `--SD_api_key`: Your Stability Diffusion API key.
- `--engine_id`: Engine ID for the Stability API. (default: `stable-diffusion-xl-1024-v1-0`)

### Running the Script

Navigate to the directory where `card_generator.py` is located and run the following command:

\`\`\`bash
python card_generator.py --categories "category1" "category2" --num_images 5 --OAI_api_key "your_openai_api_key" --SD_api_key "your_stability_api_key"
\`\`\`

Replace `category1`, `category2`, `your_openai_api_key`, and `your_stability_api_key` with your own values.

### Output

The script will generate images and SEO descriptions for each category and save them in a folder named after the category. A JSON file containing the metadata for each image will also be created in the same folder.
