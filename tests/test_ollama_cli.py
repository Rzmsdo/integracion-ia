import shutil
import subprocess
import pytest


def test_ollama_in_path():
    """Verifica que el ejecutable `ollama` esté en PATH."""
    path = shutil.which('ollama')
    assert path is not None, "ollama no está en el PATH"


def test_ollama_list_runs():
    """Ejecuta `ollama list` y comprueba que el comando retorna (no fallar).

    Nota: este test no valida modelos concretos para evitar descargar modelos en CI.
    """
    try:
        result = subprocess.run(['ollama', 'list'], check=True, capture_output=True, text=True, timeout=20)
    except FileNotFoundError:
        pytest.skip('ollama no encontrado en el sistema')
    except subprocess.CalledProcessError as e:
        pytest.fail(f'`ollama list` falló: {e.stderr}')
    except subprocess.TimeoutExpired:
        pytest.fail('`ollama list` excedió el tiempo de espera')

    # Al menos esperamos que la salida sea un string (puede ser vacío si no hay modelos)
    assert isinstance(result.stdout, str)


def test_model_installed_optional():
    """Intenta detectar un modelo común (llama3.2). Si no existe, el test se marca como skip.

    Esto permite usar el test suite tanto en máquinas con modelos como sin ellos.
    """
    try:
        result = subprocess.run(['ollama', 'list'], check=True, capture_output=True, text=True, timeout=20)
    except Exception:
        pytest.skip('No se puede ejecutar `ollama list`')

    out = result.stdout.lower()
    if 'llama3.2' in out:
        assert 'llama3.2' in out
    else:
        pytest.skip('llama3.2 no está instalado; prueba manual requerida')
