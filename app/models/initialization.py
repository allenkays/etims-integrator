"""Data models used during the initialization workflow."""

from pydantic import BaseModel
from typing import Optional


class InitInfoRequest(BaseModel):
    """Request payload required to initialize a device with VSCU.

    Attributes:
        tin: Taxpayer identification number.
        bhfId: Business or branch identifier supplied by the integrator.
        dvcSrlNo: Device serial number associated with the initialization request.
    """

    tin: str
    bhfId: str
    dvcSrlNo: str


class InitTaxpayer(BaseModel):
    """Details about the taxpayer returned by the VSCU initialization API.

    Attributes:
        tin: Taxpayer identification number.
        taxprNm: Taxpayer or business name.
        bsnsActv: Business activity description or code.
    """

    tin: str
    taxprNm: str
    bsnsActv: str


class InitBranch(BaseModel):
    """Branch (business location) information returned by the initializer.

    Attributes:
        bhfId: Branch identifier.
        bhfNm: Branch name.
        bhfOpenDt: Branch opening date (string as returned by VSCU).
        prvncNm: Province name.
        dstrtNm: District name.
        sctrNm: Sector name.
        locDesc: Human-readable location description.
        hqYn: Flag indicating whether this branch is headquarter ('Y'/'N').
        mgrNm: Manager name.
        mgrTelNo: Manager telephone number.
        mgrEmail: Manager email address.
    """

    bhfId: str
    bhfNm: str
    bhfOpenDt: str
    prvncNm: str
    dstrtNm: str
    sctrNm: str
    locDesc: str
    hqYn: str
    mgrNm: str
    mgrTelNo: str
    mgrEmail: str


class InitDevice(BaseModel):
    """Device-specific information returned during initialization.

    Attributes:
        dvcId: Device identifier assigned by VSCU.
        sdicId: Optional secondary ID for the device.
        mrcNo: Optional merchant number.
        intrlKey: Optional internal key material (if provided).
        signKey: Optional signing key.
        cmcKey: Optional CMC key.

        lastSaleInvcNo: Last sale invoice number seen by the device.
        lastPchsInvcNo: Last purchase invoice number.
        lastSaleRcptNo: Last sale receipt number.
        lastInvcNo: Last invoice number.
        lastTrainInvcNo: Last training invoice number.
        lastProfrmInvcNo: Last proforma invoice number.
        lastCopyInvcNo: Last copy invoice number.
    """

    dvcId: str
    sdicId: Optional[str] = None
    mrcNo: Optional[str] = None
    intrlKey: Optional[str] = None
    signKey: Optional[str] = None
    cmcKey: Optional[str] = None

    lastSaleInvcNo: Optional[int] = None
    lastPchsInvcNo: Optional[int] = None
    lastSaleRcptNo: Optional[int] = None
    lastInvcNo: Optional[int] = None
    lastTrainInvcNo: Optional[int] = None
    lastProfrmInvcNo: Optional[int] = None
    lastCopyInvcNo: Optional[int] = None


class InitInfo(BaseModel):
    """Container for grouped initialization details.

    Attributes:
        taxpayer: Optional taxpayer details.
        branch: Optional branch details.
        device: Optional device details.
    """

    taxpayer: Optional[InitTaxpayer] = None
    branch: Optional[InitBranch] = None
    device: Optional[InitDevice] = None


class InitData(BaseModel):
    """Top-level data payload returned by the VSCU initializer.

    Attributes:
        info: The `InitInfo` object containing taxpayer/branch/device data.
    """

    info: Optional[InitInfo] = None


class InitInfoResponse(BaseModel):
    """Response model for the initialization endpoint.

    Attributes:
        resultCd: Result code returned by VSCU.
        resultMsg: Human-readable message accompanying the result code.
        resultDt: Timestamp string when the result was produced.
        data: Optional `InitData` payload with detailed information.
    """

    resultCd: str
    resultMsg: str
    resultDt: str
    data: Optional[InitData] = None