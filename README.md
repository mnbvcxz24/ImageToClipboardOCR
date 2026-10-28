# ImageToClipboardOCR

A small Windows desktop utility that captures a screenshot, lets you select a screen region, reads the selected area with OCR, and copies **numbers only** to the clipboard.

## How to use

1. Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/). During installation, enable **Add Python to PATH**.
2. Download this repository or clone it.
3. Double-click `RUN.bat`. It checks Python and pip, installs the required packages, and launches the app.
4. Click **START SELECTION**.
5. Drag a rectangle around the number(s) you want to copy. Press **Esc** to cancel.
6. Recognized numbers are copied to the clipboard. Paste them wherever you need them.

## Number-only output

The tool filters OCR text to numeric tokens, including optional minus/plus signs, decimal points, and comma-separated thousands (for example, `-123`, `45.67`, or `1,234.00`). Non-numeric labels and words are ignored. If multiple numbers are detected, they are copied on separate lines.

## Requirements

- Windows
- Python 3.11 or newer
- Pillow
- RapidOCR ONNX Runtime
- NumPy

The first launch requires an internet connection so pip can install the Python packages and RapidOCR can obtain any required model files.

## Privacy

The screenshot and crop are processed locally by the application. The script does not connect to a spreadsheet, submit OCR text to a web service, or automatically paste anything. The recognized numbers are placed on your local clipboard only.

## Notes

- Crop tightly around the text for better recognition.
- OCR accuracy depends on image sharpness, contrast, font, and size.
- The current version captures the primary monitor.
