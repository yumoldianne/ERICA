import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="ERICA",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("ERICA ⚙️")

st.write("Economic Resilience Index for Capacity Adaptation or ERICA is designed to assess and enhance the financial resilience of MSMEs, particularly in underserved regions and vulnerable sectors like agriculture. The goal is to help these MSMEs withstand economic shocks such as crises or natural disasters by providing financial institutions with a comprehensive understanding of the extent of each MSME’s resilience.")

# Load the data
@st.cache_data
def load_data():
    # Replace this with your data loading code
    data = pd.read_csv('Resilience Score Analysis DF.csv')
    return data

data = load_data()

# Helper functions
def classify_risk(resilience_score):
    if resilience_score < -0.5:
        return 'High Risk'
    elif resilience_score < 0.5:
        return 'Moderate Risk'
    else:
        return 'Low Risk'

# 1. Risk Assessment Summary
#st.title("MSME Financial Resilience Dashboard")

# Step 1: Resilience Score Calculation
st.header("Economic Resilience Score Calculation")

# Explanation dropdown for Resilience Score
with st.expander("How does the Economic Resilience Score work?"):
    st.write("""
    The Economic Resilience Score is a composite indicator that assesses the financial resilience of an MSME. 
    It is calculated by analyzing several key metrics:
    - **Financial Health**: Evaluates the liquidity and stability of the MSME’s finances.
    - **Credit Reliability**: Considers the consistency and reliability in loan repayments.
    - **Customer Engagement**: Measures interaction levels with banking products.
    - **Socioeconomic Stability**: Takes into account the broader economic environment the MSME operates in.
    
    These components are combined using a weighted formula to produce a Resilience Score, which indicates the MSME’s ability to withstand economic shocks.
    **Thresholds for Resilience Score**:
    - A score below **-0.5** is considered low, indicating that the MSME may be vulnerable to financial shocks and lacks the financial stability to weather economic downturns.
    - Scores between **-0.5 and 0.5** are moderate, suggesting that the MSME has some resilience but may need improvements in certain areas.
    - A score above **0.5** is considered high, indicating strong financial resilience and stability.

    These components are combined using a weighted formula to produce the final Resilience Score, which highlights the MSME’s ability to withstand economic pressures.
    """)

st.sidebar.header("Risk Assessment Filter")
selected_customer = st.sidebar.selectbox("Select Customer ID", data['CUSTOMER_ID'].unique())

st.sidebar.info("""Please note that this dashboard is a prototype. 
                Users are advised that the tool may contain errors, 
                bugs, or limitations and should be used with caution 
                and awareness of potential risks, and the developers 
                make no warranties or guarantees regarding its performance, 
                reliability, or suitability for any specific purpose.""")

st.header("1. Risk Assessment Summary")
customer_data = data[data['CUSTOMER_ID'] == selected_customer].iloc[0]
resilience_score = customer_data['Resilience_Score']
risk_level = classify_risk(resilience_score)

st.write(f"Risk Level: {risk_level}")
st.write(f"Resilience Score: {resilience_score:.2f}")

# Visualize contributions of each component score to the Resilience Score
scores = ['Financial Health_Score', 'Credit Reliability_Score', 'Customer Engagement_Score', 'Socioeconomic Stability_Score']
score_values = [customer_data[score] for score in scores]

# Set up the figure
fig, ax = plt.subplots(figsize=(8, 5))

# Define a green-based palette and apply to bar plot
palette = sns.color_palette("Greens", len(scores))
sns.barplot(x=score_values, y=scores, ax=ax, palette=palette, orient='h')

# Enhance plot appearance
ax.set_xlabel("Score Contribution", fontsize=12, fontweight='bold', color="darkgreen")
ax.set_ylabel("")  # Removing y-label as the bar labels serve that role
ax.set_title("Resilience Score Breakdown", fontsize=14, fontweight='bold', color="darkgreen")

# Adjust grid and style
sns.despine(left=True, bottom=True)  # Clean up borders
ax.grid(axis='x', linestyle='--', alpha=0.6)  # Grid for x-axis only

# Display the plot in Streamlit
st.pyplot(fig)

# Define thresholds for each resilience-driving factor
factor_thresholds = {
    'Financial Health_Score': 0.3,  # Below 0.3 considered low for financial health
    'Credit Reliability_Score': 0.4,  # Below 0.4 considered low for credit reliability
    'Customer Engagement_Score': 0.5,  # Below 0.5 considered low engagement
    'Socioeconomic Stability_Score': 0.6  # Below 0.6 suggests low socioeconomic stability
}

