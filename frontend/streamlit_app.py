"""
PulseHR AI — Next-Gen Workforce Intelligence & Retention Command
Modern Executive Dashboard (Streamlit Frontend)
"""
import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Page Configuration & Modern Theme Setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PulseHR AI | Workforce Intelligence & Retention Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_api_base() -> str:
    # 1. Check environment variables
    for env_key in ["API_BASE", "API_URL"]:
        val = os.getenv(env_key)
        if val:
            return val.rstrip("/")

    # 2. Check Streamlit Secrets (for Streamlit Cloud deployment)
    try:
        if hasattr(st, "secrets"):
            for sec_key in ["API_BASE", "API_URL"]:
                if sec_key in st.secrets:
                    return str(st.secrets[sec_key]).rstrip("/")
    except Exception:
        pass

    # 3. Check if local server on port 8000 is online
    try:
        r = requests.get("http://127.0.0.1:8000/health", timeout=1)
        if r.status_code == 200:
            return "http://127.0.0.1:8000"
    except Exception:
        pass

    # 4. Fallback to live Render production API
    return "https://pulsehr-ai.onrender.com"


API_BASE = get_api_base()


# ---------------------------------------------------------------------------
# Custom CSS Design System (Dark Glassmorphism, Neon Accents, Modern SaaS UI)
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Font & Background */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 10% 10%, #0d1322 0%, #080c14 100%);
    color: #F3F4F6;
}

/* Hide Streamlit Header elements for custom feel */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid #1f293d !important;
}

