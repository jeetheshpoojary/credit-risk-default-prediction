import streamlit as st
from prediction_helper import predict


# -------------------------------------------------------
# Applicant Information
# -------------------------------------------------------
def applicant_info():
    st.subheader("👤 Applicant Information")

    col1, col2 = st.columns(2)

    age = col1.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=28,
        step=1
    )

    residence_type = col2.selectbox(
        "Residence Type",
        ["Owned", "Rented", "Mortgage"]
    )

    return age, residence_type


# -------------------------------------------------------
# Loan Information
# -------------------------------------------------------
def loan_info():
    st.subheader("🏦 Loan Information")

    col1, col2, col3 = st.columns(3)

    income = col1.number_input(
        "Annual Income",
        min_value=1.0,
        value=1200000.0,
        step=10000.0
    )

    loan_amount = col2.number_input(
        "Loan Amount",
        min_value=1.0,
        value=2500000.0,
        step=10000.0
    )

    loan_tenure_months = col3.number_input(
        "Loan Tenure (Months)",
        min_value=1,
        value=36,
        step=1
    )

    col1, col2 = st.columns(2)

    loan_purpose = col1.selectbox(
        "Loan Purpose",
        ["Education", "Home", "Personal", "Auto"]
    )

    loan_type = col2.selectbox(
        "Loan Type",
        ["Secured", "Unsecured"]
    )

    return (
        income,
        loan_amount,
        loan_tenure_months,
        loan_purpose,
        loan_type
    )


# -------------------------------------------------------
# Credit History
# -------------------------------------------------------
def credit_history():
    st.subheader("💳 Credit History")

    col1, col2, col3 = st.columns(3)

    num_open_accounts = col1.number_input(
        "Number of Open Loan Accounts",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    credit_utilization_ratio = col2.number_input(
        "Credit Utilization Ratio (%)",
        min_value=0.0,
        max_value=100.0,
        value=35.0
    )

    delinquency_ratio = col3.number_input(
        "Delinquency Ratio (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1
    )

    return (
        num_open_accounts,
        credit_utilization_ratio,
        delinquency_ratio
    )


# -------------------------------------------------------
# Calculated Features
# -------------------------------------------------------
def engineered_features(
    income,
    loan_amount,
    loan_tenure_months,
):
    loan_to_income = (
        round(loan_amount / income, 2)
        if income > 0
        else 0
    )

    monthly_installment = (
        round(loan_amount / loan_tenure_months, 2)
        if loan_tenure_months > 0
        else 0
    )

    st.subheader("⚙️ Automatically Calculated Features")

    c1, c2 = st.columns(2)

    c1.metric("Loan To Income", loan_to_income)
    c2.metric("Monthly Installment", f"{monthly_installment:,.2f}")


# -------------------------------------------------------
# Prediction
# -------------------------------------------------------
def prediction_section(
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

    if st.button("Calculate Credit Risk", use_container_width=True):

        probability, credit_score, rating = predict(
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

        st.subheader("📈 Prediction Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Default Probability",
            f"{probability:.2%}"
        )

        col2.metric(
            "Credit Score",
            credit_score
        )

        col3.metric(
            "Credit Rating",
            rating
        )

        if probability < 0.30:
            st.success("✅ Low Credit Risk")

        elif probability < 0.60:
            st.warning("⚠️ Medium Credit Risk")

        else:
            st.error("❌ High Credit Risk")


# -------------------------------------------------------
# Main
# -------------------------------------------------------
def main():

    st.set_page_config(
        page_title="Credit Risk Prediction System",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 Credit Risk Prediction System")

    st.markdown(
        "Provide the applicant's information below to estimate the probability of loan default."
    )

    age, residence_type = applicant_info()

    (
        income,
        loan_amount,
        loan_tenure_months,
        loan_purpose,
        loan_type,
    ) = loan_info()

    (
        num_open_accounts,
        credit_utilization_ratio,
        delinquency_ratio,
    ) = credit_history()

    engineered_features(
        income,
        loan_amount,
        loan_tenure_months,
    )

    prediction_section(
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


if __name__ == "__main__":
    main()