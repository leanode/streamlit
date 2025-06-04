import streamlit as st
import pandas as pd
from openai import OpenAI
from openai import RateLimitError

# 🔐 Load OpenAI API key
# old code: openai.api_key = st.secrets["OPENAI_API_KEY"]
st.write("Sorry, this app is now on vacation.")
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# 📄 Load preloaded CSV
CSV_PATH = "data/sales_data_sample.csv"  # Update if needed
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    st.error(f"❌ Could not find file at {CSV_PATH}. Please upload it to your repo.")
    st.stop()

# 🧠 App Title and Instructions
st.title("🧠 AI-Powered Data Insights")
st.subheader("Analyze a Preloaded Dataset Using OpenAI")

st.markdown("""
Welcome! This app uses **OpenAI** to generate plain-English insights from a preloaded CSV dataset.

### 📋 How to Use:
1. **Review the dataset preview** below
2. **Click an example question** or ask your own
3. **Wait a few seconds** while OpenAI analyzes the data and returns insights

> The AI analyzes only the **first 1000 rows** to stay within processing limits.
""")

# 🧾 Show data preview
st.markdown("### 🧾 Data Preview")
st.dataframe(df.head())

# 💡 Example questions
example_questions = [
    "How many orders are there?",
    "When is the most recent order?",
    "What trends or patterns can you find?",
    "Which column seems to have the most variation?",
    "Summarize this dataset for me.",
]

with st.expander("💡 Click to use an example question"):
    selected_example = st.radio("Try an example:", example_questions)

# Use example or custom input
user_question = st.text_input("❓ Ask a question about the data:", value=selected_example or "")

if user_question:
    with st.spinner("🧠 Analyzing with OpenAI..."):

        preview_csv = df.head(1000).to_csv(index=False)

        prompt = f"""
You're a senior data analyst. Analyze the following table of data.

Your job is to:
1. Identify important patterns, correlations, or outliers
2. Summarize trends across columns (e.g., sales by region, top categories)
3. Point out missing values or data quality issues
4. Suggest actionable insights

Here are the first 1000 rows of the dataset (CSV format):

{preview_csv}

Question: {user_question}
Answer clearly and precisely using column names.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You're a helpful data analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            st.markdown("### 💡 Insight:")
            st.write(answer)

        except RateLimitError:
            st.error("🚫 OpenAI Rate Limit Exceeded. Please wait and try again.")
        except Exception as e:
            st.error(f"❌ OpenAI Error: {e}")
