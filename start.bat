@echo off

echo ========================================
echo 🚀 Iniciando Backend - Documentation AI
echo ========================================

REM 1. Verificar si existe venv
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM 2. Activar venv
echo 🔌 Activando entorno virtual...
call venv\Scripts\activate

REM 3. Instalar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM 4. Verificar .env
if not exist ".env" (
    echo ⚙️  Creando archivo .env...
    copy .env.example .env
    echo ⚠️  IMPORTANTE: Edita .env con tu configuración de MongoDB
)

REM 5. Ejecutar servidor
echo 🏃 Iniciando servidor FastAPI...
python run.py

pause
