import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ERICA",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data
@st.cache_data
def load_data():
    # Replace this with your data loading code
    data = pd.read_csv('Resilience Score Analysis DF.csv')
    return data

data = load_data()
customer_data = data[data['CUSTOMER_ID'] == 17582714.2857]

st.title("Actionable Recommendations & Risk Mitigation Suggestions")

# Customer data variables
monthly_income = customer_data['MONTHLY_INCOME']
financial_health_score = customer_data['Financial Health_Score']
credit_reliability_score = customer_data['Credit Reliability_Score']
loan_amount = customer_data.get('LOAN_AMOUNT', 0)
bank_tenure = customer_data.get('BANK_TENURE', 0)

# Dynamic calculation of loan suggested percentage of income based on financial health
if financial_health_score > 0.75:
    loan_suggested_percentage_income = 0.2  # 20% for high financial health
elif 0.5 <= financial_health_score <= 0.75:
    loan_suggested_percentage_income = 0.15
else:
    loan_suggested_percentage_income = 0.1  # 10% for low financial health

# Dynamic calculation of savings percentage of income based on credit reliability
if credit_reliability_score > 0.75:
    savings_percentage_income = 0.15  # 15% for high credit reliability
elif 0.5 <= credit_reliability_score <= 0.75:
    savings_percentage_income = 0.20
else:
    savings_percentage_income = 0.25  # 25% for low credit reliability

# Dynamic calculation of recommended loan duration
if financial_health_score > 0.75:
    recommended_loan_duration_years = 3  # Shorter duration for good financial health
elif 0.5 <= financial_health_score <= 0.75:
    recommended_loan_duration_years = 5
else:
    recommended_loan_duration_years = 7  # Longer duration for lower financial health

# Dynamic calculation of savings target months
if credit_reliability_score > 0.75:
    savings_target_months = 3  # Lower savings target for high reliability
elif 0.5 <= credit_reliability_score <= 0.75:
    savings_target_months = 6
else:
    savings_target_months = 12  # Higher target for low reliability

# Loan Recommendation calculations based on income and dynamic loan duration
recommended_loan_amount = monthly_income * loan_suggested_percentage_income * 12 * recommended_loan_duration_years

# Savings Recommendation calculations based on dynamic savings target
recommended_savings_amount = monthly_income * savings_percentage_income * savings_target_months

# Display Actionable Recommendations
st.subheader("📑 Actionable Recommendations")
st.info("💡 Recommendations to improve financial resilience are provided based on the MSME's indicators.")

# Loan Recommendation based on loan indicators
auto_loan_indicator = customer_data.get('AUTO_LOAN_INDICATOR', 0)
housing_loan_indicator = customer_data.get('HOUSING_LOAN_INDICATOR', 0)

if auto_loan_indicator == 1 or housing_loan_indicator == 1:
    st.subheader("Loan Modification Options")
    st.write(f"""❗ **Loan Indicator**: It appears that your business has active loans. 
    Managing these responsibly is crucial for resilience:
    
    - **Recommended Loan Amount**: Based on your monthly income of {monthly_income:.2f}, we suggest a maximum loan amount of {recommended_loan_amount:.2f}.
    - **Suggested Loan Duration**: {recommended_loan_duration_years} years.
    - **Avoid Over-borrowing**: Ensure monthly loan payments are no more than {loan_suggested_percentage_income * 100:.1f}% of your monthly income.
    """)
else:
    st.write("✅ **Loan Indicator**: You don't have any active loans! You're on the right track.")

# Savings Recommendation based on account indicator and monthly income
if customer_data.get('SAVINGS_ACCOUNT_INDICATOR', 0) == 0:
    st.subheader("Savings Recommendations")
    st.write(f"""❗ **Savings Account Indicator**: It seems that you do not have an active savings account. 
    Building a financial buffer can significantly enhance resilience:
    
    - **Recommended Savings Target**: Aim to save up to {recommended_savings_amount:.2f} to cover **{savings_target_months} months** of expenses.
    - **Suggested Monthly Savings**: Set aside about {savings_percentage_income * 100:.1f}% of your monthly income ({monthly_income * savings_percentage_income:.2f}) for your savings fund.
    """)
else:
    st.write("✅ **Savings Account Indicator**: You have an active savings account. Good job staying prepared!")

# Explanation dropdown for Actionable Recommendations
with st.expander("What are actionable recommendations?"):
    st.write("""
    Recommendations are tailored based on indicators to help improve financial resilience:
    
    - **Loan Indicators**: MSMEs with active loans are advised on restructuring or adjusting loan terms to manage cash flow.
    - **Savings**: MSMEs without savings accounts are encouraged to save for at least 3 months of operating expenses to build resilience.
    - **Engagement**: Low engagement scores suggest exploring additional financial products that could support business needs during challenging times.
    """)
