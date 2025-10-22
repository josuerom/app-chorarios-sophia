import pandas as pd
from itertools import combinations, product
from src.configuracion import MAX_CREDITOS, RANGOS_HORARIOS


def normalizar_hora(valor):
   """Convierte un valor numérico a formato HH:MM."""
   if pd.isna(valor) or valor == "":
      return ""
   try:
      valor = int(valor)
      h, m = divmod(valor, 100)
      return f"{h:02d}:{m:02d}"
   except (ValueError, TypeError):
      return ""


def hay_cruce_entre_bloques(bloque_a, bloque_b):
   """Verifica si hay cruce horario entre dos bloques."""
   for dia in bloque_a["dias"]:
      if dia in bloque_b["dias"]:
         if not (bloque_a["HF"] <= bloque_b["HI"] or bloque_b["HF"] <= bloque_a["HI"]):
               return True
   return False


def hay_cruce(curso_a, curso_b):
   """Determina si dos cursos se cruzan en horario."""
   for bloque_a in curso_a["horarios"]:
      for bloque_b in curso_b["horarios"]:
         if hay_cruce_entre_bloques(bloque_a, bloque_b):
               return True
   return False


def curso_en_turno(curso, turno):
   """Verifica si un curso pertenece a un turno específico."""
   if not turno:
      return True
   for bloque in curso["horarios"]:
      hi = bloque.get("HI")
      if not hi:
         continue
      try:
         hi_h = int(hi.split(":")[0])
         inicio, fin = RANGOS_HORARIOS[turno]
         if inicio <= hi_h < fin:
               return True
      except (ValueError, IndexError):
         continue
   return False
