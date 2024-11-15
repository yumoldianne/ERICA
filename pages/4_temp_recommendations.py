import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ERICA",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

data = pd.read_csv('Resilience Score Analysis Unscaled.csv')

customer_data = data[data['CUSTOMER_ID'] == 17582714.2857]

# Customer data variables
monthly_income = customer_data['MONTHLY_INCOME'].values[0] if 'MONTHLY_INCOME' in customer_data else 0
financial_health_score = customer_data['Financial Health_Score'].values[0]
credit_reliability_score = customer_data['Credit Reliability_Score'].values[0]
loan_amount = customer_data['LOAN_AMOUNT'].values[0] if 'LOAN_AMOUNT' in customer_data else 0
bank_tenure = customer_data['BANK_TENURE'].values[0] if 'BANK_TENURE' in customer_data else 0

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
st.subheader("📑 Recommendations")
#st.info("💡 Recommendations to improve financial resilience are provided based on your existing assets and loans.")

auto_loan_indicator = customer_data['AUTO_LOAN_INDICATOR'].values[0] if 'AUTO_LOAN_INDICATOR' in customer_data else 0
housing_loan_indicator = customer_data['HOUSING_LOAN_INDICATOR'].values[0] if 'HOUSING_LOAN_INDICATOR' in customer_data else 0

# Constants for loan and savings calculations
RECOMMENDED_MAX_MONTHLY_INSTALLMENT_PERCENT = 0.2  # Max 20% of monthly income for loans
INTEREST_RATE = 0.06  # Annual interest rate
COMPOUNDING_PERIODS = 12  # Monthly compounding

# Function to calculate monthly installment
def calculate_monthly_installment(principal, annual_rate, years):
    monthly_rate = annual_rate / COMPOUNDING_PERIODS
    months = years * COMPOUNDING_PERIODS
    if monthly_rate == 0:  # Handle case where interest rate is zero
        return principal / months
    return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

# Dynamic variables for recommendations
monthly_income = customer_data['MONTHLY_INCOME'].values[0] if 'MONTHLY_INCOME' in customer_data else 0
loan_suggested_percentage_income = 0.15  # Recommend 15% of monthly income for loans
savings_percentage_income = 0.10  # Recommend 10% of monthly income for savings
recommended_loan_duration_years = 5  # Default loan duration
savings_target_months = 3  # Target 3 months of savings

# Calculate recommended amounts
recommended_loan_amount = round(monthly_income * loan_suggested_percentage_income * 12 * recommended_loan_duration_years, -1)
recommended_savings_amount = round(monthly_income * savings_target_months, -1)

# Calculate monthly installment for future loan
future_monthly_installment = round(calculate_monthly_installment(
    recommended_loan_amount, INTEREST_RATE, recommended_loan_duration_years
),-1)

# Ensure the installment is within recommended limits
if future_monthly_installment > monthly_income * RECOMMENDED_MAX_MONTHLY_INSTALLMENT_PERCENT:
    # Adjust loan amount to fit within limits
    max_allowed_loan = (monthly_income * RECOMMENDED_MAX_MONTHLY_INSTALLMENT_PERCENT) * \
                       (1 - (1 + INTEREST_RATE / COMPOUNDING_PERIODS) ** (-COMPOUNDING_PERIODS * recommended_loan_duration_years)) / \
                       (INTEREST_RATE / COMPOUNDING_PERIODS)
    recommended_loan_amount = max_allowed_loan
    future_monthly_installment = calculate_monthly_installment(
        recommended_loan_amount, INTEREST_RATE, recommended_loan_duration_years
    )

# Active loan recommendations
if auto_loan_indicator > 0 or housing_loan_indicator > 0:
    st.subheader("Loan Modification Options")
    st.write(f"""❗ **Loan Indicator**: It appears that your business has active loans. 
    Managing these responsibly is crucial for resilience:
    
    - **Restructure Loans**: Consider negotiating extended payment terms or lower interest rates to free up cash flow.
    - **Recommended Loan Amount**: Based on your monthly income of {monthly_income:.2f}, we suggest a maximum loan amount of {recommended_loan_amount:.2f}.
    - **Suggested Loan Duration**: {recommended_loan_duration_years} years.
    - **Avoid Over-borrowing**: Ensure monthly loan payments are no more than {loan_suggested_percentage_income * 100:.1f}% of your monthly income.
    """)

