# DIBLOCK NMAP PRO TOOL v16 🛡️

**Diblock Nmap Pro Tool** es un script avanzado en Bash diseñado para automatizar y optimizar la fase de reconocimiento y escaneo de red utilizando Nmap. Va más allá del simple escaneo: incorpora parseo automático de resultados, análisis heurístico de vulnerabilidades y generación de reportes profesionales estructurados (JSON, CSV, Markdown y TXT).

Ideal para Pentesters, analistas de seguridad y administradores de sistemas que buscan agilizar sus auditorías.

## Características Principales ✨

* **Gestión Inteligente de Privilegios:** Detecta automáticamente si se ejecuta como `root` para habilitar técnicas avanzadas (`-sS`, `-O`, UDP) o se adapta a un usuario sin privilegios (`-sT`).
* **Escaneo Modular:** Desde escaneos ultrarrápidos hasta escaneos agresivos y evasión de firewalls automática.
* **Pipeline de Análisis:** Convierte el output XML de Nmap en bases de datos estructuradas (`services.json`, `services.csv`).
* **Detección Heurística:** Analiza las versiones de los servicios descubiertos y alerta sobre vulnerabilidades críticas y CVEs conocidos (ej. *EternalBlue*, *vsftpd backdoor*, *Apache path traversal*).
* **Generación de Reportes:** Crea un informe final en formato Markdown y texto plano clasificando los hallazgos por nivel de riesgo (LOW, MEDIUM, HIGH, CRITICAL).

## Requisitos Previos 📋

El script está diseñado para entornos Linux. Necesita las siguientes herramientas instaladas para funcionar correctamente:

* `nmap` (Motor principal de escaneo)
* `jq` (Para el procesamiento de archivos JSON)
* `libxml2-utils` (Proporciona `xmllint` para parsear el XML de Nmap)

Puedes instalar todas las dependencias en sistemas basados en Debian/Ubuntu ejecutando:
```bash
sudo apt update
sudo apt install nmap jq libxml2-utils -y

1.Instalación 🔧
Clona este repositorio o descarga el script:

git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO

2.Dale permisos de ejecución al script:

chmod +x Flow4Scan.sh

Uso 🚀
Para aprovechar al máximo las capacidades del script (especialmente la detección de SO, SYN scans y escaneos UDP), se recomienda ejecutarlo con privilegios de administrador:

sudo ./Flow4Scan.sh

Al iniciar, el script te preguntará en qué directorio deseas guardar los resultados y te mostrará un menú interactivo:

Opciones del Menú 🧰
Fast Scan: Escaneo rápido (-F) para descubrir los servicios más comunes rápidamente.

Aggressive Scan: Escaneo en profundidad (-A) para obtener versiones, scripts por defecto y SO.

Auto Port Scan: Escanea todos los puertos abiertos primero (-p-) de forma muy rápida y luego lanza un análisis detallado solo sobre los puertos descubiertos.

Multi Target: Permite ingresar la ruta de un archivo .txt que contenga una lista de IPs o dominios para escanearlos en lote.

Full Pro + Analysis: Escaneo agresivo + scripts de vulnerabilidad. Una vez finaliza, ejecuta el pipeline de análisis para generar los reportes (JSON, CSV, MD).

UDP Scan: Escaneo de puertos UDP (Requiere ser root).

Evasión Automática: Comprueba si el objetivo tiene un firewall. Si detecta puertos filtrados, aplica técnicas de evasión (fragmentación, delay, longitud de datos).

Analizar XML existente: Si ya tienes un escaneo de Nmap en formato XML, puedes pasárselo a esta herramienta para que genere los reportes de vulnerabilidades sin tener que volver a escanear.

Salir.

Estructura de Resultados 📁
Al finalizar un escaneo con análisis (Opción 5 u 8), se creará una carpeta con la fecha, tipo de escaneo y objetivo. Dentro encontrarás:

scan.nmap, scan.xml, scan.gnmap: Resultados crudos de Nmap.

services.json / services.csv: Puertos y servicios parseados.

analysis.json: Análisis detallado con vectores de ataque sugeridos.

report.md / report.txt: Informes finales listos para entregar.

Aviso Legal ⚠️
Esta herramienta ha sido creada con fines educativos y para su uso en entornos controlados o auditorías autorizadas. El autor no se hace responsable del mal uso de este software. Pide siempre permiso antes de escanear un objetivo.
