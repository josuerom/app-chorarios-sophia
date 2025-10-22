import json
import random
import openai
import sys
import io

# 🔧 Garantizar UTF-8 para todo el entorno (evita errores de ascii)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Solo configurar la salida UTF-8 si existe sys.stdout (en modo consola)
# if sys.stdout and hasattr(sys.stdout, "buffer"):
   # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def generar_prompts_con_openai(df_cursos, n_prompts_lote=50):
   """Genera prompts utilizando la API de OpenAI sin errores de codificación."""
   try:
      api_key = "API_KEY"
      client = openai.OpenAI(api_key=api_key)
   except Exception as e:
      print(f"🚨 Error al inicializar OpenAI: {e}")
      return None

   try:
      materias = df_cursos["TITULO"].dropna().unique().tolist()
      facultades = df_cursos["FACULTAD_RESPONSABLE"].dropna().unique().tolist()

      # 🔠 Forzar UTF-8 al construir el prompt
      materias = [str(m).encode('utf-8', errors='ignore').decode('utf-8') for m in materias]
      facultades = [str(f).encode('utf-8', errors='ignore').decode('utf-8') for f in facultades]

      meta_prompt = f"""
      Genera {n_prompts_lote} prompts en español para inscripción de cursos universitarios.
      Materias de ejemplo: {random.sample(materias, min(30, len(materias)))}
      Facultades: {facultades}
      Reglas:
      1. Pide entre 1 y 9 materias.
      2. Usa solo materias reales.
      3. Varía turno, días y facultad.
      Devuelve un JSON con formato:
      {{
         "prompts": ["texto del prompt 1", "texto del prompt 2", ...]
      }}
      """

      completion = client.chat.completions.create(
         model="gpt-4o",
         messages=[
            {"role": "system", "content": "Eres un generador de prompts JSON."},
            {"role": "user", "content": meta_prompt},
         ],
         response_format={"type": "json_object"}
      )

      data = json.loads(completion.choices[0].message.content)
      prompts = data.get("prompts", [])

      # 🔍 Normalizar cualquier tipo de salida a texto puro
      prompts_limpios = []
      for p in prompts:
         if isinstance(p, dict):
            texto = p.get("prompt") or p.get("texto") or str(p)
         else:
            texto = str(p)
         texto = texto.encode('utf-8', errors='ignore').decode('utf-8').strip()
         prompts_limpios.append(texto)

      if not prompts_limpios:
         raise ValueError("La respuesta de la API no contenía prompts válidos.")

      print(f"   ✅ Recibidos {len(prompts_limpios)} prompts correctamente.")
      return prompts_limpios

   except Exception as e:
      print(f"🚨 Error al generar prompts: {e}")
      return None
