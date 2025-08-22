import streamlit as st
import requests
import os

st.set_page_config(page_title="HR Resource Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 HR Resource Query Chatbot — Advanced")
st.caption("Semantic retrieval (FAISS) + Local LLM (Ollama). Falls back to lexical if unavailable.")

api_url = st.text_input("Backend URL", value=os.environ.get("HR_API_URL", "http://127.0.0.1:8000"))

with st.form("chat_form"):
    query = st.text_area("Your request", height=120, placeholder="e.g., Find Python developers with 3+ years for a healthcare project, available immediately in Bengaluru")
    submitted = st.form_submit_button("Search")
    if submitted:
        try:
            resp = requests.post(f"{api_url}/chat", json={"query": query}, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                st.markdown(data["answer"])
                recs = data.get("recommendations", [])
                if recs:
                    st.subheader("Top Matches")
                    for r in recs:
                        with st.container(border=True):
                            st.markdown(f"**{r['name']}** — {r['title']} ({r['experience_years']} yrs)")
                            st.write(f"Skills: {', '.join(r['skills'])}")
                            st.write(f"Projects: {', '.join(r['projects'])}")
                            st.write(f"Domains: {', '.join(r['domains'])}")
                            st.write(f"Location: {r['location']} | Availability: {r['availability']}")
                else:
                    st.info("No matches found. Try adding specific skills or a domain.")
            else:
                st.error(f"API error: {resp.status_code} — {resp.text}")
        except Exception as e:
            st.exception(e)

st.divider()
st.subheader("Advanced Filters (direct API call)")
col1, col2, col3 = st.columns(3)
with col1:
    skills = st.text_input("Skills (comma separated)", value="Python,AWS")
with col2:
    min_exp = st.number_input("Min experience (years)", min_value=0, max_value=30, value=3, step=1)
with col3:
    availability = st.selectbox("Availability", ["", "available", "busy"])

col4, col5, col6 = st.columns(3)
with col4:
    project = st.text_input("Project keyword", value="")
with col5:
    domain = st.text_input("Domain (e.g., healthcare, fintech, saas)", value="")
with col6:
    location = st.text_input("Location (e.g., Bengaluru, Remote)", value="")

if st.button("Run Filtered Search"):
    params = {}
    if skills.strip():
        params["skills"] = [s.strip() for s in skills.split(",") if s.strip()]
    if min_exp:
        params["min_experience"] = int(min_exp)
    if availability:
        params["availability"] = availability
    if project:
        params["project"] = project
    if domain:
        params["domain"] = domain
    if location:
        params["location"] = location

    try:
        resp = requests.get(f"{api_url}/employees/search", params=params, timeout=30)
        if resp.status_code == 200:
            rows = resp.json()
            st.write(f"Found {len(rows)} employees")
            for r in rows:
                with st.container(border=True):
                    st.markdown(f"**{r['name']}** — {r['title']} ({r['experience_years']} yrs)")
                    st.write(f"Skills: {', '.join(r['skills'])}")
                    st.write(f"Projects: {', '.join(r['projects'])}")
                    st.write(f"Domains: {', '.join(r['domains'])}")
                    st.write(f"Location: {r['location']} | Availability: {r['availability']}")
        else:
            st.error(f"API error: {resp.status_code} — {resp.text}")
    except Exception as e:
        st.exception(e)