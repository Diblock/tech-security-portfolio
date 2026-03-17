#!/usr/bin/env bash

set -o pipefail

# =========================
# COLORES
# =========================
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
NC='\033[0m'

# =========================
# CONFIG / ESTADO
# =========================
OUTPUT_DIR="$(pwd)"
SCAN_TYPE="-sT"
OS_FLAG=""
IS_ROOT=0
CURRENT_SCAN_DIR=""
CURRENT_BASE=""
TMP_FILES=()

# =========================
# TRAPS / LIMPIEZA
# =========================
cleanup() {
  local f
  for f in "${TMP_FILES[@]}"; do
    [[ -n "$f" && -f "$f" ]] && rm -f -- "$f"
  done
}

on_interrupt() {
  echo -e "\n${RED}[!] Ejecución cancelada por el usuario${NC}"
  cleanup
  exit 130
}

trap cleanup EXIT
trap on_interrupt INT TERM

# =========================
# UTILIDADES
# =========================
banner() {
  clear 2>/dev/null || true
  echo -e "${CYAN}"
  echo "╔══════════════════════════════════════════════╗"
  echo "║         DIBLOCK NMAP PRO TOOL v16            ║"
  echo "║   Recon • Pentest • Parsing • Reporting      ║"
  echo "╚══════════════════════════════════════════════╝"
  echo -e "${NC}"
}

msg_info()  { echo -e "${CYAN}[*]${NC} $*"; }
msg_ok()    { echo -e "${GREEN}[✔]${NC} $*"; }
msg_warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
msg_err()   { echo -e "${RED}[ERROR]${NC} $*"; }

pause() {
  echo
  read -r -p "Pulsa ENTER para volver al menú... " _
}

require_cmd() {
  local cmd="$1"
  local pkg="${2:-$1}"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    msg_err "Falta dependencia: $cmd"
    echo "Instala con: sudo apt install $pkg"
    return 1
  fi
}

init_runtime() {
  require_cmd nmap nmap || exit 1
  require_cmd jq jq || exit 1
  require_cmd xmllint libxml2-utils || exit 1

  if [[ $EUID -eq 0 ]]; then
    IS_ROOT=1
    SCAN_TYPE="-sS"
    OS_FLAG="-O"
  else
    IS_ROOT=0
    SCAN_TYPE="-sT"
    OS_FLAG=""
    msg_warn "No root: usando -sT y desactivando OS detection y técnicas avanzadas."
    sleep 2
  fi
}

sanitize_target() {
  printf '%s' "$1" | tr -cd '[:alnum:].:_-'
}

set_output_dir() {
  local dir
  echo -e "${CYAN}╭─[ DIRECTORIO DE SALIDA ]${NC}"
  read -r -p "$(echo -e "${CYAN}╰─➤ ${NC}Ruta base (ENTER = actual): ")" dir
  [[ -z "$dir" ]] && dir="$(pwd)"

  if ! mkdir -p -- "$dir" 2>/dev/null; then
    msg_err "No se pudo crear/acceder al directorio: $dir"
    return 1
  fi

  OUTPUT_DIR="$dir"
  msg_ok "Resultados base: $OUTPUT_DIR"
}

create_scan_dir() {
  local scan_type="$1"
  local target="$2"
  local safe_target timestamp

  safe_target="$(sanitize_target "$target")"
  [[ -z "$safe_target" ]] && safe_target="target"
  timestamp="$(date +%Y%m%d_%H%M%S)"

  CURRENT_SCAN_DIR="$OUTPUT_DIR/${scan_type}_${safe_target}_${timestamp}"
  CURRENT_BASE="$CURRENT_SCAN_DIR/scan"

  mkdir -p -- "$CURRENT_SCAN_DIR" || {
    msg_err "No se pudo crear la carpeta de resultados"
    return 1
  }
}

