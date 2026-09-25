import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Google Photos Discovery Engine",
    page_icon="📸",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("google_photos_discovery_research.csv")

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📸 Google Photos Discovery Engine")

st.markdown(
    """
    **Exploring how users retrieve photos when they remember the memory,
    but not the exact searchable details.**
    """
)

st.divider()

# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Reviews analyzed",
        "1,027"
    )

with col2:
    st.metric(
        "Potential retrieval cases",
        "58"
    )

with col3:
    st.metric(
        "Potential core-retrieval cases",
        "27"
    )

st.caption(
    "These figures come from an automated research pipeline using Google Play reviews. "
    "AI classifications are directional signals and are not population-level prevalence estimates."
)

st.divider()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Explore the evidence")

failure_options = [
    "All",
    "photo existed but was difficult to locate",
    "photo was not indexed or recognized correctly",
    "search did not understand the user's query",
    "photo was missing, deleted or not backed up",
    "access, permission or account problem"
]

selected_failure = st.sidebar.selectbox(
    "Where did retrieval break?",
    failure_options
)

memory_options = ["All"] + sorted(
    df["memory_type"].dropna().unique().tolist()
)

selected_memory = st.sidebar.selectbox(
    "What did the user remember?",
    memory_options
)

search_options = ["All"] + sorted(
    df["search_behavior"].dropna().unique().tolist()
)

selected_search = st.sidebar.selectbox(
    "How did the user search?",
    search_options
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

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

# --------------------------------------------------
# RETRIEVAL SIGNALS
# --------------------------------------------------

st.header("Retrieval signals")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("What users remember")

    memory_counts = (
        df["memory_type"]
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
        df["search_behavior"]
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
        df["failure_type"]
        .value_counts()
        .rename_axis("Failure")
        .reset_index(name="Cases")
    )

    st.bar_chart(
        failure_counts.set_index("Failure")
    )

st.divider()

# --------------------------------------------------
# EVIDENCE
# --------------------------------------------------

st.header("User evidence")

st.write(
    f"Showing **{len(filtered_df)}** of **{len(df)}** AI-identified cases."
)

search_text = st.text_input(
    "Search the evidence",
    placeholder="Try: car engine, old photos, collection, date..."
)

if search_text:
    filtered_df = filtered_df[
        filtered_df["review"]
        .str.contains(search_text, case=False, na=False)
    ]

# --------------------------------------------------
# DISPLAY REVIEWS
# --------------------------------------------------

for _, row in filtered_df.iterrows():

    with st.expander(
        f"{row['failure_type']}  •  "
        f"{row['memory_type']}"
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
            "Source: Google Play review"
        )

st.divider()

# --------------------------------------------------
# RESEARCH NOTE
# --------------------------------------------------

st.header("How to interpret this engine")

st.info(
    """
    This is a discovery tool, not a population-level survey.

    The pipeline automatically collected Google Photos reviews, screened
    them for retrieval-related discussions, and classified potential
    patterns using an AI model.

    The resulting patterns should be treated as research signals and
    validated against the underlying user evidence.
    """
)
