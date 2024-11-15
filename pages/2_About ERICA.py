import streamlit as st

st.set_page_config(
    page_title="About ERICA",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 What is ERICA? ")

st.info("💡 **Economic Resilience Index for Capacity Adaptation or ERICA** is designed to assess and enhance the financial resilience of MSMEs, particularly in underserved regions and vulnerable sectors like agriculture. The goal is to help these MSMEs withstand economic shocks such as crises or natural disasters by providing financial institutions with a comprehensive understanding of the extent of each MSME’s resilience.")

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

#Resilience Score Explanation
st.subheader("Resilience Score")

st.write("""
        The CSR for MSMEs was developed by analyzing various financial and socioeconomic indicators. Transactional and behavioral data were first consolidated into quarterly sums to smooth out short-term fluctuations. Categorical variables were then converted to numeric values through appropriate mapping techniques. After preprocessing the features, correlation-based feature selection was performed to enhance model efficiency, removing variables with correlation coefficients exceeding 0.8 to eliminate redundancy while preserving the most informative indicators.
         
         The framework categorized indicators into four fundamental concepts: `Financial Health`, `Credit Reliability`, `Customer Engagement`, and `Socioeconomic Stability`. Within each concept, the mean of the features was taken and then standardized using z-score transformation to ensure comparability across different measures. These standardized features were then combined through mean aggregation to create composite scores that captured the overall strength of each conceptual dimension.
         
         The final resilience score was computed by taking the average of the four concept-specific composite scores, ensuring equal weight distribution across all dimensions. To enhance interpretability, the resulting score was scaled to a range of 0 to 1 using min-max scaling. This standardized approach produced a robust metric that effectively captures multiple aspects of MSME resilience while maintaining simplicity and clarity in its interpretation.

         """)

#Dashboard Components Explanation
st.subheader("ERICA Dashboard")

st.write("""
        ERICA combines the Economic Resilience Score Calculation, Risk Assessment Summary, Target Resilience Score Calculator, Peer Benchmarking, and Resilience Score Predictor to provide insights into a customer’s financial health and areas for improvement.
         
         The `Economic Resilience Score` aggregates the concepts to create a composite score representing a customer’s ability to handle financial disruptions. This score is used in peer comparisons to contextualize the customer’s performance.
         
         The `Risk Assessment Summary` identifies potential financial risks by highlighting areas where the customer’s scores fall below benchmarks. It provides a quick, color-coded overview of high-risk areas, helping users prioritize improvement actions.
         
         The `Target Resilience Score Calculator` allows users to simulate the impact of changes in the concepts, helping set realistic performance targets. Users can test various scenarios to visualize how adjustments could improve the customer’s resilience score.
         
         `Peer Benchmarking` compares the customer’s resilience score and financial metrics against peers in similar Retail and Business Banking groups. This includes two visualizations, a box plot (displays the customer’s Resilience Score against peer scores), and radar chart (compares the customer’s performance across the concepts to the peer average, highlighting areas of strength and opportunities for improvement).
         
         `Resilience Score Predictor` predicts resilience scores for customers using three different machine learning models.
         
         """)

st.title("🐟 About MisSME?")

st.write("""
         MiSSME? (pronounced as miss me? as a play on words of MSMEs) is a group of four college students from Ateneo de Manila University.
         The team comprises of Zaidamin Haron (3 BS CTM), Andrea Senson (4 BS AMDSc), Rafael Tagulao (4 BS AMDSc), and Dianne Yumol (4 BS AMDSc).
         """)