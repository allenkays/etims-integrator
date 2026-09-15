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
    """ A model representing an item classification."""
    itemClsCd: str
    itemClsNm: str
    itemClsLvl: int
    taxTyCd: Optional[str] = None
    mjrTgYn: Optional[str] = None
    useYn: str


class ItemClassificationData(BaseModel):
    """
    A model representing the data returned from an item classification request.
    """
    itemClsList: list[ItemClassification] = []


class ItemClassificationResponse(BaseModel):
    """
    A response model for item classification requests.
    """
    resultCd: str
    resultMsg: str
    resultDt: str
    data: Optional[ItemClassificationData] = None