# Analyze each factor's contribution to the resilience score
for factor, threshold in factor_thresholds.items():
    score = customer_data[factor]
    if score < threshold:
        if factor == 'Financial Health_Score':
            st.write("- **Financial Health**: Low financial health score may indicate insufficient cash flow or limited income stability. Consider strategies like cash flow monitoring and budgeting.")
        elif factor == 'Credit Reliability_Score':
            st.write("- **Credit Reliability**: Low credit reliability score suggests inconsistent loan or credit repayment behavior. Improving repayment practices can strengthen this score.")
        elif factor == 'Customer Engagement_Score':
            st.write("- **Customer Engagement**: Low engagement with banking or financial products might imply underuse of resources. Increase usage of available services for better resilience.")
        elif factor == 'Socioeconomic Stability_Score':
            st.write("- **Socioeconomic Stability**: A low socioeconomic stability score can suggest external risks. Strengthening financial stability with a savings plan can mitigate some risks.")

    else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ **{factor.replace('_', ' ').title()}**: Your score looks good! You're on the right track in this area.")

# 5. Actionable Recommendations & Risk Mitigation Suggestions
st.header("2. Actionable Recommendations")

# Explanation dropdown for Actionable Recommendations
with st.expander("How Actionable Recommendations Work"):
    st.write("""
    Actionable recommendations are provided based on the MSME's indicators, helping to improve financial resilience. Here’s how these recommendations are tailored:
    
    - **Loan Indicators**: If an MSME has active loans, such as auto or housing loans, they are assessed for restructuring options. 
      - MSMEs with multiple active loans or recent missed payments are recommended to explore extended payment terms or restructuring. 
    - **Savings**: MSMEs with no active savings accounts are advised to build a savings buffer to manage unexpected expenses. 
      - If an MSME has less than **3 months of operating expenses saved**, they are encouraged to increase their savings for better resilience.
    - **Engagement**: MSMEs with low customer engagement scores are advised to explore new banking products.
      - Engagement scores below **0.5** are considered low, indicating limited use of available financial products, which could limit support during challenging times.
    """)

# Displaying loan-based recommendation based on loan indicators
auto_loan_indicator = customer_data.get('AUTO_LOAN_INDICATOR', None)
housing_loan_indicator = customer_data.get('HOUSING_LOAN_INDICATOR', None)

if auto_loan_indicator == 1 or housing_loan_indicator == 1:
    st.subheader("Loan Modification Options")
    st.write("""It appears that your business has active loans. Managing these responsibly is crucial for maintaining resilience:
    
    - **Restructure Loans**: Consider negotiating extended payment terms or lower interest rates with lenders. Doing so can free up cash flow to invest in business operations.
    - **Avoid Over-borrowing**: If loan repayments are high (over 20 percent of monthly revenue), we suggest reducing reliance on credit to minimize the risk of default.
    - **Set up an Emergency Fund**: In parallel, establish a fund to cover loan repayments in case of income fluctuations.
    
    Managing debt efficiently can help prevent liquidity issues and enable smoother cash flow management.
    """)
else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ **Loan Indicator**: You don't have any active loans! You're on the right track in this area.")

# Additional components for savings recommendations
if customer_data.get('SAVINGS_ACCOUNT_INDICATOR', 0) == 0:
    st.subheader("Savings Recommendations")
    st.write("""It seems that you do not currently have an active savings account. Building a financial buffer can significantly enhance resilience:
    
    - **Establish a Savings Fund**: Aim to save enough for at least **3 months of operating expenses**. This fund can protect against unexpected costs or economic slowdowns.
    - **Automate Savings Contributions**: Set aside a percentage of monthly revenue to grow your savings incrementally.
    - **Use a High-Interest Savings Account**: Consider a high-interest account for better returns, which can grow your buffer more effectively.
    
    Having a dedicated savings account reduces financial vulnerability, enabling your business to handle unforeseen costs with greater confidence.
    """)
else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ **Savings Account Indicator**: It seems like you have an active savings account. You're on the right track in this area.")

# Step 3: Customer Engagement Recommendation
st.subheader("Customer Engagement Recommendation")

# Explanation dropdown for Engagement Recommendation
with st.expander("Understanding Customer Engagement Score"):
    st.write("""
    The Customer Engagement Score reflects the MSME’s interaction with financial products. A low engagement score may indicate unfamiliarity with financial products or limited access to beneficial products.
    
    **Thresholds for Engagement Score**:
    - A score below **0.5** is considered low, indicating that the MSME has limited interaction with available financial products.
    - Scores between **0.5 and 0.8** are moderate, suggesting some familiarity but room for greater engagement.
    - A score above **0.8** is high, indicating proactive use and familiarity with a wide range of financial products.
    """)