# Future loan recommendations
st.subheader("Future Loans")




# Simulate feature adjustments
adjusted_customer_data = customer_data.copy()
adjusted_customer_data['TOTAL_BALANCE'] += recommended_loan_amount  # Increase liquidity
adjusted_customer_data['CURRENT_MONTH_BILLING'] += future_monthly_installment  # Add loan installment
adjusted_customer_data['LOAN_AMOUNT'] += recommended_loan_amount  # New loan amount
adjusted_customer_data['LOAN_BEHAVIOR'] = 4  # Improved reliability

# Recompute concept scores
adjusted_scores = {}

concepts = {
    "Financial Health": [
        'TRANSACTION_AMOUNT_DEBIT',
        'MONTHLY_INCOME',
        'TOTAL_BALANCE',
        'CURRENT_MONTH_BILLING'
 ],
    "Credit Reliability": [
        'AUTO_LOAN_INDICATOR',
        'HOUSING_LOAN_INDICATOR',
        'SAVINGS_ACCOUNT_INDICATOR',
        'DIGITAL_INDICATOR',
        'REVOLVING_BALANCE',
        'LOAN_BEHAVIOR',
        'LOAN_AMOUNT'
 ],
    "Customer Engagement": [
        'BANK_TENURE', 'CUSTOMER_SEGMENT', 'TRANSACTION_AMOUNT_IBFT', 
        'TRANSACTION_AMOUNT_CC'
    ],
    "Socioeconomic Stability": [
        'SEC', 'GENDER', 'EDUCATION'
    ]
}

for concept, features in concepts.items():
    feature_data = adjusted_customer_data[features]
    z_scores = (feature_data - data[features].mean()) / data[features].std()  # Standardize
    adjusted_scores[f'{concept}_Score'] = z_scores.mean()

# Recalculate resilience score
adjusted_resilience_score = sum(value.mean() if isinstance(value, pd.Series) else float(value) for value in adjusted_scores.values()) / len(concepts)

# Scale the new resilience score
min_resilience = data['Resilience_Score'].min()
max_resilience = data['Resilience_Score'].max()
adjusted_resilience_score_scaled = (adjusted_resilience_score - min_resilience) / (max_resilience - min_resilience)

# Compute resilience boost
original_resilience_score = customer_data['Resilience_Score']
resilience_boost = adjusted_resilience_score_scaled - original_resilience_score

resilience_boost_value = resilience_boost.iloc[0] if isinstance(resilience_boost, pd.Series) else resilience_boost

new_resilience_score = original_resilience_score + resilience_boost_value


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Recommended Loan Amount", value=f"₱{recommended_loan_amount:,.2f}")

with col2:
    st.metric(label="Loan Duration", value=f"{recommended_loan_duration_years} years")

with col3:
    st.metric(label="Estimated Monthly Installment", value=f"₱{future_monthly_installment:,.2f}")

with col4:
    st.metric(label="New Resilience Score", value=round(new_resilience_score, 2), delta=round(resilience_boost_value, 2))

# Output the resilience boost
st.write(f"By responsibly leveraging this loan, your resilience score could improve by approximately **{resilience_boost_value:.2f} points**, reflecting increased financial stability and flexibility.")

# Explanation dropdown for Actionable Recommendations
st.subheader("💡 What do these recommendations mean for your business?")
st.info("""
    By following the above recommendations:
    
    1. **Enhanced Liquidity**: The recommended loan can provide immediate financial resources to invest in critical business areas, such as inventory, equipment, or expansion.
    
    2. **Improved Resilience Score**: A higher resilience score reflects stronger financial health, credit reliability, and stability, making your business more robust against economic shocks and more appealing to investors.
    
    3. **Long-term Planning**: The suggested loan duration and monthly installment align with your income, ensuring manageable payments without jeopardizing cash flow.
        
    **Note**: Always consider your business's capacity to manage loan repayments effectively. While loans can boost growth, over-borrowing may strain financial resources. Use the recommendations as a guide to make informed decisions.
    """)

st.markdown("### Ready to Apply?")
st.write("Take the next step to strengthen your financial health. [Apply for a BPI loan](https://www.bpi.com.ph/personal/loans/personal-loan) today!")