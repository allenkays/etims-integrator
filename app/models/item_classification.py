from typing import Optional

from pydantic import BaseModel


class ItemClassificationRequest(BaseModel):
    """
    A request model for item classification.
    """
    tin: str
    bhfId: str
    lastReqDt: str


class ItemClassification(BaseModel):
    """
    A model representing an item classification.
    """
    itemClsCd: str
    itemClsNm: str
    itemClsLvl: int
    taxTyCd: Optional[str] = None


class ItemClassificationResponse(BaseModel):
    """
    A response model for item classification requests.
    """
    resultCd: str
    resultMsg: str
    resultDt: str
    data: Optional[list[ItemClassification]] = None
