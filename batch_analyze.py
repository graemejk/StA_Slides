#!/usr/bin/env python3
"""
Batch Image Analysis with Google Gemini
This script processes multiple slide images and saves the results.
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from PIL import Image
from datetime import datetime

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

def get_image_files(directory):
    """Get all image files from the specified directory."""
    image_dir = Path(directory)
    if not image_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Get all image files (jpeg, jpg, png, etc.)
    image_files = sorted([
        f for f in image_dir.iterdir()
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    ])

    return image_files

def analyze_image(client, image_path, prompt="What is in this image? Describe it in detail."):
    """
    Analyze an image using Google Gemini.

    Args:
        client: Gemini client instance
        image_path: Path to the image file
        prompt: Question or instruction for Gemini

    Returns:
        Dictionary with structured analysis data
    """
    try:
        # Load and verify image
        img = Image.open(image_path)
        print(f"  Image size: {img.size}")
        print(f"  Image format: {img.format}")

        # Generate response
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )

        # Try to parse JSON response
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '', 1)
        if response_text.startswith('```'):
            response_text = response_text.replace('```', '', 1)
        if response_text.endswith('```'):
            response_text = response_text.rsplit('```', 1)[0]

        response_text = response_text.strip()

        # Parse JSON
        parsed_data = json.loads(response_text)

        # Map field names (LLM returns these field names)
        result = {
            "EADUnitTitle": parsed_data.get("EADUnitTitle", ""),
            "EADScopeAndContent": parsed_data.get("EADScope+Content", ""),
            "EADUnitDate": parsed_data.get("EADUnitDate", "")
        }

        return result

    except json.JSONDecodeError as e:
        print(f"  ⚠ Warning: Could not parse JSON response: {e}")
        return {
            "EADUnitTitle": "",
            "EADScopeAndContent": response.text,
            "EADUnitDate": "",
            "parse_error": str(e)
        }
    except Exception as e:
        return {
            "error": str(e),
            "EADUnitTitle": "",
            "EADScopeAndContent": "",
            "EADUnitDate": ""
        }

def create_empty_record():
    """Create a record structure with all required fields initialized to empty values."""
    return {
        "ColDepartment": "",
        "PhoPhotoCollectionRef.irn": "",
        "EADRepositoryRef.irn": "",
        "ColObjectType": "",
        "PhoRecordLevel": "",
        "EADLevelAttribute": "",
        "ColObjectStatus": "",
        "PhoRecordStatus": "",
        "EADUnitTitle": "",
        "EADUnitID": "",
        "EADIdentifier": "",
        "ColParentRecordRef.irn": "",
        "EADScopeAndContent": "",
        "EADExtent_tab": "",
        "EADUnitDate": "",
        "EADUnitDateEarliest": "",
        "EADUnitDateLatest": "",
        "EADOriginationRef_tab.irn": "",
        "EADPhysicalTechnical": "",
        "LocCurrentLocationRef.irn": "",
        "AdmPublishWebNoPassword": "",
        "PhoMedia_tab": "",
        "PhoFormat_tab": ""
    }

def save_results(results, output_file="results.json"):
    """Save analysis results to a JSON file."""
    output_path = Path(output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {output_path}")

def main():
    """Main function to run batch image analysis."""
    # Configuration
    images_directory = "images/slides/"

    # Museum catalogue-style prompt for structured extraction
    prompt = """Analyze this slide image and extract the following information in JSON format:

1. "EADUnitTitle": Extract all handwritten text, labels, or annotations visible on the slide mount or border. Include reference numbers, titles, or any written information. If none visible, use empty string.

2. "EADScope+Content": Provide a museum catalogue-style description of the photograph itself. Describe what is depicted in the image as you would for a museum or archive catalogue entry. Be detailed and professional. Focus on the subject matter, composition, and notable features of the photograph.

3. "EADUnitDate": Extract any dates mentioned on the slide (in handwriting or printed). This could be a year, full date, or date range. If no date is visible, use empty string.

