
# DIBLOCK Steganography Tool

A **Python steganography tool** designed to hide and extract information inside images using the **LSB (Least Significant Bit)** technique.

This project is part of a **technical cybersecurity portfolio focused on information hiding techniques and security tooling development**.

---

# What does this tool do?

The application allows:

• Hide **text messages** inside images  
• Extract **hidden messages**  
• Hide **complete files** inside images  
• Extract **hidden files**  
• Display a **progress bar** during operations  
• Provide a **structured console interface**

The goal is to demonstrate **digital steganography techniques used in security research**.

---

# 🏗 Project Architecture

The project is organized modularly to separate logic from interface.

Steneografia/

Steneografia/
│
├── core/
│   ├── encoder.py
│   ├── decoder.py
│   ├── file_encoder.py
│   ├── file_decoder.py
│   └── progress.py
│
├── ui/
│   ├── menu.py
│   ├── ui_central.py
│   ├── extractor.py
│   └── image_selector.py
│
├── images/
├── output/
├── main.py
└── requirements.txt

core/
- encoder.py → hide messages
- decoder.py → extract messages
- file_encoder.py → hide files
- file_decoder.py → extract files
- progress.py → progress bar

ui/
- menu.py → main interface
- ui_central.py → visual interface and banner
- extractor.py → extraction workflow
- image_selector.py → image selector

images/ → test images  
output/ → generated stego-images  

main.py → application entry point  
requirements.txt → project dependencies  

---

# LSB Technique

The tool uses **Least Significant Bit (LSB)** steganography.

---

# Supported File Types

Since the tool works at a **binary level**, it can hide almost any file type:

txt  
pdf  
docx  
xlsx  
csv  
png  
bmp  
gif  
mp3  
wav  
mp4  
zip  
rar  
7z  
exe  
bin  
py  
js  
html  

As long as the file **fits inside the image capacity**.

---

# Important Note About JPG

**JPG/JPEG images must not be used as carrier images.**

Reason:

• JPG uses **lossy compression**  
• Compression alters the least significant bits  
• Hidden data may be destroyed  

For this reason the tool uses **PNG images**.

---

# Installation

## Clone repository

git clone https://github.com/your-repo/steganography-tool.git

cd steganography-tool

---

## Create virtual environment

Windows:

python -m venv venv

venv\Scripts\activate

Linux / macOS:

python3 -m venv venv

source venv/bin/activate

---

## Install dependencies

pip install -r requirements.txt

Main dependencies:

- Pillow
- numpy
- colorama

---

# Run the application

python main.py

---

# Menu Features

1. Load image
2. Write secret message
3. Hide message
4. Extract message
5. Hide file inside image
6. Extract file from image
7. Exit

---

# Author

Francisco Javier Jiménez Cortés  
Cybersecurity • Software Development • Steganography Research