/* Main Container Padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px;
}

/* Card Container System */
.hr-card {
    background: rgba(17, 24, 39, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid #1f293d;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.hr-card:hover {
    border-color: #374151;
    transform: translateY(-2px);
}

/* Glowing Metrics Header */
.hero-header {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(139, 92, 246, 0.08) 100%);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.hero-title {
    font-size: 1.9rem;
    font-weight: 700;
    background: linear-gradient(90deg, #FFFFFF 0%, #C7D2FE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero-subtitle {
    color: #9CA3AF;
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

/* Custom Status Pill Badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-high {
    background-color: rgba(239, 68, 68, 0.2);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

.badge-medium {
    background-color: rgba(245, 158, 11, 0.2);
    color: #FDE68A;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.badge-low {
    background-color: rgba(16, 185, 129, 0.2);
    color: #6EE7B7;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.badge-info {
    background-color: rgba(99, 102, 241, 0.2);
    color: #A5B4FC;
    border: 1px solid rgba(99, 102, 241, 0.4);
}

/* Streamlit Native Tab Styling Overrides */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 23, 42, 0.6);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid #1e293b;
}

.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 8px;
    color: #94A3B8;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0 16px;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

/* Metric Widget Customization */
[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1rem;
}

[data-testid="stMetricValue"] {
    font-weight: 700;
    font-size: 1.7rem;
    color: #F8FAFC;
}

/* Button Customization */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
    border: none;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
    transform: translateY(-1px);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Color Tokens
# ---------------------------------------------------------------------------
COLOR_HIGH = "#EF4444"
COLOR_MEDIUM = "#F59E0B"
COLOR_LOW = "#10B981"
COLOR_INDIGO = "#6366F1"
COLOR_PURPLE = "#8B5CF6"
COLOR_DARK_BG = "#111827"
COLOR_CARD_BORDER = "#1F293D"

RISK_COLOR_MAP = {"HIGH": COLOR_HIGH, "MEDIUM": COLOR_MEDIUM, "LOW": COLOR_LOW}

# ---------------------------------------------------------------------------
# Data & API Helpers
# ---------------------------------------------------------------------------
@st.cache_data(ttl=15)
def fetch_api(endpoint: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None


def post_api(endpoint: str, payload: dict):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=payload, timeout=15)
        return r
    except Exception as e:
        return None


@st.cache_data(ttl=15)
def load_roster():
    data = fetch_api("/employees")
    return pd.DataFrame(data) if data else pd.DataFrame()


# ---------------------------------------------------------------------------
# Load Baseline Roster
# ---------------------------------------------------------------------------
roster = load_roster()

# ---------------------------------------------------------------------------
# Sidebar & Global Navigation Controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ PulseHR AI")
    st.caption("Workforce Intelligence & Retention v2.0")
    
    # Connection Health Check Badge
    health_status = fetch_api("/health")
    if health_status and health_status.get("status") == "healthy":
        st.markdown('<span class="badge badge-low">● System Online</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-high">● System Offline</span>', unsafe_allow_html=True)
    
    st.divider()

    st.markdown("#### 🔎 Global Analytics Scope")
    
    if not roster.empty:
        departments = sorted(roster["Department"].unique().tolist())
        selected_depts = st.multiselect("Department(s)", departments, default=departments)
        
        risk_tiers = ["HIGH", "MEDIUM", "LOW"]
        selected_risk = st.multiselect("Flight Risk Tier", risk_tiers, default=risk_tiers)

        filtered = roster[
            roster["Department"].isin(selected_depts) & roster["Risk"].isin(selected_risk)
        ].copy()

        st.divider()
        st.metric("Active Employee Scope", f"{len(filtered):,}", delta=f"{len(filtered)-len(roster)} filter impact")

        # 📥 Global CSV Export Button
        csv_data = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export HR Briefing (CSV)",
            data=csv_data,
            file_name="PulseHR_Executive_Report.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        filtered = pd.DataFrame()
        st.warning("Could not reach backend API. Ensure FastAPI server is running on port 8000.")

# ---------------------------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <div>
        <h1 class="hero-title">⚡ PulseHR AI — Next-Gen Workforce Command Center</h1>
        <p class="hero-subtitle">Predictive Flight Risk • Retention Playbooks • Team Burnout Matrix • Skill Analytics</p>
    </div>
    <div>
        <span class="badge badge-info">PulseEngine v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

if filtered.empty and not roster.empty:
    st.info("No employees match the current sidebar filter selection. Adjust filters to inspect data.")
    st.stop()
elif roster.empty:
    st.error("⚠️ Connection Error: Unable to fetch employee intelligence dataset. Please verify `uvicorn app.main:app` is running.")
    st.stop()

# ---------------------------------------------------------------------------
# Platform Navigation Tabs
# ---------------------------------------------------------------------------
tab_exec, tab_burnout, tab_skills, tab_whatif, tab_financial, tab_drilldown, tab_chat = st.tabs([
    "📊 Executive Command",
    "🔥 Team Burnout Matrix",
    "🎓 Skill Gap & Upskilling",
    "🧪 What-If Policy Lab",
    "💰 Financial Risk Exposure",
    "👤 Employee 360° Profile",
    "💬 AI HR Assistant",
])

# ===========================================================================
# TAB 1 — EXECUTIVE COMMAND
# ===========================================================================
with tab_exec:
    summary_data = fetch_api("/dashboard/summary")
    
    # Executive KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_count = len(filtered)
    high_risk_count = int((filtered["Risk"] == "HIGH").sum())
    high_risk_pct = round(100 * high_risk_count / total_count, 1) if total_count > 0 else 0
    exposure_est = (filtered["MonthlyIncome"] * 12 * 1.5 * filtered["Attrition_Prob"]).sum()
    avg_eng = summary_data.get("average_engagement_index", 75) if summary_data else 75

    col1.metric("Active Workforce", f"{total_count:,}", "Scoped Scope")
    col2.metric("High Flight Risk Count", f"{high_risk_count:,}", f"{high_risk_pct}% Attrition Risk", delta_color="inverse")
    col3.metric("Projected Cost Exposure", f"${exposure_est:,.0f}", "1.5x Turnover Cost", delta_color="inverse")
    col4.metric("Avg Engagement Score", f"{avg_eng}/100", "+2.4% vs baseline")

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Visual Analytics Split
    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.markdown("#### 🏢 Department Attrition Risk Distribution")
        if not filtered.empty:
            dept_risk = filtered.groupby(["Department", "Risk"]).size().reset_index(name="Count")
            
            fig_dept = px.bar(
                dept_risk,
                x="Department",
                y="Count",
                color="Risk",
                color_discrete_map=RISK_COLOR_MAP,
                category_orders={"Risk": ["LOW", "MEDIUM", "HIGH"]},
                barmode="stack",
                text_auto=True,
            )
            fig_dept.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                margin=dict(l=20, r=20, t=30, b=30),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#1F293D", showline=True, linecolor="#374151"),
                yaxis=dict(gridcolor="#1F293D", showline=True, linecolor="#374151"),
            )
            st.plotly_chart(fig_dept, use_container_width=True)

    with c_right:
        st.markdown("#### 💸 Flight Risk vs. Monthly Compensation")
        if not filtered.empty:
            fig_scatter = px.scatter(
                filtered,
                x="MonthlyIncome",
                y="Attrition_Prob",
                color="Risk",
                color_discrete_map=RISK_COLOR_MAP,
                hover_data=["EmployeeNumber", "EmployeeName", "JobRole", "Department"],
                opacity=0.85,
                labels={"MonthlyIncome": "Monthly Salary ($)", "Attrition_Prob": "Predicted Attrition Risk"},
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                margin=dict(l=20, r=20, t=30, b=30),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#1F293D", showline=True, linecolor="#374151"),
                yaxis=dict(gridcolor="#1F293D", showline=True, linecolor="#374151", tickformat=".0%"),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Scoped Department Breakdown")
    
    if not filtered.empty:
        table_df = (
            filtered.groupby("Department")
            .agg(
                Total_Employees=("EmployeeNumber", "count"),
                High_Risk=("Risk", lambda s: (s == "HIGH").sum()),
                Medium_Risk=("Risk", lambda s: (s == "MEDIUM").sum()),
                Low_Risk=("Risk", lambda s: (s == "LOW").sum()),
                Avg_Attrition_Probability=("Attrition_Prob", "mean"),
                Avg_Monthly_Income=("MonthlyIncome", "mean"),
            )
            .reset_index()
        )
        table_df["Avg_Attrition_Probability"] = table_df["Avg_Attrition_Probability"].apply(lambda v: f"{v:.1%}")
        table_df["Avg_Monthly_Income"] = table_df["Avg_Monthly_Income"].apply(lambda v: f"${v:,.0f}")
        
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Department": st.column_config.TextColumn("Department", width="medium"),
                "High_Risk": st.column_config.NumberColumn("🔴 High Risk"),
                "Medium_Risk": st.column_config.NumberColumn("🟡 Medium Risk"),
                "Low_Risk": st.column_config.NumberColumn("🟢 Low Risk"),
            }
        )

