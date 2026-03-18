import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os



# Load API Keys

load_dotenv()

GROQ_API_KEY = os.getenv("groq_api_key")
PINECONE_API_KEY = os.getenv("pinecone_api_key")

client = Groq(api_key=GROQ_API_KEY)



# Page Config

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)



# Dark UI Theme

st.markdown("""
<style>

.stApp{
background-color:#FFF8FD;
color:Black;
}

h1{
color:#38bdf8;
}

div[data-testid="stChatMessageContent"]{
font-size:16px;
}

</style>
""", unsafe_allow_html=True)



# Load Embedding Model

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()



# Pinecone Init

@st.cache_resource
def init_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index("data-ingesstion-v2")

index = init_pinecone()



# Session State Setup

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
    st.session_state.conversations["Chat 1"] = []



# Sidebar (Chat History)

with st.sidebar:

    st.title("💬 Chats")

    if st.button("➕ New Chat"):

        chat_name = f"Chat {len(st.session_state.conversations)+1}"

        st.session_state.conversations[chat_name] = []

        st.session_state.current_chat = chat_name

    st.markdown("---")

    for chat in st.session_state.conversations:

        if st.button(chat):

            st.session_state.current_chat = chat



# Header

col1, col2 = st.columns([8,2])

with col1:
    st.title("🤖 AI Chatbot")

with col2:

    if st.button("🗑 Clear Chat"):

        st.session_state.conversations[
            st.session_state.current_chat
        ] = []

        st.rerun()



# Current Chat Messages

messages = st.session_state.conversations[
    st.session_state.current_chat
]



# Retrieve Context from Pinecone

def fetch_context(query):

    vector = model.encode(query).tolist()

    results = index.query(
        vector=vector,
        top_k=3,
        include_metadata=True
    )

    context = []

    for match in results.matches:
        context.append(match.metadata.get("text",""))

    return "\n".join(context)



# Generate Response

def generate_response(query, context):

    completion = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role":"system",
                "content":"You are a helpful assistant. Answer clearly using the context."
            },
            {
                "role":"user",
                "content":f"""
Context:
{context}

Question:
{query}
"""
            }
        ],

        temperature=0.7,
        max_completion_tokens=1000,
        stream=False
    )

    return completion.choices[0].message.content



for msg in messages:

    with st.chat_message(
        msg["role"],
        avatar="🙂" if msg["role"]=="user" else "🤖"
    ):
        st.markdown(msg["content"])


if prompt := st.chat_input("Ask something..."):

    messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)

    context = fetch_context(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            response = generate_response(prompt, context)

        st.markdown(response)

    messages.append({
        "role":"assistant",
        "content":response
    })
    