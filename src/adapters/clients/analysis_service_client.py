import httpx
from typing import Any, Dict, Optional


class AnalysisServiceError(Exception):
    """Error personalizado para fallos al comunicarse con el servicio de análisis."""


class AnalysisServiceClient:
    """Cliente HTTP para comunicarse con el microservicio de análisis."""

    def __init__(self, base_url: Optional[str], timeout: float = 30.0) -> None:
        if not base_url:
            raise AnalysisServiceError(
                "ANALYSIS_SERVICE_BASE_URL no está configurada."
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def analyze_letter(
        self,
        letter_char: str,
        image_bytes: bytes,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Envía la imagen al servicio de análisis y retorna las métricas."""
        if not image_bytes:
            raise AnalysisServiceError("La imagen recibida está vacía.")

        files = {
            "file": (
                filename or "practice.png",
                image_bytes,
                content_type or "application/octet-stream",
            )
        }
        data = {"letter_char": letter_char}
        url = f"{self.base_url}/analyze"
        
        print(f"[AnalysisServiceClient] Enviando petición a: {url}")
        print(f"[AnalysisServiceClient] Parámetros - letra: {letter_char}, tamaño imagen: {len(image_bytes)} bytes")

        # Configurar cliente HTTP con seguimiento automático de redirects y mejor timeout
        timeout_config = httpx.Timeout(
            connect=10.0,  # Timeout para establecer conexión
            read=self.timeout,  # Timeout para leer respuesta
            write=10.0,  # Timeout para escribir datos
            pool=5.0  # Timeout para obtener conexión del pool
        )
        
        async with httpx.AsyncClient(timeout=timeout_config, follow_redirects=True) as client:
            try:
                response = await client.post(url, data=data, files=files)
                print(f"[AnalysisServiceClient] Respuesta recibida: {response.status_code}")
            except httpx.ConnectError as exc:
                error_msg = f"No se pudo conectar al servicio de análisis en {url}. Verifica que el servicio esté corriendo."
                print(f"[AnalysisServiceClient] ERROR de conexión: {error_msg}")
                raise AnalysisServiceError(error_msg) from exc
            except httpx.TimeoutException as exc:
                error_msg = f"Timeout al esperar respuesta del servicio de análisis (timeout: {self.timeout}s)."
                print(f"[AnalysisServiceClient] ERROR de timeout: {error_msg}")
                raise AnalysisServiceError(error_msg) from exc
            except Exception as exc:
                error_msg = f"Error inesperado al comunicarse con el servicio de análisis: {type(exc).__name__}: {exc}"
                print(f"[AnalysisServiceClient] ERROR inesperado: {error_msg}")
                raise AnalysisServiceError(error_msg) from exc

        if response.status_code >= 400:
            error_detail = response.text[:500]  # Limitar tamaño del mensaje de error
            error_msg = f"Error {response.status_code} desde Analysis-service: {error_detail}"
            print(f"[AnalysisServiceClient] ERROR HTTP: {error_msg}")
            raise AnalysisServiceError(error_msg)

        try:
            result = response.json()
            print(f"[AnalysisServiceClient] Análisis completado exitosamente")
            return result
        except ValueError as exc:
            error_msg = f"La respuesta del servicio de análisis no es JSON válido. Status: {response.status_code}, Contenido: {response.text[:200]}"
            print(f"[AnalysisServiceClient] ERROR parsing JSON: {error_msg}")
            raise AnalysisServiceError(error_msg) from exc

