import streamlit as st
import requests

st.set_page_config(
    page_title="SunnyStep Retail Revenue Optimizer",
    page_icon="📈",
    layout="wide"
)

# ----------------------------
# CSS
# ----------------------------

st.markdown("""
<style>

.main{
    background:#F7F9FC;
}

.block-container{
    padding-top:1.5rem;
}

.metric-card{

    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);

}

.recommend-card{

    background:white;
    padding:18px;
    border-left:6px solid #ff4b4b;
    border-radius:10px;
    margin-bottom:15px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);

}

.summary{

    background:#eef8ee;
    padding:20px;
    border-radius:10px;
    border-left:8px solid green;

}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("👟 SunnyStep")

    st.caption("Retail Revenue Optimizer")

    st.divider()

    st.write("📊 Overview")
    st.write("📦 Inventory")
    st.write("👥 Customers")
    st.write("💰 Revenue")
    st.write("🚀 Recommendations")

# ----------------------------
# Header
# ----------------------------

st.title("📈 Retail Revenue Optimization Dashboard")

st.caption(
    "AI-powered retail insights and revenue recommendations."
)

# ----------------------------
# Layout
# ----------------------------

left, right = st.columns([1, 1.5])

# ============================
# LEFT
# ============================

with left:

    st.subheader("Retail Store Data")

    store = st.text_input(
        "Store",
        "SunnyStep Orchard"
    )

    month = st.selectbox(
        "Month",
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June"
        ],
        index=4
    )

    revenue = st.number_input(
        "Revenue",
        value=82500
    )

    transactions = st.number_input(
        "Transactions",
        value=1210
    )

    aov = st.number_input(
        "Average Order Value",
        value=68.2
    )

    conversion = st.slider(
        "Conversion Rate",
        0.0,
        100.0,
        21.4
    )

    upt = st.number_input(
        "Units / Transaction",
        value=1.35
    )

    stockouts = st.slider(
        "Stockouts",
        0,
        50,
        18
    )

    slow = st.slider(
        "Slow Moving Products",
        0,
        100,
        45
    )

    sellers = st.text_input(
        "Best Sellers",
        "Cloud Walker, Urban Lite"
    )

    feedback = st.text_area(
        "Customer Feedback",
        """Not enough sizes
Long checkout queues
Wanted more promotions"""
    )

    analyze = st.button(
        "🚀 Analyze Store",
        type="primary",
        use_container_width=True
    )

# ============================
# RIGHT
# ============================

with right:

    st.subheader("Current Store KPIs")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Revenue",
        f"${revenue:,.0f}"
    )

    c2.metric(
        "Transactions",
        transactions
    )

    c3.metric(
        "AOV",
        f"${aov}"
    )

    c4.metric(
        "Conversion",
        f"{conversion}%"
    )

    c5.metric(
        "UPT",
        upt
    )

# ====================================
# CALL API
# ====================================

if analyze:

    payload = {

        "retail_data": {

            "store_name": store,

            "month": month,

            "sales": {

                "revenue": revenue,

                "transactions": transactions,

                "average_order_value": aov,

                "conversion_rate": conversion,

                "units_per_transaction": upt

            },

            "inventory": {

                "stockouts": stockouts,

                "slow_moving_products": slow,

                "best_sellers": [

                    x.strip()

                    for x in sellers.split(",")

                ]

            },

            "customer_feedback": feedback.splitlines()

        }

    }

    with st.spinner("Analyzing retail performance..."):

        response = requests.post(

            "http://localhost:8000/analyze",

            json=payload

        )

        result = response.json()

    st.divider()

    # ====================================
    # Store Health
    # ====================================

    st.subheader("🏪 Store Health")

    health = result["store_health"]

    if health == "Excellent":

        st.success(health)

    elif health == "Good":

        st.info(health)

    elif health == "Average":

        st.warning(health)

    else:

        st.error(health)

    # ====================================
    # Findings
    # ====================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Key Findings")

        for item in result["key_findings"]:

            st.success(item)

    with col2:

        st.subheader("🔍 Root Causes")

        for item in result["root_causes"]:

            st.error(item)

    # ====================================
    # Recommendations
    # ====================================

    st.subheader("🚀 AI Recommendations")

    for rec in result["recommended_actions"]:

        st.markdown(f"""
<div class="recommend-card">

### {rec["priority"]} Priority

**Action**

{rec["action"]}

**Expected Impact**

{rec["expected_impact"]}

</div>
""", unsafe_allow_html=True)

    # ====================================
    # Revenue Opportunities
    # ====================================

    st.subheader("💰 Revenue Opportunities")

    cols = st.columns(len(result["revenue_opportunities"]))

    for i, item in enumerate(result["revenue_opportunities"]):

        cols[i].info(item)

    # ====================================
    # Summary
    # ====================================

    st.subheader("📄 Executive Summary")

    st.markdown(f"""
<div class="summary">

{result["summary"]}

</div>
""", unsafe_allow_html=True)