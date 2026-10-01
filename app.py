import hashlib
import json
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TruePresence | Anti-Ghost School Integrity Engine",
    page_icon="🏫",
    layout="wide",
)

# Mock Data
INITIAL_SCHOOLS = [
    {
        "id": "KHP-0104",
        "name": "GBPS Mir Ali Murad Khan",
        "taluka": "Kot Diji",
        "reported_students": 145,
        "food_rations_consumed": 22,
        "cellular_sim_density": 8,
        "allocated_budget_pkr": 1_850_000,
    },
    {
        "id": "KHP-0209",
        "name": "GGPS Gambat Main",
        "taluka": "Gambat",
        "reported_students": 180,
        "food_rations_consumed": 172,
        "cellular_sim_density": 165,
        "allocated_budget_pkr": 2_400_000,
    },
    {
        "id": "KHP-0312",
        "name": "GBPS Piryaloi Rural",
        "taluka": "Kingri",
        "reported_students": 95,
        "food_rations_consumed": 14,
        "cellular_sim_density": 5,
        "allocated_budget_pkr": 1_200_000,
    },
]

if "schools" not in st.session_state:
  st.session_state.schools = INITIAL_SCHOOLS

if "audit_logs" not in st.session_state:
  st.session_state.audit_logs = []


def calculate_anomaly_score(reported: int, food: int, sims: int) -> dict:
  score = 100
  expected_food = reported * 0.85
  if food < expected_food * 0.35:
    score -= 40
  if sims < reported * 0.20:
    score -= 30
  verdict = (
      "Operational"
      if score >= 70
      else "Audit Needed"
      if score >= 45
      else "Ghost School"
  )
  return {"score": score, "verdict": verdict}


st.title("🏫 TruePresence: Anti-Ghost School Verification System")
st.caption(
    "Sukkur IBA IET TechFest Hackathon 2026 | Focus Area: Rural Khairpur"
)

role = st.sidebar.radio(
    "Select Operating Perspective:",
    [
        "1. Field Inspector App (Mobile Simulator)",
        "2. District Command & Anomaly Dashboard",
        "3. Cluster Budget Protection Rebalancer",
    ],
)

# 1. Field Inspector View
if role == "1. Field Inspector App (Mobile Simulator)":
  st.subheader("📱 Field Inspector Mobile Terminal")
  st.info("Direct Logistics & Blind Dispatch Mode[cite: 1].")

  col1, col2 = st.columns(2)
  with col1:
    st.markdown("### 🔒 Step 1: Blind Route Dispatch")
    arrived = st.checkbox("Simulate GPS Arrival (< 500m from site)")
    if arrived:
      st.success("📍 GPS Verified: Inside Geofence")
      st.markdown("**Target Unlocked:** `GBPS Mir Ali Murad Khan (Kot Diji)`")
      st.metric(
          label="Direct Daily TA/DA Fuel Allowance",
          value="PKR 2,500 via Mobile Wallet",
      )
    else:
      st.warning("🔒 Target details are encrypted until arrival.")

  with col2:
    st.markdown("### 📸 Step 2: Unannounced Field Verification")
    if arrived:
      observed_students = st.number_input(
          "Actual Headcount in Classrooms:", min_value=0, max_value=300, value=6
      )
      teacher_present = st.radio(
          "Is Appointed Teacher Present?", ["No", "Yes", "Proxy Relative"]
      )
      if st.button("Submit Cryptographic Inspection Receipt"):
        payload = {
            "school_id": "KHP-0104",
            "count": observed_students,
            "teacher": teacher_present,
            "time": datetime.now().isoformat(),
        }
        receipt_hash = hashlib.sha256(
            json.dumps(payload).encode()
        ).hexdigest()[:16]
        st.session_state.audit_logs.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "School ID": "KHP-0104",
            "Observed": observed_students,
            "Hash": receipt_hash,
        })
        st.success(f"Audit recorded! Tamper-proof Hash: `{receipt_hash}`")
    else:
      st.write("Complete Step 1 to unlock inspection form.")

# 2. District Dashboard View
elif role == "2. District Command & Anomaly Dashboard":
  st.subheader("📊 District Education Office - Anomaly Matrix")
  df = pd.DataFrame(st.session_state.schools)
  scores, verdicts = [], []
  for _, row in df.iterrows():
    res = calculate_anomaly_score(
        row["reported_students"],
        row["food_rations_consumed"],
        row["cellular_sim_density"],
    )
    scores.append(res["score"])
    verdicts.append(res["verdict"])
  df["Integrity Score"] = scores
  df["Auto Detection"] = verdicts

  m1, m2, m3 = st.columns(3)
  m1.metric("Total District Enrollment", f"{df['reported_students'].sum():,}")
  m2.metric(
      "Ghost / Flagged Facilities", len(df[df["Auto Detection"] != "Operational"])
  )
  m3.metric(
      "District Budget Tracked",
      f"PKR {df['allocated_budget_pkr'].sum() / 1_000_000:.2f} M",
  )

  st.dataframe(df, use_container_width=True)
  st.markdown("### 📡 Real-Time Audit Sync Feed")
  if st.session_state.audit_logs:
    st.table(pd.DataFrame(st.session_state.audit_logs))
  else:
    st.caption("No audits submitted yet today.")

# 3. Cluster Budget View
elif role == "3. Cluster Budget Protection Rebalancer":
  st.subheader("🛡️ Cluster Safe-Harbor Funding Rebalance")
  st.markdown(
      "Ghost school budget local Union Council me lock rehta hai aur bacho ki"
      " transport aur honest schools ko shift hota hai[cite: 1]."
  )

  col1, col2 = st.columns(2)
  with col1:
    st.markdown("#### 🚨 Detected Ghost School: GBPS Mir Ali Murad Khan")
    st.write(
        "**Location:** Kot Diji rural belt[cite: 1]  \n**Allocated Salary"
        " & Upkeep:** PKR 1,850,000  \n**Real Attendance:** 6 students"
    )
    reallocate = st.button("Trigger Cluster Funding Protection Order")

  with col2:
    st.markdowngg 🔄 Reallocation Formula")
    if reallocate:
      st.success("District Budget Retained at PKR 1.85M!")
      st.markdown("""
            * 🚐 **PKR 750,000:** Student transport van/rickshaw stipends[cite: 1].
            * 📚 **PKR 650,000:** Neighboring functional school upgrades[cite: 1].
            * 🏗️ **PKR 450,000:** Local infrastructure maintenance fund.
            """)
      st.metric(
          "Net Loss to Honest Schools",
          "PKR 0",
          help="Honest schools keep full funding under cluster safe harbor[cite: 1].",
      )
    else:
      st.info("Click the button to simulate reallocation.")