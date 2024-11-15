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

st.info("💡 **Economic Resilience Index for Capacity Adaptation or ERICA** is designed to assess and enhance the financial resilience of MSMEs, particularly in underserved regions and vulnerable sectors. The goal is to help these MSMEs withstand economic shocks such as crises or natural disasters by providing financial institutions with a comprehensive understanding of the extent of each MSME’s resilience.")

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
st.subheader("📈 Economic Resilience Score Calculation")

st.info("💡 The Economic Resilience Score is a composite indicator that assesses the financial resilience of an MSME.")

# Explanation dropdown for Resilience Score
with st.expander("How does the Economic Resilience Score work?"):
    st.write("""
    
    It is calculated by analyzing several key metrics:
    
    - **Financial Health**: Evaluates the liquidity and stability of the MSME’s finances.
    - **Credit Reliability**: Considers the consistency and reliability in loan repayments.
    - **Customer Engagement**: Measures interaction levels with banking products.
    - **Socioeconomic Stability**: Takes into account the broader economic environment the MSME operates in.
    
    These components are combined using a mean aggregation to produce a Resilience Score, which indicates the MSME’s ability to withstand economic shocks. 
    
    **Thresholds for Resilience Score**:
    - A score below **-0.5** is considered low, indicating that the MSME may be vulnerable to financial shocks and lacks the financial stability to weather economic downturns.
    - Scores between **-0.5 and 0.5** are moderate, suggesting that the MSME has some resilience but may need improvements in certain areas.
    - A score above **0.5** is considered high, indicating strong financial resilience and stability.
    """)

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

st.subheader("⚡ Financial Risk Assessment Summary")
customer_data = data[data['CUSTOMER_ID'] == selected_customer].iloc[0]
resilience_score = customer_data['Resilience_Score']
risk_level = classify_risk(resilience_score)

col1, col2 = st.columns(2)
col1.metric("Resilience Score", f"{resilience_score:.2f}")
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
            st.write("❗ **Financial Health**: Low financial health score may indicate insufficient cash flow or limited income stability. Consider strategies like cash flow monitoring and budgeting.")
        elif factor == 'Credit Reliability_Score':
            st.write("❗ **Credit Reliability**: Low credit reliability score suggests inconsistent loan or credit repayment behavior. Improving repayment practices can strengthen this score.")
        elif factor == 'Customer Engagement_Score':
            st.write("❗ **Customer Engagement**: Low engagement with banking or financial products might imply underuse of resources. Increase usage of available services for better resilience.")
        elif factor == 'Socioeconomic Stability_Score':
            st.write("❗ **Socioeconomic Stability**: A low socioeconomic stability score can suggest external risks. Strengthening financial stability with a savings plan can mitigate some risks.")

    else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ **{factor.replace('_', ' ').title()}**: Your score looks good! You're on the right track in this area.")

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

# 5. Actionable Recommendations & Risk Mitigation Suggestions
st.subheader("📑 Actionable Recommendations")

st.info("💡 Actionable recommendations are provided based on the MSME's indicators, helping to improve financial resilience.")

# Explanation dropdown for Actionable Recommendations
with st.expander("What are actionable recommendations?"):
    st.write("""
    
    Here’s how these recommendations are tailored:
    
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
    st.write("""❗ **Loan Indicator**: It appears that your business has active loans. Managing these responsibly is crucial for maintaining resilience:
    
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
    st.write("""❗**Savings Account Indicator**: It seems that you do not currently have an active savings account. Building a financial buffer can significantly enhance resilience:
    
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
    st.write("""
    
    ❗**Customer Engagament Score**: Your engagement with financial services appears to be low. Increasing engagement can offer greater stability and access to resources:
    
    - **Explore Digital Banking Options**: Digital products can streamline access to essential banking services, making it easier to manage finances on the go.
    - **Utilize Financial Management Tools**: Many banks offer budgeting tools and analytics to help track cash flow, income, and expenses more effectively.
    - **Consider Additional Products**: Speak with a financial advisor to explore products like business credit lines or insurance options that provide added security and flexibility.
    
    Increasing engagement with financial services can boost resilience by providing your business with access to supportive tools and resources.
    
    """)

else:
        # If the score is above the threshold, provide a congratulatory message
        st.write(f"✅ *Customer Engagament Score**: Your engagement with financial services appears to be high! You're on the right track in this area.")


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
st.subheader("🌍 Peer Benchmarking")

st.info("💡 Peer Benchmarking compares your Resilience Score with similar customers to assess your financial resilience. A higher score than peers suggests stronger resilience. Scores below a certain percentile (e.g., below 25th percentile) may indicate lower resilience and areas for improvement.")

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