# Example of using Customer Engagement Score for recommendation
if customer_data.get('CUSTOMER_ENGAGEMENT_SCORE', 0) < 0.5:
    st.subheader("Engagement Enhancement")
    st.write("""Your engagement with financial services appears to be low. Increasing engagement can offer greater stability and access to resources:""")

else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ *Customer Engagament Score**: Your engagement with financial services appears to be high! You're on the right track in this area.")

# Add the following later
#    - **Explore Digital Banking Options**: Digital products can streamline access to essential banking services, making it easier to manage finances on the go.
#    - **Utilize Financial Management Tools**: Many banks offer budgeting tools and analytics to help track cash flow, income, and expenses more effectively.
#    - **Consider Additional Products**: Speak with a financial advisor to explore products like business credit lines or insurance options that provide added security and flexibility.
    
#    Increasing engagement with financial services can boost resilience by providing your business with access to supportive tools and resources.

# Final Summary of Recommendations
st.subheader("Summary of Recommendations")

st.write("Summary of tailored recommendations based on the MSME's profile:")
# Example summary recommendation
if customer_data.get('SAVINGS_ACCOUNT_INDICATOR', 0) == 0:
    st.write("- Build a savings account as a buffer.")
if auto_loan_indicator == 1 or housing_loan_indicator == 1:
    st.write("- Restructure loans for more flexible repayment.")
if customer_data.get('CUSTOMER_ENGAGEMENT_SCORE', 0) < 0.5:
    st.write("- Enhance engagement with digital products.")

# 6. Peer Benchmarking
st.header("3. Peer Benchmarking")

# Adding explanation for Peer Benchmarking
with st.expander("What is Peer Benchmarking?"):
    st.write("""
    Peer Benchmarking compares your Resilience Score with similar customers to assess your financial resilience. 
    A higher score than peers suggests stronger resilience. Scores below a certain percentile (e.g., below 25th percentile) 
    may indicate lower resilience and areas for improvement.
    """)

    st.write("""
    **How to interpret the boxplot:**  
    - The box represents the middle 50% of peer scores (between the 25th and 75th percentile).
    - The dashed line indicates your current Resilience Score. A score above the box shows strong resilience relative to peers.
    - A score within or below the box might suggest improvement areas.
    """)

# Filter by location and segment to compare with peers
peer_data = data[(data['CUSTOMER_LOCATION'] == customer_data['CUSTOMER_LOCATION']) &
                 (data['CUSTOMER_SEGMENT'] == customer_data['CUSTOMER_SEGMENT'])]

# Plotting Resilience Score comparison
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(x=peer_data['Resilience_Score'], color='lightgrey', ax=ax)
ax.axvline(resilience_score, color='darkgreen', linestyle='--', label='Customer Score')
ax.set_title("Resilience Score Comparison with Peers", fontsize=14, fontweight='bold', color="darkgreen")
ax.set_xlabel("Resilience Score", fontsize=12, fontweight='bold', color="darkgreen")
ax.legend(loc='upper right')
st.pyplot(fig)

def plot_radar_chart(scores, peer_means, labels):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

    # Complete the loop for radar chart
    scores = np.concatenate((scores, [scores[0]]))
    peer_means = np.concatenate((peer_means, [peer_means[0]]))
    angles += angles[:1]

    # Plotting the radar chart for customer and peers
    sns.set_palette("Greens")
    ax.plot(angles, scores, 'o-', color='darkgreen', label='Customer')
    ax.fill(angles, scores, color='green', alpha=0.25)

    ax.plot(angles, peer_means, 'o-', color='grey', label='Peer Average')
    ax.fill(angles, peer_means, color='grey', alpha=0.25)

    # Styling the radar chart
    ax.set_yticklabels([])  # Hides radial labels for a cleaner look
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold', color="darkgreen")
    ax.set_title("Comparative Radar Chart of Component Scores", fontsize=14, fontweight='bold', color="darkgreen")
    ax.legend(loc='upper right')
    st.pyplot(fig)

peer_means = peer_data[scores].mean().values
plot_radar_chart(score_values, peer_means, scores)

# Explanation of Radar Chart Benchmarking
with st.expander("Understanding the Radar Chart"):
    st.write("""
    The radar chart visualizes your performance on different financial metrics relative to the peer average.
    
    **How to interpret the radar chart:**
    - The green area represents your scores across various metrics.
    - The grey area shows the peer average. Areas where your green shape is outside the grey indicate strengths compared to peers.
    - If your scores are consistently within the peer average, consider targeting those areas for improvement.
    """)