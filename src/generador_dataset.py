import json
from src.funciones_auxiliares import curso_en_turno, hay_cruce
from src.configuracion import MAX_CREDITOS
from itertools import combinations, product
import pandas as pd


def extraer_info_prompt(prompt, df):
   """Extrae información relevante del texto del usuario."""
   info = {"materias": [], "docente": None, "dias": [], "facultad": None, "turno": None, "virtual": False}
   prompt_lower = prompt.lower()

   if "mañana" in prompt_lower: info["turno"] = "mañana"
   elif "tarde" in prompt_lower: info["turno"] = "tarde"
   elif "noche" in prompt_lower: info["turno"] = "noche"

   if "virtual" in prompt_lower: info["virtual"] = True

   mapa_dias = {"lunes": "L", "martes": "M", "miércoles": "I", "jueves": "J", "viernes": "V", "sábado": "S"}
   for k, v in mapa_dias.items():
      if k in prompt_lower: info["dias"].append(v)

   for titulo in df["TITULO"].dropna().unique():
      if titulo.lower() in prompt_lower:
         info["materias"].append(titulo)

   return info


def encontrar_mejores_horarios(df, info):
   """Encuentra las mejores combinaciones de horarios sin cruces."""
   materias = info.get("materias", [])
   if not materias:
      return []

   opciones_por_materia = []
   for materia in materias:
      df_materia = df[df["TITULO"] == materia]
      mascara = pd.Series(True, index=df_materia.index)
      if info.get("turno"):
         mascara &= df_materia.apply(curso_en_turno, axis=1, turno=info["turno"])
      opciones_por_materia.append(df_materia[mascara].to_dict("records"))

   horarios = []
   for k in range(len(materias), 0, -1):
      for subset_indices in combinations(range(len(materias)), k):
         subset = [opciones_por_materia[i] for i in subset_indices if opciones_por_materia[i]]
         if len(subset) != k:
               continue
         for combinacion in product(*subset):
               horario = list(combinacion)
               creditos = sum(c.get("CREDITO", 0) for c in horario)
               if creditos > MAX_CREDITOS:
                  continue
               if not any(hay_cruce(horario[i], horario[j]) for i in range(k) for j in range(i + 1, k)):
                  puntaje = len(horario) * 10
                  horarios.append({"horario": horario, "puntaje": puntaje, "creditos": creditos})
      if horarios:
         break
   return horarios[:3]


def formatear_respuesta_top3(opciones, info):
   """Genera texto explicativo con las tres mejores combinaciones."""
   if not opciones:
      return "No se encontró ninguna combinación viable."
   salida = []
   for i, opcion in enumerate(opciones):
      salida.append(f"Opción {i+1} - Créditos: {opcion['creditos']}")
      for curso in opcion["horario"]:
         salida.append(f"- {curso['TITULO']} ({curso['NRC']})")
   return "\n".join(salida)


def generar_dataset(df_cursos, prompts, ruta_salida):
   """Genera y guarda el dataset de entrenamiento."""
   dataset = []
   for i, prompt in enumerate(prompts):
      info = extraer_info_prompt(prompt, df_cursos)
      opciones = encontrar_mejores_horarios(df_cursos, info)
      respuesta = formatear_respuesta_top3(opciones, info)
      dataset.append({"prompt": prompt, "response": respuesta})

   with open(ruta_salida, "w", encoding="utf-8") as f:
      for item in dataset:
         f.write(json.dumps(item, ensure_ascii=False) + "\n")

   print(f"🎉 Dataset generado con {len(dataset)} ejemplos.")
