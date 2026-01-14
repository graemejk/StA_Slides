# Slides - LLM-Enhanced Metadata Extraction

An experimental project by the University of St Andrews exploring the use of Large Language Models (LLMs) to extract and enhance metadata from historical photograph slides with minimal existing documentation.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/UC_Slides.git
cd UC_Slides
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your Gemini API key

# Add images
mkdir -p images/slides
# Copy your slide images to images/slides/

# Run
python batch_analyze.py
```

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

## AI Model

This project uses **Google Gemini 2.5 Flash** for image analysis. The model:
- Supports multimodal input (text prompts + images)
- Excels at OCR and handwriting recognition
- Generates structured JSON output
- Available through the Google AI API with free tier access

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
TEST_MODE = False  # Change from True to False on line 169
```

Then run:
```bash
python batch_analyze.py
```

Results will be saved to `batch_results.json`.

**Rate Limiting**: The script automatically enforces a rate limit of 5 images per minute (12-second delay between images) to comply with API quota restrictions.

**Processing Time Estimates**:
- 10 images: ~2 minutes
- 50 images: ~10 minutes
- 100 images: ~20 minutes

The script displays progress for each image and shows estimated wait times between batches.

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

### Example Output

For a slide showing a rural farm scene with handwritten text "AIR SHAFT BALCARRES WARD 34/6/11 NO 467 072":

```json
{
  "EADUnitTitle": "AIR SHAFT BALCARRES WARD 34/6/11 NO 467 072",
  "EADScopeAndContent": "A landscape photograph featuring a ploughed field in the foreground. A low stone wall structure, possibly an old wellhead or an air shaft structure, is visible in the mid-ground. Beyond this, a cluster of farm buildings with red roofs and a taller, lighter-colored building are situated. The sky is clear and blue with a few wispy clouds. A wooden utility pole stands to the right of the frame.",
  "EADUnitDate": "34/6/11",
  "EADUnitID": "ms39080",
  "ColDepartment": "Special Collections - Archive Collections",
  "ColObjectType": "Photograph",
  "PhoRecordStatus": "Catalogued"
}
```

The LLM successfully:
- ✓ Extracted the complete handwritten text from the slide mount
- ✓ Identified and transcribed the date notation
- ✓ Generated a professional archival description
- ✓ Described the photograph's subject matter and composition

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
├── LICENSE              # MIT License
├── README.md            # This file
├── .env.example         # Environment variable template
├── .gitignore           # Git exclusions
├── images/              # Images directory (not in repo)
│   └── slides/          # Slide photographs go here
├── test_results.json    # Test mode output (not in repo)
└── batch_results.json   # Full batch output (not in repo)
```

**Note**: Images and JSON result files are excluded from the repository via `.gitignore` to protect source materials and keep the repository size manageable.

## Limitations & Considerations

- **API Quotas**: Free tier has rate limits; processing large batches may require pauses
- **OCR Accuracy**: Handwriting recognition depends on image quality and legibility
- **Date Interpretation**: The LLM may interpret ambiguous dates differently; manual review recommended
- **Hallucinations**: As with all LLMs, descriptions should be reviewed for accuracy
- **Image Quality**: Higher resolution images produce better OCR and description results
- **Manual Review**: All LLM-generated content should be reviewed by archivists before final cataloguing

## Troubleshooting

### API Quota Errors

If you encounter `429 RESOURCE_EXHAUSTED` errors:
- Wait a few minutes before retrying
- Check your API quota at [Google AI Studio](https://aistudio.google.com/)
- The free tier has daily and per-minute limits
- Consider upgrading to a paid tier for larger batches

### Model Not Found Errors

If you see `404 models/gemini-X-X is not found`:
- The model name may have changed
- Check [Google's documentation](https://ai.google.dev/models/gemini) for current model names
- Update the `model` parameter in the scripts

### JSON Parsing Errors

If the LLM output cannot be parsed as JSON:
- The error is logged but processing continues
- Check `parse_error` field in results
- The raw LLM response is stored in `EADScopeAndContent`
- Consider adjusting the prompt for clearer JSON output

### Missing EADUnitTitle or Dates

If fields are empty:
- The slide may not have visible handwritten text
- Image quality may be too low for OCR
- Try running the single image script with a custom prompt to test
- Consider manual data entry for problematic slides

## Best Practices

### For Best Results

1. **Image Quality**: Use high-resolution scans (at least 1200 DPI)
2. **File Naming**: Name files with MS numbers (e.g., `ms39080-51-5-1-1.jpeg`)
3. **Batch Size**: Process in batches of 50-100 for manageable review
4. **Verification**: Always review LLM-generated metadata before importing to systems
5. **Test First**: Run test mode on a few samples before full batch processing

### Workflow Recommendation

1. Digitize slides at high resolution
2. Name files according to your archival numbering system
3. Run batch processing on a small test set (5-10 images)
4. Review test results for accuracy
5. Process full batch
6. Export to CSV or import directly to collection management system
7. Have archivists review and correct any errors

## Contributing

This is an experimental research project. Contributions are welcome in the following areas:

- **Bug Reports**: Report issues via GitHub Issues
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests for bug fixes or enhancements
- **Documentation**: Improve or translate documentation
- **Model Testing**: Test with different Gemini models and report results
- **Use Cases**: Share your experience using this with different slide collections

Please open an issue to discuss major changes before submitting a pull request.

## License

MIT License

Copyright (c) 2025 University of St Andrews

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Future Enhancements

Potential improvements under consideration:

- CSV export functionality for direct import to collection management systems
- Batch resume capability for interrupted processing
- Support for multiple prompt templates
- Integration with IIIF image servers
- Web interface for non-technical users
- Additional metadata fields (subject headings, geographic locations)
- Multilingual support for non-English annotations

## Acknowledgments

**University of St Andrews**
Library Collections and University Collections

This project demonstrates the potential of AI-assisted metadata enhancement for cultural heritage collections.

## Contact

For questions or collaboration opportunities, please contact Graeme Kemp.

---

**Version**: 1.0
**Last Updated**: January 2025
**Model**: Google Gemini 2.5 Flash