print_menu() {
  echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║${NC}                 ${BLUE}M E N Ú${NC}                    ${CYAN}║${NC}"
  echo -e "${CYAN}╠══════════════════════════════════════════════╣${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[1]${NC} Fast Scan                              ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[2]${NC} Aggressive Scan                        ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[3]${NC} Auto Port Scan                         ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[4]${NC} Multi Target                           ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[5]${NC} Full Pro + Analysis                    ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[6]${NC} UDP Scan (root)                        ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[7]${NC} Evasión Automática                     ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${YELLOW}[8]${NC} Analizar XML existente                 ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC} ${RED}[9]${NC} Salir                                  ${CYAN}║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
}

ask_target() {
  local target
  echo -e "${CYAN}╭─[ OBJETIVO ]${NC}" >&2
  read -r -p "$(echo -e "${CYAN}╰─➤ ${NC}IP / dominio / rango: ")" target >&2
  
  # Trim spaces but allow CIDR ranges like 192.168.1.0/24
  target="$(echo -e "${target}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

  if [[ -z "$target" ]]; then
    msg_err "Objetivo vacío" >&2
    return 1
  fi
  printf '%s\n' "$target"
}

check_host_quick() {
  local target="$1"
  local tmp
  tmp="$(mktemp)"
  TMP_FILES+=("$tmp")

  if nmap -sn --host-timeout 15s "$target" -oG "$tmp" >/dev/null 2>&1; then
    grep -q "Status: Up" "$tmp"
    return $?
  fi
  return 1
}

run_scan() {
  local cmd=("$@")
  local start_time status duration

  [[ -z "$CURRENT_BASE" ]] && {
    msg_err "No hay ruta de salida inicializada"
    return 1
  }

  echo -e "${MAGENTA}================ SCAN OUTPUT ================${NC}"
  echo -e "${YELLOW}[...] Ejecutando:${NC} ${cmd[*]} -oA ${CURRENT_BASE}"

  start_time=$(date +%s)

  "${cmd[@]}" -oA "$CURRENT_BASE" | tee "$CURRENT_BASE.log"
  status=${PIPESTATUS[0]}
  duration=$(( $(date +%s) - start_time ))

  if [[ $status -ne 0 ]]; then
    msg_warn "Nmap reportó errores internos o fue interrumpido (código $status)"
  fi

  if [[ ! -s "$CURRENT_BASE.xml" || ! -s "$CURRENT_BASE.nmap" ]]; then
    msg_err "El escaneo no generó resultados válidos."
    return 1
  fi

  msg_ok "Scan completado en ${duration}s"
  echo -e "${BLUE}[📁] Carpeta:${NC} $CURRENT_SCAN_DIR"

  if grep -E -q '^[0-9]+/(tcp|udp)[[:space:]]+filtered' "$CURRENT_BASE.nmap"; then
    msg_warn "Puertos filtrados detectados (posible firewall)"
  fi

  return 0
}

# =========================
# PARSE / ANÁLISIS
# =========================
parse_xml_to_structured() {
  local xml_file="$1"
  local out_dir="$2"
  local json_file csv_file summary_file tmp_jq

  json_file="$out_dir/services.json"
  csv_file="$out_dir/services.csv"
  summary_file="$out_dir/summary.json"
  tmp_jq="$out_dir/.tmp_jq.json"
  TMP_FILES+=("$tmp_jq")

  [[ ! -f "$xml_file" ]] && {
    msg_err "No existe XML: $xml_file"
    return 1
  }

  echo '[]' > "$json_file"
  echo 'port,protocol,service,product,version,extrainfo' > "$csv_file"

  # FIX: Validar si hay puertos abiertos antes de intentar parsear
  if ! grep -q 'state="open"' "$xml_file"; then
    msg_warn "No se encontraron puertos abiertos en el archivo XML."
    return 1
  fi

  xmllint --xpath '//port[state/@state="open"]' "$xml_file" 2>/dev/null | \
  sed 's/<port/\n<port/g' | grep '<port' | while read -r line; do

    local port proto service product version extrainfo

    port=$(echo "$line" | grep -oP 'portid="\K[^"]+')
    proto=$(echo "$line" | grep -oP 'protocol="\K[^"]+')
    service=$(echo "$line" | grep -oP 'name="\K[^"]+' | head -1)
    product=$(echo "$line" | grep -oP 'product="\K[^"]+' | head -1)
    version=$(echo "$line" | grep -oP 'version="\K[^"]+' | head -1)
    extrainfo=$(echo "$line" | grep -oP 'extrainfo="\K[^"]+' | head -1)

    [[ -z "$port" ]] && continue

    printf '%s,%s,%s,%s,%s,%s\n' "$port" "$proto" "$service" "$product" "$version" "$extrainfo" >> "$csv_file"

    if ! jq \
      --arg port "$port" \
      --arg protocol "$proto" \
      --arg service "$service" \
      --arg product "$product" \
      --arg version "$version" \
      --arg extrainfo "$extrainfo" \
      '. += [{
        port:$port,
        protocol:$protocol,
        service:$service,
        product:$product,
        version:$version,
        extrainfo:$extrainfo
      }]' \
      "$json_file" > "$tmp_jq"; then
      msg_err "jq falló al generar services.json"
      return 1
    fi

    mv -- "$tmp_jq" "$json_file"
  done

  if ! jq '{open_ports:length, services:(map(.service) | unique | length)}' "$json_file" > "$summary_file"; then
    msg_err "jq falló al generar summary.json"
    return 1
  fi

  return 0
}

