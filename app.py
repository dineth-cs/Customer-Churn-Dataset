import streamlit as st
import pandas as pd
import joblib  

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnGuard | Telco Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load AI Model ──────────────────────────────────────────────────────────────

@st.cache_resource
def load_model():
    return joblib.load('churn_model_top5.pkl')

model = load_model()

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .stApp { background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #141428 100%); background-attachment: fixed; }
  [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a3e 0%, #0f0c29 100%); border-right: 1px solid rgba(255, 255, 255, 0.06); }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  [data-testid="stSidebar"] .stSlider label, [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stNumberInput label { font-size: 0.78rem !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: #94a3b8 !important; }
  .sidebar-header { padding: 1.5rem 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 1.5rem; }
  .sidebar-header h2 { font-size: 1.15rem; font-weight: 700; color: #f8fafc !important; margin: 0; letter-spacing: -0.02em; }
  .sidebar-header p { font-size: 0.75rem; color: #64748b !important; margin: 0.25rem 0 0 0; }
  .metric-card { background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem 1.5rem; transition: all 0.25s ease; backdrop-filter: blur(12px); position: relative; overflow: hidden; }
  .metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4); opacity: 0; transition: opacity 0.3s ease; }
  .metric-card:hover { background: rgba(255, 255, 255, 0.07); border-color: rgba(99, 102, 241, 0.35); transform: translateY(-2px); box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15); }
  .metric-card:hover::before { opacity: 1; }
  .metric-card .card-icon { font-size: 1.6rem; margin-bottom: 0.6rem; display: block; }
  .metric-card .card-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #64748b; margin-bottom: 0.35rem; }
  .metric-card .card-value { font-size: 1.55rem; font-weight: 700; color: #f1f5f9; font-family: 'DM Mono', monospace; letter-spacing: -0.02em; line-height: 1.1; }
  .metric-card .card-sub { font-size: 0.72rem; color: #475569; margin-top: 0.3rem; }
  .section-title { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #6366f1; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
  .section-title::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(99,102,241,0.4), transparent); }
  div[data-testid="stButton"] > button { width: 100% !important; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%) !important; color: #ffffff !important; font-family: 'DM Sans', sans-serif !important; font-size: 1rem !important; font-weight: 700 !important; letter-spacing: 0.04em !important; border: none !important; border-radius: 14px !important; padding: 0.85rem 2rem !important; cursor: pointer !important; transition: all 0.3s ease !important; box-shadow: 0 4px 24px rgba(99, 102, 241, 0.35) !important; text-transform: none !important; margin-top: 0.5rem !important; }
  div[data-testid="stButton"] > button:hover { transform: translateY(-2px) scale(1.01) !important; box-shadow: 0 8px 36px rgba(99, 102, 241, 0.55) !important; filter: brightness(1.1) !important; }
  div[data-testid="stAlert"] { border-radius: 14px !important; border: none !important; }
  hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }
  [data-testid="stNumberInput"] input:disabled { background: rgba(255,255,255,0.03) !important; color: #94a3b8 !important; -webkit-text-fill-color: #94a3b8 !important; cursor: not-allowed !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>📡 Customer Profile</h2>
        <p>Configure parameters below</p>
    </div>
    """, unsafe_allow_html=True)

    contract_type = st.selectbox(
        "Contract Type",
        options=["Month-to-month", "One year", "Two year"],
        index=0,
    )

    tenure = st.slider("Tenure (Months)", 0, 72, 12, 1)
    monthly_charges = st.slider("Monthly Charges ($)", 15.0, 120.0, 65.0, 0.5, format="%.2f")
    
    total_charges = monthly_charges * tenure
    st.number_input("Total Charges ($)  —  Auto-calculated", value=total_charges, disabled=True, format="%.2f")

    cltv = st.slider("CLTV (Customer Lifetime Value)", 2000, 6000, 3800, 50)

    st.markdown("---")
    st.markdown("""<p style="font-size:0.7rem; color:#334155; text-align:center; margin:0;">ChurnGuard v2.1 &nbsp;·&nbsp; Telco Analytics Suite</p>""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([6, 1])
with col_title:
    st.markdown("""
    <div style="padding: 0.5rem 0 0.25rem 0;">
        <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #e2e8f0 30%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -0.04em;">ChurnGuard Analytics</h1>
        <p style="color: #64748b; font-size: 0.9rem; margin: 0.4rem 0 0 0;">Telco Customer Churn Prediction · Powered by Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
with col_badge:
    st.markdown("""<div style="display: flex; align-items: center; justify-content: flex-end; padding-top: 0.6rem;"><span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #10b981; font-size: 0.68rem; font-weight: 700; padding: 0.3rem 0.7rem; border-radius: 999px;">● Live</span></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Customer Summary Cards ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">Customer Profile Summary</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, "📄", "Contract Type",   contract_type,           "Billing cycle"),
    (c2, "📅", "Tenure",          f"{tenure} mo",            "Months active"),
    (c3, "💳", "Monthly Charges", f"${monthly_charges:,.2f}", "Per billing cycle"),
    (c4, "💰", "Total Charges",   f"${total_charges:,.2f}",  "Lifetime spend"),
    (c5, "🏆", "CLTV Score",      f"{cltv:,}",               "Predicted value"),
]

for col, icon, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <span class="card-icon">{icon}</span>
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Predict Button ─────────────────────────────────────────────────────────────
predict_clicked = st.button("🚀  Predict Churn Risk")

# ── Prediction Logic using AI Model ────────────────────────────────────────────
if predict_clicked:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)

   
    contract_mapping = {"Month-to-month": 0, "One year": 1, "Two year": 2}
    encoded_contract = contract_mapping[contract_type]

    
    input_data = pd.DataFrame({
        'Total Charges': [total_charges],
        'Monthly Charges': [monthly_charges],
        'Tenure Months': [tenure],
        'CLTV': [cltv],
        'Contract': [encoded_contract]
    })

   
    prediction = model.predict(input_data)[0]  
    churn_prob = model.predict_proba(input_data)[0][1]   
    is_high_risk = (prediction == 1)

    
    if is_high_risk:
        st.error(f"""
### 🔴  HIGH CHURN RISK DETECTED

This customer shows a **strong propensity to churn** according to our Machine Learning model. Immediate intervention is recommended.

**Recommended Retention Actions:**

| Priority | Action | Expected Impact |
|----------|--------|----------------|
| 🔥 Critical | Offer a **15% loyalty discount** on next 3 billing cycles | Reduces financial friction |
| ⚡ High | Escalate to **Priority Support** tier instantly | Increases perceived value |
| 📞 High | Schedule a **proactive outreach call** within 48 hrs | Rebuilds personal connection |

> ⚠️  **Model Warning:** Based on similar customer patterns, this profile is highly volatile.
        """)
    else:
        st.success(f"""
### 🟢  LOW CHURN RISK — Customer is Stable

Our AI model indicates this customer demonstrates healthy retention signals. Focus on deepening loyalty and maximising lifetime value.

**Recommended Retention Strategies:**

| Priority | Action | Expected Impact |
|----------|--------|----------------|
| ✅ Standard | Enrol in **Automated Loyalty Rewards** email programme | Strengthens brand affinity |
| 🎁 Standard | Offer **anniversary perks** at tenure milestones | Celebrates customer journey |
| 📊 Medium | Present an **annual plan upgrade** with a small incentive | Increases contract commitment |

> ✔️  **Model Confidence:** Customer matches patterns of long-term stability.
        """)

    # ── Key Metrics Row ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Model Confidence Indicators</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    retention_score = 1 - churn_prob
    risk_label   = "High Risk" if is_high_risk else "Low Risk"

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="card-icon">{"🔴" if is_high_risk else "🟢"}</span>
            <div class="card-label">Churn Probability</div>
            <div class="card-value" style="color: {"#f87171" if is_high_risk else "#4ade80"};">{churn_prob:.0%}</div>
            <div class="card-sub">AI Model prediction</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="card-icon">💪</span>
            <div class="card-label">Retention Score</div>
            <div class="card-value">{retention_score:.0%}</div>
            <div class="card-sub">Likelihood to remain</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="card-icon">🧠</span>
            <div class="card-label">AI Classification</div>
            <div class="card-value" style="font-size:1.15rem; color: {"#f87171" if is_high_risk else "#4ade80"};">{risk_label}</div>
            <div class="card-sub">Random Forest Analysis</div>
        </div>
        """, unsafe_allow_html=True)