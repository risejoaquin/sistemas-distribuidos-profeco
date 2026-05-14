#!/bin/bash
# ProFeCo System - Startup Script
# Este script inicia el stack completo: Bases de Datos, RabbitMQ, Gateway Nginx, Microservicios y Frontend

set -e

echo "=========================================="
echo "🚀 ProFeCo System - Docker Compose Stack"
echo "=========================================="
echo ""

# Verificar Docker Desktop
if ! command -v docker &> /dev/null; then
    echo "❌ Docker Desktop no detectado. Instálalo desde https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker detectado"
echo ""

# Limpiar contenedores previos (opcional)
read -p "¿Deseas limpiar contenedores previos? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Limpiando contenedores..."
    docker-compose down --volumes || true
fi

echo ""
echo "🔨 Construyendo imágenes (primera ejecución)..."
docker-compose build --no-cache

echo ""
echo "🚀 Iniciando stack completo..."
docker-compose up -d

echo ""
echo "⏳ Esperando a que los servicios se inicien (30 segundos)..."
sleep 30

echo ""
echo "=========================================="
echo "✅ SISTEMA INICIADO"
echo "=========================================="
echo ""
echo "📍 ENDPOINTS DISPONIBLES:"
echo "   • Frontend:        http://localhost:3000"
echo "   • API Gateway:     http://localhost:80"
echo "   • Catalog API:     http://localhost/api/catalog/items"
echo "   • Identity API:    http://localhost/api/auth/health"
echo "   • Audit API:       http://localhost/api/audit/health"
echo "   • RabbitMQ:        http://localhost:15672 (guest/guest)"
echo ""
echo "📊 BASES DE DATOS:"
echo "   • Identity DB:     localhost:5433 (profeco_identity)"
echo "   • Catalog DB:      localhost:5434 (profeco_catalog)"
echo "   • Audit DB:        localhost:5435 (profeco_audit)"
echo ""
echo "📋 COMANDOS ÚTILES:"
echo "   • Ver logs:        docker-compose logs -f"
echo "   • Ver servicios:   docker-compose ps"
echo "   • Detener:         docker-compose down"
echo "   • Ejecutar mvn:    mvn quarkus:dev (desde Apache NetBeans)"
echo ""
echo "=========================================="