analyze_services() {
  local services_json="$1"
  local analysis_json="$2"
  local report_md="$3"
  local report_txt="$4"
  local tmp_jq

  tmp_jq="$(dirname "$analysis_json")/.analysis_tmp.json"
  TMP_FILES+=("$tmp_jq")

  [[ ! -f "$services_json" ]] && {
    msg_err "No existe services.json para analizar"
    return 1
  }

  echo '[]' > "$analysis_json"

  while IFS=$'\t' read -r port protocol service product version extrainfo; do
    [[ -z "$port" ]] && continue

    local risk="LOW"
    local criticality="No"
    local vector="Recon adicional"
    local cve="None"
    local notes=""

    case "${service,,}" in
      ssh)
        risk="MEDIUM"; criticality="Sí"; vector="Bruteforce, versiones antiguas de OpenSSH"; notes="Revisar rate limiting y hardening" ;;
      ftp)
        risk="HIGH"; criticality="Sí"; vector="Anonymous login, subida de archivos"; notes="Comprobar anonymous login y TLS" ;;
      telnet)
        risk="CRITICAL"; criticality="Sí"; vector="Credenciales en claro, MITM"; notes="Servicio inseguro por diseño" ;;
      http|https)
        risk="MEDIUM"; criticality="Sí"; vector="XSS, SQLi, LFI/RFI, RCE web"; notes="Revisar headers, CMS y tecnologías detectadas" ;;
      smb|microsoft-ds|netbios-ssn)
        risk="CRITICAL"; criticality="Sí"; vector="SMB relay, EternalBlue, shares expuestos"; cve="CVE-2017-0144 (heurístico)"; notes="Revisar SMBv1" ;;
      mysql|ms-sql-s|postgresql|oracle)
        risk="HIGH"; criticality="Sí"; vector="Acceso BBDD, creds débiles"; notes="Verificar exposición externa" ;;
      rdp|ms-wbt-server)
        risk="HIGH"; criticality="Sí"; vector="BlueKeep, fuerza bruta"; cve="CVE-2019-0708 (heurístico)"; notes="Comprobar NLA y exposición" ;;
      vnc)
        risk="HIGH"; criticality="Sí"; vector="Acceso remoto inseguro"; notes="Revisar cifrado" ;;
      ldap|kerberos-sec)
        risk="HIGH"; criticality="Sí"; vector="Ataque AD, AS-REP roasting"; notes="Entorno de AD potencial" ;;
      dns|domain)
        risk="MEDIUM"; criticality="Sí"; vector="AXFR, amplificación"; notes="Comprobar transferencias de zona" ;;
      smtp|pop3|imap)
        risk="MEDIUM"; criticality="Sí"; vector="User enum, relay, STARTTLS débil"; notes="Probar VRFY/EXPN/relay" ;;
      snmp)
        risk="HIGH"; criticality="Sí"; vector="Comunidades por defecto, fuga info"; notes="Verificar versión SNMP" ;;
      redis|mongodb|memcached|elasticsearch)
        risk="CRITICAL"; criticality="Sí"; vector="BBDD expuesta, fuga de datos"; notes="Revisar autenticación local" ;;
      docker|docker-registry)
        risk="CRITICAL"; criticality="Sí"; vector="Escalada a host, fuga de imágenes"; notes="No exponer Docker sin protección" ;;
      *)
        risk="LOW"; criticality="No"; vector="Análisis manual"; notes="Servicio genérico" ;;
    esac

    local blob="${service} ${product} ${version} ${extrainfo}"
    shopt -s nocasematch
    if [[ "$blob" =~ openssh[[:space:]]*7\.[0-4] ]]; then
      cve="Posible CVE-2018-15473 (heurístico)"
      [[ "$risk" == "LOW" ]] && risk="MEDIUM"
    elif [[ "$blob" =~ apache[[:space:]]*2\.4\.49|apache[[:space:]]*2\.4\.50 ]]; then
      cve="Posible CVE-2021-41773 / CVE-2021-42013"
      risk="HIGH"
    elif [[ "$blob" =~ samba[[:space:]]*3\.|samba[[:space:]]*4\.[0-6] ]]; then
      cve="Posibles CVE históricas en Samba"
      [[ "$risk" == "LOW" ]] && risk="HIGH"
    elif [[ "$blob" =~ vsftpd[[:space:]]*2\.3\.4 ]]; then
      cve="Posible CVE-2011-2523 (backdoor)"
      risk="CRITICAL"
    fi
    shopt -u nocasematch

    if ! jq \
      --arg port "$port" \
      --arg protocol "$protocol" \
      --arg service "$service" \
      --arg product "$product" \
      --arg version "$version" \
      --arg extrainfo "$extrainfo" \
      --arg risk "$risk" \
      --arg criticality "$criticality" \
      --arg vector "$vector" \
      --arg cve "$cve" \
      --arg notes "$notes" \
      '. += [{port:$port, protocol:$protocol, service:$service, product:$product, version:$version, extrainfo:$extrainfo, risk:$risk, critical_service:$criticality, attack_vector:$vector, potential_cve:$cve, notes:$notes}]' \
      "$analysis_json" > "$tmp_jq"; then
      msg_err "jq falló al generar analysis.json"
      return 1
    fi
    mv -- "$tmp_jq" "$analysis_json"
  done < <(jq -r '.[] | [.port,.protocol,.service,.product,.version,.extrainfo] | @tsv' "$services_json")

  generate_report "$analysis_json" "$report_md" "$report_txt"
}

