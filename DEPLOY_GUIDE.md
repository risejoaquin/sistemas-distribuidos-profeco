# ProFeCo System - Guía de Despliegue Profesional

## 🎯 Arquitectura Entregada

### Backend (Java 17 + Quarkus + Maven)

#### Servicios Microservicios:

**1. Catalog Service** (`/api/catalog`)
```java
// CatalogItemsResource.java
- GET  /api/catalog/health      → Estado del servicio
- GET  /api/catalog/items       → Lista de productos (ID, Nombre, Precio, Categoría)
- POST /api/catalog/report-price → Registra variación de precio
```
**Contexto:** Lee desde `profeco_catalog` PostgreSQL (Puerto interno 5432, externo 5434)

---

**2. Identity Service** (`/api/auth`)
```java
// HealthResource.java
- GET  /api/auth/health → Estado del servicio con check de BD
```
**Contexto:** Gestiona credenciales en `profeco_identity` (Puerto interno 5432, externo 5433)

---

**3. Audit Service** (`/api/audit`)
```java
// AuditEventsResource.java
- GET  /api/audit/health → Estado del servicio
- POST /api/audit/events → Recibe eventos de precio desde el frontend
- GET  /api/audit/events → Historial de eventos registrados
```
**Contexto:** Almacena auditoría en `profeco_audit` (Puerto interno 5432, externo 5435)

---

### Gateway & Networking (Nginx)

**Configuración `infra/nginx.conf`:**
- **Puerto único:** 80 (HTTP)
- **Rutas:**
  - `/api/auth/*`      → identity-service:8080
  - `/api/catalog/*`   → catalog-service:8080
  - `/api/audit/*`     → audit-service:8080
- **CORS Habilitado:** Permite requests desde cualquier origen
- **Health Endpoint:** GET `/health` → Status agregado

---

### Frontend (Next.js + React + Tailwind CSS)

**Ubicación:** `/app/page.tsx`

**Funcionalidades Implementadas:**

1. **Verificación de Gateway**
   - Ping a `http://localhost/health` cada 10 segundos
   - Indica estado con indicador visual (Verde=Conectado, Rojo=Desconectado)

2. **Carga de Catálogo**
   - Fetch GET a `http://localhost/api/catalog/items`
   - Renderiza tabla con: ID, Nombre, Categoría, Precio
   - Error handler elegante con mensajes claros

3. **Reporte de Precios**
   - Botón "Reportar" por cada producto
   - Modal expandible con textarea para comentarios
   - POST a `http://localhost/api/audit/events` con estructura JSON:
     ```json
     {
       "type": "PRICE_REPORT",
       "item_id": 1,
       "item_name": "Leche Integral 1L",
       "reported_price": 2.50,
       "message": "Comentario del usuario",
       "timestamp": "2026-05-14T00:00:00Z"
     }
     ```

4. **Estadísticas Footer**
   - Total de productos
   - Promedio de precio
   - Hora de última actualización

---

## 🚀 INSTRUCCIONES DE DESPLIEGUE

### Paso 1: Verificar Prerequisites

```bash
# Verificar Docker Desktop
docker --version
# Docker version XX.X.X, build XXXXX

# Verificar Docker Compose
docker-compose --version
# Docker Compose version X.XX.X
```

### Paso 2: Limpiar Estado Previo (Opcional)

```bash
# Detener todos los contenedores
docker-compose down

# Eliminar volúmenes (CUIDADO: Borra datos!)
docker-compose down -v
```

### Paso 3: Construir Imágenes

```bash
# Desde la raíz del proyecto
docker-compose build --no-cache
```

**Esperado:**
- ✅ Build de 3 servicios: catalog, identity, audit
- ✅ Tiempo: ~3-5 minutos (primera vez)
- ✅ Maven descarga dependencias

### Paso 4: Iniciar Stack

```bash
docker-compose up -d
```

**Verificar estado:**
```bash
docker-compose ps
```

**Esperado:**
```
NAME                 STATUS
profeco_db_identity  Up 2 minutes (healthy)
profeco_db_catalog   Up 2 minutes (healthy)
profeco_db_audit     Up 2 minutes (healthy)
profeco_rabbitmq     Up 2 minutes
profeco_gateway      Up 2 minutes
identity_service     Up 2 minutes (healthy)
catalog_service      Up 2 minutes (healthy)
audit_service        Up 2 minutes (healthy)
```

### Paso 5: Verificar Conectividad

```bash
# Test Gateway
curl http://localhost/health
# Response: {"status":"operational","gateway":"online","timestamp":"XXXXX"}

# Test Catalog
curl http://localhost/api/catalog/items
# Response: {"success":true,"data":[...],"count":5}

# Test Identity
curl http://localhost/api/auth/health
# Response: {"status":"UP","service":"Identity Service","...}

# Test Audit
curl http://localhost/api/audit/health
# Response: {"status":"UP","service":"Audit Service","timestamp":XXXXX}
```

### Paso 6: Iniciar Frontend (Next.js)

**En otra terminal:**

```bash
cd /ruta/del/proyecto

# Si no has instalado dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

**Acceder:**
- Frontend: `http://localhost:3000`
- Deberías ver tabla de productos cargando desde `/api/catalog/items`

---

## 🛠️ DESARROLLO LOCAL (Apache NetBeans)

### Ejecutar un Servicio en Quarkus Dev Mode

```bash
cd backend/catalog-service
mvn quarkus:dev
```

