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

st.title("⚙️ ERICA ")

#st.write("💡 **Economic Resilience Index for Capacity Adaptation or ERICA** is designed to assess and enhance the financial resilience of MSMEs, particularly in underserved regions and vulnerable sectors. The goal is to help these MSMEs withstand economic shocks such as crises or natural disasters by providing financial institutions with a comprehensive understanding of the extent of each MSME’s resilience.")

# Load the data
@st.cache_data
def load_data():
    # Replace this with your data loading code
    data = pd.read_csv('Resilience Score Analysis DF.csv')
    return data

data = load_data()

def load_group():
    # Replace this with your data loading code
    group = pd.read_csv('Res Score with Cus Group.csv')
    return group

group = load_group()

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
#st.subheader("📈 Economic Resilience Score Calculation")

st.subheader("📈 Economic Resilience Score")
#st.info("💡 The Economic Resilience Score is a composite indicator that assesses the financial resilience of an MSME.")

# Explanation dropdown for Resilience Score
# with st.expander("How does the Economic Resilience Score work?"):
#     st.write("""
    
#     It is calculated by analyzing several key metrics:
    
#     - **Financial Health**: Evaluates the liquidity and stability of the MSME’s finances.
#     - **Credit Reliability**: Considers the consistency and reliability in loan repayments.
#     - **Customer Engagement**: Measures interaction levels with banking products.
#     - **Socioeconomic Stability**: Takes into account the broader economic environment the MSME operates in.
    
#     These components are combined using a mean aggregation to produce a Resilience Score, which indicates the MSME’s ability to withstand economic shocks. 
    
#     **Thresholds for Resilience Score**:
#     - A score below **-0.5** is considered low, indicating that the MSME may be vulnerable to financial shocks and lacks the financial stability to weather economic downturns.
#     - Scores between **-0.5 and 0.5** are moderate, suggesting that the MSME has some resilience but may need improvements in certain areas.
#     - A score above **0.5** is considered high, indicating strong financial resilience and stability.
#     """)

st.sidebar.subheader("Customer Information")
selected_customer = st.sidebar.selectbox("Select Customer ID", data['CUSTOMER_ID'].unique())
#selected_customer = st.sidebar.text_input("Enter Customer ID")

st.sidebar.info("""Please note that this dashboard is a prototype. 
                Users are advised that the tool may contain errors, 
                bugs, or limitations and should be used with caution 
                and awareness of potential risks, and the developers 
                make no warranties or guarantees regarding its performance, 
                reliability, or suitability for any specific purpose.""")

with st.sidebar:
        st.caption('Developed by MisSME?')
        col1, col2, col3, col4 = st.columns([0.05,0.05,0.05,0.15])
        with col1:
            st.markdown("""<a href="https://github.com/yumoldianne/ERICA">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/1200px-Octicons-mark-github.svg.png?20180806170715" 
                width="30" height="30"></a>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<a href="https://docs.google.com/document/d/1eu39rT-Zh6KhUNwXrAzOwdOJv0_lz3IDv4X_GEmaDsA/edit?usp=sharing">
                <img src="https://cdn-icons-png.flaticon.com/512/482/482202.png" 
                width="30" height="30"></a>""", unsafe_allow_html=True)
        #with col3:
            #st.markdown("""<a href="https://www.instagram.com/eltgnd_v/">
                #<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" 
                #width="30" height="30"></a>""", unsafe_allow_html=True)

#st.subheader("⚡ Financial Risk Assessment Summary")
customer_data = data[data['CUSTOMER_ID'] == selected_customer].iloc[0]
resilience_score = customer_data['Resilience_Score']
risk_level = classify_risk(resilience_score)

col1, col2 = st.columns(2)
col1.metric("Score", f"{resilience_score:.2f}")
col2.metric("Risk Level", risk_level)

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
            st.write("❗ **Financial Health**: Low financial health score may indicate insufficient cash flow or limited income stability.")
        elif factor == 'Credit Reliability_Score':
            st.write("❗ **Credit Reliability**: Low credit reliability score suggests inconsistent loan or credit repayment behavior.")
        elif factor == 'Customer Engagement_Score':
            st.write("❗ **Customer Engagement**: Low engagement with banking or financial products might imply underuse of resources.")
        elif factor == 'Socioeconomic Stability_Score':
            st.write("❗ **Socioeconomic Stability**: A low socioeconomic stability score can suggest external risks.")

    else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ **{factor.replace('_', ' ').title()}**: Your score looks good! You're on the right track in this area.")





