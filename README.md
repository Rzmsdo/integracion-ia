# Proyecto de integración de una IA en local

Voy a tratar de serguir los pasos de varios turoriales que encontré para añadir una IA a nuestros proyectos de forma local sin acceso a internet. Sera menos eficiente que las que encontramos pero vamos a ver hasta donde llegamos.

Una vez finalizado comentaré resultado.

Desarrollado con Python

Inicio::

-Instalar ollma (codespace(linux))

Visitar la web de Ollama -Download -Linux -->

curl -fsSL https://ollama.com/install.sh | sh 



Ver comandos: (en la terminal) ollama

    Comandos:
 
 Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model
  show        Show information for a model
  # Proyecto: IA local con Ollama

  Este proyecto documenta los pasos básicos para instalar y ejecutar un modelo de lenguaje localmente usando Ollama en un entorno Linux (por ejemplo, GitHub Codespaces). El objetivo es poder usar un LLM sin dependencia de Internet.

  Estado: guía de instalación y uso (con ejemplos y notas prácticas).

  Requisitos

  - Sistema operativo: Linux (Ubuntu recomendado)
  - Acceso a la terminal
  - Espacio en disco suficiente (los modelos pueden ocupar varios GB)
  - Python (opcional si vas a integrar el modelo en una app)

  Instalación de Ollama

  1. Desde la terminal, ejecutar el instalador oficial:

  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

  2. Comprobar que `ollama` está instalado:

  ```bash
  ollama --version
  ```

  Comandos útiles de `ollama`

  - `serve`   — Inicia el servidor de Ollama
  - `create`  — Crea un modelo
  - `show`    — Muestra información de un modelo
  - `run`     — Ejecuta un modelo
  - `stop`    — Detiene un modelo en ejecución
  - `pull`    — Descarga un modelo desde el registro
  - `push`    — Sube un modelo al registro
  - `signin` / `signout` — Gestión de sesión
  - `list`    — Lista modelos instalados
  - `ps`      — Lista modelos en ejecución
  - `rm`      — Elimina un modelo

  Para ver la ayuda de cualquier comando:

  ```bash
  ollama <comando> --help
  ```

  Ejemplo: instalar y ejecutar Llama 3.2 (ejemplo)

  > Nota: `llama3.2` es un ejemplo; usa la versión disponible que prefieras.

  1. Descargar el modelo (puede tardar y ocupar GB):

  ```bash
  ollama pull llama3.2
  ```

  2. Verificar la instalación:

  ```bash
  ollama list
  ```

  Salida esperada (ejemplo):

  ```
  NAME               ID              SIZE      MODIFIED
  llama3.2:latest    a80c4f17acd5    ~2.0 GB   About a minute ago
  ```

  3. Ejecutar el modelo en la terminal:

  ```bash
  ollama run llama3.2
  ```

  Opciones prácticas

  - Ejecutar como servidor (si tu versión de Ollama lo soporta):

  ```bash
  ollama serve
  ```

  - Enviar un prompt directamente:

  ```bash
  ollama run llama3.2 --prompt "Escribe un resumen breve sobre X"
  ```

  Recomendaciones

  - Los modelos requieren mucha RAM/CPU; si no tienes GPU la inferencia será lenta.
  - Vigila el espacio en disco; elimina modelos con `ollama rm <nombre>` cuando no los uses.
  - Consulta la documentación oficial de Ollama para opciones avanzadas y configuración.

  Integración con Python (siguiente paso)

  Aquí tienes un ejemplo práctico para invocar Ollama usando la CLI desde Python. Este enfoque es útil cuando no hay una API HTTP disponible o deseas integrar rápido la CLI en un script. Requiere que `ollama` esté instalado y en el `PATH`, y que el modelo (por ejemplo `llama3.2`) esté previamente descargado con `ollama pull`.

  Ejemplo 1 — usando subprocess (sin lista de args, forma sencilla):

  ```python
  import subprocess
  import shlex

  def run_ollama_prompt(model='llama3.2', prompt='Escribe un resumen breve sobre X', timeout=60):
    # Construye el comando de forma segura
    cmd = f"ollama run {shlex.quote(model)} --prompt {shlex.quote(prompt)}"
    try:
      result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, timeout=timeout)
      return result.stdout.strip()
    except subprocess.CalledProcessError as e:
      raise RuntimeError(f"El comando falló (codigo {e.returncode}): {e.stderr}") from e
    except subprocess.TimeoutExpired:
      raise RuntimeError("El comando tardó demasiado y se agotó el tiempo.")

  if __name__ == '__main__':
    print(run_ollama_prompt())
  ```

  Ejemplo 2 — usando subprocess con lista de argumentos (recomendado, sin shell):

  ```python
  import subprocess

  def run_ollama_prompt_noshell(model='llama3.2', prompt='Hola mundo'):
    cmd = ['ollama', 'run', model, '--prompt', prompt]
    try:
      result = subprocess.run(cmd, check=True, capture_output=True, text=True)
      return result.stdout.strip()
    except subprocess.CalledProcessError as e:
      raise RuntimeError(f"Comando fallido (codigo {e.returncode}): {e.stderr}") from e

  if __name__ == '__main__':
    print(run_ollama_prompt_noshell())
  ```

  Notas y recomendaciones

  - Asegúrate de que el usuario que ejecuta el script tiene `ollama` en su `PATH`.
  - Si la salida del comando incluye metadatos o formato adicional, adapta el parsing según sea necesario.
  - Para integraciones más robustas o de producción, si Ollama expone una API HTTP (por ejemplo al ejecutar `ollama serve`), es más recomendable usar peticiones HTTP en lugar de invocar la CLI.

  Si quieres, puedo añadir un script runnable en el repositorio (por ejemplo `examples/run_ollama_cli.py`) y pequeños tests que validen la presencia de `ollama` y un modelo instalado.

  Licencia y Créditos

  Guía creada por el autor del repositorio. Basada en la documentación pública de Ollama.
