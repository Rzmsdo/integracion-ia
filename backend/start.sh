#!/bin/bash

# Script de inicio rápido para Document Analyzer Backend
# Este script verifica prerrequisitos, instala dependencias y levanta el servidor

set -e  # Exit on error

echo "======================================"
echo "🚀 Document Analyzer - Quick Start"
echo "======================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mensajes
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "ℹ $1"
}

# 1. Verificar Python
echo "1️⃣  Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python3 no está instalado"
    exit 1
fi

# 2. Verificar si estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    print_error "No se encuentra main.py. Ejecuta este script desde el directorio backend/"
    exit 1
fi
print_success "Directorio correcto"

# 3. Crear entorno virtual si no existe
echo ""
echo "2️⃣  Configurando entorno virtual..."
if [ ! -d "env" ]; then
    print_info "Creando entorno virtual..."
    python3 -m venv env
    print_success "Entorno virtual creado"
else
    print_success "Entorno virtual ya existe"
fi

# 4. Activar entorno virtual
print_info "Activando entorno virtual..."
source env/bin/activate
print_success "Entorno virtual activado"

# 5. Instalar/actualizar dependencias
echo ""
echo "3️⃣  Instalando dependencias..."
print_info "Esto puede tomar unos minutos..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Dependencias instaladas"

# 6. Verificar archivo .env
echo ""
echo "4️⃣  Verificando configuración..."
if [ ! -f ".env" ]; then
    print_warning ".env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    print_warning "⚠️  IMPORTANTE: Edita .env con tus credenciales de Supabase"
    print_info "   - SUPABASE_URL"
    print_info "   - SUPABASE_KEY"
    print_info "   - SECRET_KEY (genera con: openssl rand -hex 32)"
    echo ""
    read -p "¿Has configurado .env? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Configura .env antes de continuar"
        exit 1
    fi
else
    print_success ".env encontrado"
fi

# 7. Verificar Ollama
echo ""
echo "5️⃣  Verificando Ollama..."
if command -v ollama &> /dev/null; then
    print_success "Ollama CLI encontrado"
    
    # Verificar si el servidor está corriendo
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_success "Servidor Ollama corriendo"
        
        # Verificar modelo llama3.2
        if ollama list | grep -q "llama3.2"; then
            print_success "Modelo llama3.2 disponible"
        else
            print_warning "Modelo llama3.2 no encontrado"
            read -p "¿Descargar modelo llama3.2? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_info "Descargando modelo llama3.2 (esto puede tardar varios minutos)..."
                ollama pull llama3.2
                print_success "Modelo descargado"
            fi
        fi
    else
        print_warning "Servidor Ollama no está corriendo"
        print_info "Iniciando Ollama en segundo plano..."
        ollama serve > /dev/null 2>&1 &
        sleep 2
        print_success "Ollama iniciado"
    fi
else
    print_error "Ollama no está instalado"
    print_info "Instala Ollama desde: https://ollama.com"
    print_info "Linux/Mac: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

# 8. Crear directorio uploads si no existe
echo ""
echo "6️⃣  Verificando directorios..."
mkdir -p uploads
print_success "Directorio uploads listo"

# 9. Verificar Supabase (opcional)
echo ""
echo "7️⃣  Verificando Supabase..."
source .env 2>/dev/null || true
if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_KEY" ]; then
    if [ "$SUPABASE_URL" != "https://your-project.supabase.co" ]; then
        print_success "Credenciales de Supabase configuradas"
    else
        print_warning "Configura tus credenciales de Supabase en .env"
    fi
else
    print_warning "Variables de Supabase no configuradas"
fi

# 10. Listo para iniciar
echo ""
echo "======================================"
echo "✅ Todo listo!"
echo "======================================"
echo ""
print_info "Iniciando servidor FastAPI..."
echo ""
echo "📊 Documentación API disponible en:"
echo "   - Swagger UI: http://localhost:8000/api/v1/docs"
echo "   - ReDoc:      http://localhost:8000/api/v1/redoc"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
sleep 2

# 11. Iniciar servidor
python main.py
