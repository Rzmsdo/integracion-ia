Rzmsdo: # Proyecto de creacion de una IA en local

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
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  signin      Sign in to ollama.com
  signout     Sign out from ollama.com
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.

Seguimos instalando ollama serve

Visitamos de nuevo la web de Ollama -Models y buscamos llama3.2 (o última versión)

Instalamos en una nueva terminal --->

ollama pull llama3.2

Comprobar la instalacioncon : --> ollama list

nos deberia aparecer:
NAME               ID              SIZE      MODIFIED           
llama3.2:latest    a80c4f17acd5    2.0 GB    About a minute ago 

Para iniciar la IA de en la terminal:

ollama run llama3.2   ¿puedes mejorar la presentacion?

GitHub Copilot: Voy a crear una lista de tareas (para seguimiento) y luego actualizar README.md para mejorar su presentación; al final marcaré la tarea como completada y daré un resumen de los cambios y cómo probarlos. Ejecutaré: 1) crear la todo list y marcar la primera tarea en progreso; 2) aplicar el parche que actualiza README.md; 3) marcar todas las tareas como completadas. Espera el progreso después de las tres operaciones. Ahora creo la lista de tareas. 

Se han creado 3 tareas pendientes

Progreso: la lista de tareas fue creada y la tarea 1 marcada en progreso. Ahora aplicaré el parche para mejorar la presentación de README.md. 

Usando "Aplicar revisión"

Voy a leer el contenido actual de README.md para aplicar el parche con el contexto correcto. Luego actualizaré el archivo. 

Leer [](file:///workspaces/portfolio/README.md)

Ahora aplicaré un parche que reemplace todo el contenido del archivo por la versión mejorada. 

Usando "Aplicar revisión"

He borrado el archivo original para reemplazarlo con la versión mejorada (paso intermedio). Ahora crearé el nuevo README.md con la presentación mejorada. 

Se ha creado [](file:///workspaces/portfolio/README.md)

El archivo fue eliminado antes, pero parece que la operación de borrado mostró salida vacía; ahora intento actualizar el archivo (reemplazar contenido). Haré un update patch para insertar el nuevo contenido. 

Usando "Aplicar revisión"


```

```
Progreso: actualicé README.md con la versión mejorada. Ahora marcaré las tareas 2 y 3 como completadas. Luego daré un resumen y cómo probar. 

Completado (1/3) *Crear plan inicial*

He mejorado la presentación del README.md con instrucciones claras, formato, notas y ejemplos de uso de Ollama y del modelo Llama 3.2. A continuación detallo lo que hice, cómo probarlo y siguientes pasos opcionales.

## Qué hice
- Reescribí y formateé README.md para que sea más legible y práctico:
  - Añadí secciones: requisitos, instalación, comandos útiles, ejemplo paso a paso para descargar y ejecutar `llama3.2`, opciones prácticas y recomendaciones.
  - Incluí ejemplos de comandos CLI y una nota sobre recursos y espacio en disco.
  - Añadí una propuesta para integrar con Python si quieres que lo haga.

Archivo modificado:
- README.md — guía de instalación y uso de Ollama (mejorada).

## Cómo probar localmente
Abre una terminal en el directorio del proyecto y sigue estos pasos:

1. Instalar Ollama (desde terminal):
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Verificar que `ollama` está disponible:
```bash
ollama --version
```

3. Descargar el modelo de ejemplo (puede tardar y usar varios GB):
```bash
ollama pull llama3.2
```

4. Verificar los modelos instalados:
```bash
ollama list
```

5. Ejecutar el modelo:
```bash
ollama run llama3.2
```

Opcional: ejecutar en modo servidor (si tu versión lo soporta):
```bash
ollama serve
```

Ejemplo de enviar prompt directo:
```bash
ollama run llama3.2 --prompt "Escribe un resumen breve sobre X"
```

## Validaciones realizadas
- Actualicé el archivo README.md en el repositorio. No he ejecutado comandos de instalación o `ollama` en este contenedor porque eso requiere permisos y/o acceso a la máquina donde quieras instalar Ollama. Si quieres, puedo ejecutar comandos locales en la terminal del devcontainer si me indicas hacerlo.

## Siguientes pasos (opcional)
- Añadir un ejemplo en Python para invocar al modelo:
  - Opción A: ejemplo usando HTTP (si `ollama serve` expone una API).
  - Opción B: ejemplo que llama a la CLI `ollama` desde Python (subprocess).
- Añadir notas sobre requisitos mínimos de memoria y cómo configurar swap o límites.
- Incluir scripts de comprobación automática (por ejemplo, un script `check_ollama.py` que compruebe la presencia de `ollama` y modelos).

¿Quieres que añada el ejemplo en Python (y cuál de las dos opciones prefieres: HTTP o CLI)?

Se realizaron cambios.

Rzmsdo: si añade el ejemplo de usando la CLI desde Python

GitHub Copilot: Voy a: 1) crear una lista de tareas pequeña para este cambio y marcar la primera como en progreso; 2) actualizar README.md añadiendo el ejemplo de "usar la CLI desde Python" con dos variantes y notas. Resultado esperado: nuevo todo list y README actualizado con el ejemplo. Ejecutaré ambas operaciones en paralelo. 