Return ONLY valid JSON in this exact format:
{
  "EADUnitTitle": "text here",
  "EADScope+Content": "description here",
  "EADUnitDate": "date here"
}"""

    # For testing: set to True to process only first image
    # For full processing: set to False to process all images
    TEST_MODE = False

    # Rate limiting: 5 images per minute = 12 seconds between images
    RATE_LIMIT_DELAY = 12  # seconds

    print("=" * 60)
    print("Batch Image Analysis with Google Gemini")
    print("=" * 60)
    print(f"Rate limit: 5 images per minute ({RATE_LIMIT_DELAY}s delay between images)")

    # Get all image files
    try:
        image_files = get_image_files(images_directory)
        print(f"\nFound {len(image_files)} image(s) in {images_directory}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not image_files:
        print("No image files found!")
        sys.exit(1)

    # Filter to first image only if in test mode
    if TEST_MODE:
        image_files = [image_files[0]]
        print(f"\n*** TEST MODE: Processing only first image ***")

    # Initialize Gemini client
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    print("\nGemini client initialized successfully")

    # Process images
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_images": len(image_files),
        "prompt": prompt,
        "images": []
    }

    print(f"\nProcessing {len(image_files)} image(s)...\n")

    for idx, image_path in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] Analyzing: {image_path.name}")

        try:
            analysis_data = analyze_image(client, image_path, prompt)

            # Start with empty record structure
            image_result = create_empty_record()

            # Extract MS number from filename (e.g., ms39080 from ms39080-51-5-1-1.jpeg)
            filename = image_path.name
            ms_number = ""
            if filename.startswith("ms"):
                # Extract the ms number (e.g., ms39080)
                parts = filename.split("-")
                if parts:
                    ms_number = parts[0]

            # Add metadata fields
            image_result["filename"] = filename
            image_result["path"] = str(image_path)
            image_result["status"] = "success" if "error" not in analysis_data else "error"

            # Set static values
            image_result["ColDepartment"] = "Special Collections - Archive Collections"
            image_result["ColObjectType"] = "Photograph"
            image_result["PhoRecordLevel"] = "Item"
            image_result["EADLevelAttribute"] = "Item"
            image_result["ColObjectStatus"] = "1- Available"
            image_result["PhoRecordStatus"] = "Catalogued"
            image_result["EADUnitID"] = ms_number
            image_result["EADIdentifier"] = ms_number
            image_result["PhoMedia_tab"] = "slides (photographs)"
            image_result["PhoFormat_tab"] = "positives (photographs)"

            # Merge in LLM-populated fields
            image_result["EADUnitTitle"] = analysis_data.get("EADUnitTitle", "")
            image_result["EADScopeAndContent"] = analysis_data.get("EADScopeAndContent", "")
            image_result["EADUnitDate"] = analysis_data.get("EADUnitDate", "")

            # Add error fields if present
            if "error" in analysis_data:
                image_result["error"] = analysis_data["error"]
            if "parse_error" in analysis_data:
                image_result["parse_error"] = analysis_data["parse_error"]

            print(f"  ✓ Analysis complete")
            if image_result["EADUnitTitle"]:
                print(f"    Title: {image_result['EADUnitTitle'][:60]}...")
            if image_result["EADUnitDate"]:
                print(f"    Date: {image_result['EADUnitDate']}")

        except Exception as e:
            # Create empty record on error
            image_result = create_empty_record()

            # Extract MS number even on error
            filename = image_path.name
            ms_number = ""
            if filename.startswith("ms"):
                parts = filename.split("-")
                if parts:
                    ms_number = parts[0]

            image_result["filename"] = filename
            image_result["path"] = str(image_path)
            image_result["status"] = "error"
            image_result["error"] = str(e)

            # Set static values even on error
            image_result["ColDepartment"] = "Special Collections - Archive Collections"
            image_result["ColObjectType"] = "Photograph"
            image_result["PhoRecordLevel"] = "Item"
            image_result["EADLevelAttribute"] = "Item"
            image_result["ColObjectStatus"] = "1- Available"
            image_result["PhoRecordStatus"] = "Catalogued"
            image_result["EADUnitID"] = ms_number
            image_result["EADIdentifier"] = ms_number
            image_result["PhoMedia_tab"] = "slides (photographs)"
            image_result["PhoFormat_tab"] = "positives (photographs)"

            print(f"  ✗ Error: {e}")

        results["images"].append(image_result)

        # Rate limiting: wait between images (except after the last one)
        if idx < len(image_files):
            print(f"  ⏳ Waiting {RATE_LIMIT_DELAY}s before next image (rate limit: 5 images/min)...")
            time.sleep(RATE_LIMIT_DELAY)

        print()

    # Save results
    output_filename = "test_results.json" if TEST_MODE else "batch_results.json"
    save_results(results, output_filename)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    successful = sum(1 for img in results["images"] if img["status"] == "success")
    failed = sum(1 for img in results["images"] if img["status"] == "error")
    print(f"Total processed: {len(results['images'])}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("=" * 60)

if __name__ == "__main__":
    main()
