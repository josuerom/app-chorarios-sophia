"""Archivo de configuración general del proyecto."""

EXCEL_FILE = "data/chorarios.xlsx"
OUTPUT_FILE = "output/resultados_entrenamiento_phi4.jsonl"
# N_EJEMPLOS = 4999
N_EJEMPLOS = 20
MAX_CREDITOS = 18

RANGOS_HORARIOS = {
   "mañana": (6, 12),
   "tarde": (12, 18),
   "noche": (18, 22)
}
