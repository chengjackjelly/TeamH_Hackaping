import streamlit as st
import matplotlib.pyplot as plt  # This is what 'plt' refers to
import pandas as pd

# Default supply chain data (simplified from your schema)
DEFAULT_DATA = {
    "Stages": [
        "Raw Material Extraction",
        "Material Processing",
        "Component Manufacturing",
        "Final Assembly",
        "Packaging & Distribution"
    ],
    "Default Choice": [
        "Global mix (Rio Tinto, Glencore, Exxon)",
        "China-based processors",
        "TSMC (Taiwan), CATL (China), Samsung (Korea)",
        "Foxconn (China)",
        "Maersk shipping + local packaging"
    ],
    "Default Cost ($)": [25, 35, 300, 30, 15],
    "Default CO₂ (kg)": [60, 120, 250, 15, 30]
}

# Alternative options for each stage
ALTERNATIVES = {
    "Raw Material Extraction": {
        "Conflict-free minerals": {"Cost": 35, "CO₂": 55, "Suppliers": "Pact-certified (Rwanda, Canada)"},
        "Recycled materials": {"Cost": 40, "CO₂": 30, "Suppliers": "Redwood Materials (US)"}
    },
    "Material Processing": {
        "EU-based (renewable energy)": {"Cost": 50, "CO₂": 60, "Suppliers": "Hydro (Norway), Umicore (Belgium)"},
        "Localized processing": {"Cost": 45, "CO₂": 90, "Suppliers": "Regional smelters"}
    },
    "Component Manufacturing": {
        "US chips (Intel)": {"Cost": 400, "CO₂": 200, "Suppliers": "Intel (US), Tesla (batteries)"},
        "India-based": {"Cost": 280, "CO₂": 270, "Suppliers": "Tata Electronics, BYD India"}
    },
    "Final Assembly": {
        "Vietnam (renewables)": {"Cost": 35, "CO₂": 10, "Suppliers": "Luxshare (Vietnam)"},
        "Mexico (NAFTA)": {"Cost": 40, "CO₂": 18, "Suppliers": "Flex (Mexico)"}
    },
    "Packaging & Distribution": {
        "Carbon-neutral shipping": {"Cost": 25, "CO₂": 5, "Suppliers": "Maersk ECO Delivery"},
        "Air freight (urgent)": {"Cost": 50, "CO₂": 80, "Suppliers": "DHL Express"}
    }
}

# Initialize session state
if 'current_data' not in st.session_state:
    st.session_state.current_data = pd.DataFrame(DEFAULT_DATA)

def handle_disruption(stage, choice):
    """Update costs and CO₂ based on user selection"""
    df = st.session_state.current_data.copy()
    idx = df[df['Stages'] == stage].index[0]
    
    if choice != "Default":
        alt = ALTERNATIVES[stage][choice]
        df.at[idx, "Default Choice"] = alt["Suppliers"]
        df.at[idx, "Default Cost ($)"] = alt["Cost"]
        df.at[idx, "Default CO₂ (kg)"] = alt["CO₂"]
    
    st.session_state.current_data = df

# Streamlit UI
st.title("🌍 Laptop Supply Chain Simulator")
st.subheader("Simulate disruptions and see cost/CO₂ impact")

# 1. Display default configuration
st.header("Current Configuration")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Cost", f"${st.session_state.current_data['Default Cost ($)'].sum():.0f}")
with col2:
    st.metric("Total CO₂ Footprint", f"{st.session_state.current_data['Default CO₂ (kg)'].sum():.0f} kg")

st.dataframe(st.session_state.current_data, hide_index=True)

# 2. User input for disruptions
st.header("⚡ Simulate a Disruption")
stage = st.selectbox("Select supply chain stage:", DEFAULT_DATA["Stages"])
event = st.selectbox("Select disruption/alternative:", 
                    ["Default"] + list(ALTERNATIVES[stage].keys()))

if st.button("Apply Change"):
    handle_disruption(stage, event)
    st.rerun()

# 3. Comparison visualization
st.header("📊 Impact Analysis")
df = st.session_state.current_data

fig1, ax1 = plt.subplots()
ax1.bar(df['Stages'], df['Default Cost ($)'])
plt.xticks(rotation=45)
ax1.set_ylabel("Cost ($)")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.bar(df['Stages'], df['Default CO₂ (kg)'], color='orange')
plt.xticks(rotation=45)
ax2.set_ylabel("CO₂ (kg)")
st.pyplot(fig2)