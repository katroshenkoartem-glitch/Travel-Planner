import httpx
import logging
from fastapi import HTTPException, logger, status

logger = logging.getLogger(__name__)


class ChicagoAPIClient:

    BASE_URL = "https://api.artic.edu/api/v1/artworks"

    @classmethod
    async def check_place_exists(cls, external_id: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{cls.BASE_URL}/{external_id}")
                return response.status_code == 200
        except Exception as exc:
            logger.error(f"Unexpected error in Chicago API client: {exc}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error while validating the place.",
            )