Se han creado 3 tareas pendientes

Usando "Aplicar revisión"


```

```
Progreso: añadí la tarea y actualicé README.md con dos ejemplos en Python (usando subprocess con shell y sin shell) y notas. Ahora marcaré las tareas como completadas. Luego daré instrucciones para probar y ofreceré crear el archivo de ejemplo Python si lo deseas. 

Completado (1/3) *Agregar ejemplo Python CLI*

He añadido al README.md un apartado con ejemplos de cómo invocar Ollama desde Python usando la CLI (dos variantes: con shell y sin shell), más notas y recomendaciones.

Resumen de la sección añadida
- Ejemplo 1: usar subprocess con shell (construcción del comando vía string).
- Ejemplo 2: usar subprocess sin shell (lista de args) — más seguro y recomendado.
- Notas sobre PATH, parsing de la salida y recomendaciones para producción (usar HTTP si hay API).

¿Quieres que:
- Cree el archivo de ejemplo `examples/run_ollama_cli.py` en el repo con el código (y un test rápido)? — Puedo crearlo ahora.
- O prefieres que además añada un pequeño test que verifique que `ollama` está en el `PATH` y que un modelo está instalado (prueba rápida, no descarga de modelos)?

Dime cuál prefieres y lo implemento.

Se realizaron cambios.

Rzmsdo: añadir un script runnable en el repositorio (por ejemplo examples/run_ollama_cli.py) y pequeños tests que validen la presencia de ollama y un modelo instalado.

GitHub Copilot: Voy a crear la lista de tareas y añadir dos archivos: `examples/run_ollama_cli.py` (script runnable) y `tests/test_ollama_cli.py` (tests unitarios). Resultado esperado: archivos creados y TODO actualizado a "in-progress". Ejecutaré ambos en paralelo. 

Se ha creado 1 tarea pendiente

Usando "Aplicar revisión"


```

```
He creado el script run_ollama_cli.py. Ahora crearé los tests en `tests/test_ollama_cli.py` y un archivo `tests/__init__.py` para que pytest los encuentre. Luego ejecutaré los tests si el entorno lo permite. Ejecutaré las creaciones en paralelo. 

Usando "Aplicar revisión"


```

```


Usando "Aplicar revisión"


```

```
Progreso: creé run_ollama_cli.py, test_ollama_cli.py y __init__.py. El verificador mostró un lint error indicando que `pytest` no está instalado en el entorno virtual aunque el archivo se añadió correctamente. Ahora actualizaré el todo list marcando completado y explicaré cómo ejecutar los tests localmente (y cómo instalar pytest si hace falta). 

Completado (1/1) *Crear ejemplo runnable y tests*

He añadido los archivos solicitados y dejé tests para validar la presencia de `ollama` y, opcionalmente, de `llama3.2`.

Resumen de cambios realizados
- Añadido: run_ollama_cli.py — script runnable que:
  - Comprueba si `ollama` está en PATH.
  - Lista modelos con `ollama list`.
  - Ejecuta prompts contra un modelo con `ollama run`.
  - Se puede usar como CLI: `--check`, `--list`, `--model`, `--prompt`.
- Añadido: test_ollama_cli.py — tests con pytest:
  - `test_ollama_in_path` — falla si `ollama` no está en PATH.
  - `test_ollama_list_runs` — ejecuta `ollama list` y espera que el comando funcione.
  - `test_model_installed_optional` — comprueba la presencia de `llama3.2` y salta el test si no está instalado.
- Añadido: __init__.py — marcador para el paquete de tests.

Qué debes saber antes de ejecutar los tests
- Los tests usan pytest. Si no tienes `pytest` instalado en tu entorno virtual, instálalo con:
```bash
pip install pytest
```
- Los tests ejecutan `ollama` en la máquina donde corren. Si `ollama` no está instalado o no está en PATH, algunos tests fallarán o serán marcados como skip.
- `test_model_installed_optional` está diseñado para no fallar en entornos sin modelos; solo verifica `llama3.2` si aparece en la salida de `ollama list`.

Cómo ejecutar el script de ejemplo
- Hacer ejecutable y ejecutar:
```bash
python3 examples/run_ollama_cli.py --check
python3 examples/run_ollama_cli.py --list
python3 examples/run_ollama_cli.py --model llama3.2 --prompt "Escribe un poema breve sobre la luna"
```

Cómo ejecutar los tests
```bash
pip install pytest          # si necesitas instalar pytest
pytest -q
```

Notas y seguimiento
- Durante la creación apareció un mensaje de lint indicando que `pytest` no está instalado en el entorno (es normal en un contenedor mínimo). Eso no impidió añadir los tests.
- Si quieres que ejecute los tests aquí en el contenedor, puedo hacerlo; necesitaré permiso para instalar `pytest` si no está disponible, o puedo correr `pytest` y mostrar resultados tal cual (los tests fallarán si `ollama` no está instalado aquí).
- ¿Quieres que también añada un pequeño Git commit y push automático con estos cambios? ¿O prefieres que haga antes alguna modificación (por ejemplo, mejorar el parsing de la salida del modelo o añadir un README para examples)?

Se realizaron cambios.