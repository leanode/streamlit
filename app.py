import streamlit as st
import openai
from google.cloud import bigquery
import pandas as pd

# -- Setup --
st.title("🧠 Ask Public Data (AI + BigQuery)")
st.write("Type a natural language question. I’ll turn it into SQL and run it on public datasets.")

# -- User Input --
user_question = st.text_input("🔍 Ask a question (e.g. What are the top 10 complaint types in Austin 311?):")

if user_question:
    # -- Step 1: Convert to SQL using OpenAI --
    with st.spinner("Asking OpenAI to write SQL..."):
        prompt = f"""
        Write a BigQuery Standard SQL query that answers the question:
        "{user_question}"
        Only use public datasets in the bigquery-public-data project.
        Return only the SQL, no explanations.
        """

        openai.api_key = st.secrets["OPENAI_API_KEY"]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        sql = response['choices'][0]['message']['content'].strip("` ")
        st.code(sql, language="sql")

    # -- Step 2: Query BigQuery --
    with st.spinner("Running query on BigQuery..."):
        client = bigquery.Client()
        try:
            df = client.query(sql).to_dataframe()
            st.success("✅ Query succeeded!")
            st.dataframe(df)

            # -- Optional Chart --
            if len(df.columns) >= 2:
                st.bar_chart(df.set_index(df.columns[0]))
        except Exception as e:
            st.error(f"BigQuery error: {e}")
