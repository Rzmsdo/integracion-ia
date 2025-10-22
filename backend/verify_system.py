#!/usr/bin/env python3
"""
Script de verificación completa del sistema.
Prueba todos los componentes: Ollama, API, y análisis de documentos.
"""

import asyncio
import sys
from pathlib import Path
import httpx

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

async def test_ollama_connection():
    """Test 1: Verificar conexión con Ollama"""
    print_header("TEST 1: Conexión con Ollama")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                print_success(f"Ollama está activo en http://localhost:11434")
                print_info(f"Modelos disponibles: {', '.join(models)}")
                return True, models
            else:
                print_error(f"Ollama respondió con código {response.status_code}")
                return False, []
    except Exception as e:
        print_error(f"No se pudo conectar con Ollama: {e}")
        print_warning("Ejecuta: ollama serve")
        return False, []

async def test_ollama_generation(model="llama3.2:1b"):
    """Test 2: Verificar generación de texto"""
    print_header("TEST 2: Generación de Texto")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": "Di 'Hola' en una palabra",
                    "stream": False
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('response', '')
                print_success(f"Generación exitosa con modelo {model}")
                print_info(f"Respuesta: {result[:100]}...")
                return True
            else:
                print_error(f"Error en generación: {response.status_code}")
                print_info(f"Respuesta: {response.text}")
                return False
    except httpx.ReadTimeout:
        print_error("Timeout en generación (>60s)")
        return False
    except Exception as e:
        print_error(f"Error en generación: {e}")
        return False

async def test_backend_health():
    """Test 3: Verificar estado del backend"""
    print_header("TEST 3: Estado del Backend")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/v1/system/health", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                print_success("Backend está activo")
                print_info(f"Ollama: {data.get('ollama', 'unknown')}")
                print_info(f"Supabase: {data.get('supabase', 'unknown')}")
                print_info(f"Modelo: {data.get('model', 'unknown')}")
                return True
            else:
                print_error(f"Backend respondió con código {response.status_code}")
                return False
    except Exception as e:
        print_error(f"No se pudo conectar con el backend: {e}")
        print_warning("Ejecuta: cd backend && python main.py")
        return False

async def test_document_analysis():
    """Test 4: Probar análisis de documentos"""
    print_header("TEST 4: Análisis de Documentos")
    
    # Crear archivo de prueba
    test_file = Path("/tmp/test_doc.txt")
    test_content = """Inteligencia Artificial y Machine Learning

La inteligencia artificial está revolucionando la tecnología moderna.
El machine learning permite a las computadoras aprender de los datos.
Las aplicaciones incluyen reconocimiento de imágenes, procesamiento de lenguaje natural,
y sistemas de recomendación."""
    
    test_file.write_text(test_content.strip())
    
    try:
        async with httpx.AsyncClient() as client:
            # Test análisis general
            print_info("Probando análisis general...")
            with open(test_file, 'rb') as f:
                files = {'file': ('test_doc.txt', f, 'text/plain')}
                data = {'analysis_type': 'general'}
                
                response = await client.post(
                    "http://localhost:8000/api/v1/documents/upload",
                    files=files,
                    data=data,
                    timeout=120.0
                )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print_success("Análisis general completado")
                    analysis = result.get('analysis', {})
                    print_info(f"Tipo: {analysis.get('type', 'N/A')}")
                    summary = analysis.get('summary', '')
                    print_info(f"Resumen: {summary[:100]}...")
                    return True
                else:
                    print_error(f"Error en análisis: {result.get('error', 'Unknown')}")
                    return False
            else:
                print_error(f"Error HTTP {response.status_code}")
                print_info(f"Respuesta: {response.text[:200]}")
                return False
                
    except httpx.ReadTimeout:
        print_error("Timeout en análisis (>120s)")
        return False
    except Exception as e:
        print_error(f"Error en análisis: {e}")
        return False
    finally:
        if test_file.exists():
            test_file.unlink()

async def main():
    """Ejecutar todos los tests"""
    print_header("🧪 VERIFICACIÓN COMPLETA DEL SISTEMA")
    
    results = {}
    
    # Test 1: Ollama
    ollama_ok, models = await test_ollama_connection()
    results['ollama_connection'] = ollama_ok
    
    if ollama_ok and models:
        # Test 2: Generación
        gen_ok = await test_ollama_generation(models[0])
        results['ollama_generation'] = gen_ok
    else:
        print_warning("Saltando test de generación (Ollama no disponible)")
        results['ollama_generation'] = False
    
    # Test 3: Backend
    backend_ok = await test_backend_health()
    results['backend_health'] = backend_ok
    
    if backend_ok:
        # Test 4: Análisis
        analysis_ok = await test_document_analysis()
        results['document_analysis'] = analysis_ok
    else:
        print_warning("Saltando tests de backend (no disponible)")
        results['document_analysis'] = False
    
    # Resumen
    print_header("📊 RESUMEN DE RESULTADOS")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        if result:
            print_success(f"{test}: PASADO")
        else:
            print_error(f"{test}: FALLIDO")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests pasados{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ¡TODOS LOS TESTS PASARON!{Colors.END}")
        print(f"{Colors.GREEN}El sistema está completamente funcional.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ ALGUNOS TESTS FALLARON{Colors.END}")
        print(f"{Colors.YELLOW}Revisa los errores arriba.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrumpidos por el usuario{Colors.END}")
        sys.exit(1)