**Esperado:**
- ✅ Compila y ejecuta en puerto 8080
- ✅ Hot reload de código
- ✅ Logs en tiempo real

**Acceso local:**
```bash
curl http://localhost:8080/api/catalog/items
```

**Nota:** Si ejecutas `mvn quarkus:dev`, **detén el contenedor de Docker** para ese servicio para evitar conflicto de puertos:
```bash
docker-compose stop catalog-service
```

---

## 📊 MONITOREO Y TROUBLESHOOTING

### Ver logs de un servicio

```bash
docker-compose logs -f catalog-service
docker-compose logs -f identity-service
docker-compose logs -f audit-service
docker-compose logs -f gateway
```

### Entrar a un contenedor

```bash
docker-compose exec catalog-service sh
```

### Verificar base de datos

```bash
# Conectar a PostgreSQL (desde host)
psql -h localhost -p 5434 -U admin -d profeco_catalog
# Password: admin123

# Listar tablas
\dt

# Salir
\q
```

### RabbitMQ Management

```
URL: http://localhost:15672
User: guest
Password: guest
```

### Si Docker Desktop falla

1. **Reiniciar Docker Desktop**
2. **Limpiar volúmenes:**
   ```bash
   docker volume prune
   ```
3. **Reconstruir desde cero:**
   ```bash
   docker-compose down -v
   docker system prune -a
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## ✅ CHECKLIST DE VALIDACIÓN

- [ ] `docker-compose ps` → Todos los servicios en "Up"
- [ ] `curl http://localhost/health` → Response HTTP 200
- [ ] `http://localhost:3000` → Tabla de productos visible
- [ ] Frontend carga datos sin errores de CORS
- [ ] Botón "Reportar" funciona → Modal aparece
- [ ] Reporte enviado → Respuesta "success": true en consola

---

## 📁 ESTRUCTURA FINAL DEL PROYECTO

```
sistema-profeco/
├── app/
│   ├── page.tsx (← Frontend NUEVO: Catálogo funcional)
│   ├── layout.tsx
│   └── globals.css
├── backend/
│   ├── catalog-service/
│   │   ├── Dockerfile (← ACTUALIZADO: Contexto raíz)
│   │   ├── src/main/java/com/profeco/catalog/
│   │   │   ├── CatalogItemsResource.java (← NUEVO: GET items, POST report)
│   │   │   └── CatalogHealthResource.java
│   │   └── pom.xml
│   ├── identity-service/
│   │   ├── Dockerfile (← ACTUALIZADO)
│   │   └── src/main/java/com/profeco/identity/
│   │       └── HealthResource.java
│   ├── audit-service/
│   │   ├── Dockerfile (← ACTUALIZADO)
│   │   └── src/main/java/com/profeco/audit/
│   │       ├── AuditEventsResource.java (← NUEVO: POST events)
│   │       └── AuditHealthResource.java
│   ├── profeco-shared/
│   │   └── (DTOs y Enums compartidos)
│   └── pom.xml (Parent)
├── infra/
│   ├── nginx.conf (← ACTUALIZADO: CORS, rutas completas)
│   ├── init-db-identity.sql
│   ├── init-db-catalog.sql
│   └── init-db-audit.sql
├── frontend/
│   ├── package.json
│   └── (config files)
├── docker-compose.yml
├── start.sh (← NUEVO: Script de arranque)
└── DEPLOY_GUIDE.md (← ESTE DOCUMENTO)
```

---

## 🔐 CREDENCIALES POR DEFECTO

| Servicio   | Usuario | Password    | Host           | Puerto |
|-----------|---------|-------------|----------------|--------|
| PostgreSQL | admin   | admin123    | localhost      | 5433-5435 |
| RabbitMQ  | guest   | guest       | localhost      | 15672  |
| Gateway   | (N/A)   | (N/A)       | localhost      | 80     |

**Cambiar credenciales:** Edita `docker-compose.yml` y `.env`

---

## 🎓 ARQUITECTURA EXPLICADA (Senior Level)

### Database-Per-Service Pattern
Cada microservicio tiene su propia BD independiente:
- **Identity:** Maneja usuarios, sesiones
- **Catalog:** Gestiona productos, precios
- **Audit:** Registra cambios y eventos

**Beneficio:** Escalabilidad independiente y fácil migración de datos

### API Gateway (Nginx)
Punto único de entrada que:
- Enruta requests a servicios específicos
- Aplica rate limiting y CORS
- Centraliza logging y monitoreo
- Simplifica certificados SSL/TLS en producción

### Message-Driven (RabbitMQ)
Para comunicación asíncrona entre servicios:
- Reportes de precio → Cola de auditoría
- Notificaciones → Cola de eventos
- Evita acoplamiento directo entre servicios

### Quarkus + Java 17
Stack moderno con:
- Startup time < 1 segundo
- Footprint bajo (40MB vs 500MB de Spring Boot)
- GraalVM compatible para compilación nativa
- Dev mode con hot reload

---

## 📞 SOPORTE

Si encuentras errores:

1. **Revisa logs:** `docker-compose logs -f [servicio]`
2. **Verifica puertos:** `docker ps`
3. **Prueba conectividad:** `curl http://localhost/health`
4. **Reinicia:** `docker-compose restart`
5. **Reconstruye:** `docker-compose down -v && docker-compose up -d --build`

---

**Documento versión 1.0 - ProFeCo System**
**Última actualización: 2026-05-14**
**Arquitecto: Senior FullStack Developer**
