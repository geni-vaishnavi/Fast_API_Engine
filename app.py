from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Dict

from coa_logic import calculate_coa_score
from soa_logic import calculate_soa_score
from ir_model import calculate_ir
from fr_logic import calculate_fr_score
from fastapi import Body


app = FastAPI(title="COA + SOA + IR + FR Fast Engine")


# CORS (ALLOW ALL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# INPUT MODELS
# -----------------------------
class CoaInput(BaseModel):
    bounce_cheques: int = Field(..., ge=1, le=4)
    ongoing_relationship: int = Field(..., ge=1, le=4)
    delay_installments: int = Field(..., ge=1, le=4)
    delinquency_history: int = Field(..., ge=1, le=4)
    write_off: int = Field(..., ge=1, le=2)
    fraud_litigation: int = Field(..., ge=1, le=4)


class SoaInput(BaseModel):
    year_in_business: int = Field(..., ge=1, le=4)
    location: int = Field(..., ge=1, le=3)
    relationship_age: int = Field(..., ge=1, le=4)
    auditor_quality: int = Field(..., ge=1, le=5)
    auditor_opinion: int = Field(..., ge=1, le=5)
    nationalization: int = Field(..., ge=1, le=5)


class IRInput(BaseModel):
    industry: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Fast Engine is running",
        "endpoints": [
         
            "/docs"
        ]
    }

# FR: accept raw JSON mapping (years -> metrics)
# Example body (raw JSON): { "2022": {...}, "2023": {...}, "2024": {...} }
# We accept a generic dict payload
# -----------------------------
# API ENDPOINTS
# -----------------------------
@app.post("/coa/score")
def get_coa_score(payload: CoaInput):
    try:
        return {"coa_score": calculate_coa_score(payload.dict())}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/soa/score")
def get_soa_score(payload: SoaInput):
    try:
        return {"soa_score": calculate_soa_score(payload.dict())}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ir/score")
def get_ir_score(payload: IRInput):
    """
    Input: industry name
    Output: industry + IR score only
    """
    try:
        result = calculate_ir(payload.industry)

        # defensive: result may be dict or number
        if isinstance(result, dict):
            score = result.get("ir_score") or result.get("score") or None
        else:
            score = result

        if score is None:
            raise ValueError("IR score not found in model output")

        return {
            "industry": payload.industry,
            "ir_score": round(float(score), 3)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/fr/score")
def get_fr_score(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "2022": {
                "Net Sales": 116218.0,
                "COGS": 93951.0,
                "Total Liabilities": 121306.0,
                "EBITDA": 10775.0,
                "EBIT": 10775.0,
                "Current Assets": 128622.0,
                "Current Liabilities": 118787.0,
                "Interest Payments": 2682.0,
                "Debt Service": 38165.0,
                "Trade and other receivables": 59631.0,
                "Trade Creditors": 79816.0,
                "Shareholders Equity": 9949.0,
                "Intangible assets": 35.0,
                "Operating Cash flows": 11043.0,
                "Net Profit": 7825.0,
                "Inventory": 41131.0
            },
            "2023": {
                "Net Sales": 117554.0,
                "COGS": 93319.0,
                "Total Liabilities": 112566.0,
                "EBITDA": 14567.0,
                "EBIT": 14567.0,
                "Current Assets": 111109.0,
                "Current Liabilities": 105687.0,
                "Interest Payments": 5317.0,
                "Debt Service": 70119.0,
                "Trade and other receivables": 29104.0,
                "Trade Creditors": 35297.0,
                "Shareholders Equity": 18867.0,
                "Intangible assets": 25.0,
                "Operating Cash flows": 14900.0,
                "Net Profit": 8917.0,
                "Inventory": 7124.0
            },
            "2024": {
                "Net Sales": 135572.0,
                "COGS": 106486.0,
                "Total Liabilities": 153607.0,
                "EBITDA": 17926.0,
                "EBIT": 17926.0,
                "Current Assets": 161490.0,
                "Current Liabilities": 138351.0,
                "Interest Payments": 9744.0,
                "Debt Service": 76210.0,
                "Trade and other receivables": 19641.0,
                "Trade Creditors": 60131.0,
                "Shareholders Equity": 26392.0,
                "Intangible assets": 15.0,
                "Operating Cash flows": 18582.0,
                "Net Profit": 7526.0,
                "Inventory": 18289.0
            }
        }
    )
):
    try:
        return calculate_fr_score(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