generate_report() {
  local analysis_json="$1"
  local report_md="$2"
  local report_txt="$3"
  local total critical_count high_count medium_count

  total=$(jq 'length' "$analysis_json")
  critical_count=$(jq '[.[] | select(.risk=="CRITICAL")] | length' "$analysis_json")
  high_count=$(jq '[.[] | select(.risk=="HIGH")] | length' "$analysis_json")
  medium_count=$(jq '[.[] | select(.risk=="MEDIUM")] | length' "$analysis_json")

  {
    echo "# Informe automático de análisis"
    echo
    echo "- Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- Servicios abiertos analizados: $total"
    echo "- Riesgo CRITICAL: $critical_count"
    echo "- Riesgo HIGH: $high_count"
    echo "- Riesgo MEDIUM: $medium_count"
    echo
    echo "## Hallazgos"
    echo
    jq -r '.[] | "### Puerto " + .port + "/" + .protocol + " – " + (.service // "unknown") + "\n" +
      "- Producto: " + ((.product // "") | if .=="" then "N/D" else . end) + "\n" +
      "- Versión: " + ((.version // "") | if .=="" then "N/D" else . end) + "\n" +
      "- Riesgo: " + .risk + "\n" +
      "- Servicio crítico: " + .critical_service + "\n" +
      "- Vector de ataque: " + .attack_vector + "\n" +
      "- Posible CVE: " + .potential_cve + "\n" +
      "- Notas: " + .notes + "\n"' "$analysis_json"
  } > "$report_md"

  {
    echo "INFORME AUTOMÁTICO DE ANÁLISIS"
    echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Servicios analizados: $total"
    echo "CRITICAL: $critical_count | HIGH: $high_count | MEDIUM: $medium_count"
    echo
    jq -r '.[] | "[*] Puerto " + .port + "/" + .protocol + " - " + (.service // "unknown") +
      " | Riesgo: " + .risk +
      " | CVE: " + .potential_cve +
      " | Vector: " + .attack_vector' "$analysis_json"
  } > "$report_txt"
}

run_pipeline_analysis() {
  local xml_file="$1"
  local out_dir="$2"
  local services_json analysis_json report_md report_txt

  services_json="$out_dir/services.json"
  analysis_json="$out_dir/analysis.json"
  report_md="$out_dir/report.md"
  report_txt="$out_dir/report.txt"

  parse_xml_to_structured "$xml_file" "$out_dir" || return 1
  analyze_services "$services_json" "$analysis_json" "$report_md" "$report_txt" || return 1
  cleanup # Limpiamos basura temporal aquí
  return 0
}

# =========================
# FUNCIONES DE ESCANEO
# =========================
do_fast_scan() {
  local target="$1"
  create_scan_dir "FastScan" "$target" || return 1
  run_scan nmap "$SCAN_TYPE" -T4 -F --host-timeout 2m "$target"
}

do_aggressive_scan() {
  local target="$1"
  create_scan_dir "AggressiveScan" "$target" || return 1
  run_scan nmap "$SCAN_TYPE" -A -T4 --host-timeout 3m "$target"
}

do_auto_scan() {
  local target="$1"
  local temp_file open_ports

  create_scan_dir "AutoScan" "$target" || return 1

  msg_info "Comprobando si el host responde..."
  if ! check_host_quick "$target"; then
    msg_warn "El host no respondió. Pruebo con -Pn en el escaneo de puertos."
  fi

  msg_info "Fase 1: descubrimiento de puertos abiertos"
  temp_file="$CURRENT_SCAN_DIR/initial_scan.gnmap"

  if ! nmap -p- --open "$SCAN_TYPE" -n --min-rate 1000 --max-retries 2 "$target" -oG "$temp_file" >/dev/null 2>&1; then
    msg_err "Falló el descubrimiento inicial de puertos"
    return 1
  fi

  open_ports=$(grep '/open/' "$temp_file" | cut -d '/' -f1 | paste -sd ',' -)

  if [[ -z "$open_ports" ]]; then
    msg_warn "No hay puertos abiertos detectados accesibles."
    return 0
  fi

  msg_ok "Puertos detectados: $open_ports"
  msg_info "Fase 2: análisis detallado de servicios"

  run_scan nmap "$SCAN_TYPE" -sV $OS_FLAG -sC -p "$open_ports" "$target"
}

do_multi_target_scan() {
  local file ip

  echo -e "${CYAN}╭─[ ARCHIVO DE OBJETIVOS ]${NC}"
  read -r -p "$(echo -e "${CYAN}╰─➤ ${NC}Ruta del archivo con IPs/hosts: ")" file

  if [[ ! -f "$file" ]]; then
    msg_err "Archivo no encontrado"
    return 1
  fi

  while IFS= read -r ip || [[ -n "$ip" ]]; do
    ip="$(printf '%s' "$ip" | tr -d '[:space:]')"
    [[ -z "$ip" || "$ip" =~ ^# ]] && continue

    msg_info "Escaneando $ip"
    create_scan_dir "MultiTarget" "$ip" || continue
    run_scan nmap "$SCAN_TYPE" -sV --host-timeout 2m "$ip" || msg_warn "Error escaneando $ip"
  done < "$file"
}

do_full_pro_scan() {
  local target="$1"

  create_scan_dir "FullProScan" "$target" || return 1
  run_scan nmap "$SCAN_TYPE" -A --script vuln,safe --host-timeout 4m "$target" || return 1

  msg_info "Ejecutando pipeline de parseo y análisis..."
  if run_pipeline_analysis "$CURRENT_BASE.xml" "$CURRENT_SCAN_DIR"; then
     msg_ok "Análisis completado: JSON, CSV e informe generados"
  else
     msg_err "El pipeline de análisis se abortó."
  fi
}

do_udp_scan() {
  local target="$1"

  if [[ $IS_ROOT -ne 1 ]]; then
    msg_err "UDP Scan requiere root"
    return 1
  fi

  create_scan_dir "UDPScan" "$target" || return 1
  run_scan nmap -sU -F -sV --version-intensity 0 --host-timeout 3m "$target"
}

do_evasion_scan() {
  local target="$1"

  msg_info "Fase 1: test rápido de filtrado"
  create_scan_dir "EvasionInitial" "$target" || return 1

  if ! nmap -T4 -F "$target" -oG "$CURRENT_BASE.gnmap" >/dev/null 2>&1; then
    msg_err "Falló el test inicial de firewall"
    return 1
  fi

  if grep -q 'filtered' "$CURRENT_BASE.gnmap"; then
    msg_warn "Filtrado detectado → aplicando evasión suave"
    create_scan_dir "EvasionAdvanced" "$target" || return 1

    if [[ $IS_ROOT -eq 1 ]]; then
      run_scan nmap "$SCAN_TYPE" -Pn -n -f -T2 --scan-delay 100ms --max-retries 2 --data-length 16 "$target"
    else
      run_scan nmap "$SCAN_TYPE" -Pn -n -T2 --scan-delay 100ms --max-retries 2 "$target"
    fi
  else
    msg_ok "No se detecta filtrado fuerte → escaneo normal avanzado"
    create_scan_dir "EvasionNormal" "$target" || return 1
    run_scan nmap "$SCAN_TYPE" -A --host-timeout 3m "$target"
  fi
}

do_analyze_existing_xml() {
  local xml

  echo -e "${CYAN}╭─[ XML EXISTENTE ]${NC}"
  read -r -p "$(echo -e "${CYAN}╰─➤ ${NC}Ruta del XML: ")" xml

  if [[ ! -f "$xml" ]]; then
    msg_err "No existe el XML indicado"
    return 1
  fi

  create_scan_dir "ParsedXML" "existing" || return 1
  cp -- "$xml" "$CURRENT_BASE.xml" || {
    msg_err "No se pudo copiar el XML al directorio de trabajo"
    return 1
  }

  msg_info "Parseando..."
  run_pipeline_analysis "$CURRENT_BASE.xml" "$CURRENT_SCAN_DIR" || return 1
  msg_ok "Análisis completado sobre XML existente"
}

# =========================
# MAIN
# =========================
main() {
  local opt target

  init_runtime

  banner
  set_output_dir || exit 1

  while true; do
    echo
    print_menu
    echo -e "${CYAN}╭─[ SELECCIÓN ]${NC}"
    read -r -p "$(echo -e "${CYAN}╰─➤ ${NC}Opción: ")" opt

    case "$opt" in
      1)
        target=$(ask_target) || continue
        do_fast_scan "$target"
        pause
        ;;
      2)
        target=$(ask_target) || continue
        do_aggressive_scan "$target"
        pause
        ;;
      3)
        target=$(ask_target) || continue
        do_auto_scan "$target"
        pause
        ;;
      4)
        do_multi_target_scan
        pause
        ;;
      5)
        target=$(ask_target) || continue
        do_full_pro_scan "$target"
        pause
        ;;
      6)
        target=$(ask_target) || continue
        do_udp_scan "$target"
        pause
        ;;
      7)
        target=$(ask_target) || continue
        do_evasion_scan "$target"
        pause
        ;;
      8)
        do_analyze_existing_xml
        pause
        ;;
      9)
        msg_ok "Hasta luego."
        exit 0
        ;;
      *)
        msg_err "Opción inválida"
        sleep 1
        ;;
    esac
  done
}

main "$@"
