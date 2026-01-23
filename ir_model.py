# ir_model.py
from typing import Dict, Any, List, Optional
import re
from industry_data import INDUSTRY_DATA


# MASTER definition (simplified, same as you approved)
MASTER = {
    "factorGroups": {
        "STRUCTURAL": {
            "name": "Structural Factors",
            "factors": {
                "COMPETITIVENESS": {
                    "name": "Competitiveness",
                    "assessmentOptions": [
                        {"label": "NONE", "score": 600},
                        {"label": "UNTHREATENING", "score": 400},
                        {"label": "AGGRESSIVE", "score": 200},
                        {"label": "HOSTILE", "score": 0}
                    ]
                },
                "ENVIRONMENTAL_CONCERNS": {
                    "name": "Environmental Concerns",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                },
                "FISCAL_POLICY_DEPENDENCE": {
                    "name": "Fiscal Policy Dependence",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                }
            }
        },
        "ECONOMIC": {
            "name": "Economic Conditions",
            "factors": {
                "BUSINESS_CYCLICALITY": {
                    "name": "Business Cyclicality",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                },
                "INFLATION_SENSITIVITY": {
                    "name": "Inflation Sensitivity",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                },
                "FX_SENSITIVITY": {
                    "name": "FX Sensitivity",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                },
                "INTEREST_RATE_SENSITIVITY": {
                    "name": "Interest Rate Sensitivity",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                }
            }
        },
        "INDUSTRY_PERFORMANCE": {
            "name": "Industry Performance",
            "factors": {
                "INDUSTRY_SALES_TREND": {
                    "name": "Industry Sales Trend",
                    "assessmentOptions": [
                        {"label": "STRONGDECREASE", "score": 600},
                        {"label": "DECREASE", "score": 450},
                        {"label": "STABLE", "score": 300},
                        {"label": "INCREASE", "score": 150},
                        {"label": "STRONGINCREASE", "score": 0}
                    ]
                },
                "INDUSTRY_PROFITABILITY": {
                    "name": "Industry Profitability",
                    "assessmentOptions": [
                        {"label": "STRONGDECREASE", "score": 600},
                        {"label": "DECREASE", "score": 450},
                        {"label": "STABLE", "score": 300},
                        {"label": "INCREASE", "score": 150},
                        {"label": "STRONGINCREASE", "score": 0}
                    ]
                },
                "INDUSTRY_STAGE": {
                    "name": "Industry Stage",
                    "assessmentOptions": [
                        {"label": "ENTREPRENEURIAL", "score": 600},
                        {"label": "GROWTH/EARLY", "score": 450},
                        {"label": "GROWTH/MATURE", "score": 300},
                        {"label": "STABLE/MATURE", "score": 150},
                        {"label": "DECLINE", "score": 0}
                    ]
                },
                "IMPORT_PENETRATION": {
                    "name": "Import Penetration",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                },
                "INDUSTRY_FAILURE_RATE": {
                    "name": "Industry Failure Rate",
                    "assessmentOptions": [
                        {"label": "LOW", "score": 600},
                        {"label": "AVERAGE", "score": 400},
                        {"label": "HIGH", "score": 200},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                }
            }
        },
        "PRODUCTION_CONDITIONS": {
            "name": "Production Conditions",
            "factors": {
                "SKILLED_LABOUR_GAP": {
                    "name": "Skilled Labour Gap",
                    "assessmentOptions": [
                        {"label": "FULLYAVAILABLE", "score": 600},
                        {"label": "SMALLGAP", "score": 400},
                        {"label": "SOMEPROBLEMS", "score": 200},
                        {"label": "LARGEGAP", "score": 0}
                    ]
                },
                "PRODUCT_POSITIONING": {
                    "name": "Product Positioning",
                    "assessmentOptions": [
                        {"label": "CUSTOM", "score": 600},
                        {"label": "HIGH", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "SLIGHT", "score": 150},
                        {"label": "COMMODITY", "score": 0}
                    ]
                },
                "CAPITAL_SENSITIVITY": {
                    "name": "Capital Sensitivity",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                },
                "TECHNOLOGY_DEPENDENCE": {
                    "name": "Technology Dependence",
                    "assessmentOptions": [
                        {"label": "INSIGNIFICANT", "score": 600},
                        {"label": "LOW", "score": 450},
                        {"label": "MODERATE", "score": 300},
                        {"label": "HIGH", "score": 150},
                        {"label": "VERYHIGH", "score": 0}
                    ]
                }
            }
        }
    }
}

FACTOR_WEIGHT = 1 / 16  # per earlier design

# ---------- helpers ----------

def _normalize_factor_key(label: str) -> str:
    """
    Normalize human-readable factor label to uppercase underscore key,
    removing punctuation and collapsing spaces.
    Also normalizes LABOR -> LABOUR to match MASTER.
    """
    k = str(label).upper()

    # replace punctuation / spaces with underscore
    k = re.sub(r'[^A-Z0-9]+', '_', k)
    k = re.sub(r'__+', '_', k).strip('_')

    # 🔧 FIX: normalize US vs UK spelling
    k = k.replace("LABOR", "LABOUR")

    return k


def _find_factor_def(normalized_key: str) -> Optional[Dict[str, Any]]:
    """
    Search MASTER factorGroups for the normalized key.
    Returns the factor definition dict (copy) plus _group key, or None.
    """
    for group_key, group in MASTER["factorGroups"].items():
        factors = group.get("factors", {})
        if normalized_key in factors:
            d = factors[normalized_key].copy()
            d["_group"] = group_key
            return d
    return None

def _lookup_score_from_def(factor_def: Optional[Dict[str, Any]], qualitative_value: str) -> int:
    """
    Given a factor definition and qualitative label return the numeric score.
    If not found, return 0 (safe fallback).
    """
    if not factor_def:
        return 0
    av = str(qualitative_value).strip().upper()
    for opt in factor_def.get("assessmentOptions", []):
        if opt.get("label", "").upper() == av:
            return int(opt.get("score", 0))
    # loose matching: remove non-alnum and compare startswith
    av_norm = re.sub(r'[^A-Z0-9]', '', av)
    for opt in factor_def.get("assessmentOptions", []):
        lab_norm = re.sub(r'[^A-Z0-9]', '', str(opt.get("label","")).upper())
        if lab_norm.startswith(av_norm) or av_norm.startswith(lab_norm):
            return int(opt.get("score", 0))
    return 0

# ---------- main functions ----------

def calculate_ir(industry_name: str) -> Dict[str, Any]:
    """
    Compute IR score using INDUSTRY_DATA and MASTER.
    Returns structured JSON:
    {
      "industry": "...",
      "ir_score": float,
      "factor_weight": FACTOR_WEIGHT,
      "factors": [ {factor, qualitative_value, group, raw_score, weighted_score}, ... ]
    }
    """
    if industry_name not in INDUSTRY_DATA:
        raise ValueError(f"Industry '{industry_name}' not found")

    industry_factors = INDUSTRY_DATA[industry_name]
    total_score = 0.0
    breakdown = []

    for factor_label, qualitative_value in industry_factors.items():
        normalized = _normalize_factor_key(factor_label)
        factor_def = _find_factor_def(normalized)
        raw_score = _lookup_score_from_def(factor_def, qualitative_value)
        weighted = raw_score * FACTOR_WEIGHT
        total_score += weighted

        breakdown.append({
            "factor": factor_label,
            "qualitative_value": qualitative_value,
            "group": factor_def.get("_group") if factor_def else None,
            "raw_score": raw_score,
            "weighted_score": round(weighted, 3)
        })

    return {
        "industry": industry_name,
        "ir_score": round(total_score, 3),
        "factor_weight": FACTOR_WEIGHT,
        "factors": breakdown
    }

def generate_matrix() -> Dict[str, Any]:
    """
    Create a matrix representation:
      - industries: [list of industry names in consistent order]
      - factors: [list of factor labels in order]
      - matrix: { factor_label: { industry_name: qualitative_value, ... }, ... }
    Useful for rendering the spreadsheet-like table.
    """
    industries = list(INDUSTRY_DATA.keys())
    # gather unique factor labels in order of MASTER factorGroups, falling back to any keys in INDUSTRY_DATA
    factors_ordered: List[str] = []
    for group in MASTER["factorGroups"].values():
        for k, v in group["factors"].items():
            # the displayed label is v["name"]
            factors_ordered.append(v["name"])

    # also include any other factor labels that exist in industry_data but not in MASTER (defensive)
    extra_factors = []
    for ind in industries:
        for f in INDUSTRY_DATA[ind].keys():
            if f not in factors_ordered and f not in extra_factors:
                extra_factors.append(f)
    factors_ordered.extend(extra_factors)

    matrix = {}
    for f in factors_ordered:
        row = {}
        for ind in industries:
            row[ind] = INDUSTRY_DATA[ind].get(f, "")  # empty if missing
        matrix[f] = row

    return {
        "industries": industries,
        "factors": factors_ordered,
        "matrix": matrix
    }
