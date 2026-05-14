#!/bin/bash
# ProFeCo System - Quick Verification Script

echo "═════════════════════════════════════════════════════════"
echo "✅ ProFeCo System - Estado Final"
echo "═════════════════════════════════════════════════════════"
echo ""

echo "📊 Contenedores Docker:"
docker-compose ps

echo ""
echo "🧪 Probando endpoints:"
echo ""

echo "1️⃣  Gateway Health:"
curl -s http://localhost/health | jq .

echo ""
echo "2️⃣  Catálogo de Productos:"
curl -s http://localhost/api/catalog/items | jq '.data[0:2]'

echo ""
echo "3️⃣  Identity Service:"
curl -s http://localhost/api/auth/health | jq .

echo ""
echo "4️⃣  Audit Service:"
curl -s http://localhost/api/audit/health | jq .

echo ""
echo "5️⃣  Test POST Audit:"
curl -s -X POST http://localhost/api/audit/events \
  -H "Content-Type: application/json" \
  -d '{"type":"TEST","message":"Verificación"}' | jq .

echo ""
echo "═════════════════════════════════════════════════════════"
echo "✅ ACCESO FRONTEND:"
echo "   http://localhost:3000"
echo "═════════════════════════════════════════════════════════"
