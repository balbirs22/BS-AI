import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model,gemini_pro_vision_response,embedding_model_response,gemini_pro_response)

working_directory = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="BS AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected = option_menu("BS AI",
                           ["ChatBot", "Image Captioning", "Embed Text", "Ask me Anything"],
                           menu_icon='robot',
                           icons=['chat-left-text-fill', 'image', 'textarea-t', 'person-raised-hand'],
                           default_index=0)


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


if selected == "ChatBot":
    model = load_gemini_pro_model()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])


    st.title("🤖ChatBot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)


    user_prompt = st.chat_input("Ask Gemini Pro....")

    if user_prompt :
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)



if selected == "Image Captioning":
    st.title("Generate Captions for Your Images 📸")
    uploaded_image = st.file_uploader("Upload an image....", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)
        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)
        default_prompt = "write a short caption for this image for an instagram post"
        caption = gemini_pro_vision_response(default_prompt,image)

        with col2:
            st.info(caption)


if selected == "Embed Text":
    st.title("Embed Text 🔠")
    input_text = st.text_area(label="", placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)


if selected == "Ask me Anything":
    st.title("Ask me a question 🙋")
    user_prompt = st.text_area(label="", placeholder="Ask me anything....")
    if(st.button("Generate an Answer")):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)

