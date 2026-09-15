"""Tests for the initialization data models."""

import pytest
from pydantic import ValidationError
from app.models.code import (
    CodeRequest,
    CodeDetail,
    CodeClassification,
    CodeData,
    CodeResponse,
)
from app.models.initialization import (
    InitInfoRequest,
    InitTaxpayer,
    InitBranch,
    InitDevice,
    InitInfoResponse,
)
from app.models.item_classification import (
    ItemClassification,
    ItemClassificationRequest,
    ItemClassificationResponse,
)


class TestInitInfoRequest:
    """Tests for the InitInfoRequest model."""

    def test_valid_request(self):
        """Test creating a valid InitInfoRequest."""
        request = InitInfoRequest(
            tin="123456789",
            bhfId="BRN001",
            dvcSrlNo="DEVICE001"
        )
        assert request.tin == "123456789"
        assert request.bhfId == "BRN001"
        assert request.dvcSrlNo == "DEVICE001"

    def test_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            InitInfoRequest(tin="123456789", bhfId="BRN001")

    def test_missing_all_fields(self):
        """Test that missing all fields raises ValidationError."""
        with pytest.raises(ValidationError):
            InitInfoRequest()

    def test_model_dump(self):
        """Test converting model to dictionary."""
        request = InitInfoRequest(
            tin="123456789",
            bhfId="BRN001",
            dvcSrlNo="DEVICE001"
        )
        data = request.model_dump()
        assert data == {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }


class TestInitTaxpayer:
    """Tests for the InitTaxpayer model."""

    def test_valid_taxpayer(self):
        """Test creating a valid InitTaxpayer."""
        taxpayer = InitTaxpayer(
            tin="123456789",
            taxprNm="Example Company",
            bsnsActv="Manufacturing"
        )
        assert taxpayer.tin == "123456789"
        assert taxpayer.taxprNm == "Example Company"
        assert taxpayer.bsnsActv == "Manufacturing"

    def test_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            InitTaxpayer(
                tin="123456789",
                taxprNm="Example Company"
            )

    def test_model_validate_from_dict(self):
        """Test validating from dictionary."""
        data = {
            "tin": "123456789",
            "taxprNm": "Example Company",
            "bsnsActv": "Manufacturing"
        }
        taxpayer = InitTaxpayer.model_validate(data)
        assert taxpayer.tin == "123456789"


class TestInitBranch:
    """Tests for the InitBranch model."""

    def test_valid_branch(self):
        """Test creating a valid InitBranch."""
        branch = InitBranch(
            bhfId="BRN001",
            bhfNm="Main Branch",
            bhfOpenDt="2020-01-01",
            prvncNm="Kigali",
            dstrtNm="Gasabo",
            sctrNm="Gacuriro",
            locDesc="Main office location",
            hqYn="Y",
            mgrNm="John Doe",
            mgrTelNo="250788123456",
            mgrEmail="john@example.com"
        )
        assert branch.bhfId == "BRN001"
        assert branch.hqYn == "Y"

    def test_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            InitBranch(
                bhfId="BRN001",
                bhfNm="Main Branch",
                bhfOpenDt="2020-01-01"
            )

    def test_all_required_fields(self):
        """Test that all required fields are actually required."""
        # required_fields = {
        #     "bhfId", "bhfNm", "bhfOpenDt", "prvncNm", "dstrtNm",
        #     "sctrNm", "locDesc", "hqYn", "mgrNm", "mgrTelNo", "mgrEmail"
        # }
        partial_data = {
            "bhfId": "BRN001",
            "bhfNm": "Main Branch",
            "bhfOpenDt": "2020-01-01",
            "prvncNm": "Kigali",
            "dstrtNm": "Gasabo",
            "sctrNm": "Gacuriro",
            "locDesc": "Main office location",
            "hqYn": "Y",
            "mgrNm": "John Doe",
            "mgrTelNo": "250788123456",
        }
        # Remove last required field
        with pytest.raises(ValidationError):
            InitBranch.model_validate(partial_data)


