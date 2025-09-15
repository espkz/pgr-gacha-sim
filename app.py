import os, base64, json
from collections import defaultdict
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from utils import Gacha


# sidebar
banner_choice = st.sidebar.selectbox(
    "Select Banner",
    ["Themed Banner", "Fate Themed Banner", "Base Member Target", "CUB Target"]
)
banner_files = {
    "Themed Banner" : "standard_themed_banner",
    "Fate Themed Banner" : "fate_themed_banner",
    "Base Member Target" : "member_target_banner",
    "CUB Target" : "cub_target_banner"
}
with open(f'data/banners/{banner_files[banner_choice]}.json', "r", encoding="utf-8") as f:
    selected_banner = json.load(f)


# initialize
if "gacha" not in st.session_state or st.session_state.gacha_banner != banner_choice:
    st.session_state.gacha = Gacha(gacha_banner=banner_files[banner_choice])
    st.session_state.gacha_banner = banner_choice
    st.session_state.last_pull = []
    st.session_state.pulling = False

gacha = st.session_state.gacha

# complete pulls in one session
def do_pull(count):
    if not st.session_state.pulling:
        st.session_state.pulling = True
        st.session_state.last_pull = gacha._pull(count)
        st.session_state.pulling = False

# reset function
def reset_all():
    for key in ["gacha", "last_pull", "pulling"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# inline base64 for local image (so it always renders)

# standard BC
CURRENCY_IMG_PATH = "data/ui/bc.png"
def inline_img(path: str, width: int = 20) -> str:
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{b64}" width="{width}" style="vertical-align:middle; margin-bottom:2px;" />'
    return "🟣"

st.set_page_config(page_title="PGR Gacha Simulator", layout="wide")

# styling
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
.result-name { font-size: 1.1rem; font-weight: bold; }
.rarity-6 { color: #FF5349; }
.rarity-5 { color: gold; }
.rarity-4 { color: #E03FD8; }
.rarity-3 { color: blue; }

.spoils-wrap { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.spoils-col {
    background: #1f1f2e;
    border-radius: 12px;
    padding: 10px 12px;
    height: 300px;
    overflow-y: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.35);
}
.spoils-title { font-weight: 700; margin-bottom: 8px; }
.spoils-item { margin: 2px 0; }

.banner-card h2 {
    color: white;
    margin-bottom: 8px;
    font-size: 2rem;
}

.banner-card h3 {
    color: white;
    margin-bottom: 16px;
    font-size: 1.5rem;
}

.pull-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 16px;
}

div.stButton > button {
    font-size: 1.4rem;
    padding: 12px 24px;
    border-radius: 12px;
    background-color: #4A90E2;
    color: white;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
}
div.stButton > button:hover {
    background-color: #6AAFF6;
}
div.stButton > button {
    font-size: 1.6rem;
    padding: 14px 28px;
    border-radius: 16px;
    background-color: #4A90E2;
    color: white;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
div.stButton > button:hover {
    background-color: #6AAFF6;
    transform: scale(1.05);
}
div.stButton > button:active {
    transform: scale(0.97);
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.stForm div.stButton {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# banner
st.markdown(f"<h2 style=\"text-align: center\">{selected_banner['title']}</h2>", unsafe_allow_html=True)
# base banner UI
if selected_banner["title"] == "Member Target Banner":
    # currency used is blue ticket
    CURRENCY_IMG_PATH = "data/ui/blue_ticket.png"
    # set target type to unit
    gacha.change_target_type("unit")

    # make target list
    with open("data/category_rates/s_rank_omniframe.json", "r", encoding="utf-8") as f:
        s_rank_units = [u["name"] for u in json.load(f) if "base" in u["banner"]]
    with open("data/category_rates/a_b_rank_omniframe.json", "r", encoding="utf-8") as f:
        ab_units = json.load(f)
        a_rank_units = [u["name"] for u in ab_units if u.get("rank") == "A"]

    st.markdown("### Select Targets")

    selected_s = st.selectbox("S-Rank Target", ["Random"] + s_rank_units)
    selected_a = st.selectbox("A-Rank Target", ["Random"] + a_rank_units)

    gacha.change_target(6, "" if selected_s == "Random" else selected_s)
    gacha.change_target(5, "" if selected_a == "Random" else selected_a)

# CUB banner UI
elif selected_banner["title"] == "CUB Target Banner":
    # currency used is blue ticket
    CURRENCY_IMG_PATH = "data/ui/cub_ticket.png"
    # set target type to unit
    gacha.change_target_type("cub")

    # make target list
    with open("data/category_rates/cub.json", "r", encoding="utf-8") as f:
        cubs = json.load(f)
        s_rank_cubs = [u["name"] for u in cubs if u["rarity"] == 6]

    st.markdown("### Select Targets")

    selected_s = st.selectbox("S-Rank Target", s_rank_cubs)

    gacha.change_target(6, selected_s)

else: # for themed banner
    gacha.change_target_type("")
    st.markdown(f"<h3>{selected_banner['subtitle']}</h3>", unsafe_allow_html=True)
    st.image(selected_banner['img'])
    st.markdown(f"<h4>Global Start Date: {selected_banner['start_date']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4>Target {selected_banner['target']}: {selected_banner['target_name']}</h4>", unsafe_allow_html=True)

# rates
with st.expander("Show Gacha Rates", expanded=False):
    for category in selected_banner['rates']:
        st.markdown(f"- {category['name']}: {round(category['rate']*100,2)}%")

# pull button
with st.form("pull_form"):
    # create columns for spacing
    col1, col2, col3, col4, col5 = st.columns([1.75, 1, 2, 1, 1])

    # place buttons in columns
    with col2:
        pull_x1 = st.form_submit_button("Pull x1")
    with col4:
        pull_x10 = st.form_submit_button("Pull x10")

    # handle button clicks
    if pull_x1:
        do_pull(1)
    elif pull_x10:
        do_pull(10)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# display results
st.markdown("### Pull Results")
if st.session_state.last_pull:
    cols = st.columns(5)
    for idx, result in enumerate(st.session_state.last_pull):
        if not isinstance(result, dict) or "img" not in result:
            continue
        col = cols[idx % 5]
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

# pity counter
st.markdown(f"### Pity Counter: {gacha.pity_count}/{selected_banner['pity']}")
st.divider()

# sort spoils
by_rarity = defaultdict(lambda: defaultdict(int))
for s in gacha.spoils:
    r = s.get("rarity", 3)
    n = s.get("name", "Unknown")
    by_rarity[r][n] += 1

def render_group(title: str, pairs, default_class=""):
    items_html = ""
    if not pairs:
        items_html = "<div class='spoils-item'>—</div>"
    else:
        for name, rarity, count in pairs:
            # Find the path for this item
            img_path = next((s['img'] for s in gacha.spoils if s.get('name') == name), None)
            img_html = inline_img(img_path, width=30) if img_path else ""
            cls = f"rarity-{rarity}" if rarity else default_class
            items_html += (
                f"<div class='spoils-item' style='display:flex; align-items:center; gap:6px;'>"
                f"{img_html}"
                f"<span class='{cls}'>{name} x{count}</span>"
                f"</div>"
            )
    return f"""
    <div class="spoils-col">
        <div class="spoils-title">{title}</div>
        {items_html}
    </div>
    """

def collect_pairs(target_rarities):
    out = []
    for r in target_rarities:
        for name, cnt in by_rarity[r].items():
            out.append((name, r, cnt))
    out.sort(key=lambda x: (-x[2], x[0]))
    return out

s_rank  = collect_pairs([6])
a_b_rank = collect_pairs([5])
mats  = collect_pairs([4, 3])

# BC and spoils
cols = st.columns([1, 1, 1, 1])

with cols[0]:
    # total bc
    currency_img_html = inline_img(CURRENCY_IMG_PATH, width=40)
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-weight:700; font-size:1.8rem;">Total {currency_img_html}</span>
            <span style="font-weight:700; font-size:1.8rem;">{gacha.bc:,}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # pulls
    st.markdown(
        f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                <span style="font-weight:700; font-size:1.8rem;">Total Pulls</span>
                <span style="font-weight:700; font-size:1.8rem;">{gacha.pulls:,}</span>
            </div>
            """,
        unsafe_allow_html=True
    )

    # reset button
    with stylable_container(
            "red",
            css_styles="""
            div.stButton > button {
                background-color: #FF0000 !important;
                color: white;
                font-weight: 800;
                font-size: 1.8rem;
                border-radius: 15px;
            }
            div.stButton > button:hover {
                background-color: #FF5555 !important;
            }
            """
    ):
        reset = st.button("Reset")

    if reset:
        reset_all()

# spoils

with cols[1]:
    s_rank = collect_pairs([6])
    st.markdown(render_group("6★", s_rank), unsafe_allow_html=True)
with cols[2]:
    a_b_rank = collect_pairs([5])
    st.markdown(render_group("5★", a_b_rank), unsafe_allow_html=True)
with cols[3]:
    mats = collect_pairs([4, 3])
    st.markdown(render_group("4★", mats), unsafe_allow_html=True)
