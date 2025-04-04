import streamlit as st
import matplotlib.pyplot as plt  # This is what 'plt' refers to
import pandas as pd

# Default supply chain data (simplified from your schema)
DEFAULT_DATA = {
    "Stages": [
        "Raw Material Extraction",
        "Component Manufacturing",
        "Final Assembly",
    ],
    "Default Choice": [
        "Global mix (Rio Tinto, Glencore, Exxon)",
        "TSMC (Taiwan), CATL (China), Samsung (Korea)",
        "Foxconn (China)",
    ],
    "Default Cost ($)": [
        25,
        35,
        300,
    ],
    "Default CO₂ (kg)": [
        60,
        120,
        250,
    ],
    "New Cost ($)": [
        25,
        35,
        300,
    ],
    "New CO₂ (kg)": [
        60,
        120,
        250,
    ],
}

# Alternative options for each stage
ALTERNATIVES = {
    "Raw Material Extraction": {
        "Conflict-free minerals": {
            "Cost": 35,
            "CO₂": 55,
            "Suppliers": "Pact-certified (Rwanda, Canada)",
        },
        "Recycled materials": {
            "Cost": 40,
            "CO₂": 30,
            "Suppliers": "Redwood Materials (US)",
        },
    },
    "Component Manufacturing": {
        "US chips (Intel)": {
            "Cost": 400,
            "CO₂": 200,
            "Suppliers": "Intel (US), Tesla (batteries)",
        },
        "India-based": {
            "Cost": 280,
            "CO₂": 270,
            "Suppliers": "Tata Electronics, BYD India",
        },
    },
    "Final Assembly": {
        "Vietnam (renewables)": {
            "Cost": 35,
            "CO₂": 10,
            "Suppliers": "Luxshare (Vietnam)",
        },
        "Mexico (NAFTA)": {"Cost": 40, "CO₂": 18, "Suppliers": "Flex (Mexico)"},
    },
}

# Initialize session state
if "current_data" not in st.session_state:
    st.session_state.current_data = pd.DataFrame(DEFAULT_DATA)


def handle_disruption(stage, choice):
    """Update costs and CO₂ in new columns while preserving original values"""
    df = st.session_state.current_data.copy()
    idx = df[df["Stages"] == stage].index[0]

    # Initialize new columns if they don't exist
    if "New Choice" not in df.columns:
        df["New Choice"] = df["Default Choice"]
        df["New Cost ($)"] = df["Default Cost ($)"]
        df["New CO₂ (kg)"] = df["Default CO₂ (kg)"]

    if choice == "Default":
        # Revert to default values
        df.at[idx, "New Choice"] = df.at[idx, "Default Choice"]
        df.at[idx, "New Cost ($)"] = df.at[idx, "Default Cost ($)"]
        df.at[idx, "New CO₂ (kg)"] = df.at[idx, "Default CO₂ (kg)"]
    else:
        # Apply alternative values
        alt = ALTERNATIVES[stage][choice]
        df.at[idx, "New Choice"] = alt["Suppliers"]
        df.at[idx, "New Cost ($)"] = alt["Cost"]
        df.at[idx, "New CO₂ (kg)"] = alt["CO₂"]

    st.session_state.current_data = df


# Streamlit UI
st.title("🌍 Laptop Supply Chain Simulator")
st.subheader("Simulate disruptions and see cost/CO₂ impact")

# 1. Display default configuration
st.header("Current Configuration")
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Total Cost", f"${st.session_state.current_data['Default Cost ($)'].sum():.0f}"
    )
with col2:
    st.metric(
        "Total CO₂ Footprint",
        f"{st.session_state.current_data['Default CO₂ (kg)'].sum():.0f} kg",
    )

st.dataframe(st.session_state.current_data, hide_index=True)

# 2. User input for disruptions
st.header("⚡ Simulate Event")
event = st.text_input(
    "event",
    value="",
    max_chars=None,
    key=None,
    type="default",
    help=None,
    autocomplete=None,
    on_change=None,
    args=None,
    kwargs=None,
    placeholder=None,
    disabled=False,
    label_visibility="visible",
)

if st.button("Apply Event"):
    handle_disruption(event)
    st.rerun()

# 3. Comparison visualization (updated)
st.header("📊 Impact Comparison")

if "previous_data" not in st.session_state:
    st.session_state.previous_data = st.session_state.current_data.copy()

# Calculate deltas
delta_cost = (
    st.session_state.current_data["New Cost ($)"].sum()
    - st.session_state.current_data["Default Cost ($)"].sum()
)
delta_co2 = (
    st.session_state.current_data["New CO₂ (kg)"].sum()
    - st.session_state.current_data["Default CO₂ (kg)"].sum()
)
# Display delta metricsi
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Total Cost Change",
        f"${st.session_state.current_data['Default Cost ($)'].sum():.0f}",
        delta=f"{delta_cost:.0f} $",
    )
with col2:
    st.metric(
        "Total CO₂ Change",
        f"{st.session_state.current_data['Default CO₂ (kg)'].sum():.0f} kg",
        delta=f"{delta_co2:.0f} kg",
    )

# Side-by-side bar plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Cost comparison
width = 0.35
x = range(len(st.session_state.current_data))
ax1.bar(
    x,
    st.session_state.current_data["Default Cost ($)"],
    width,
    label="Default",
    color="blue",
)
ax1.bar(
    [p + width for p in x],
    st.session_state.current_data["New Cost ($)"],
    width,
    label="After Event",
    color="orange",
)
ax1.set_xticks([p + width / 2 for p in x])
ax1.set_xticklabels(st.session_state.current_data["Stages"], rotation=45)
ax1.set_ylabel("Cost ($)")
ax1.set_title("Cost Comparison")
ax1.legend()

# CO2 comparison
ax2.bar(
    x,
    st.session_state.current_data["Default CO₂ (kg)"],
    width,
    label="Default",
    color="green",
)
ax2.bar(
    [p + width for p in x],
    st.session_state.current_data["New CO₂ (kg)"],
    width,
    label="After Event",
    color="red",
)
ax2.set_xticks([p + width / 2 for p in x])
ax2.set_xticklabels(st.session_state.current_data["Stages"], rotation=45)
ax2.set_ylabel("CO₂ (kg)")
ax2.set_title("CO₂ Footprint Comparison")
ax2.legend()

plt.tight_layout()
st.pyplot(fig)

# Update previous data (for next change)
st.session_state.previous_data = st.session_state.current_data.copy()
