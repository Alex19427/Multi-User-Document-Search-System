import streamlit as st
import os
import re
from PyPDF2 import PdfReader

USER_DOCUMENTS = {
    "alice@email.com": ["company_a.pdf"],
    "bob@email.com": ["company_b.pdf", "company_c.pdf"],
    "charlie@email.com": ["company_d.pdf", "company_e.pdf"],
}

def load_documents(user_email):
    docs = USER_DOCUMENTS.get(user_email, [])
    document_texts = {}
    for doc in docs:
        if os.path.exists(doc):
            reader = PdfReader(doc)
            text = "".join(page.extract_text() for page in reader.pages)
            # cleaning the data
            text = re.sub('\n', '', text)
            text = text.encode('ascii', errors='ignore').strip().decode('ascii')
            document_texts[doc] = text
    return document_texts

def search_documents(query, documents):
    results = []
    for doc_name, text in documents.items():
        if query.lower() in text.lower():
            excerpt_start = max(0, text.lower().find(query.lower()) - 50)
            excerpt_end = excerpt_start + 300
            results.append(f"From {doc_name}:\n{text[excerpt_start:excerpt_end]}...\n")
    return results

# Streamlit UI

if "email" not in st.session_state:
    st.session_state.email = ""
if "query" not in st.session_state:
    st.session_state.query = ""

def clear_input():
    """Clears the text input field."""
    # Reset the query in session state
    st.session_state.query = "" 
    st.session_state.email = ""
    st.session_state.context = []
    st.session_state.logged_in = False
    st.session_state.documents = {}

st.title("Multi-User Document Search System")

# Login simulation
st.sidebar.title("Login")
email = st.sidebar.text_input("Enter your email", value=st.session_state.email, key="email")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.sidebar.button("Login"):
    if email in USER_DOCUMENTS:
        st.session_state.logged_in = True
        st.session_state.documents = load_documents(email)
        st.sidebar.success("Login successful!")
    else:
        st.sidebar.error("Invalid email. Access denied.")
       
if st.session_state.logged_in:
    if "documents" in st.session_state and st.session_state.documents:
        st.subheader("Search Documents")
        query = st.text_input("Enter your query", value=st.session_state.query, key='query')
        if st.button("Search"):
            if query:  # Ensure query is not None or empty
                results = search_documents(query, st.session_state.documents)
                if results:
                    st.write("\n\n".join(results))
                else:
                    st.write("No results found.")
            else:
                st.warning("Please enter a query to search.")

        # Contextual follow-up simulation
        if "context" not in st.session_state:
            st.session_state.context = []
        if query:
            st.session_state.context.append(query)

        st.subheader("Conversation Context")
        st.write(" > ".join(st.session_state.context))
    else:
        st.write("No documents accessible for this user.")


if st.sidebar.button("Logout", on_click=clear_input):
    st.sidebar.info("Logged out successfully.")