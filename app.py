import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Google Photos Discovery Engine",
    page_icon="📸",
    layout="wide"
)

# -----------------------------
# Load research data
# -----------------------------
df = pd.read_csv("google_photos_discovery_research.csv")

# Core retrieval cases
core_failure_types = [
    "photo existed but was difficult to locate",
    "photo was not indexed or recognized correctly",
    "search did not understand the user's query"
]

core_df = df[
    df["failure_type"].isin(core_failure_types)
].copy()

# -----------------------------
# Header
# -----------------------------
st.title("📸 Google Photos Discovery Engine")

st.markdown(
    """
    **Exploring how users retrieve photos when they remember the memory,
    but not the exact searchable details.**
    """
)

st.divider()

# -----------------------------
# Research funnel
# -----------------------------
st.header("Research funnel")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Reviews analyzed",
        "1,027"
    )
    st.caption(
        "Google Photos reviews collected from Google Play"
    )

with col2:
    st.metric(
        "AI-identified retrieval cases",
        "58"
    )
    st.caption(
        "Reviews classified as retrieval-related"
    )

with col3:
    st.metric(
        "Potential core-retrieval cases",
        "27"
    )
    st.caption(
        "Cases involving search, indexing or locating"
    )

st.info(
    """
    **How to read this funnel:**  
    1,027 Google Photos reviews were collected → 58 were identified
    as retrieval-related → 27 were classified as potential
    core-retrieval failures.

    These are research-set counts, **not population-level prevalence estimates**.
    AI classifications are directional and require evidence validation.
    """
)

st.divider()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Explore the evidence")

scope_options = [
    "All AI-identified retrieval cases",
    "Potential core-retrieval cases only"
]

selected_scope = st.sidebar.radio(
    "Research scope",
    scope_options
)

if selected_scope == "Potential core-retrieval cases only":
    working_df = core_df.copy()
else:
    working_df = df.copy()

failure_options = ["All"] + sorted(
    working_df["failure_type"].dropna().unique().tolist()
)

selected_failure = st.sidebar.selectbox(
    "Where did retrieval break?",
    failure_options
)

memory_options = ["All"] + sorted(
    working_df["memory_type"].dropna().unique().tolist()
)

selected_memory = st.sidebar.selectbox(
    "What did the user remember?",
    memory_options
)

search_options = ["All"] + sorted(
    working_df["search_behavior"].dropna().unique().tolist()
)

selected_search = st.sidebar.selectbox(
    "How did the user search?",
    search_options
)

filtered_df = working_df.copy()

if selected_failure != "All":
    filtered_df = filtered_df[
        filtered_df["failure_type"] == selected_failure
    ]

if selected_memory != "All":
    filtered_df = filtered_df[
        filtered_df["memory_type"] == selected_memory
    ]

if selected_search != "All":
    filtered_df = filtered_df[
        filtered_df["search_behavior"] == selected_search
    ]

# -----------------------------
# Retrieval signals
# -----------------------------
st.header("Retrieval signals")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("What users remember")

    memory_counts = (
        working_df["memory_type"]
        .value_counts()
        .rename_axis("Memory")
        .reset_index(name="Cases")
    )

    st.bar_chart(
        memory_counts.set_index("Memory")
    )

with col2:
    st.subheader("How users search")

    search_counts = (
        working_df["search_behavior"]
        .value_counts()
        .rename_axis("Search behavior")
        .reset_index(name="Cases")
    )

    st.bar_chart(
        search_counts.set_index("Search behavior")
    )

with col3:
    st.subheader("Where retrieval breaks")

    failure_counts = (
        working_df["failure_type"]
        .value_counts()
        .rename_axis("Failure")
        .reset_index(name="Cases")
    )

    st.bar_chart(
        failure_counts.set_index("Failure")
    )

st.divider()

# -----------------------------
# Evidence
# -----------------------------
st.header("User evidence")

st.write(
    f"Showing **{len(filtered_df)}** of "
    f"**{len(working_df)}** cases in the selected research scope."
)

search_text = st.text_input(
    "Search the evidence",
    placeholder="Try: car engine, old photos, collection, date..."
)

if search_text:
    filtered_df = filtered_df[
        filtered_df["review"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

for _, row in filtered_df.iterrows():

    with st.expander(
        f"{row['failure_type']}  •  {row['memory_type']}"
    ):

        st.write(row["review"])

        st.caption(
            f"Search behavior: {row['search_behavior']}"
        )

        st.caption(
            f"AI category: {row['AI_category']} "
            f"| AI confidence: {row['AI_confidence']:.2f}"
        )

        st.caption(
            f"Failure classification confidence: "
            f"{row['failure_confidence']:.2f}"
        )

        st.caption(
            "Source: Google Play review"
        )

st.divider()

# -----------------------------
# Interpretation
# -----------------------------
st.header("How to interpret this engine")

st.markdown(
    """
    This engine is designed to surface **research signals**, not to
    estimate how common a problem is across all Google Photos users.

    The pipeline:

    **Collect reviews → identify retrieval-related cases → classify
    memory and search behavior → identify potential failure points →
    inspect underlying user evidence.**
    """
)

st.warning(
    """
    **Research caution:** AI classifications can contain false positives
    or ambiguous cases. Any product insight should be validated against
    the underlying user evidence.
    """
)
