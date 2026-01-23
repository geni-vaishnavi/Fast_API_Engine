# coa_logic.py

WEIGHTS = {
    "bounce_cheques": 0.20,
    "ongoing_relationship": 0.15,
    "delay_installments": 0.20,
    "delinquency_history": 0.20,
    "write_off": 0.10,
    "fraud_litigation": 0.15
}

SCORE_MAP = {
    "bounce_cheques": {
        1: 600,
        2: 400,
        3: 200,
        4: 0
    },
    "ongoing_relationship": {
        1: 600,
        2: 400,
        3: 200,
        4: 0
    },
    "delay_installments": {
        1: 600,
        2: 400,
        3: 200,
        4: 0
    },
    "delinquency_history": {
        1: 600,
        2: 400,
        3: 200,
        4: 0
    },
    "write_off": {
        1: 600,
        2: 0
    },
    "fraud_litigation": {
        1: 600,
        2: 400,
        3: 200,
        4: 0
    }
}

def calculate_coa_score(input_codes: dict) -> int:
    total_score = 0

    for field, weight in WEIGHTS.items():
        if field not in input_codes:
            raise ValueError(f"Missing field: {field}")

        code = input_codes[field]

        if code not in SCORE_MAP[field]:
            raise ValueError(f"Invalid code {code} for {field}")

        raw_score = SCORE_MAP[field][code]
        total_score += raw_score * weight

    return round(total_score)