class TestInitDevice:
    """Tests for the InitDevice model."""

    def test_valid_device_minimal(self):
        """Test creating a valid InitDevice with minimal fields."""
        device = InitDevice(dvcId="DEVICE001")
        assert device.dvcId == "DEVICE001"
        assert device.sdicId is None
        assert device.mrcNo is None

    def test_valid_device_full(self):
        """Test creating a valid InitDevice with all fields."""
        device = InitDevice(
            dvcId="DEVICE001",
            sdicId="SDIC123",
            mrcNo="MRC001",
            intrlKey="key1",
            signKey="key2",
            cmcKey="key3",
            lastSaleInvcNo=100,
            lastPchsInvcNo=50,
            lastSaleRcptNo=75,
            lastInvcNo=120,
            lastTrainInvcNo=10,
            lastProfrmInvcNo=5,
            lastCopyInvcNo=15
        )
        assert device.dvcId == "DEVICE001"
        assert device.sdicId == "SDIC123"
        assert device.lastSaleInvcNo == 100

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        device = InitDevice(dvcId="DEVICE001")
        assert device.sdicId is None
        assert device.mrcNo is None
        assert device.intrlKey is None
        assert device.signKey is None
        assert device.cmcKey is None
        assert device.lastSaleInvcNo is None

    def test_invoice_numbers_as_integers(self):
        """Test that invoice numbers are integers."""
        device = InitDevice(
            dvcId="DEVICE001",
            lastSaleInvcNo=100
        )
        assert isinstance(device.lastSaleInvcNo, int)
        assert device.lastSaleInvcNo == 100


class TestInitInfoResponse:
    """Tests for the InitInfoResponse model."""

    def test_valid_response_full(self):
        """Test creating a valid InitInfoResponse with full data."""
        response = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "info": {
                    "taxpayer": {
                        "tin": "123456789",
                        "taxprNm": "Example Company",
                        "bsnsActv": "Manufacturing"
                    },
                    "branch": {
                        "bhfId": "BRN001",
                        "bhfNm": "Main Branch",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Gasabo",
                        "sctrNm": "Gacuriro",
                        "locDesc": "Main office location",
                        "hqYn": "Y",
                        "mgrNm": "John Doe",
                        "mgrTelNo": "250788123456",
                        "mgrEmail": "john@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE001",
                        "lastSaleInvcNo": 100
                    }
                }
            }
        )

        assert response.resultCd == "00"
        assert response.resultMsg == "Success"
        assert response.data is not None
        assert response.data.info is not None
        assert response.data.info.taxpayer.tin == "123456789"

    def test_valid_response_minimal(self):
        """Test creating a valid InitInfoResponse with minimal data."""
        response = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z"
        )

        assert response.resultCd == "00"
        assert response.resultMsg == "Success"
        assert response.data is None

    def test_missing_required_result_code(self):
        """Test that missing resultCd raises ValidationError."""
        with pytest.raises(ValidationError):
            InitInfoResponse(
                resultMsg="Success",
                resultDt="2024-01-01T12:00:00Z"
            )

    def test_model_validate_from_dict(self):
        """Test validating InitInfoResponse from nested dictionary."""
        data = {
            "resultCd": "00",
            "resultMsg": "Success",
            "resultDt": "2024-01-01T12:00:00Z",
            "data": {
                "info": {
                    "taxpayer": {
                        "tin": "123456789",
                        "taxprNm": "Example Company",
                        "bsnsActv": "Manufacturing"
                    },
                    "branch": {
                        "bhfId": "BRN001",
                        "bhfNm": "Main Branch",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Gasabo",
                        "sctrNm": "Gacuriro",
                        "locDesc": "Main office location",
                        "hqYn": "Y",
                        "mgrNm": "John Doe",
                        "mgrTelNo": "250788123456",
                        "mgrEmail": "john@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE001",
                        "lastSaleInvcNo": 100
                    }
                }
            }
        }
        response = InitInfoResponse.model_validate(data)
        assert response.resultCd == "00"
        assert response.data.info.taxpayer.tin == "123456789"


