import streamlit as st

# Page config
st.set_page_config(page_title="PGR Gacha Simulator", layout="wide")

# --- CSS styling ---
st.markdown("""
<style>
/* Pull result cards */
.result-card {
    background-color: #2d2d44;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    margin: 6px;
}
.result-name {
    font-size: 1.1rem;
    font-weight: bold;
}
.rarity-6 { color: gold; }
.rarity-5 { color: plum; }
.rarity-4 { color: lightgray; }
</style>
""", unsafe_allow_html=True)

# --- Banner Section ---
st.markdown("## 🎴 Themed Banner")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Debut Unit: **Bianca: Crepuscule**")
    st.write("_Limited-time rate-up banner!_")

with col2:
    st.image("https://via.placeholder.com/200", caption="Bianca: Crepuscule", use_container_width=True)

st.divider()

# --- Pull Buttons ---
st.markdown("### ✨ Perform Pulls")

col3, col4 = st.columns([1, 1])
with col3:
    if st.button("Pull x1", use_container_width=True):
        st.session_state.last_pull = [
            {"name": "Placeholder Construct", "rarity": 6}
        ]

with col4:
    if st.button("Pull x10", use_container_width=True):
        st.session_state.last_pull = [
            {"name": f"Result {i+1}", "rarity": (6 if i==0 else 4)} for i in range(10)
        ]

st.divider()

# --- Pull Results ---
st.markdown("### 🎁 Pull Results")
if "last_pull" in st.session_state:
    cols = st.columns(5)  # grid layout
    for idx, result in enumerate(st.session_state.last_pull):
        col = cols[idx % 5]
        rarity_class = f"rarity-{result['rarity']}"
        col.markdown(
            f"""
            <div class="result-card">
                <div class="result-name {rarity_class}">{result['name']}</div>
                <div>{result['rarity']}★</div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.write("No pulls yet.")

st.divider()

# --- Totals ---
st.markdown("### 📊 Totals")
if "bc_spent" not in st.session_state:
    st.session_state.bc_spent = 0
if "spoils" not in st.session_state:
    st.session_state.spoils = 0

col5, col6 = st.columns(2)
col5.metric("Total BC Spent", f"{st.session_state.bc_spent:,}")
col6.metric("Total Spoils", f"{st.session_state.spoils:,}")