#!/bin/bash

echo "🚀 Iniciando Backend - Documentation AI"
echo "========================================"

# 1. Verificar si existe venv
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# 2. Activar venv
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# 3. Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# 4. Verificar .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita .env con tu configuración de MongoDB"
fi

# 5. Ejecutar servidor
echo "🏃 Iniciando servidor FastAPI..."
python run.py
