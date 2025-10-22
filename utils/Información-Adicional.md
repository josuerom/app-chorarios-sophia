# App-Chorarios-Sophia

**Generador de Dataset de Horarios Universitarios**

Una aplicación de escritorio desarrollada en **Python** con interfaz gráfica que genera datasets de horarios académicos sin cruces, útil para entrenar modelos de lenguaje (por ejemplo **Phi-3**) que aprendan a sugerir horarios válidos.

---

## 🧩 Descripción general

Esta herramienta permite cargar datos de asignaturas, bloques horarios y restricciones académicas, y genera combinaciones válidas de horarios sin conflictos.  
El dataset resultante está listo para ser usado en entrenamiento o ajuste fino (*fine-tuning*) de modelos de IA capaces de proponer horarios automáticos.

La aplicación cuenta con una interfaz amigable que facilita la carga de archivos desde la carpeta `data/`, la ejecución del proceso de validación y generación, y la exportación de resultados a la carpeta `output/`.

---

## ⚙️ Requisitos

- **Python 3.8
- Bibliotecas incluidas en `requirements.txt`
- Sistema operativo con soporte para GUI (Windows / Linux / MacOS)
- Archivos de entrada en carpeta `data/`

---

## 🚀 Instalación y ejecución

```bash
# Clonar repositorio
git clone https://github.com/josuerom/app-chorarios-sophia.git
cd app-chorarios-sophia

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

También se incluyen scripts por lotes (por ejemplo RunApp.bat o BuildProject.bat) para facilitar la ejecución o compilación en Windows.

## 📂 Estructura del proyecto

```readme
app-chorarios-sophia/
│
│   app.py                  # Punto de entrada principal
│   requirements.txt         # Dependencias del proyecto
│   BuildProject.bat         # Script para construir el proyecto
│   RunApp.bat               # Script para ejecutar la aplicación
│
├── data/                    # Archivos de entrada (ej. Excel, CSV)
│
├── output/                  # Resultados y datasets generados
│
├── dist/                    # Archivos compilados o de distribución
│
├── src/                     # Módulos principales del programa
│   ├── generador.py         # Lógica de generación de horarios
│   ├── validador.py         # Validación de conflictos
│   └── gui_backend.py       # Control de la interfaz gráfica
│
├── utils/                   # Funciones auxiliares
│   ├── helpers.py
│   └── file_manager.py
│
└── static/                  # Recursos estáticos (iconos, imágenes)
```

## 🔍 Cómo funciona internamente

1. app.py inicia la interfaz gráfica y gestiona la interacción con el usuario.

2 El usuario carga los archivos de entrada desde la carpeta data/.

3. Los módulos en src/ procesan los datos: leen, validan y generan combinaciones de horarios sin superposición.

4. Los resultados se transforman en registros estructurados y se exportan a output/ en formatos como CSV, JSON o Excel.

5. Los scripts en utils/ manejan tareas auxiliares (validación, logging, manejo de archivos, conversión de formatos).

6. La carpeta static/ almacena los recursos visuales utilizados por la GUI.

7. La carpeta dist/ puede contener ejecutables o versiones empaquetadas del proyecto.

## 🧠 Posibles mejoras / Extensiones futuras

- Validaciones más complejas (profesor, aula, prerrequisitos).

- Exportación en múltiples formatos (Excel, CSV, JSON, TXT).

- Configuración avanzada desde la interfaz (número máximo de paralelos, preferencias de horario).

- Registro de logs y reportes de calidad del dataset.

- Empaquetado multiplataforma (instaladores).

- Integración con modelos de IA para retroalimentación automática del dataset generado.

## 🤖 Uso para IA / Generación de diagramas

La estructura modular del proyecto facilita su comprensión por parte de herramientas de inteligencia artificial.
Cualquier IA puede analizar este repositorio para generar automáticamente:

* Diagrama de arquitectura: flujo de datos desde data/ → src/ → output/.

* Diagrama de flujo de usuario-GUI: “Cargar datos → Configurar parámetros → Ejecutar generación → Exportar resultados”.

* Diagrama UML de clases: con entidades como Asignatura, BloqueHorario, Restricción, GeneradorHorarios, DatasetWriter.

* Plan de desarrollo o roadmap: etapas de carga, validación, generación, exportación y empaquetado.

## 👨‍💻 Autores

Josué Romero - Jhon Castiblanco

Universidad Minuto de Dios – Ingeniería de Sistemas

Desarrolladores del proyecto Chorarios Semillero Sophia Octubre 2025


## ©️ Contribuidores

Andres Guerra - Hermes Arias

Universidad Minuto de Dios – Ingeniería de Sistemas

Planitificadores y diseñadores del proyecto Chorarios Semillero Sophia Octubre 2025


## 👜 Repositorio

Ubicación oficial: https://github.com/josuerom/app-chorarios-sophia