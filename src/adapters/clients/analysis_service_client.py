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

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, data=data, files=files)

        if response.status_code >= 400:
            raise AnalysisServiceError(
                f"Error {response.status_code} desde Analysis-service: {response.text}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise AnalysisServiceError(
                "La respuesta del servicio de análisis no es JSON válido."
            ) from exc

