import streamlit as st
from utils import Gacha

# initialize
if "gacha" not in st.session_state:
    st.session_state.gacha = Gacha()
if "last_pull" not in st.session_state:
    st.session_state.last_pull = []
if "pulling" not in st.session_state:
    st.session_state.pulling = False

gacha = st.session_state.gacha

def do_pull(count):
    if not st.session_state.pulling:
        st.session_state.pulling = True
        st.session_state.last_pull = gacha._pull(count)
        st.session_state.pulling = False

st.set_page_config(page_title="PGR Gacha Simulator", layout="wide")

st.markdown("""
<style>
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
.rarity-6 { color: #FF5349; }
.rarity-5 { color: gold; }
.rarity-4 { color: #E03FD8; }
.rarity-3 { color: blue; }
</style>
""", unsafe_allow_html=True)


st.markdown("## 🎴 Themed Banner")
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Debut Unit: **Bianca: Crepuscule**")
with col2:
    st.image("data/category_img/s_rank_omniframe/crepuscule.png", caption="Bianca: Crepuscule", width=150)

st.divider()

# buttons
with st.form("pull_form"):
    col3, col4 = st.columns([1,1])
    pull_x1 = col3.form_submit_button("Pull x1")
    pull_x10 = col4.form_submit_button("Pull x10")

    if pull_x1:
        st.session_state.last_pull = gacha._pull(1)
    elif pull_x10:
        st.session_state.last_pull = gacha._pull(10)

st.divider()

st.markdown("### Pull Results")

if st.session_state.last_pull:
    cols = st.columns(5)
    for idx, result in enumerate(st.session_state.last_pull):
        # check for if it accidentally skipped (it shouldn't but still)
        if not isinstance(result, dict) or "img" not in result:
            continue

        col = cols[idx % 5]

        # display
        col.image(result["img"], width=150)
        rarity_class = f"rarity-{result.get('rarity', 4)}"
        col.markdown(
            f"""
            <div class="result-name {rarity_class}">
                {result.get('name', 'Unknown')}
            </div>
            <div>{result.get('rarity', '?')}★</div>
            """,
            unsafe_allow_html=True
        )
else:
    st.write("No pulls yet.")


st.divider()

st.markdown("### Totals")
col5, col6, col7 = st.columns(3)
col5.metric("Total BC Spent", f"{gacha.bc:,}")
col6.metric("Total Spoils", f"{len(gacha.spoils):,}")
col7.metric("Pity Counter", f"{gacha.pity}/60")

if st.button("Reset"):
    for key in ["gacha", "last_pull", "bc_spent", "spoils", "pulling"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()