st.divider()






# Peer Benchmarking
st.subheader("🌍 Peer Benchmarking")

st.info("💡 Peer Benchmarking compares your Resilience Score with similar customers to assess your financial resilience.")
        
tab1, tab2, tab3 = st.tabs(["Overall Performance", "Retailers", "Business Banking"])

with tab1:
    st.write(f"**Benchmarking Against All Peers**")
     # Adding explanation for Peer Benchmarking
    with st.expander("How do you interpret your perfomance in the boxplot?"):
        st.write("""
                 **How to interpret the boxplot:**  
                 - The box represents the middle 50% of peer scores (between the 25th and 75th percentile).
                 - The dashed line indicates your current Resilience Score. A score above the box shows strong resilience relative to peers.
                 - A score within or below the box might suggest improvement areas.
                 """)
     
     #Filter by location and segment to compare with peers
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

# Explanation of Radar Chart Benchmarking
    with st.expander("How do you interpret your performance in the radar chart?"):
        st.write("""
        The radar chart visualizes your performance on different financial metrics relative to the peer average.
    
        **How to interpret the radar chart:**
        - The green area represents your scores across various metrics.
        - The grey area shows the peer average. Areas where your green shape is outside the grey indicate strengths compared to peers.
        - If your scores are consistently within the peer average, consider targeting those areas for improvement.
        """)

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

with tab2:
    # Define the metrics to benchmark and get customer scores
    scores = ['Financial Health_Score', 'Credit Reliability_Score', 'Customer Engagement_Score', 
          'Socioeconomic Stability_Score']
    customer_scores = customer_data[scores].values
    resilience_score = customer_data['Resilience_Score']

    # Loop through both 'Retail' and 'Business Banking' groups for peer benchmarking
    for segment in ['RETAIL']:
        
        # Filter peers in the current group
        peer_data = data[(group['CUSTOMER_GROUP'] == segment) &
                         (group['CUSTOMER_LOCATION'] == customer_data['CUSTOMER_LOCATION']) &
                         (group['CUSTOMER_SEGMENT'] == customer_data['CUSTOMER_SEGMENT'])]
        
        # Display the group being benchmarked
        st.write(f"**Benchmarking Against the Retail Group**")
        
        # Box Plot for Resilience Score Comparison
        with st.expander(f"How to interpret your performance in the boxplot for the retail group?"):
            st.write("""
                     **How to interpret the boxplot:**  
                     - The box represents the middle 50% of peer scores (between the 25th and 75th percentile).
                     - The dashed line indicates your current Resilience Score. A score above the box shows strong resilience relative to peers.
                     - A score within or below the box might suggest improvement areas.
                     """)
            
        # Plotting Resilience Score comparison for each customer group
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(x=peer_data['Resilience_Score'], color='lightgrey', ax=ax)
        ax.axvline(resilience_score, color='darkgreen', linestyle='--', label='Customer Score')
        ax.set_title(f"Resilience Score Comparison with Retail Group", fontsize=14, fontweight='bold', color="darkgreen")
        ax.set_xlabel("Resilience Score", fontsize=12, fontweight='bold', color="darkgreen")
        ax.legend(loc='upper right')
        st.pyplot(fig)
            
            # Explanation of the radar chart for each group
        with st.expander("How do you interpret your performance in the radar chart for the retail group?"):
            st.write("""
                     The radar chart visualizes your performance on different financial metrics relative to the peer average.
                     
                     **How to interpret the radar chart:**
                     - The green area represents your scores across various metrics.
                     - The grey area shows the peer average. Areas where your green shape is outside the grey indicate strengths compared to peers.
                     - If your scores are consistently within the peer average, consider targeting those areas for improvement.
                     """)
                
        # Radar Chart for Comparative Analysis with Peers in the Current Group
        def plot_radar_chart(scores, peer_means, labels, segment):
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
            ax.set_title(f"Comparative Radar Chart of Component Scores for Retail Group", fontsize=14, fontweight='bold', color="darkgreen")
            ax.legend(loc='upper right')
            st.pyplot(fig)

    # Calculate peer means for the current group
    peer_means = peer_data[scores].mean().values
    
    # Plot radar chart for current group
    plot_radar_chart(customer_scores, peer_means, scores, group)

