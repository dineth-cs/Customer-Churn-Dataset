import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from streamlit_option_menu import option_menu

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="ChurnGuard Enterprise", page_icon="⚡", layout="wide")

# ── Load AI Model ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load('churn_model_top5.pkl')

model = load_model()

# ── Modern Premium CSS (Fixed for Light Mode issues) ───────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  * { font-family: 'Inter', sans-serif; }
  
  /* Force dark background and white text globally to override light mode */
  .stApp { background-color: #0B0F19 !important; }
  [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #1F2937 !important; }
  .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown p, label, .stMarkdown span { color: #F9FAFB !important; }
  
  /* Custom Cards */
  .glass-card { background: #1F2937 !important; border: 1px solid #374151 !important; border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 16px; }
  .metric-title { color: #9CA3AF !important; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;}
  .metric-val { color: #F9FAFB !important; font-size: 2.2rem; font-weight: 700; }
  .metric-sub { color: #10B981 !important; font-size: 0.85rem; font-weight: 500; margin-top: 6px; display: flex; align-items: center; gap: 4px;}
  .metric-sub.negative { color: #EF4444 !important; }
  
  /* Inputs fixing */
  div[data-baseweb="select"] > div, input { background-color: #374151 !important; color: white !important; border-color: #4B5563 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sleek Sidebar Menu ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 30px; padding-top: 20px;'><h1 style='color: #F9FAFB !important; font-weight: 800; font-size: 26px; margin: 0;'><span style='color: #6366F1;'>⚡</span> ChurnGuard</h1><p style='color: #6B7280 !important; font-size: 13px; margin-top: 4px;'>Enterprise AI Platform</p></div>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Analytics Dashboard", "Single Predictor", "Batch Predictor", "AI Insights", "Financial ROI"],
        icons=["bar-chart-fill", "person-bounding-box", "people-fill", "cpu-fill", "currency-dollar"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#6B7280", "font-size": "16px"},
            "nav-link": {"color": "#9CA3AF", "font-size": "14px", "font-weight": "500", "margin":"4px 0", "border-radius": "10px", "padding": "12px 16px"},
            "nav-link-selected": {"background-color": "rgba(99, 102, 241, 0.15)", "color": "#818CF8", "font-weight": "600", "border": "1px solid rgba(99, 102, 241, 0.3)"},
        }
    )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: ANALYTICS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if selected == "Analytics Dashboard":
    st.markdown("<h2>Business Overview</h2><p>Real-time metrics and customer retention intelligence.</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="glass-card"><div class="metric-title">Total Users</div><div class="metric-val">7,043</div><div class="metric-sub">↑ +124 this month</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="glass-card"><div class="metric-title">Churn Rate</div><div class="metric-val">26.5%</div><div class="metric-sub negative">↓ -2.1% vs last month</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="glass-card"><div class="metric-title">Monthly Revenue</div><div class="metric-val">$456K</div><div class="metric-sub">↑ +5.4% growth</div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="glass-card"><div class="metric-title">Active Subs</div><div class="metric-val">5,174</div><div class="metric-sub">Stable</div></div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("<div class='glass-card'><h4>Revenue vs Churn Impact</h4>", unsafe_allow_html=True)
        df_line = pd.DataFrame({'Month': ['Jan','Feb','Mar','Apr','May','Jun'], 'Revenue': [400, 420, 410, 440, 430, 456], 'Lost': [50, 45, 60, 40, 35, 30]})
        fig1 = px.area(df_line, x='Month', y=['Revenue', 'Lost'], color_discrete_sequence=['#4F46E5', '#EF4444'], template='plotly_dark')
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown("<div class='glass-card'><h4>Customer Base by Contract</h4>", unsafe_allow_html=True)
        df_bar = pd.DataFrame({'Contract': ['Month-to-month', 'One year', 'Two year'], 'Users': [3875, 1473, 1695]})
        fig2 = px.bar(df_bar, x='Contract', y='Users', color='Contract', color_discrete_sequence=['#F59E0B', '#10B981', '#3B82F6'], template='plotly_dark')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: SINGLE PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Single Predictor":
    st.markdown("<h2>Individual Risk Analysis</h2><p>Evaluate a single customer's flight risk.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.8], gap="large")
    with col1:
        st.markdown("<div class='glass-card'><h4>Profile Settings</h4>", unsafe_allow_html=True)
        contract_type = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        tenure = st.slider("Tenure (Months)", 0, 72, 12, 1)
        monthly_charges = st.slider("Monthly Charges ($)", 15.0, 120.0, 65.0, 0.5)
        total_charges = monthly_charges * tenure
        st.number_input("Total Charges ($)", value=total_charges, disabled=True)
        cltv = st.slider("Customer Lifetime Value", 2000, 6000, 3800, 50)
        st.markdown("</div>", unsafe_allow_html=True)
        predict_btn = st.button("🚀 Process Analysis")

    with col2:
        if predict_btn:
            contract_mapping = {"Month-to-month": 0, "One year": 1, "Two year": 2}
            encoded_contract = contract_mapping[contract_type]
            input_data = pd.DataFrame({'Total Charges': [total_charges], 'Monthly Charges': [monthly_charges], 'Tenure Months': [tenure], 'CLTV': [cltv], 'Contract': [encoded_contract]})
            
            prediction = model.predict(input_data)[0]
            churn_prob = model.predict_proba(input_data)[0][1]
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            if prediction == 1:
                st.markdown(f"<h3 style='color: #EF4444 !important;'>⚠️ High Flight Risk Detected</h3><p>Probability of Cancellation: <b>{churn_prob:.1%}</b></p>", unsafe_allow_html=True)
                st.progress(float(churn_prob))
                st.error("Action Required: Trigger discount campaign and route to priority support.")
            else:
                st.markdown(f"<h3 style='color: #10B981 !important;'>✅ Healthy Customer Profile</h3><p>Probability of Retention: <b>{1-churn_prob:.1%}</b></p>", unsafe_allow_html=True)
                st.progress(float(1-churn_prob))
                st.success("Stable behavior. Proceed with standard lifecycle marketing.")
            st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: BATCH PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Batch Predictor":
    st.markdown("<h2>Bulk Prediction Engine</h2><p>Upload a CSV file containing multiple customers to predict churn at scale.</p>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>1. Download CSV Template</h4>", unsafe_allow_html=True)
    
    template_df = pd.DataFrame({'Total Charges': [150.50, 850.20], 'Monthly Charges': [50.00, 25.50], 'Tenure Months': [3, 33], 'CLTV': [2500, 4500], 'Contract': [0, 2]})
    st.download_button(label="📥 Download Template.csv", data=template_df.to_csv(index=False).encode('utf-8'), file_name='churn_template.csv', mime='text/csv')
    
    st.markdown("<br><h4>2. Upload Customer Data</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])
    
    if uploaded_file is not None:
        try:
            bulk_data = pd.read_csv(uploaded_file)
            if st.button("🚀 Analyze Bulk Data"):
                with st.spinner("AI is analyzing records..."):
                    predictions = model.predict(bulk_data)
                    probabilities = model.predict_proba(bulk_data)[:, 1]
                    bulk_data['Churn_Risk'] = ['High Risk' if p==1 else 'Low Risk' for p in predictions]
                    bulk_data['Probability'] = [f"{prob:.1%}" for prob in probabilities]
                    st.success(f"Analysis Complete for {len(bulk_data)} customers!")
                    st.dataframe(bulk_data)
                    st.download_button(label="📥 Download Analysis Results", data=bulk_data.to_csv(index=False).encode('utf-8'), file_name='churn_results.csv', mime='text/csv')
        except Exception as e:
            st.error("Error processing file. Please ensure it matches the template.")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: AI INSIGHTS 
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "AI Insights":
    st.markdown("<h2>AI Decision Insights</h2><p>Understand how the Random Forest model evaluates customer risk.</p>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'><h4>Feature Importance (What drives churn?)</h4>", unsafe_allow_html=True)
    
    importances = model.feature_importances_
    features = ['Total Charges', 'Monthly Charges', 'Tenure Months', 'CLTV', 'Contract']
    df_importance = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=True)
    
    fig = px.bar(df_importance, x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='Purpor', template='plotly_dark')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: FINANCIAL ROI (NEW PAGE!)
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Financial ROI":
    st.markdown("<h2>💰 Financial Impact & ROI</h2><p>Calculate the estimated revenue saved by using this AI model.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        st.markdown("<div class='glass-card'><h4>Campaign Parameters</h4>", unsafe_allow_html=True)
        at_risk_users = st.number_input("Identified At-Risk Customers", min_value=10, max_value=5000, value=500, step=10)
        avg_cltv = st.number_input("Average CLTV ($)", min_value=100, max_value=10000, value=3800, step=100)
        campaign_cost = st.slider("Cost per Retention Offer ($)", 5, 100, 25)
        success_rate = st.slider("Estimated Campaign Success Rate (%)", 5, 80, 30)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Math calculations
        revenue_at_risk = at_risk_users * avg_cltv
        total_campaign_cost = at_risk_users * campaign_cost
        customers_saved = int(at_risk_users * (success_rate / 100))
        revenue_saved = customers_saved * avg_cltv
        net_profit = revenue_saved - total_campaign_cost
        
        st.markdown("<div class='glass-card'><h4>Projected Outcomes</h4>", unsafe_allow_html=True)
        st.markdown(f"<p>Total Revenue at Risk: <b style='color:#EF4444; font-size:1.2rem;'>${revenue_at_risk:,.2f}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p>Total Campaign Cost: <b style='color:#F59E0B; font-size:1.2rem;'>${total_campaign_cost:,.2f}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #374151; margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<p>Customers Successfully Retained: <b style='color:#10B981; font-size:1.2rem;'>{customers_saved}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p>Gross Revenue Saved: <b style='color:#10B981; font-size:1.2rem;'>${revenue_saved:,.2f}</b></p>", unsafe_allow_html=True)
        
        profit_color = "#10B981" if net_profit > 0 else "#EF4444"
        st.markdown(f"<div style='background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 16px; border-radius: 12px; margin-top: 15px;'><h3>Net ROI (Profit): <span style='color:{profit_color};'>${net_profit:,.2f}</span></h3></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)