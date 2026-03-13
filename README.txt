# Steganography Tool (Python)

A Python application for hiding and extracting data inside images using steganography techniques.

## Features

- Hide text inside images
- Hide files inside images
- Extract hidden payloads
- Progress bar for large payloads
- Modular architecture

## Project Structure

- `main.py` - Main entry point
- `core/` - Core logic
  - `encoder.py` - Text encoding
  - `decoder.py` - Text decoding
  - `file_encoder.py` - File encoding
  - `file_decoder.py` - File decoding
  - `progress.py` - Progress bar
- `ui/` - User interface
  - `menu.py` - Main menu
  - `extractor.py` - Extraction UI
  - `image_selector.py` - Image selection
- `images/` - Sample images
- `output/` - Generated images

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Steneografia
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

## Author

Francisco Javier Jiménez Cortés ---> DIBLOCK

## License

MIT License