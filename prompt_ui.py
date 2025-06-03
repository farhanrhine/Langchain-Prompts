# prompt_ui.py
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate  # Correct place now
from dotenv import load_dotenv
import streamlit as st
from utils import load_prompt



load_dotenv()
model = Ollama(model='tinydolphin')

st.header('Reasearch Tool')

paper_options = ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis", "Other..."]
selected_paper = st.selectbox("Select Research Paper Name", paper_options)

# If "Other..." is selected, show a text input for custom paper name
if selected_paper == "Other...":
    paper_input = st.text_input("Enter research paper name")
else:
    paper_input = selected_paper

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

template = load_prompt('template.json')



if st.button('Summarize'):
    chain = template | model
    result = chain.invoke({
        'paper_input':paper_input,
        'style_input':style_input,
        'length_input':length_input
    })
    st.write(result)
