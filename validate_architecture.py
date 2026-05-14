#!/usr/bin/env python3
"""
ProFeCo System - Validador de Arquitectura
Verifica que todos los componentes estén en su lugar correcto
"""

import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def check_file(path, description):
    """Verifica si un archivo existe"""
    exists = Path(path).exists()
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    print(f"  {status} {description}: {path}")
    return exists

def check_directory(path, description):
    """Verifica si un directorio existe"""
    exists = Path(path).is_dir()
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    print(f"  {status} {description}: {path}")
    return exists

def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}ProFeCo System - Validación de Arquitectura{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    
    checks = []
    
    # BACKEND - JAVA RESOURCES
    print(f"{BOLD}BACKEND - JAVA RESOURCES:{RESET}")
    checks.append(check_file(
        "backend/catalog-service/src/main/java/com/profeco/catalog/CatalogItemsResource.java",
        "Catalog Items Resource (GET items, POST report)"
    ))
    checks.append(check_file(
        "backend/identity-service/src/main/java/com/profeco/identity/HealthResource.java",
        "Identity Health Resource"
    ))
    checks.append(check_file(
        "backend/audit-service/src/main/java/com/profeco/audit/AuditEventsResource.java",
        "Audit Events Resource (POST events)"
    ))
    
    # DOCKERFILES
    print(f"\n{BOLD}DOCKERFILES:{RESET}")
    checks.append(check_file("backend/catalog-service/Dockerfile", "Catalog Dockerfile"))
    checks.append(check_file("backend/identity-service/Dockerfile", "Identity Dockerfile"))
    checks.append(check_file("backend/audit-service/Dockerfile", "Audit Dockerfile"))
    
    # INFRASTRUCTURE
    print(f"\n{BOLD}INFRAESTRUCTURA:{RESET}")
    checks.append(check_file("infra/nginx.conf", "Nginx Gateway Config (actualizado con CORS)"))
    checks.append(check_file("infra/init-db-identity.sql", "Identity DB Init Script"))
    checks.append(check_file("infra/init-db-catalog.sql", "Catalog DB Init Script"))
    checks.append(check_file("infra/init-db-audit.sql", "Audit DB Init Script"))
    
    # FRONTEND
    print(f"\n{BOLD}FRONTEND - NEXT.JS:{RESET}")
    checks.append(check_file("app/page.tsx", "Catalog Page (con tabla, reportes, error handling)"))
    checks.append(check_file("app/layout.tsx", "Layout"))
    checks.append(check_file("app/globals.css", "Tailwind CSS Global Styles"))
    
    # DOCKER COMPOSE
    print(f"\n{BOLD}ORQUESTACIÓN:{RESET}")
    checks.append(check_file("docker-compose.yml", "Docker Compose Stack"))
    
    # DOCUMENTACIÓN
    print(f"\n{BOLD}DOCUMENTACIÓN:{RESET}")
    checks.append(check_file("DEPLOY_GUIDE.md", "Guía de Despliegue Completa"))
    checks.append(check_file("RESUMEN_TECNICO.md", "Resumen Técnico de Arquitectura"))
    checks.append(check_file("start.sh", "Script de Inicio Automático"))
    
    # RESUMEN
    total = len(checks)
    passed = sum(checks)
    failed = total - passed
    
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}RESUMEN DE VALIDACIÓN:{RESET}")
    print(f"  Total: {total} componentes")
    print(f"  {GREEN}✓ Listos: {passed}{RESET}")
    if failed > 0:
        print(f"  {RED}✗ Faltantes: {failed}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    
    if failed == 0:
        print(f"{GREEN}{BOLD}✓ ARQUITECTURA COMPLETA - LISTO PARA DESPLIEGUE{RESET}\n")
        print("PRÓXIMOS PASOS:")
        print("1. Construir imágenes:  docker-compose build --no-cache")
        print("2. Iniciar stack:       docker-compose up -d")
        print("3. Esperar 30 segundos")
        print("4. Verificar estado:    docker-compose ps")
        print("5. Acceder frontend:    http://localhost:3000")
        print("6. Acceder API:         http://localhost/api/catalog/items\n")
        return 0
    else:
        print(f"{RED}{BOLD}✗ EXISTEN COMPONENTES FALTANTES - REVISAR ARRIBA{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
