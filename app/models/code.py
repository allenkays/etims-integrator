from typing import Optional
from pydantic import BaseModel


class CodeRequest(BaseModel):
    """Request model for the VSCU selectCode endpoint.
    Attributes:
        tin: The taxpayer identification number for the request.
        bhfId: The branch identifier for the request.
        lastReqDt: The last request date in 'YYYY-MM-DD' format.
    """
    tin: str
    bhfId: str
    lastReqDt: str


class CodeDetail(BaseModel):
    """Data model for a code detail returned by the VSCU selectCode endpoint.
    Attributes:
        cd: The code identifier.
        cdNm: The name of the code.
        cdDesc: An optional description of the code.
        srtOrd: An optional sort order for the code.
        userDfnCd1: An optional user-defined code for the code.
        userDfnCd2: An optional user-defined code for the code.
        userDfnCd3: An optional user-defined code for the code.
        useYn: A flag indicating whether the code is active.
    """
    cd: str
    cdNm: str
    cdDesc: Optional[str] = None
    srtOrd: Optional[int] = None
    userDfnCd1: Optional[str] = None
    userDfnCd2: Optional[str] = None
    userDfnCd3: Optional[str] = None
    useYn: str


class CodeClassification(BaseModel):
    """Data model for a code classification returned by the VSCU selectCode
        endpoint.
    Attributes:
        cdCls: The code classification identifier.
        cdClsNm: The name of the code classification.
        cdClsDesc: An optional description of the code classification.
        userDfnNm1: An optional user-defined name for the code classification.
        userDfnNm2: An optional user-defined name for the code classification.
        userDfnNm3: An optional user-defined name for the code classification.
        useYn: A flag indicating whether the code classification is active.
        dtlList: A list of CodeDetail objects representing the codes within
            this classification.
    """
    cdCls: str
    cdClsNm: str
    cdClsDesc: Optional[str] = None
    userDfnNm1: Optional[str] = None
    userDfnNm2: Optional[str] = None
    userDfnNm3: Optional[str] = None
    useYn: str
    dtlList: list[CodeDetail] = []


class CodeData(BaseModel):
    """Data model for the VSCU selectCode endpoint response.
    Attributes:
        clsList: A list of code classifications returned by the upstream API.
    """
    clsList: list[CodeClassification] = []


class CodeResponse(BaseModel):
    """Response model for the VSCU selectCode endpoint.
    Attributes:
        resultCd: The result code returned by the upstream API.
        resultMsg: The result message returned by the upstream API.
        resultDt: The timestamp of the response returned by the upstream API.
        data: The code data returned by the upstream API, if any.
    """
    resultCd: str
    resultMsg: str
    resultDt: str
    data: Optional[CodeData] = None