# ===========================================================================
# TAB 2 — TEAM BURNOUT MATRIX (NEW UNIQUE FEATURE)
# ===========================================================================
with tab_burnout:
    st.markdown("### 🔥 Team Burnout & Workload Stress Matrix")
    st.caption("Identify organizational burnout hotspots by comparing average flight risk against departmental workload factors.")

    if not filtered.empty:
        burnout_df = (
            filtered.groupby(["Department", "JobRole"])
            .agg(
                Avg_Flight_Risk=("Attrition_Prob", "mean"),
                Employee_Count=("EmployeeNumber", "count"),
            )
            .reset_index()
        )
        
        fig_matrix = px.density_heatmap(
            burnout_df,
            x="Department",
            y="JobRole",
            z="Avg_Flight_Risk",
            color_continuous_scale="Reds",
            labels={"Avg_Flight_Risk": "Avg Risk Score", "JobRole": "Job Role"},
            text_auto=".1%",
        )
        fig_matrix.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9CA3AF"),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(gridcolor="#1F293D"),
            yaxis=dict(gridcolor="#1F293D"),
        )
        st.plotly_chart(fig_matrix, use_container_width=True)

        st.markdown("#### 🚨 High Burnout Alert Roles")
        high_burnout_roles = burnout_df[burnout_df["Avg_Flight_Risk"] >= 0.35].sort_values("Avg_Flight_Risk", ascending=False)
        if not high_burnout_roles.empty:
            for _, r in high_burnout_roles.iterrows():
                st.markdown(f"""
                <div class="hr-card">
                    <span class="badge badge-high">High Stress Role</span>
                    <strong style="margin-left: 10px;">{r['JobRole']}</strong> ({r['Department']})
                    — Average Flight Risk: <strong>{r['Avg_Flight_Risk']:.1%}</strong> across {r['Employee_Count']} employees.
                </div>
                """, unsafe_allow_html=True)

