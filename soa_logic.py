# soa_logic.py

YEAR_IN_BUSINESS_SCORE = {
    1: 600,
    2: 400,
    3: 200,
    4: 0
}

LOCATION_SCORE = {
    1: 600,
    2: 300,
    3: 0
}

RELATIONSHIP_AGE_SCORE = {
    1: 600,
    2: 400,
    3: 200,
    4: 0
}

AUDITOR_QUALITY_SCORE = {
    1: 600,
    2: 450,
    3: 300,
    4: 150,
    5: 0
}

AUDITOR_OPINION_SCORE = {
    1: 600,
    2: 450,
    3: 0,
    4: 0,
    5: 0
}

NATIONALIZATION_SCORE = {
    1: 600,
    2: 450,
    3: 300,
    4: 0,
    5: 0
}

WEIGHTS = {
    "year_in_business": 0.20,
    "location": 0.15,
    "relationship_age": 0.10,
    "auditor_quality": 0.20,
    "auditor_opinion": 0.20,
    "nationalization": 0.15
}

def calculate_soa_score(inputs: dict) -> float:
    total = 0

    total += YEAR_IN_BUSINESS_SCORE[inputs["year_in_business"]] * WEIGHTS["year_in_business"]
    total += LOCATION_SCORE[inputs["location"]] * WEIGHTS["location"]
    total += RELATIONSHIP_AGE_SCORE[inputs["relationship_age"]] * WEIGHTS["relationship_age"]
    total += AUDITOR_QUALITY_SCORE[inputs["auditor_quality"]] * WEIGHTS["auditor_quality"]
    total += AUDITOR_OPINION_SCORE[inputs["auditor_opinion"]] * WEIGHTS["auditor_opinion"]
    total += NATIONALIZATION_SCORE[inputs["nationalization"]] * WEIGHTS["nationalization"]

    return round(total, 1)
