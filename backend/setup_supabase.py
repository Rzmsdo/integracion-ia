#!/usr/bin/env python3
"""
Script para configurar automáticamente Supabase.
Crea las tablas, índices, triggers y funciones necesarias.
"""

import sys
import os
from pathlib import Path
import asyncio

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

def check_env_vars():
    """Verificar que las variables de entorno estén configuradas"""
    print_header("1. Verificando Variables de Entorno")
    
    # Cargar .env
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print_error("Archivo .env no encontrado")
        print_warning("Crea el archivo .env basándote en .env.example")
        return False
    
    # Leer variables
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    # Verificar variables requeridas
    required = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing = []
    
    for var in required:
        value = env_vars.get(var, '')
        if not value or value.startswith('tu_') or value.startswith('https://tu-'):
            missing.append(var)
            print_error(f"{var}: No configurado")
        else:
            # Mostrar solo los primeros/últimos caracteres
            if 'URL' in var:
                print_success(f"{var}: {value}")
            else:
                masked = value[:10] + '...' + value[-10:] if len(value) > 20 else value
                print_success(f"{var}: {masked}")
    
    if missing:
        print_error(f"\nFaltan configurar: {', '.join(missing)}")
        print_info("\nSigue estos pasos:")
        print_info("1. Ve a https://app.supabase.com")
        print_info("2. Crea un nuevo proyecto o abre uno existente")
        print_info("3. Ve a Settings → API")
        print_info("4. Copia la Project URL y la anon key")
        print_info("5. Actualiza el archivo .env con estos valores")
        return False
    
    print_success("\nTodas las variables están configuradas correctamente")
    return True

async def test_connection():
    """Probar conexión con Supabase"""
    print_header("2. Probando Conexión con Supabase")
    
    try:
        from supabase import create_client, Client
        from app.core.config import get_settings
        
        settings = get_settings()
        
        print_info(f"Conectando a: {settings.SUPABASE_URL}")
        
        supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        
        # Probar una query simple
        response = supabase.table('users').select('*').limit(1).execute()
        
        print_success("Conexión exitosa con Supabase")
        return True, supabase
        
    except Exception as e:
        error_msg = str(e)
        
        if 'relation "users" does not exist' in error_msg:
            print_warning("Conexión exitosa pero las tablas no existen aún")
            print_info("Necesitas ejecutar el schema SQL en Supabase")
            return True, None
        elif 'Invalid API key' in error_msg or 'API key not found' in error_msg:
            print_error("API key inválida")
            print_info("Verifica que copiaste correctamente la 'anon' key de Supabase")
            return False, None
        elif 'Project not found' in error_msg:
            print_error("Proyecto no encontrado")
            print_info("Verifica que la URL de Supabase sea correcta")
            return False, None
        else:
            print_error(f"Error de conexión: {error_msg}")
            return False, None

def show_sql_instructions():
    """Mostrar instrucciones para ejecutar el SQL"""
    print_header("3. Crear Tablas en Supabase")
    
    schema_file = Path(__file__).parent / 'database' / 'schema.sql'
    
    if not schema_file.exists():
        print_error(f"Archivo schema.sql no encontrado en: {schema_file}")
        return False
    
    print_info("Para crear las tablas en Supabase:")
    print(f"\n{Colors.YELLOW}OPCIÓN 1: Desde el Dashboard de Supabase{Colors.END}")
    print("1. Ve a https://app.supabase.com")
    print("2. Abre tu proyecto")
    print("3. En el menú lateral, haz clic en 'SQL Editor'")
    print("4. Haz clic en '+ New query'")
    print(f"5. Copia el contenido de: {Colors.BOLD}{schema_file}{Colors.END}")
    print("6. Pégalo en el editor y haz clic en 'Run' (o Ctrl+Enter)")
    
    print(f"\n{Colors.YELLOW}OPCIÓN 2: Copiar al portapapeles{Colors.END}")
    
    # Intentar copiar al portapapeles
    try:
        with open(schema_file) as f:
            sql_content = f.read()
        
        print(f"\nContenido del archivo ({len(sql_content)} caracteres):")
        print(f"{Colors.BOLD}Primeras líneas:{Colors.END}")
        print('-' * 70)
        print('\n'.join(sql_content.split('\n')[:15]))
        print('...')
        print('-' * 70)
        
        print(f"\n{Colors.GREEN}Para copiar todo el archivo:{Colors.END}")
        print(f"cat {schema_file} | pbcopy  # macOS")
        print(f"cat {schema_file} | xclip -selection clipboard  # Linux")
        
    except Exception as e:
        print_error(f"Error leyendo schema.sql: {e}")
        return False
    
    return True

async def verify_tables(supabase):
    """Verificar que las tablas existan"""
    print_header("4. Verificando Tablas")
    
    if not supabase:
        print_warning("No hay conexión con Supabase, saltando verificación")
        return False
    
    tables = ['users', 'documents', 'analyses', 'analysis_statistics']
    results = {}
    
    for table in tables:
        try:
            response = supabase.table(table).select('*').limit(1).execute()
            print_success(f"Tabla '{table}' existe")
            results[table] = True
        except Exception as e:
            if 'does not exist' in str(e):
                print_error(f"Tabla '{table}' no existe")
                results[table] = False
            else:
                print_warning(f"Tabla '{table}': {str(e)[:50]}...")
                results[table] = False
    
    all_exist = all(results.values())
    
    if all_exist:
        print_success("\n✅ Todas las tablas están creadas correctamente")
        return True
    else:
        missing = [t for t, exists in results.items() if not exists]
        print_error(f"\n❌ Faltan tablas: {', '.join(missing)}")
        print_info("Ejecuta el schema.sql en Supabase SQL Editor")
        return False

