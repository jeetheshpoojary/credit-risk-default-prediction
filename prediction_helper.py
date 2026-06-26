import joblib
import pandas as pd

# -------------------------------------------------------
# Load Model
# -------------------------------------------------------

MODEL_PATH = "artifacts/brf_model.pkl"

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
scaler = model_data["scaler"]
features = model_data["features"]
cols_to_scale = model_data["cols_to_scale"]


# -------------------------------------------------------
# Prepare Input
# -------------------------------------------------------
def prepare_input(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    delinquency_ratio,
    credit_utilization_ratio,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type,
):

    monthly_installment = (
        loan_amount / loan_tenure_months
        if loan_tenure_months > 0
        else 0
    )

    loan_to_income = (
        round(loan_amount / income, 2)
        if income > 0
        else 0
    )

    input_data = {
        "age": age,
        "number_of_open_accounts": num_open_accounts,
        "credit_utilization_ratio": credit_utilization_ratio,
        "delinquency_ratio": delinquency_ratio,
        "monthly_installment": monthly_installment,
        "loan_to_income": loan_to_income,
        "residence_type_Owned": 1 if residence_type == "Owned" else 0,
        "residence_type_Rented": 1 if residence_type == "Rented" else 0,
        "loan_purpose_Education": 1 if loan_purpose == "Education" else 0,
        "loan_purpose_Home": 1 if loan_purpose == "Home" else 0,
        "loan_purpose_Personal": 1 if loan_purpose == "Personal" else 0,
        "loan_type_Unsecured": 1 if loan_type == "Unsecured" else 0,
    }

    input_df = pd.DataFrame([input_data])

    input_df = input_df.reindex(columns=features, fill_value=0)

    input_df[cols_to_scale] = scaler.transform(
        input_df[cols_to_scale]
    )

    return input_df


# -------------------------------------------------------
# Credit Score
# -------------------------------------------------------
def calculate_credit_score(default_probability):

    credit_score = int(
        300 + ((1 - default_probability) * 600)
    )

    if credit_score < 500:
        rating = "Poor"

    elif credit_score < 650:
        rating = "Average"

    elif credit_score < 750:
        rating = "Good"

    else:
        rating = "Excellent"

    return credit_score, rating


# -------------------------------------------------------
# Prediction
# -------------------------------------------------------
def predict(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    delinquency_ratio,
    credit_utilization_ratio,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type,
):

    input_df = prepare_input(
        age,
        income,
        loan_amount,
        loan_tenure_months,
        delinquency_ratio,
        credit_utilization_ratio,
        num_open_accounts,
        residence_type,
        loan_purpose,
        loan_type,
    )

    probability = model.predict_proba(input_df)[0][1]

    credit_score, rating = calculate_credit_score(
        probability
    )

    return probability, credit_score, rating