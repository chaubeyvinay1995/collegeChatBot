import os

import streamlit as st
from configurations.page import page_config
from langchain_classic import ConversationChain
from langchain_classic.memory import ConversationBufferMemory

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load api key
GOOGLE_API_KEY = "AIzaSyDRJoOfb5WdVlwaLsgxvA7fDwaLzrnR85o"
GEMINI_MODEL = "gemini-2.0-flash"


# set page configuration
st.set_page_config(page_title=page_config.PageTitle, layout=page_config.Layout, page_icon=page_config.Icon)
st.title(page_config.Title)

with st.sidebar:
    st.markdown("Developed by [Vinay Chaubey](https://www.linkedin.com/in/vinaygo1995/)")
    st.image("assets/logo.png", use_container_width=150)
    st.markdown(
        """
        <div style='text-align: center;'>
            <h4><b> 🌟ABES Engineering College ChatBot🌟 </b>\n\n Services \n\n----------------- \n\n <em>Empowering youth through Education</em> </h4>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.sidebar:

    st.markdown("### 📌 Contact Us")
    st.write("📧 Email: info@abes.ac.in")
    st.write("📞 Phone: 01207135112")
    st.write("🌐 Website: https://www.abes.ac.in/")
    st.write("📍  Address: 19th KM Stone, NH-09 Ghaziabad (UP) PIN - 201009.")
    st.write("🔗 [Facebook](https://www.facebook.com/collegeofengabes/) | [Instagram](https://www.instagram.com/abesec_official/) | [LinkedIn](https://in.linkedin.com/school/abes-engineering-college/)")

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state["has_greeted"] = False

if not st.session_state["has_greeted"]:
    initial_greeting = page_config.InitialGreeting
    st.session_state["chat_history"].append({"role": "assistant", "content": initial_greeting})
    st.session_state["has_greeted"] = True

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory()

# load knowledge base file
with open("knowledge_base.txt", "r", encoding="utf-8") as file:
    SCRIPT = file.read()


if GOOGLE_API_KEY:
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.5
    )
    prompt_template = PromptTemplate(
        input_variables=["history", "input"],
        template="""
        {script}
        Conversation History:
        {history}

        User: {input}
        Assistant:""".strip()
    )

    chain = ConversationChain(
        llm=llm,
        memory=st.session_state["memory"],
        prompt=prompt_template.partial(script=SCRIPT),
        verbose=False,
    )

else:
    st.error("Google API key not found. Please add it to `.streamlit/secrets.toml` as GOOGLE_API_KEY")
    st.stop()

user_input = st.chat_input("Ask something about ABES Engineering college...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state["chat_history"].append({"role": "assistant", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                bot_response = chain.run(user_input)
                st.markdown(bot_response)
                st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"Error: {e}")