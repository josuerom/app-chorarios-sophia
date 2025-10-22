import pandas as pd
from src.funciones_auxiliares import normalizar_hora


def procesar_datos_agrupados(df):
   """Procesa y consolida los cursos del archivo Excel."""
   cursos_consolidados = []
   if "NRC" not in df.columns:
      raise ValueError("El archivo Excel debe contener la columna 'NRC'.")

   for nrc, grupo in df.groupby("NRC"):
      registro = grupo.iloc[0].to_dict()
      curso = {
         "NRC": nrc,
         "TITULO": registro.get("TITULO", "Sin Título"),
         "CREDITO": registro.get("CREDITO", 0),
         "NOMBRE_DOCENTE": registro.get("NOMBRE_DOCENTE", "Por asignar"),
         "SEDE": registro.get("SEDE", ""),
         "EDIFICIO": registro.get("EDIFICIO", ""),
         "FACULTAD_RESPONSABLE": registro.get("FACULTAD_RESPONSABLE", ""),
         "horarios": []
      }

      for _, fila in grupo.iterrows():
         dias = [d for d in ['L', 'M', 'I', 'J', 'V', 'S', 'D'] if pd.notna(fila.get(d)) and str(fila[d]).strip()]
         if dias:
            curso["horarios"].append({
               "dias": dias,
               "HI": normalizar_hora(fila.get("HI", "")),
               "HF": normalizar_hora(fila.get("HF", ""))
            })

      if curso["horarios"]:
         cursos_consolidados.append(curso)

   return pd.DataFrame(cursos_consolidados)
