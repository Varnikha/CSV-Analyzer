import streamlit as st
import pandas as pd

# ---- Page setup ----
st.set_page_config(page_title="Insightly", page_icon="🔎", layout="wide")

# ---- Custom CSS for a modern SaaS landing-page look ----
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: "Segoe UI", "Helvetica Neue", sans-serif; }

    /* Hero header banner */
    .app-header {
        background-color: #0b1e3d;
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
    }
    .app-header h1 {
        color: #ffffff;
        font-size: 2.1rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .app-header p {
        color: #b8c4d9;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }

    /* Metric cards -> rounded white cards with shadow */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: none;
        border-radius: 14px;
        padding: 1.2rem 1.2rem 0.8rem 1.2rem;
        box-shadow: 0 4px 14px rgba(11,30,61,0.08);
    }
    div[data-testid="stMetric"] label {
        color: #6b7688 !important;
        font-weight: 600;
    }

    /* Buttons -> bold, rounded, blue accent */
    button[kind="primary"], .stDownloadButton button {
        background-color: #2f6fed !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    /* Tabs -> bolder, more spaced out */
    button[data-baseweb="tab"] {
        font-weight: 700;
        font-size: 0.95rem;
    }

    /* Section headers */
    h2, h3 { color: #0b1e3d; font-weight: 700; }

    /* Dataframe container -> rounded card */
    div[data-testid="stDataFrame"] {
        border: none;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(11,30,61,0.06);
        overflow: hidden;
    }

    /* File uploader -> rounded card */
    section[data-testid="stFileUploaderDropzone"] {
        border-radius: 12px;
        border: 2px dashed #c7d2e3;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <h1>🔎 Insightly</h1>
    <p>Upload any CSV to explore metrics, statistics, groupings, and data quality — instantly.</p>
</div>
""", unsafe_allow_html=True)

# ---- Cache the CSV loading so it doesn't re-read the file on every interaction ----
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

# ---- Step 1: File uploader ----
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Only proceed if a file has been uploaded
if uploaded_file is not None:
    df = load_csv(uploaded_file)

    st.success(f"File uploaded successfully: {uploaded_file.name}")

    # ---- Auto-detect column types ----
    all_numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()
    numeric_cols = [c for c in all_numeric_cols if "id" not in c.lower()]

    # ---- Create tabs ----
    tab_home, tab_stats, tab_group, tab_missing = st.tabs(
        ["🏠 Home & Search", "📊 Summary Stats", "🔄 Group & Analyze", "⚠️ Missing Data"]
    )

    # =========================================================
    # TAB 1: HOME & SEARCH
    # =========================================================
    with tab_home:
        st.subheader("Key Metrics")
        st.write("Choose which columns to feature:")
        pick1, pick2 = st.columns(2)
        with pick1:
            chosen_text_col = st.selectbox(
                "Category column for 'Most Common' card:", text_cols
            ) if text_cols else None
        with pick2:
            chosen_num_col = st.selectbox(
                "Numeric column for 'Average' card:", numeric_cols
            ) if numeric_cols else None

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Rows", df.shape[0])

        if chosen_text_col:
            modes = df[chosen_text_col].mode()
            top_value = modes.iloc[0] if not modes.empty else "N/A"
            m2.metric(f"Most Common {chosen_text_col}", str(top_value))
        else:
            m2.metric("Most Common Category", "N/A")

        if chosen_num_col:
            avg_value = df[chosen_num_col].mean()
            m3.metric(f"Average {chosen_num_col}", f"{avg_value:.2f}")
        else:
            m3.metric("Average Value", "N/A")

        st.divider()

        # Global Search Filter
        st.subheader("🔍 Search & Filter Data")
        search_query = st.text_input("Type anything to filter the table rows:")

        filtered_df = df.copy()
        if search_query:
            filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)]
            st.write(f"Showing {filtered_df.shape[0]} matching rows out of {df.shape[0]}.")

        st.dataframe(filtered_df.head(100))

        # Download Filtered/Cleaned Data
        st.subheader("📥 Export Data")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download current view as CSV",
            data=csv_data,
            file_name=f"analyzed_{uploaded_file.name}",
            mime="text/csv",
        )

        st.divider()
        st.subheader("Dataset Properties")
        col1, col2 = st.columns(2)
        col1.write("**Numeric columns detected:**")
        col1.write(numeric_cols if numeric_cols else "None")
        col2.write("**Text/category columns detected:**")
        col2.write(text_cols if text_cols else "None")

    # =========================================================
    # TAB 2: SUMMARY STATS
    # =========================================================
    with tab_stats:
        st.subheader("Summary Statistics (numeric columns)")
        if numeric_cols:
            st.dataframe(df[numeric_cols].describe())
        else:
            st.info("No numeric columns found in this file.")

    # =========================================================
    # TAB 3: GROUP & ANALYZE
    # =========================================================
    with tab_group:
        st.subheader("Group & Analyze")
        if text_cols:
            g1, g2, g3 = st.columns(3)
            with g1:
                group_col = st.selectbox("Group by column:", text_cols, key="group_col")
            with g2:
                agg_options = ["Count rows"] + [f"Average {c}" for c in numeric_cols] + [f"Sum {c}" for c in numeric_cols]
                agg_choice = st.selectbox("Show:", agg_options, key="agg_choice")
            with g3:
                chart_type = st.selectbox("Chart Type:", ["Bar Chart", "Line Chart", "Area Chart"])

            if agg_choice == "Count rows":
                result = df[group_col].value_counts().head(15).reset_index()
                result.columns = [group_col, "Count"]
                result = result.set_index(group_col)
                main_col = "Count"
            elif agg_choice.startswith("Average"):
                num_col = agg_choice.replace("Average ", "")
                grouped = df.groupby(group_col)[num_col]
                avg_result = grouped.mean().rename(agg_choice)
                count_result = grouped.count().rename("Records Used")
                result = pd.concat([avg_result, count_result], axis=1).sort_values(agg_choice, ascending=False).head(15)
                main_col = agg_choice
            else:
                num_col = agg_choice.replace("Sum ", "")
                grouped = df.groupby(group_col)[num_col]
                sum_result = grouped.sum().rename(agg_choice)
                count_result = grouped.count().rename("Records Used")
                result = pd.concat([sum_result, count_result], axis=1).sort_values(agg_choice, ascending=False).head(15)
                main_col = agg_choice

            st.write(f"📊 Top 15 groups — {agg_choice} by {group_col}")
            if "Records Used" in result.columns:
                st.caption(
                    "'Records Used' shows how many non-missing values contributed to each group's number — "
                    "a low count means that result is less reliable."
                )
            st.dataframe(result)

            chart_data = result[main_col]
            if chart_type == "Bar Chart":
                st.bar_chart(chart_data)
            elif chart_type == "Line Chart":
                st.line_chart(chart_data)
            elif chart_type == "Area Chart":
                st.area_chart(chart_data)
        else:
            st.info("No text/category columns available to group by.")

    # =========================================================
    # TAB 4: MISSING DATA
    # =========================================================
    with tab_missing:
        st.subheader("Missing Values per Column")
        missing_data = df.isnull().sum().rename("Missing Count")
        st.dataframe(missing_data)

        if missing_data.sum() > 0:
            st.warning("Your dataset contains missing values. Use the table above to spot which columns need cleaning.")
        else:
            st.success("Great news! Your dataset has zero missing values.")

else:
    st.info("Please upload a CSV file to get started.")