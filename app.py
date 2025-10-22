import time
import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox
from tkinter import ttk
from src.configuracion import EXCEL_FILE, OUTPUT_FILE, N_EJEMPLOS
from src.procesar_datos import procesar_datos_agrupados
from src.openai_api import generar_prompts_con_openai
from src.generador_dataset import generar_dataset


# =============================================
# Interfaz gráfica para generar dataset Sophia
# =============================================

class App:
   def __init__(self, root):
      self.root = root
      self.root.title("Generador de Dataset - Grupo Chorarios")
      self.root.geometry("590x340")
      self.root.resizable(False, False)
      self.root.configure(bg="#F8F9FA")

      # --- Estilo general ---
      style = ttk.Style()
      style.configure("TLabel", font=("Segoe UI", 10), background="#F8F9FA")
      style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
      style.configure("TEntry", font=("Segoe UI", 10))

      # --- Título ---
      ttk.Label(root, text="📘 Generador de Dataset", font=("Segoe UI", 16, "bold"),
               background="#F8F9FA").pack(pady=10)

      # --- Archivo Excel ---
      frame_excel = ttk.Frame(root)
      frame_excel.pack(pady=10)
      ttk.Label(frame_excel, text="Archivo Excel de horarios (.csv): ").grid(row=0, column=0, padx=5)
      self.excel_path = tk.StringVar()
      ttk.Entry(frame_excel, textvariable=self.excel_path, width=45).grid(row=0, column=1)
      ttk.Button(frame_excel, text="📂 Explorar", command=self.seleccionar_excel).grid(row=0, column=2, padx=5)

      # --- Número de ejemplos ---
      frame_num = ttk.Frame(root)
      frame_num.pack(pady=10)
      ttk.Label(frame_num, text="Número de ejemplos a generar: ").grid(row=0, column=0, padx=5)
      self.num_ejemplos = tk.StringVar()
      ttk.Entry(frame_num, textvariable=self.num_ejemplos, width=10).grid(row=0, column=1)

      # --- Archivo de salida ---
      frame_salida = ttk.Frame(root)
      frame_salida.pack(pady=10)
      ttk.Label(frame_salida, text="Archivo de salida (.jsonl): ").grid(row=0, column=0, padx=5)
      self.output_path = tk.StringVar()
      ttk.Entry(frame_salida, textvariable=self.output_path, width=45).grid(row=0, column=1)
      ttk.Button(frame_salida, text="💾 Guardar como...", command=self.seleccionar_salida).grid(row=0, column=2, padx=5)

      # --- Botón principal ---
      self.btn_generar = ttk.Button(root, text="🚀 Generar Dataset", command=self.generar_dataset)
      self.btn_generar.pack(pady=20)

      # --- Asignar tecla Enter ---
      self.root.bind("<Return>", lambda event: self.generar_dataset())

      # --- Mensaje inferior ---
      ttk.Label(root, text="Desarrollado por Semillero Sophia - Uniminuto 10/2025",
               font=("Segoe UI", 9, "italic"), background="#F8F9FA").pack(side="bottom", pady=10)

   # ------------------------------
   # Métodos auxiliares
   # ------------------------------

   def seleccionar_excel(self):
      ruta = filedialog.askopenfilename(
         title="Seleccionar archivo Excel",
         filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
      )
      if ruta:
         self.excel_path.set(ruta)

   def seleccionar_salida(self):
      ruta = filedialog.asksaveasfilename(
         title="Guardar archivo de salida",
         defaultextension=".jsonl",
         filetypes=[("Archivos Excel", "*.jsonl"), ("Todos los archivos", "*.*")]
      )
      if ruta:
         self.output_path.set(ruta)

   def generar_dataset(self):
      """Validación inicial antes de ejecutar el proceso."""
      archivo_excel = self.excel_path.get().strip()
      archivo_salida = self.output_path.get().strip()
      num_ejemplos = self.num_ejemplos.get().strip()

      if not archivo_excel:
         messagebox.showwarning("Campo faltante", "Por favor selecciona el archivo Excel de horarios.")
         return
      if not num_ejemplos.isdigit():
         messagebox.showwarning("Dato inválido", "El número de ejemplos debe ser un número entero.")
         return
      if not archivo_salida:
         messagebox.showwarning("Campo faltante", "Por favor selecciona la ruta del archivo de salida.")
         return

      # Mostrar confirmación antes de ejecutar
      messagebox.showinfo("Confirma los siguientes datos:",
                           f"✅ Archivo de entrada:\n{archivo_excel}\n\n"
                           f"📦 Ejemplos a generar: {num_ejemplos}\n\n"
                           f"💾 Archivo de salida:\n{archivo_salida}")

      # Llamar al proceso completo
      self.arranque_del_programa(archivo_excel, int(num_ejemplos), archivo_salida)

   def arranque_del_programa(self, archivo_excel, num_ejemplos, archivo_salida):
      """Ejecuta el flujo completo del proyecto."""
      try:
         print("➡️ [Paso 1] Leyendo y procesando el archivo Excel...")
         dataframe = pd.read_excel(archivo_excel)
         df_cursos = procesar_datos_agrupados(dataframe)
         print(f"✅ [Paso 2] Datos procesados. Se encontraron {len(df_cursos)} cursos únicos.")
      except Exception as e:
         print(f"🚨 ¡ERROR! Al leer o procesar el Excel: {e}")
         messagebox.showerror("Error", f"Error al procesar el archivo Excel:\n{e}")
         return

      todos_los_prompts = []
      tamano_lote = 50

      print(f"➡️ [Paso 3] Conectando con OpenAI para generar {num_ejemplos} prompts en lotes de {tamano_lote}...")
      while len(todos_los_prompts) < num_ejemplos:
         faltantes = num_ejemplos - len(todos_los_prompts)
         lote_actual = min(tamano_lote, faltantes)

         print(f"   ... Pidiendo un lote de {lote_actual} prompts...")
         nuevos_prompts = generar_prompts_con_openai(df_cursos, n_prompts_lote=lote_actual)

         if nuevos_prompts:
            todos_los_prompts.extend(nuevos_prompts)
            print(f"   ... Recibidos {len(nuevos_prompts)} prompts. Total: {len(todos_los_prompts)}.")
         else:
            print("   ... No se recibieron prompts. Reintentando en 5 segundos...")
            time.sleep(5)

         time.sleep(1)

      print("➡️ [Paso 4] Generando dataset final...")
      generar_dataset(df_cursos, todos_los_prompts, archivo_salida)
      print(f"✅ Dataset generado exitosamente en {archivo_salida}")
      messagebox.showinfo("Completado", f"El dataset ha sido generado exitosamente en:\n{archivo_salida}")


if __name__ == "__main__":
   root = tk.Tk()
   app = App(root)
   root.mainloop()