class TestCodeModels:
    """Tests for Code synchronization models."""

    def test_code_request(self):
        """Test creating a CodeRequest."""
        request = CodeRequest(
            tin="123456789",
            bhfId="BRN001",
            lastReqDt="20240101120000"
        )

        assert request.tin == "123456789"
        assert request.bhfId == "BRN001"
        assert request.lastReqDt == "20240101120000"

    def test_code_request_requires_all_fields(self):
        """Test CodeRequest requires all fields."""
        with pytest.raises(ValueError):
            CodeRequest(
                tin="123456789",
                bhfId="BRN001"
            )

    def test_code_detail(self):
        """Test creating a CodeDetail."""
        detail = CodeDetail(
            cd="A",
            cdNm="AEX",
            cdDesc="Exempt",
            srtOrd=1,
            useYn="Y"
        )

        assert detail.cd == "A"
        assert detail.cdNm == "AEX"
        assert detail.cdDesc == "Exempt"
        assert detail.srtOrd == 1
        assert detail.useYn == "Y"

    def test_code_classification(self):
        """Test creating a CodeClassification."""
        classification = CodeClassification(
            cdCls="04",
            cdClsNm="Tax Type",
            cdClsDesc="Tax type classification",
            useYn="Y",
            dtlList=[
                CodeDetail(
                    cd="A",
                    cdNm="AEX",
                    srtOrd=1,
                    useYn="Y"
                )
            ]
        )

        assert classification.cdCls == "04"
        assert classification.cdClsNm == "Tax Type"
        assert classification.useYn == "Y"
        assert len(classification.dtlList) == 1
        assert classification.dtlList[0].cd == "A"

    def test_code_data(self):
        """Test creating CodeData."""
        data = CodeData(
            clsList=[
                CodeClassification(
                    cdCls="04",
                    cdClsNm="Tax Type",
                    useYn="Y"
                )
            ]
        )

        assert len(data.clsList) == 1
        assert data.clsList[0].cdCls == "04"

    def test_code_response(self):
        """Test creating a CodeResponse."""
        response = CodeResponse(
            resultCd="000",
            resultMsg="Successful",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "clsList": [
                    {
                        "cdCls": "04",
                        "cdClsNm": "Tax Type",
                        "useYn": "Y",
                        "dtlList": [
                            {
                                "cd": "A",
                                "cdNm": "AEX",
                                "srtOrd": 1,
                                "useYn": "Y"
                            }
                        ]
                    }
                ]
            }
        )

        assert response.resultCd == "000"
        assert response.resultMsg == "Successful"
        assert len(response.data.clsList) == 1
        assert response.data.clsList[0].dtlList[0].cd == "A"


class TestItemClassificationModels:
    """Tests for the Item Classification models."""
    def test_request_model(self):
        """Test creating an ItemClassificationRequest."""
        request = ItemClassificationRequest(
            tin="A123456789Z",
            bhfId="00",
            lastReqDt="20180523000000",
        )

        assert request.tin == "A123456789Z"
        assert request.bhfId == "00"
        assert request.lastReqDt == "20180523000000"

    def test_item_classification_model(self):
        """Test creating an ItemClassification."""
        item_classification = ItemClassification(
            itemClsCd="1010101",
            itemClsNm="Test Classification",
            itemClsLvl=1,
            taxTyCd="A",
        )

        assert item_classification.itemClsCd == "1010101"
        assert item_classification.itemClsNm == "Test Classification"
        assert item_classification.itemClsLvl == 1
        assert item_classification.taxTyCd == "A"

    def test_response_model(self):
        """Test creating an ItemClassificationResponse."""
        response = ItemClassificationResponse(
            resultCd="000",
            resultMsg="Successful",
            resultDt="20260915190000",
            data=[
                ItemClassification(
                    itemClsCd="1010101",
                    itemClsNm="Test Classification",
                    itemClsLvl=1,
                    taxTyCd="A",
                )
            ],
        )

        assert response.resultCd == "000"
        assert response.resultMsg == "Successful"
        assert response.data is not None
        assert len(response.data) == 1
        assert response.data[0].itemClsCd == "1010101"