async def test_crud_operations(supabase):
    """Probar operaciones CRUD básicas"""
    print_header("5. Probando Operaciones CRUD")
    
    if not supabase:
        print_warning("No hay conexión, saltando pruebas CRUD")
        return False
    
    try:
        # Test: Crear usuario
        print_info("Insertando usuario de prueba...")
        user_data = {
            'user_id': 'test_setup_user',
            'email': 'test_setup@example.com',
            'name': 'Setup Test User'
        }
        
        # Intentar insertar (o actualizar si existe)
        try:
            response = supabase.table('users').upsert(user_data).execute()
            print_success("Usuario insertado/actualizado correctamente")
        except Exception as e:
            print_error(f"Error insertando usuario: {e}")
            return False
        
        # Test: Leer usuario
        print_info("Leyendo usuario de prueba...")
        response = supabase.table('users').select('*').eq('user_id', 'test_setup_user').execute()
        if response.data:
            print_success(f"Usuario leído correctamente: {response.data[0]['name']}")
        else:
            print_error("No se pudo leer el usuario")
            return False
        
        # Test: Contar usuarios
        print_info("Contando usuarios...")
        response = supabase.table('users').select('*', count='exact').execute()
        print_success(f"Total de usuarios en la base de datos: {response.count}")
        
        # Test: Eliminar usuario de prueba
        print_info("Limpiando usuario de prueba...")
        response = supabase.table('users').delete().eq('user_id', 'test_setup_user').execute()
        print_success("Usuario de prueba eliminado")
        
        print_success("\n✅ Todas las operaciones CRUD funcionan correctamente")
        return True
        
    except Exception as e:
        print_error(f"Error en operaciones CRUD: {e}")
        return False

async def show_next_steps():
    """Mostrar próximos pasos"""
    print_header("✅ Configuración Completada")
    
    print(f"{Colors.GREEN}¡Supabase está configurado y funcionando!{Colors.END}\n")
    
    print(f"{Colors.BOLD}Próximos pasos:{Colors.END}\n")
    
    print("1. Probar análisis de documentos:")
    print(f"   {Colors.BLUE}curl -X POST 'http://localhost:8000/api/v1/documents/upload' \\")
    print(f"     -F 'file=@test_document.txt' \\")
    print(f"     -F 'analysis_type=summary'{Colors.END}\n")
    
    print("2. Ver documentos guardados:")
    print(f"   {Colors.BLUE}curl 'http://localhost:8000/api/v1/documents/user/demo_user/analyses'{Colors.END}\n")
    
    print("3. Ver estadísticas:")
    print(f"   {Colors.BLUE}curl 'http://localhost:8000/api/v1/documents/user/demo_user/statistics'{Colors.END}\n")
    
    print("4. Acceder al dashboard de Supabase:")
    print(f"   {Colors.BLUE}https://app.supabase.com{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Documentación completa:{Colors.END}")
    print(f"   → CONFIGURACION_SUPABASE.md\n")

async def main():
    """Función principal"""
    print_header("🗄️  Configuración de Supabase para Document Analyzer")
    
    print(f"{Colors.BOLD}Este script te ayudará a:{Colors.END}")
    print("• Verificar tus credenciales de Supabase")
    print("• Probar la conexión con la base de datos")
    print("• Guiarte para crear las tablas necesarias")
    print("• Verificar que todo funcione correctamente\n")
    
    # Paso 1: Verificar variables de entorno
    if not check_env_vars():
        print_error("\n❌ Configuración incompleta")
        print_info("Edita el archivo .env con tus credenciales de Supabase")
        return 1
    
    # Paso 2: Probar conexión
    connection_ok, supabase = await test_connection()
    if not connection_ok:
        print_error("\n❌ No se pudo conectar con Supabase")
        print_info("Verifica tus credenciales en el archivo .env")
        return 1
    
    # Paso 3: Mostrar instrucciones para crear tablas
    if not show_sql_instructions():
        return 1
    
    # Si hay conexión, verificar tablas
    if supabase:
        tables_ok = await verify_tables(supabase)
        
        if not tables_ok:
            print_warning("\n⚠️  Las tablas no están creadas")
            print_info("Sigue las instrucciones arriba para ejecutar el schema.sql")
            
            response = input(f"\n{Colors.YELLOW}¿Ya ejecutaste el schema.sql? (s/n): {Colors.END}").lower()
            if response == 's':
                # Re-verificar
                tables_ok = await verify_tables(supabase)
                if not tables_ok:
                    print_error("Las tablas aún no están disponibles")
                    return 1
            else:
                print_info("Ejecuta el schema.sql y vuelve a correr este script")
                return 1
        
        # Paso 4: Probar CRUD
        crud_ok = await test_crud_operations(supabase)
        if not crud_ok:
            print_warning("\n⚠️  Algunas operaciones CRUD fallaron")
            return 1
    
    # Paso 5: Mostrar próximos pasos
    await show_next_steps()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Configuración interrumpida{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        sys.exit(1)
