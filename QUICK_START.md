# ⚡ QUICK START - ProFeCo System

**Si ya tienes Docker Desktop instalado, ejecuta esto:**

## 🚀 En 3 Comandos

```bash
# 1. Construir
docker-compose build --no-cache

# 2. Ejecutar
docker-compose up -d

# 3. Esperar y acceder
sleep 30
echo "🎉 Abre: http://localhost:3000"
```

**Eso es todo.** Todo debería funcionar.

---

## 📋 ¿Qué se levanta?

| Componente      | URL / Puerto      | Estado Esperado |
|-----------------|-------------------|-----------------|
| Frontend        | http://localhost:3000 | Tabla de productos |
| API Gateway     | http://localhost:80 | HTTP 200 |
| Catalog Service | http://localhost/api/catalog/items | JSON array |
| Identity Service | http://localhost/api/auth/health | {"status":"UP"} |
| Audit Service   | http://localhost/api/audit/health | {"status":"UP"} |
| PostgreSQL x3   | localhost:5433, 5434, 5435 | Ready for connections |
| RabbitMQ        | http://localhost:15672 (guest/guest) | Management UI |

---

## 🧪 Validar que todo funciona

```bash
# Test 1: Gateway respondiendo
curl http://localhost/health

# Test 2: Catálogo cargando
curl http://localhost/api/catalog/items

# Test 3: Frontend en navegador
open http://localhost:3000
```

Si ves la tabla de productos → **✅ TODO OK**

---

## ❌ Si algo falla

### "Gateway offline" en frontend
```bash
# Esperar más tiempo
sleep 60
docker-compose ps
```

### "Port already in use"
```bash
# Ver qué ocupa el puerto
docker-compose down
# O buscar proceso que use puerto 80
```

### "Containers exiting"
```bash
# Ver logs
docker-compose logs -f [servicio]
```

### Reconstruir desde cero
```bash
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

---

## 🛠️ Para Desarrollo (Apache NetBeans)

```bash
# Terminal 1: Docker (infraestructura)
docker-compose up -d

# Terminal 2: Catalog en dev mode
cd backend/catalog-service
mvn quarkus:dev

# Terminal 3: Frontend
npm run dev
```

Hot reload en ambos lados ✨

---

## 📁 Archivos Creados/Modificados

### ✨ Nuevos:
- `app/page.tsx` - Frontend funcional con tabla de catálogo
- `backend/catalog-service/src/main/java/com/profeco/catalog/CatalogItemsResource.java`
- `backend/audit-service/src/main/java/com/profeco/audit/AuditEventsResource.java`
- `DEPLOY_GUIDE.md` - Documentación completa
- `RESUMEN_TECNICO.md` - Arquitectura explicada
- `start.sh` - Script automático
- `validate_architecture.py` - Validador

### 🔄 Actualizados:
- `infra/nginx.conf` - CORS y rutas completas
- `backend/*/Dockerfile` - Contexto desde raíz + `/deployments`

---

## 🎯 Próximos Pasos

### Desarrollo
1. Agregar ORM/JPA a `pom.xml`
2. Crear entidades en cada servicio
3. Implementar endpoints CRUD completos

### Pruebas
1. Postman/Insomnia para testing manual
2. JUnit5 para tests unitarios
3. TestContainers para integración

### Producción
1. Agregar logging centralizado (ELK stack)
2. Implementar JWT en Identity Service
3. Configurar CI/CD (GitHub Actions)
4. Desplegar en cloud (Google Cloud Run, Railway)

---

## 💡 Comandos Útiles

```bash
# Ver estado
docker-compose ps

# Ver logs en vivo
docker-compose logs -f

# Entrar a un contenedor
docker-compose exec catalog-service sh

# Detener todo
docker-compose down

# Detener pero mantener datos
docker-compose stop

# Reiniciar un servicio
docker-compose restart catalog-service

# Ver IP de contenedor
docker-compose exec catalog-service hostname -I
```

---

## 🔐 Credenciales Default

```
PostgreSQL:
  Usuario: admin
  Password: admin123
  Host: localhost
  Puertos: 5433 (identity), 5434 (catalog), 5435 (audit)

RabbitMQ:
  Usuario: guest
  Password: guest
  URL: http://localhost:15672
```

---

## 📞 ¿Preguntas?

1. **Revisa** `DEPLOY_GUIDE.md` para detalles
2. **Ejecuta** `validate_architecture.py` para diagnóstico
3. **Revisa logs**: `docker-compose logs -f [servicio]`

---

**¡Listo! Disfruta desarrollando con ProFeCo System 🚀**
