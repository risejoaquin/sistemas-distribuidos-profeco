# 🚀 QUICK REFERENCE - ProFeCo System

## Estado Actual

```
✅ Backend:   Corriendo
✅ Gateway:   Corriendo
✅ Frontend:  Corriendo
✅ Database:  Corriendo
✅ Happy Path: Activo
```

## Acceso Rápido

| Componente | URL | Puerto | Status |
|-----------|-----|--------|--------|
| Frontend | http://localhost:3000 | 3000 | ✅ |
| Gateway | http://localhost/ | 80 | ✅ |
| Catalog API | http://localhost/api/catalog/items | 80 | ✅ |
| Identity API | http://localhost/api/auth/health | 80 | ✅ |
| Audit API | http://localhost/api/audit/events | 80 | ✅ |
| RabbitMQ | http://localhost:15672 | 15672 | ✅ |

## Comandos Esenciales

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs en vivo
docker-compose logs -f

# Reiniciar un servicio
docker-compose restart catalog-service

# Construir de nuevo
docker-compose build --no-cache && docker-compose up -d

# Entrar a contenedor
docker-compose exec catalog-service sh

# Verificar endpoints
curl http://localhost/health
curl http://localhost/api/catalog/items
```

## Archivos Clave

```
Backend:
  - backend/*/src/main/resources/application.properties
  - backend/*/Dockerfile

Gateway:
  - infra/nginx.conf

Frontend:
  - frontend/app/page.tsx
  - frontend/next.config.ts
```

## Flujo de Datos

```
Navegador (http://localhost:3000)
    ↓ (Fetch)
Next.js (localhost:3000)
    ↓ (Rewrite /api/* → localhost:80)
Nginx Gateway (localhost:80)
    ↓ (Proxy Pass)
Microservicios (localhost:8080)
    ↓
PostgreSQL (localhost:5433-5435)
```

## Credenciales

| Servicio | Usuario | Password |
|----------|---------|----------|
| PostgreSQL | admin | admin123 |
| RabbitMQ | guest | guest |

## Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Gateway offline" | `docker-compose up -d` y esperar 30s |
| Puerto 80 en uso | `docker-compose down` |
| 404 en /api/* | Verificar nginx.conf upstream definitions |
| CORS error | Verificar `add_header` en nginx.conf |
| Frontend no carga | Verificar `http://localhost:3000` |

## Endpoints HTTP

### GET /health
```bash
curl http://localhost/health
Response: {"status":"operational","gateway":"online"}
```

### GET /api/catalog/items
```bash
curl http://localhost/api/catalog/items
Response: {"success":true,"data":[...],"count":5}
```

### GET /api/auth/health
```bash
curl http://localhost/api/auth/health
Response: {"status":"UP","service":"Identity Service"}
```

### POST /api/audit/events
```bash
curl -X POST http://localhost/api/audit/events \
  -H "Content-Type: application/json" \
  -d '{"type":"PRICE_REPORT","message":"test"}'
Response: {"success":true,"event_id":XXXXX}
```

## Desarrollo Local

```bash
# Terminal 1: Docker (infraestructura)
docker-compose up -d

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Backend (si quieres cambios en código)
cd backend/catalog-service
mvn quarkus:dev
```

## Próximos Pasos

1. ✅ Happy Path funcionando
2. ⬜ Agregar ORM/JPA entidades
3. ⬜ Conectar a BDs reales
4. ⬜ JWT authentication
5. ⬜ RabbitMQ messaging
6. ⬜ Deploy a cloud

---

**Para más información ver:**
- HAPPY_PATH.txt (Flujo completo)
- STATUS_FINAL.txt (Cambios realizados)
- DEPLOY_GUIDE.md (Documentación completa)
