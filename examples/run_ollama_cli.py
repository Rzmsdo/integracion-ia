#!/usr/bin/env python3
"""Ejemplo para invocar Ollama desde Python usando la CLI.

Provee funciones reutilizables y un pequeño CLI para probar:
- comprobar si `ollama` está en PATH
- listar modelos (ejecuta `ollama list`)
- ejecutar prompt usando la CLI

El script no instala nada; asume que `ollama` y los modelos necesarios ya están instalados.
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Optional


def check_ollama_installed() -> Optional[str]:
    """Devuelve la ruta a `ollama` si está en PATH, o None."""
    return shutil.which('ollama')


def list_models() -> str:
    """Ejecuta `ollama list` y devuelve la salida (stdout).

    Lanza subprocess.CalledProcessError si el comando falla.
    """
    result = subprocess.run(['ollama', 'list'], check=True, capture_output=True, text=True)
    return result.stdout


def run_ollama_prompt(model: str = 'llama3.2', prompt: str = 'Escribe un resumen breve sobre X', timeout: int = 60) -> str:
    """Ejecuta `ollama run <model> --prompt <prompt>` y devuelve la salida del modelo.

    Por seguridad, construimos la lista de argumentos (sin shell).
    """
    cmd = ['ollama', 'run', model, '--prompt', prompt]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description='Ejemplo: invocar Ollama desde Python (CLI)')
    parser.add_argument('--check', action='store_true', help='Comprobar si ollama está en PATH')
    parser.add_argument('--list', action='store_true', help='Ejecutar `ollama list` y mostrar salida')
    parser.add_argument('--model', default='llama3.2', help='Nombre del modelo (por defecto: llama3.2)')
    parser.add_argument('--prompt', default='Escribe un resumen breve sobre X', help='Prompt a enviar al modelo')
    args = parser.parse_args()

    if args.check:
        path = check_ollama_installed()
        if path:
            print(f"ollama encontrado en: {path}")
        else:
            print("ollama NO se encontró en el PATH")
        return

    if args.list:
        try:
            out = list_models()
            print(out)
        except subprocess.CalledProcessError as e:
            print('Error ejecutando `ollama list`:', e)
        return

    # Por defecto, ejecutar el prompt contra el modelo indicado
    try:
        out = run_ollama_prompt(model=args.model, prompt=args.prompt)
        print(out)
    except subprocess.CalledProcessError as e:
        print('Error al ejecutar el modelo:', e)
    except subprocess.TimeoutExpired:
        print('El comando tardó demasiado y se agotó el tiempo.')


if __name__ == '__main__':
    main()
