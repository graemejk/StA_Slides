#!/usr/bin/env python3
"""
Image Analysis with Google Gemini
This script uses the Gemini API to analyze and describe images.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

def load_api_key():
    """Load the Gemini API key from .env file."""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        print("Error: GEMINI_API_KEY not found or not set properly.")
        print("Please create a .env file with your Gemini API key.")
        print("You can use .env.example as a template.")
        sys.exit(1)

    return api_key

def analyze_image(image_path, prompt="What is in this image? Describe it in detail."):
    """
    Analyze an image using Google Gemini.

    Args:
        image_path: Path to the image file
        prompt: Question or instruction for Gemini (default asks for description)

    Returns:
        Response text from Gemini
    """
    # Check if image exists
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Load and verify image
    try:
        img = Image.open(image_path)
        print(f"Analyzing image: {image_path}")
        print(f"Image size: {img.size}")
        print(f"Image format: {img.format}")
        print("-" * 50)
    except Exception as e:
        raise ValueError(f"Could not open image: {e}")

    # Initialize Gemini client
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    # Generate response using Gemini 2.5 Flash Lite
    print("Sending request to Gemini...")
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[prompt, img]
    )

    return response.text

def main():
    """Main function to run the image analysis."""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python analyze_image.py <image_path> [prompt]")
        print("\nExample:")
        print("  python analyze_image.py photo.jpg")
        print("  python analyze_image.py photo.jpg 'What colors are in this image?'")
        sys.exit(1)

    image_path = sys.argv[1]

    # Use custom prompt if provided, otherwise use default
    if len(sys.argv) >= 3:
        prompt = sys.argv[2]
    else:
        prompt = "What is in this image? Describe it in detail."

    try:
        # Analyze the image
        result = analyze_image(image_path, prompt)

        # Print the result
        print("\nGemini's Response:")
        print("=" * 50)
        print(result)
        print("=" * 50)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
