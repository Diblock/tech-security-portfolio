
# DIBLOCK Steganography Tool

Herramienta profesional de **esteganografía en Python** diseñada para ocultar y extraer información dentro de imágenes mediante la técnica **LSB (Least Significant Bit)**.

Este proyecto forma parte de un **portfolio técnico orientado a ciberseguridad, análisis de técnicas de ocultación de información y desarrollo de herramientas de seguridad**.

---

# 📌 ¿Qué hace esta herramienta?

La aplicación permite:

• Ocultar **mensajes de texto** dentro de imágenes  
• Extraer **mensajes ocultos**  
• Ocultar **archivos completos** dentro de imágenes  
• Extraer **archivos ocultos**  
• Mostrar **barra de progreso** durante el proceso  
• Utilizar una **interfaz de consola organizada y modular**  

El objetivo es demostrar el funcionamiento de técnicas de **esteganografía digital aplicadas a seguridad informática**.

---

# 🏗 Arquitectura del proyecto

El proyecto está organizado de forma modular para separar la lógica de la herramienta de la interfaz.

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
- encoder.py → ocultar mensajes
- decoder.py → extraer mensajes
- file_encoder.py → ocultar archivos
- file_decoder.py → extraer archivos
- progress.py → barra de progreso

ui/
- menu.py → menú principal
- ui_central.py → banner y visualización
- extractor.py → flujo de extracción
- image_selector.py → selector de imágenes

images/ → imágenes de prueba  
output/ → imágenes generadas con payload oculto  

main.py → punto de entrada del programa  
requirements.txt → dependencias del proyecto  

---

# 🔬 Técnica utilizada: LSB (Least Significant Bit)

La herramienta utiliza **LSB**, una técnica clásica de esteganografía.

---

# 📂 Tipos de archivos que se pueden ocultar

La herramienta trabaja a **nivel binario**, por lo que puede ocultar prácticamente cualquier archivo:

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

Siempre que el archivo **quepa dentro de la capacidad de la imagen**.

---

# ⚠ Nota importante sobre JPG / JPEG

Las imágenes **JPG o JPEG NO deben usarse como contenedor**.

Motivo:

• JPG utiliza **compresión con pérdida**
• La compresión modifica los bits menos significativos
• Esto destruye los datos ocultos

Por esta razón la herramienta utiliza **PNG**.

---

# ⚙ Instalación

## 1️⃣ Clonar el repositorio

git clone https://github.com/your-repo/steganography-tool.git

cd steganography-tool

---

## 2️⃣ Crear entorno virtual (recomendado)

Windows:

python -m venv venv

venv\Scripts\activate

Linux / macOS:

python3 -m venv venv

source venv/bin/activate

---

## 3️⃣ Instalar dependencias

pip install -r requirements.txt

Dependencias principales:

- Pillow
- numpy
- colorama

---

# ▶ Ejecutar la aplicación

python main.py

---

# 📋 Funciones del menú

1. Cargar imagen
2. Escribir mensaje secreto
3. Ocultar mensaje
4. Extraer mensaje
5. Ocultar archivo en imagen
6. Extraer archivo de imagen
7. Salir

---

# 👨‍💻 Autor

Francisco Javier Jiménez Cortés  
Cybersecurity • Software Development • Steganography Research
