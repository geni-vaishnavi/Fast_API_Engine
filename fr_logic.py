# fr_logic.py
from typing import Dict, Any


# 1. WEIGHTS & SCORING RULES 

WEIGHTS = {
    "Net Profit Margin": 0.15,
    "Sales Growth or Turnover Growth": 0.15,
    "Net CF from Operations/EBITDA": 0.15,
    "DSCR": 0.15,
    "Interest coverage ratio (ICR)": 0.10,
    "Current Ratio": 0.10,
    "Cash Conversion Cycle": 0.10,
    "Leverage (Debt / Tangible Net Worth)": 0.10
}

RULES = {
    "Net Profit Margin": [
        (0.15, 600), (0.12, 500), (0.10, 400),
        (0.08, 300), (0.05, 200), (0.02, 100)
    ],
    "Sales Growth or Turnover Growth": [
        (0.25, 600), (0.19, 500), (0.17, 400),
        (0.15, 300), (0.12, 200), (0.05, 100)
    ],
    "Net CF from Operations/EBITDA": [
        (4.00, 600), (3.00, 500), (2.00, 400),
        (1.00, 300), (0.50, 200), (0.01, 100)
    ],
    "DSCR": [
        (2.50, 600), (2.25, 500), (2.00, 400),
        (1.75, 300), (1.50, 200), (1.25, 100)
    ],
    "Interest coverage ratio (ICR)": [
        (4.00, 600), (3.50, 500), (3.00, 400),
        (2.00, 300), (1.50, 200), (1.00, 100)
    ],
    "Current Ratio": [
        (2.70, 600), (2.30, 500), (1.80, 400),
        (1.50, 300), (1.25, 200), (1.00, 100)
    ]
}


# 2. CORE FR ENGINE 


class APARFinancialModel:
    def __init__(self, data: Dict[str, Dict[str, float]]):
        self.data = data

    def calculate_single_year(self, year: str, prev_sales: float = None) -> Dict[str, float]:
        fin = self.data[year]

        npm = fin["Net Profit"] / fin["Net Sales"]
        growth = ((fin["Net Sales"] - prev_sales) / prev_sales) if prev_sales else 0.0

        cf_ebitda = fin["Operating Cash flows"] / fin["EBITDA"]
        dscr = fin["EBITDA"] / fin["Debt Service"]
        icr = fin["EBIT"] / fin["Interest Payments"]
        current_ratio = fin["Current Assets"] / fin["Current Liabilities"]

        inv_days = (fin["Inventory"] / fin["COGS"]) * 365
        rec_days = (fin["Trade and other receivables"] / fin["Net Sales"]) * 365
        pay_days = (fin["Trade Creditors"] / fin["COGS"]) * 365
        ccc = inv_days + rec_days - pay_days

        tnw = fin["Shareholders Equity"] - fin["Intangible assets"]
        leverage = fin["Total Liabilities"] / tnw

        return {
            "Net Profit Margin": npm,
            "Sales Growth or Turnover Growth": growth,
            "Net CF from Operations/EBITDA": cf_ebitda,
            "DSCR": dscr,
            "Interest coverage ratio (ICR)": icr,
            "Current Ratio": current_ratio,
            "Cash Conversion Cycle": ccc,
            "Leverage (Debt / Tangible Net Worth)": leverage
        }

    def weighted_ratios(self, curr_year: str, prev_year: str, hist_sales: float) -> Dict[str, float]:
        prev = self.calculate_single_year(prev_year, hist_sales)
        curr = self.calculate_single_year(curr_year, self.data[prev_year]["Net Sales"])

        final = {}
        for k in curr:
            if k == "Leverage (Debt / Tangible Net Worth)":
                final[k] = curr[k]
            else:
                final[k] = 0.70 * curr[k] + 0.30 * prev[k]
        return final


# 3. SCORING FUNCTION


def get_score(metric: str, value: float) -> int:
    if metric == "Cash Conversion Cycle":
        if value <= 30.01: return 600
        elif value <= 60.01: return 300
        return 0

    if metric == "Leverage (Debt / Tangible Net Worth)":
        if value <= 1.00: return 500
        elif value <= 1.70: return 400
        elif value <= 2.50: return 300
        elif value <= 3.00: return 200
        elif value <= 3.50: return 100
        return 0

    for threshold, score in RULES.get(metric, []):
        if value >= threshold:
            return score
    return 0


# 4. FASTAPI ENTRY POINT


def calculate_fr_score(inputs: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
    years = sorted(inputs.keys())
    if len(years) < 3:
        raise ValueError("At least 3 years of data required")

    hist_year, prev_year, curr_year = years[-3], years[-2], years[-1]

    model = APARFinancialModel(inputs)

    prev_ratios = model.calculate_single_year(prev_year, inputs[hist_year]["Net Sales"])
    curr_ratios = model.calculate_single_year(curr_year, inputs[prev_year]["Net Sales"])
    weighted = model.weighted_ratios(curr_year, prev_year, inputs[hist_year]["Net Sales"])

    intermediate = {
        k: {
            "previous_year": round(prev_ratios[k], 4),
            "current_year": round(curr_ratios[k], 4)
        }
        for k in prev_ratios
    }

    total_score = 0.0
    breakdown = {}

    for metric, weight in WEIGHTS.items():
        value = round(weighted[metric], 3)
        score = get_score(metric, value)
        total_score += score * weight

        breakdown[metric] = {
            "value": value,
            "score": score,
            "weight_percent": int(weight * 100)
        }

    return {
        "total_score": round(total_score, 3),
        "financial_ratios": breakdown,
        "intermediate_financial_ratios": intermediate
    }
