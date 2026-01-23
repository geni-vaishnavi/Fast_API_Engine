# fr_logic.py
from typing import Dict, Any

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


class APARFinancialModel:
    def __init__(self, data_dict: Dict[str, Dict[str, float]]):
        self.data = data_dict

    def _calculate_single_year(
        self, year: str, prev_year_revenue: float = None
    ) -> Dict[str, float]:

        fin = self.data.get(year, {})
        if not fin:
            return {}

        npm = fin.get("Net Profit", 0.0) / fin.get("Net Sales", 1)
        growth = (
            (fin["Net Sales"] - prev_year_revenue) / prev_year_revenue
            if prev_year_revenue else 0.0
        )
        cf_ebitda = fin.get("Operating Cash flows", 0.0) / fin.get("EBITDA", 1)
        dscr = fin.get("EBITDA", 0.0) / fin.get("Debt Service", 1)
        icr = fin.get("EBIT", 0.0) / fin.get("Interest Payments", 1)
        curr_ratio = fin.get("Current Assets", 0.0) / fin.get("Current Liabilities", 1)

        ccc = 0.0
        if fin.get("COGS") and fin.get("Net Sales"):
            inv = fin.get("Inventory", 0.0) / fin["COGS"] * 365
            rec = fin.get("Trade and other receivables", 0.0) / fin["Net Sales"] * 365
            pay = fin.get("Trade Creditors", 0.0) / fin["COGS"] * 365
            ccc = inv + rec - pay

        tnw = fin.get("Shareholders Equity", 0.0) - fin.get("Intangible assets", 0.0)
        leverage = fin.get("Total Liabilities", 0.0) / tnw if tnw else 0.0

        return {
            "Net Profit Margin": npm,
            "Sales Growth or Turnover Growth": growth,
            "Net CF from Operations/EBITDA": cf_ebitda,
            "DSCR": dscr,
            "Interest coverage ratio (ICR)": icr,
            "Current Ratio": curr_ratio,
            "Cash Conversion Cycle": ccc,
            "Leverage (Debt / Tangible Net Worth)": leverage
        }

    def get_weighted_ratios(self, eval_year: str, prev_year: str, hist_rev: float):
        prev = self._calculate_single_year(prev_year, hist_rev)
        curr = self._calculate_single_year(eval_year, self.data[prev_year]["Net Sales"])

        final = {}
        for k in curr:
            final[k] = curr[k] if k == "Leverage (Debt / Tangible Net Worth)" \
                else curr[k] * 0.70 + prev.get(k, 0.0) * 0.30
        return final


def get_score(metric: str, value: float) -> int:

    if metric == "Cash Conversion Cycle":
        return 600 if value <= 30.01 else 300 if value <= 60.01 else 0

    if metric == "Leverage (Debt / Tangible Net Worth)":
        if value <= 1.00: return 500
        if value <= 1.70: return 400
        if value <= 2.50: return 300
        if value <= 3.00: return 200
        if value <= 3.50: return 100
        return 0

    for threshold, score in RULES.get(metric, []):
        if value >= threshold:
            return score
    return 0


def calculate_fr_score(inputs: Dict[str, Dict[str, float]]) -> Dict[str, Any]:

    years = sorted(inputs.keys())
    eval_year, prev_year, hist_year = (
        (years[-1], years[-2], years[-3]) if len(years) >= 3
        else (years[-1], years[-2], years[-2])
    )

    model = APARFinancialModel(inputs)
    ratios = model.get_weighted_ratios(
        eval_year, prev_year, inputs[hist_year]["Net Sales"]
    )

    financial_ratios = {}
    total_score = 0.0

    for metric, weight in WEIGHTS.items():
        value = round(ratios.get(metric, 0.0), 3)
        score = get_score(metric, value)

        total_score += score * weight

        financial_ratios[metric] = {
            "value": value,
            "score": score,
            "weight_percent": int(weight * 100)
        }

    return {
        "total_score": round(total_score, 3),
        "financial_ratios": financial_ratios
    }