with tab3:
    # Define the metrics to benchmark and get customer scores
    scores = ['Financial Health_Score', 'Credit Reliability_Score', 'Customer Engagement_Score', 
          'Socioeconomic Stability_Score']
    customer_scores = customer_data[scores].values
    resilience_score = customer_data['Resilience_Score']

    # Loop through both 'Retail' and 'Business Banking' groups for peer benchmarking
    for segment in ['BUSINESS BANKING']:
        
        # Filter peers in the current group
        peer_data = data[(group['CUSTOMER_GROUP'] == segment) &
                         (group['CUSTOMER_LOCATION'] == customer_data['CUSTOMER_LOCATION']) &
                         (group['CUSTOMER_SEGMENT'] == customer_data['CUSTOMER_SEGMENT'])]
        
        # Display the group being benchmarked
        st.write(f"**Benchmarking Against the Business Banking Group**")
        
        # Box Plot for Resilience Score Comparison
        with st.expander(f"How to do you interpret your performance in the boxplot for the business banking group?"):
            st.write("""
                     **How to interpret the boxplot:**  
                     - The box represents the middle 50% of peer scores (between the 25th and 75th percentile).
                     - The dashed line indicates your current Resilience Score. A score above the box shows strong resilience relative to peers.
                     - A score within or below the box might suggest improvement areas.
                     """)
            
        # Plotting Resilience Score comparison for each customer group
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(x=peer_data['Resilience_Score'], color='lightgrey', ax=ax)
        ax.axvline(resilience_score, color='darkgreen', linestyle='--', label='Customer Score')
        ax.set_title(f"Resilience Score Comparison with Business Banking Group", fontsize=14, fontweight='bold', color="darkgreen")
        ax.set_xlabel("Resilience Score", fontsize=12, fontweight='bold', color="darkgreen")
        ax.legend(loc='upper right')
        st.pyplot(fig)
            
            # Explanation of the radar chart for each group
        with st.expander("How to interpret your peformance in the radar chart for the business banking group?"):
            st.write("""
                     The radar chart visualizes your performance on different financial metrics relative to the peer average.
                     
                     **How to interpret the radar chart:**
                     - The green area represents your scores across various metrics.
                     - The grey area shows the peer average. Areas where your green shape is outside the grey indicate strengths compared to peers.
                     - If your scores are consistently within the peer average, consider targeting those areas for improvement.
                     """)
                
        # Radar Chart for Comparative Analysis with Peers in the Current Group
        def plot_radar_chart(scores, peer_means, labels, segment):
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
            ax.set_title(f"Comparative Radar Chart of Component Scores for Business Banking Group", fontsize=14, fontweight='bold', color="darkgreen")
            ax.legend(loc='upper right')
            st.pyplot(fig)

    # Calculate peer means for the current group
    peer_means = peer_data[scores].mean().values
    
    # Plot radar chart for current group
    plot_radar_chart(customer_scores, peer_means, scores, group)




st.divider()






# Step 4: Resilience Score Calculation
st.subheader("🧮 Target Resilience Score Calculator")

st.info("💡 The Target Resilience Score Calculator computes how much each component score should ideally increase to reach the target resilience score. This lets MSMEs focus on the specific areas that can most effectively strengthen their resilience.")

with st.expander("How does the Target Resilience Score Calculator work?"):
    st.write("""
             
             Your current resilience score is calculated based on four key components: Financial Health, Credit Reliability, Customer Engagement, Socioeconomic Stability. Together, these components create a single resilience score, giving a snapshot of financial resilience.
             
             You can set a target resilience score—a goal to help your business become more financially stable. The calculator will then tell you if you’ve already achieved it or if improvements are needed.

             If your current score meets or exceeds your target, the calculator will confirm that you’re on the right track. If not, it calculates the gap and suggests ways to bridge it.

             """)

# Inputs: Current and Target Resilience Score
st.write(f"Your calculated current resilience score is: {resilience_score:.2f}")

st.write("Your score for each of the components can be found below:")

financial_health_score = customer_data['Financial Health_Score']
credit_reliability_score = customer_data['Credit Reliability_Score']
customer_engagement_score = customer_data['Customer Engagement_Score']
socioeconomic_stability_score = customer_data['Socioeconomic Stability_Score']

col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.8, 2.0])
col1.metric("Financial Health", f"{financial_health_score:.2f}")
col2.metric("Credit Reliability", f"{credit_reliability_score:.2f}")
col3.metric("Customer Engagement", f"{customer_engagement_score:.2f}")
col4.metric("Socioeconomic Stability", f"{socioeconomic_stability_score:.2f}")

