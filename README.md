# Slides - LLM-Enhanced Metadata Extraction

An experimental project by the University of St Andrews exploring the use of Large Language Models (LLMs) to extract and enhance metadata from historical photograph slides with minimal existing documentation.

## Project Overview

This project uses Google's Gemini AI to analyze digitized photographic slides from archival collections and automatically extract structured metadata. The goal is to transform images with little to no metadata into properly catalogued items suitable for museum and archive management systems.

### Key Features

- **Automated Metadata Extraction**: Uses Gemini AI to identify and transcribe handwritten annotations, dates, and reference numbers from slide mounts
- **Museum-Quality Descriptions**: Generates professional catalogue-style descriptions (EAD Scope and Content) for archival records
- **Structured Output**: Produces JSON records compatible with collection management systems
- **Batch Processing**: Process multiple slides efficiently with progress tracking
- **EAD-Compliant Fields**: Outputs data in standard archival description fields

### Use Case

Many archival photograph collections contain slides with minimal metadata—perhaps just handwritten notes on the slide mount. This project demonstrates how LLMs can:
- Read handwritten text from slide borders
- Generate professional archival descriptions
- Extract dates and reference numbers
- Produce standardized catalogue records

## Requirements

- Python 3.11+
- Google Gemini API key (free tier available)
- PIL/Pillow for image processing

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/UC_Slides.git
cd UC_Slides
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 5. Prepare Your Images

**Note**: Images are not included in this repository due to size and copyright considerations.

Create the images directory and add your slide photographs:

```bash
mkdir -p images/slides
# Copy your slide images to images/slides/
```

Images should be named with an MS number prefix (e.g., `ms39080-51-5-1-1.jpeg`) for automatic extraction of archival identifiers.

## Usage

### Single Image Analysis

Test the script on a single image:

```bash
python analyze_image.py images/slides/ms39080-51-5-1-1.jpeg
```

With a custom prompt:

```bash
python analyze_image.py images/slides/ms39080-51-5-1-1.jpeg "What text is visible on this slide?"
```

### Batch Processing

Process multiple slides and generate structured metadata:

```bash
python batch_analyze.py
```

**Test Mode**: By default, the script processes only the first image for testing. Results are saved to `test_results.json`.

**Full Batch Mode**: To process all images in `images/slides/`, edit `batch_analyze.py`:
```python
TEST_MODE = False  # Change from True to False on line 168
```

Then run:
```bash
python batch_analyze.py
```

Results will be saved to `batch_results.json`.

## Output Format

The script generates JSON records with the following structure:

```json
{
  "ColDepartment": "Special Collections - Archive Collections",
  "ColObjectType": "Photograph",
  "PhoRecordLevel": "Item",
  "EADLevelAttribute": "Item",
  "ColObjectStatus": "1- Available",
  "PhoRecordStatus": "Catalogued",
  "EADUnitTitle": "AIR SHAFT BALCARRES WARD 34/6/11 NO 467 072",
  "EADUnitID": "ms39080",
  "EADIdentifier": "ms39080",
  "EADScopeAndContent": "A landscape photograph featuring a ploughed field...",
  "EADUnitDate": "34/6/11",
  "PhoMedia_tab": "slides (photographs)",
  "PhoFormat_tab": "positives (photographs)",
  ...
}
```

### Field Descriptions

**LLM-Extracted Fields**:
- `EADUnitTitle`: Handwritten text and annotations from slide mount
- `EADScopeAndContent`: Museum catalogue-style description of the photograph
- `EADUnitDate`: Date information extracted from the slide

**Auto-Populated Fields**:
- `EADUnitID` / `EADIdentifier`: Extracted from filename (e.g., ms39080)
- `ColDepartment`, `ColObjectType`, etc.: Standard values for archival photographs

**Reserved for Future Processing**:
- `PhoPhotoCollectionRef.irn`, `EADRepositoryRef.irn`, etc.: Empty fields for downstream processing

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- WebP

## Project Structure

```
UC_Slides/
├── analyze_image.py      # Single image analysis script
├── batch_analyze.py      # Batch processing script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Git exclusions
├── images/slides/       # Input images directory (not in repo)
├── test_results.json    # Test mode output (not in repo)
└── batch_results.json   # Full batch output (not in repo)
```

**Note**: Images and JSON result files are excluded from the repository via `.gitignore` to protect source materials and keep the repository size manageable.

## Limitations & Considerations

- **API Quotas**: Free tier has rate limits; processing large batches may require pauses
- **OCR Accuracy**: Handwriting recognition depends on image quality and legibility
- **Date Interpretation**: The LLM may interpret ambiguous dates differently; manual review recommended
- **Hallucinations**: As with all LLMs, descriptions should be reviewed for accuracy

## Contributing

This is an experimental research project. Feedback and contributions are welcome! Please open an issue or submit a pull request.

## License

[Specify your license here]

## Acknowledgments

**University of St Andrews**
Library Collections and University Collections.

This project demonstrates the potential of AI-assisted metadata enhancement for cultural heritage collections.

## Contact

For questions or collaboration opportunities, please contact Graeme Kemp.
