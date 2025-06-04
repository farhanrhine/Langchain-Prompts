# prompt_ui.py
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate  # Correct place now
from dotenv import load_dotenv
import streamlit as st
from utils import load_prompt



load_dotenv()
model = Ollama(model='tinydolphin')

# Initialize chat history and state in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.show_input_form = True
    st.session_state.paper_info = {}

# Load template once
if 'template' not in st.session_state:
    st.session_state.template = load_prompt('template.json')
    st.session_state.chain = st.session_state.template | model

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show input form only if it's the first message
if st.session_state.show_input_form:
    with st.container():
        st.header('Research Tool')
        
        paper_options = ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis", "Other..."]
        selected_paper = st.selectbox("Select Research Paper Name", paper_options, key="paper_select")

        # If "Other..." is selected, show a text input for custom paper name
        if selected_paper == "Other...":
            paper_input = st.text_input("Enter research paper name", key="paper_input")
        else:
            paper_input = selected_paper

        style_input = st.selectbox("Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"], key="style_select")
        length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"], key="length_select")

        if st.button('Generate Summary'):
            if not paper_input.strip():
                st.error("Please enter a research paper name")
                st.stop()
                
            # Store paper info for follow-up questions
            st.session_state.paper_info = {
                'paper_input': paper_input,
                'style_input': style_input,
                'length_input': length_input
            }
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"I need a {style_input.lower()} summary of the research paper '{paper_input}'. Please make it {length_input.lower()}."})
            
            # Generate response
            with st.spinner('Generating summary...'):
                result = st.session_state.chain.invoke(st.session_state.paper_info)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": result})
            st.session_state.show_input_form = False
            st.rerun()

# Chat input for follow-up questions (only show if we have paper info)
elif st.session_state.paper_info:
    if prompt := st.chat_input("Ask a follow-up question or request more details..."):
        # Add user's follow-up to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Include the original paper info and the follow-up question
        chain_input = st.session_state.paper_info.copy()
        chain_input['paper_input'] = f"{st.session_state.paper_info['paper_input']} - {prompt}"
        
        # Generate response for follow-up question
        with st.spinner('Thinking...'):
            response = st.session_state.chain.invoke(chain_input)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


