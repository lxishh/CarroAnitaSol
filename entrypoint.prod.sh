#!/usr/bin/env bash

# --- SCRIPT DE ESPERA ---
echo "Esperando 15 segundos para que PostgreSQL se inicialice..."
# Pausamos el script para que el contenedor 'db' tenga tiempo de crear la base de datos 'trigorojo_prod'.
sleep 15
echo "Tiempo de espera terminado. Iniciando comandos de Django."
# ------------------------


# 1. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 2. Aplicar migraciones
python manage.py migrate --noinput

# 3. Iniciar el servidor Gunicorn
# **IMPORTANTE: Se corrige 'mysite.wsgi:application' a 'proyectoAnitaSol.wsgi:application'**
exec gunicorn proyectoAnitaSol.wsgi:application --bind 0.0.0.0:8000 --workers 3