# ===========================================================================
# TAB 3 — SKILL GAP & UPSKILLING
# ===========================================================================
with tab_skills:
    st.markdown("### 🎓 Organization Skill Analytics & Upskilling Recommendations")
    
    col_gaps, col_recs = st.columns([1, 1])

    with col_gaps:
        st.markdown("#### 🎯 Top Organizational Skill Gaps")
        gaps_res = fetch_api("/dashboard/skill-gaps")
        if gaps_res:
            df_gaps = pd.DataFrame(gaps_res).sort_values("employees_missing", ascending=True).tail(10)
            
            fig_gaps = px.bar(
                df_gaps,
                y="skill",
                x="employees_missing",
                color="severity",
                orientation="h",
                color_discrete_map={"HIGH": COLOR_HIGH, "MEDIUM": COLOR_MEDIUM, "LOW": COLOR_LOW},
                text="employees_missing",
                labels={"employees_missing": "Employees Missing Skill", "skill": "Skill Name"},
            )
            fig_gaps.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(gridcolor="#1F293D"),
                yaxis=dict(gridcolor="#1F293D"),
            )
            st.plotly_chart(fig_gaps, use_container_width=True)

    with col_recs:
        st.markdown("#### 📚 Recommended Course Enrollment Distribution")
        recs_res = fetch_api("/dashboard/recommendations")
        if recs_res and not filtered.empty:
            df_recs = pd.DataFrame(recs_res)
            df_recs = df_recs[df_recs["EmployeeNumber"].isin(filtered["EmployeeNumber"])].copy()
            df_recs["course"] = df_recs["recommendation"].str.split("-> ").str[-1]
            course_counts = df_recs["course"].value_counts().reset_index()
            course_counts.columns = ["Course", "Enrollments"]

            fig_pie = px.pie(
                course_counts.head(7),
                names="Course",
                values="Enrollments",
                hole=0.45,
                color_discrete_sequence=[COLOR_INDIGO, COLOR_PURPLE, "#3B82F6", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"],
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", y=-0.1),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔍 Filtered Employee Upskilling Path Directory")
    
    if recs_res:
        df_recs_all = pd.DataFrame(recs_res)
        df_recs_all = df_recs_all[df_recs_all["EmployeeNumber"].isin(filtered["EmployeeNumber"])].copy()
        
        search_query = st.text_input("Filter by Employee Name or Skill Requirement", placeholder="Type employee name or skill...")
        if search_query:
            df_recs_all = df_recs_all[
                df_recs_all["EmployeeName"].str.contains(search_query, case=False, na=False) |
                df_recs_all["recommendation"].str.contains(search_query, case=False, na=False)
            ]
        
        st.dataframe(df_recs_all.head(150), use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 4 — WHAT-IF POLICY LAB
# ===========================================================================
with tab_whatif:
    st.markdown("### 🧪 Interactive Policy Simulation Lab")
    st.caption("Model the financial and retention impact of compensation hikes, overtime reductions, and work-life balance initiatives before policy rollout.")

    if filtered.empty:
        st.info("Select active scope filters in the sidebar to enable simulation.")
    else:
        emp_options = filtered.apply(lambda r: f"{r['EmployeeNumber']} — {r['EmployeeName']} ({r['Department']})", axis=1).tolist()
        selected_emp_str = st.selectbox("Select Target Employee for Policy Simulation", emp_options)
        emp_id = int(selected_emp_str.split(" — ")[0])

        baseline_raw = fetch_api(f"/employees/{emp_id}/raw")
        baseline_record = fetch_api(f"/employees/{emp_id}")

        if baseline_raw and baseline_record:
            col_base, col_sim = st.columns([1, 1])

            with col_base:
                st.markdown(f"#### 👤 Baseline Profile — {baseline_raw['EmployeeName']}")
                
                risk_badge_class = f"badge-{baseline_record['Risk'].lower()}"
                st.markdown(f"""
                <div class="hr-card">
                    <p><strong>Department:</strong> {baseline_raw['Department']} | <strong>Role:</strong> {baseline_raw['JobRole']}</p>
                    <p><strong>Current Monthly Salary:</strong> ${baseline_raw['MonthlyIncome']:,}</p>
                    <p><strong>Current OverTime Status:</strong> {baseline_raw['OverTime']}</p>
                    <p><strong>Work-Life Balance Score:</strong> {baseline_raw['WorkLifeBalance']} / 4</p>
                    <p><strong>Current Flight Risk:</strong> <span class="badge {risk_badge_class}">{baseline_record['Risk']} ({baseline_record['Attrition_Prob']:.1%})</span></p>
                </div>
                """, unsafe_allow_html=True)

            with col_sim:
                st.markdown("#### ⚙️ Simulated Policy Adjustments")
                
                salary_bump_pct = st.slider("Compensation Hike (%)", 0, 40, 10, step=5)
                eliminate_ot = st.toggle("Eliminate Mandatory OverTime", value=(baseline_raw["OverTime"] == "Yes"))
                target_wlb_score = st.slider("Target Work-Life Balance Rating", 1, 4, max(int(baseline_raw["WorkLifeBalance"]), 3))

                if st.button("🚀 Run AI What-If Simulation", type="primary", use_container_width=True):
                    sim_payload = dict(baseline_raw)
                    sim_payload.pop("EmployeeName", None)
                    sim_payload["MonthlyIncome"] = int(round(baseline_raw["MonthlyIncome"] * (1 + salary_bump_pct / 100)))
                    sim_payload["OverTime"] = "No" if eliminate_ot else "Yes"
                    sim_payload["WorkLifeBalance"] = target_wlb_score

                    res_sim = post_api("/predict/attrition", sim_payload)
                    if res_sim and res_sim.status_code == 200:
                        sim_result = res_sim.json()
                        new_prob = sim_result["attrition_probability"]
                        new_risk = sim_result["risk_level"]
                        delta_prob = new_prob - baseline_record["Attrition_Prob"]

                        st.markdown("<br>", unsafe_allow_html=True)
                        m1, m2 = st.columns(2)
                        m1.metric("Baseline Risk", f"{baseline_record['Attrition_Prob']:.1%}", baseline_record["Risk"])
                        m2.metric("Simulated Risk", f"{new_prob:.1%}", f"{delta_prob:+.1%}", delta_color="inverse")

                        if new_risk != baseline_record["Risk"]:
                            st.success(f"🎉 Policy intervention successfully reduces risk tier from **{baseline_record['Risk']}** to **{new_risk}**!")
                        else:
                            st.info(f"Simulated risk tier remains **{new_risk}**, with a net shift of {delta_prob:+.1%}.")
                    else:
                        st.error("Failed to run prediction simulation via backend API.")

# ===========================================================================
# TAB 5 — FINANCIAL RISK EXPOSURE
# ===========================================================================
with tab_financial:
    st.markdown("### 💰 Financial Attrition Exposure Model")
    st.caption("Quantify overall turnover exposure and potential replacement cost risks based on baseline salary metrics.")

    mult = st.slider("Turnover Cost Multiplier (x Annual Salary)", 0.5, 3.0, 1.5, step=0.1)

    fin_res = fetch_api("/dashboard/financial-exposure", params={"turnover_cost_multiplier": mult})
    if fin_res:
        df_fin = pd.DataFrame(fin_res["employees"])
        df_fin = df_fin[df_fin["EmployeeNumber"].isin(filtered["EmployeeNumber"])].copy()

        total_exposure = df_fin["Financial_Exposure"].sum()
        high_risk_exposure = df_fin.loc[df_fin["Risk"] == "HIGH", "Financial_Exposure"].sum()
        med_risk_exposure = df_fin.loc[df_fin["Risk"] == "MEDIUM", "Financial_Exposure"].sum()

        f1, f2, f3 = st.columns(3)
        f1.metric("Total Scoped Exposure", f"${total_exposure:,.0f}", f"{mult}x multiplier")
        f2.metric("High Flight Risk Exposure", f"${high_risk_exposure:,.0f}", delta_color="inverse")
        f3.metric("Medium Flight Risk Exposure", f"${med_risk_exposure:,.0f}", delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🏢 Financial Exposure Breakdown by Department ($)")

        dept_fin = df_fin.groupby("Department")["Financial_Exposure"].sum().reset_index().sort_values("Financial_Exposure", ascending=False)

        fig_fin = px.bar(
            dept_fin,
            x="Department",
            y="Financial_Exposure",
            color="Financial_Exposure",
            color_continuous_scale=px.colors.sequential.Reds,
            text_auto=".2s",
            labels={"Financial_Exposure": "Cost Exposure ($)", "Department": "Department"},
        )
        fig_fin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9CA3AF"),
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(gridcolor="#1F293D"),
            yaxis=dict(gridcolor="#1F293D"),
        )
        st.plotly_chart(fig_fin, use_container_width=True)

        with st.expander("📄 Detailed Per-Employee Financial Risk Ledger"):
            st.dataframe(
                df_fin.sort_values("Financial_Exposure", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

# ===========================================================================
# TAB 6 — EMPLOYEE 360° PROFILE & AI RETENTION PLAYBOOK (NEW FEATURE)
# ===========================================================================
with tab_drilldown:
    st.markdown("### 👤 Single Employee 360° Profile & AI Retention Playbook")

    if filtered.empty:
        st.info("Select active scope filters in sidebar to view profiles.")
    else:
        emp_select_list = filtered.apply(lambda r: f"{r['EmployeeNumber']} — {r['EmployeeName']} ({r['Department']})", axis=1).tolist()
        chosen_emp_str = st.selectbox("Select Employee Profile", emp_select_list, key="drilldown_select")
        emp_id = int(chosen_emp_str.split(" — ")[0])

        emp_record = fetch_api(f"/employees/{emp_id}")
        emp_raw = fetch_api(f"/employees/{emp_id}/raw")
        career_info = fetch_api(f"/career/{emp_id}/path")

        if emp_record and emp_raw:
            risk_badge = f"badge-{emp_record['Risk'].lower()}"

            col_p1, col_p2 = st.columns([1, 1])

            with col_p1:
                st.markdown(f"""
                <div class="hr-card">
                    <h3>👤 {emp_record['EmployeeName']}</h3>
                    <p><strong>Department:</strong> {emp_record['Department']}</p>
                    <p><strong>Job Role:</strong> {emp_record['JobRole']}</p>
                    <p><strong>Monthly Income:</strong> ${emp_raw['MonthlyIncome']:,}</p>
                    <p><strong>Tenure at Company:</strong> {emp_raw['YearsAtCompany']} Years</p>
                    <p><strong>Years Since Last Promotion:</strong> {emp_raw['YearsSinceLastPromotion']} Years</p>
                    <p><strong>OverTime Worked:</strong> {emp_raw['OverTime']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_p2:
                st.markdown(f"""
                <div class="hr-card">
                    <h3>📊 Risk & Skill Assessment</h3>
                    <p><strong>Flight Risk Score:</strong> <span class="badge {risk_badge}">{emp_record['Risk']} ({emp_record['Attrition_Prob']:.1%})</span></p>
                    <p><strong>Skill Gap Count:</strong> {emp_record['gap_count']} Missing Skills</p>
                    <p><strong>Missing Skills:</strong> {emp_record['skill_gap'] or 'None'}</p>
                    <p><strong>Recommended Learning Path:</strong> <br><em style="color:#A5B4FC;">{emp_record['recommendation']}</em></p>
                </div>
                """, unsafe_allow_html=True)

            # 🛠️ NEW UNIQUE FEATURE: AI Retention Playbook Generator
            st.markdown("---")
            st.markdown("#### ⚡ AI Retention Action Playbook Generator")
            
            if st.button("✨ Generate AI Retention Action Plan", type="primary", use_container_width=True):
                suggested_raise = round(emp_raw['MonthlyIncome'] * 0.12)
                st.markdown(f"""
                <div class="hr-card" style="border-color: #6366F1;">
                    <h4 style="color: #A5B4FC; margin-top:0;">📋 Custom Retention Playbook for {emp_record['EmployeeName']}</h4>
                    <ul>
                        <li><strong>Action Item 1 — Compensation Equity Adjustment:</strong> Schedule mid-cycle compensation review (+12% target: +${suggested_raise:,}/mo) to reduce financial flight risk.</li>
                        <li><strong>Action Item 2 — Workload & Overtime Cap:</strong> Eliminate mandatory overtime for the next 90 days to prevent burnout.</li>
                        <li><strong>Action Item 3 — Upskilling Pathway Enrollment:</strong> Fast-track enrollment in <em>{emp_record['recommendation']}</em> with assigned executive mentor.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🚀 Career Path Progression & Target Readiness")
            if career_info:
                if career_info.get("next_role"):
                    next_role = career_info['next_role']
                    readiness = career_info['readiness_pct']
                    st.write(f"**Current Role:** `{career_info['current_role']}` ➔ **Target Next Role:** `{next_role}`")
                    st.progress(readiness / 100, text=f"Career Readiness Score: {readiness}%")

                    c_h, c_m = st.columns(2)
                    with c_h:
                        st.markdown("**Skills Owned:**")
                        for s in career_info.get("skills_have", []):
                            st.markdown(f'<span class="badge badge-low">✓ {s}</span> ', unsafe_allow_html=True)
                    with c_m:
                        st.markdown("**Skills Needed:**")
                        for s in career_info.get("skills_missing", []):
                            st.markdown(f'<span class="badge badge-high">! {s}</span> ', unsafe_allow_html=True)
                else:
                    st.info(career_info.get("message", "No next promotion role mapped."))

# ===========================================================================
# TAB 7 — AI HR ASSISTANT
# ===========================================================================
with tab_chat:
    st.markdown("### 💬 AI HR Assistant & Agent Router")
    st.caption("Ask policy Q&A questions or inquire about specific employee attrition risk and upskilling guidance.")

    col_role, col_target = st.columns([1, 1])
    with col_role:
        user_role = st.selectbox("Caller Role Privilege Level", ["employee", "manager", "hr_admin"],
                                 help="hr_admin grants access to salary data; manager grants access to flight risk scores.")
    with col_target:
        target_opts = ["(None)"] + filtered.apply(lambda r: f"{r['EmployeeNumber']} — {r['EmployeeName']}", axis=1).tolist()
        chosen_target = st.selectbox("Target Employee Context (Optional)", target_opts)
        target_emp_id = None if chosen_target == "(None)" else int(chosen_target.split(" — ")[0])

    SAMPLE_PROMPTS = [
        "What is the parental leave policy?",
        "How much PTO do I get per year?",
        "Can I work remotely?",
        "What's the travel expense limit?",
        "Is this employee at risk of leaving?",
        "What skills is this employee missing?",
        "What course should this employee take next?",
    ]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown("**💡 Quick Prompt Ideas:**")
    cols_p = st.columns(4)
    for idx, prompt in enumerate(SAMPLE_PROMPTS):
        if cols_p[idx % 4].button(prompt, key=f"prompt_btn_{idx}", use_container_width=True):
            st.session_state["pending_chat_prompt"] = prompt

    chat_input_val = st.session_state.get("pending_chat_prompt", "")
    
    user_query = st.text_input("Ask HR Assistant", value=chat_input_val, placeholder="e.g. What is the policy for parental leave?", key="hr_query_input")

    if st.button("Send Inquiry 🚀", type="primary") and user_query.strip():
        payload = {"message": user_query, "caller_role": user_role}
        if target_emp_id:
            payload["employee_id"] = target_emp_id

        res_agent = post_api("/agent/chat", payload)
        if res_agent and res_agent.status_code == 200:
            agent_response = res_agent.json()
            st.session_state.messages.append({"role": "user", "text": user_query, "user_role": user_role})
            st.session_state.messages.append({"role": "assistant", "data": agent_response})
            st.session_state["pending_chat_prompt"] = ""
        else:
            st.error("Failed to reach HR Agent Orchestrator backend.")

    st.markdown("---")
    st.markdown("#### 💬 Conversation History")

    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"**👤 ({msg['user_role']}):** {msg['text']}")
        else:
            body = msg["data"]
            agent_name = body.get("agent", "orchestrator")
            st.markdown(f'<span class="badge badge-info">🤖 Routed to: {agent_name}</span>', unsafe_allow_html=True)
            
            if body.get("status") == "permission_denied":
                st.error(f"⛔ {body.get('error')}")
            elif "error" in body:
                st.warning(f"⚠️ {body.get('error')}")
            else:
                result = body.get("result", {})
                if isinstance(result, dict) and "answer" in result:
                    st.success(result["answer"])
                    if result.get("sources"):
                        st.caption("📄 Policy Sources: " + ", ".join(result["sources"]))
                else:
                    st.json(result)
            st.markdown("<br>", unsafe_allow_html=True)
