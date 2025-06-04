import streamlit as st
import pandas as pd
from openai import OpenAI
from openai import RateLimitError

# 🔐 Load OpenAI API key
# old code: openai.api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# 📄 Load preloaded CSV
CSV_PATH = "data/sales_data_superstore.csv"  # Update if needed
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

> The AI analyzes only the **first 100 rows** to stay within processing limits.
""")

# 🧾 Show data preview
st.markdown("### 🧾 Data Preview")
st.dataframe(df.head())

# 💡 Example questions
example_questions = [
    "What are the most frequent values in each column?",
    "Are there any missing values or unusual data points?",
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

        preview_csv = df.head(20).to_csv(index=False)

        prompt = f"""
You are a helpful data analyst. Analyze the following data:

{preview_csv}

Question: {user_question}
Answer in clear, plain English. Use column names where relevant.
"""

        try:
            response = client.chat.completions.create(
                model="GPT-4o Mini",
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
