# Integración Trace-Service ↔ Analysis-Service

## Variables de entorno necesarias

En `trace-service/.env` añade:

```env
# URL base del microservicio de análisis (incluye /v1)
ANALYSIS_SERVICE_BASE_URL=http://localhost:8001/v1
ANALYSIS_SERVICE_TIMEOUT=30
```

En `Analisys-service/.env` asegúrate de exponer su API en el puerto correcto
y habilitar CORS si es necesario.

## Flujo de petición

1. El usuario sube una práctica a `/practices/` en `trace-service`.
2. `trace-service` guarda la práctica en su base de datos.
3. Se envía la imagen y el carácter al endpoint `/analyze` de `analysis-service`.
4. La respuesta se mapea a `UpdateAnalysisRequestDTO` y se actualiza la práctica.
5. El usuario recibe la práctica con el análisis (o estado pendiente si falló).

## Dependencias

- Instala los requisitos de `trace-service`:
  ```bash
  pip install -r trace-service/requirements.txt
  ```
- `analysis-service` debe estar levantado y accesible en la URL configurada.

## Puertos sugeridos

- `trace-service`: `http://localhost:8000`
- `analysis-service`: `http://localhost:8001`

Configura tu `docker-compose` o entorno local para que ambos servicios puedan comunicarse.

