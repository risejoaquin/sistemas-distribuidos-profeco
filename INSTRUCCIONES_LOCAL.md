# Guía de Ejecución - Sistema ProFeCo

## 1. Requisitos Previos
* **Docker Desktop**: Debe estar corriendo.
* **Java 17**: Instalado y configurado.
* **Apache NetBeans 25**: Usaremos el Maven embebido de NetBeans.

## 2. Paso a Paso para NetBeans (¡IMPORTANTE!)

1. **Abre NetBeans 25**.
2. **Importa el proyecto**: Clic en `File` -> `Open Project` y selecciona **únicamente** la carpeta `backend`.
3. **Compilar**: Haz clic derecho sobre el proyecto raíz **profeco-parent** y selecciona **Clean and Build**.
   * **¡IMPORTANTE!**: He corregido los archivos `pom.xml` que tenían errores de etiquetas y nombres de librerías. Ahora el "Clean and Build" debería funcionar correctamente.
   * Al terminar, DEBES ver el mensaje **"BUILD SUCCESS"** en la consola de NetBeans.

## 3. Ejecutar Infraestructura (Docker)
Cuando NetBeans termine el Build:
1. Abre una terminal de Windows (PowerShell/CMD) en la raíz: `C:\...\sistema-profeco`.
2. Ejecuta:
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

## Solución de Errores Comunes:
* **"path ... not found"**: Asegúrate de estar ejecutando el comando desde la carpeta donde está el archivo `docker-compose.yml`.
* **"target/quarkus-app not found"**: Significa que no hiciste el "Clean and Build" en NetBeans o que falló. Revisa la consola de salida de NetBeans.
* **Puerto 80 ocupado**: Cierra otros servidores (como Apache/XAMPP) o cambia el puerto en el `docker-compose.yml` en la sección `gateway`.


## 4. Ejecutar Microservicios en Modo Desarrollo
Si quieres correr un servicio y ver los cambios en tiempo real sin reconstruir el contenedor:
1. En NetBeans, expande el proyecto del servicio (ej. `identity-service`).
2. Clic derecho -> **Run**. 
3. Quarkus se iniciará en modo `dev`.

## Puertos en Localhost:
* **Gateway (Nginx)**: http://localhost:80
* **RabbitMQ Admin**: http://localhost:15672 (guest/guest)
* **Identity Health**: http://localhost:8081/api/auth/health
* **Catalog Health**: http://localhost:8082/api/catalog/health
* **Audit Health**: http://localhost:8083/api/audit/health