target_resilience_score = st.number_input("Enter your target resilience score", min_value=-1.0, max_value=1.0, step=0.01)

# Calculate the difference and feasibility
score_difference = target_resilience_score - resilience_score

# Check if the target score is achievable based on the score difference
if score_difference <= 0:
    st.write("Your scores look good! You've already reached or exceeded your target resilience score.")
else:
    st.write(f"To reach your target resilience score of {target_resilience_score}, you need to increase your overall resilience score by {score_difference:.2f}.")

    # Suggest improvements for each component
    st.markdown("### Suggested Improvements to Reach Target Resilience Score")

    # Required increment per component (assuming equal distribution of increase across components)
    required_increase_per_component = score_difference / 4

    # Display each component's current score with tailored recommendations
    for factor, current_score in zip(
        ["Financial Health", "Credit Reliability", "Customer Engagement", "Socioeconomic Stability"],
        [financial_health_score, credit_reliability_score, customer_engagement_score, socioeconomic_stability_score]
    ):
        target_score_for_factor = current_score + required_increase_per_component
        st.write(f"**{factor} Score**: Suggested Target = {target_score_for_factor:.2f}")

#        if factor == "Financial Health":
#            if current_score < target_score_for_factor:
#                st.write("🪙 Consider enhancing your financial health.")
#        elif factor == "Credit Reliability":
#            if current_score < target_score_for_factor:
#                st.write("💳 Focus on improving credit reliability.")
#        elif factor == "Customer Engagement":
#            if current_score < target_score_for_factor:
#                st.write("🫂 Increase interactions with banking products, like digital tools and resources, to boost engagement.")
#        elif factor == "Socioeconomic Stability":
#            if current_score < target_score_for_factor:
#                st.write("🏦 Building a savings plan can improve resilience against economic challenges.")





st.divider()





#5 Recommendations
unscaled_data = pd.read_csv('Resilience Score Analysis Unscaled.csv')

rcustomer_data = unscaled_data[unscaled_data['CUSTOMER_ID'] == selected_customer]

# Customer data variables
monthly_income = rcustomer_data['MONTHLY_INCOME'].values[0] if 'MONTHLY_INCOME' in rcustomer_data else 0
financial_health_score = rcustomer_data['Financial Health_Score'].values[0]
credit_reliability_score = rcustomer_data['Credit Reliability_Score'].values[0]
loan_amount = rcustomer_data['LOAN_AMOUNT'].values[0] if 'LOAN_AMOUNT' in rcustomer_data else 0
bank_tenure = rcustomer_data['BANK_TENURE'].values[0] if 'BANK_TENURE' in rcustomer_data else 0

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

auto_loan_indicator = rcustomer_data['AUTO_LOAN_INDICATOR'].values[0] if 'AUTO_LOAN_INDICATOR' in rcustomer_data else 0
housing_loan_indicator = rcustomer_data['HOUSING_LOAN_INDICATOR'].values[0] if 'HOUSING_LOAN_INDICATOR' in rcustomer_data else 0

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
monthly_income = rcustomer_data['MONTHLY_INCOME'].values[0] if 'MONTHLY_INCOME' in customer_data else 0
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
adjusted_customer_data = rcustomer_data.copy()
adjusted_customer_data['TOTAL_BALANCE'] += recommended_loan_amount  # Increase liquidity
adjusted_customer_data['CURRENT_MONTH_BILLING'] += future_monthly_installment  # Add loan installment
adjusted_customer_data['LOAN_AMOUNT'] += recommended_loan_amount  # New loan amount
adjusted_customer_data['LOAN_BEHAVIOR'] = 4 

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
    z_scores = (feature_data - unscaled_data[features].mean()) / unscaled_data[features].std()  # Standardize
    adjusted_scores[f'{concept}_Score'] = z_scores.mean()

# Recalculate resilience score
adjusted_resilience_score = sum(value.mean() if isinstance(value, pd.Series) else float(value) for value in adjusted_scores.values()) / len(concepts)
# Scale the new resilience score
min_resilience = unscaled_data['Resilience_Score'].min()
max_resilience = unscaled_data['Resilience_Score'].max()
adjusted_resilience_score_scaled = (adjusted_resilience_score - min_resilience) / (max_resilience - min_resilience)
# Compute resilience boost
original_resilience_score = rcustomer_data['Resilience_Score']
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