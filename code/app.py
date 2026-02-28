import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
from google import genai

# Activity 1: Load Environment Variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the new Google GenAI Client
client = genai.Client(api_key=api_key)

# Activity 2: Function to get Gemini response using the updated SDK
def get_gemini_response(input_text, image_data, prompt):
    # Updated to use Gemini 3 Flash, the 2026 standard for vision tasks
    model_id = "gemini-3-flash-preview"
    
    # The new SDK combines contents into a simple list
    response = client.models.generate_content(
        model=model_id,
        contents=[input_text, image_data, prompt]
    )
    return response.text

# Activity 3: Function to prepare the image for the model
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Open image using PIL to ensure it's valid
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError("No file uploaded")

# --- Activity 4: Streamlit UI Deployment ---

st.set_page_config(page_title="Civil Engineering Insight Studio", page_icon="🏗️")
st.header("Civil Engineering Insight Studio")

# User Inputs
input_text = st.text_input("Input Prompt (Optional context):", key="input")
uploaded_file = st.file_uploader("Choose an image of a structure...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image to the user
    image_display = Image.open(uploaded_file)
    st.image(image_display, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Describe Structure")

# Professional Engineering Prompt
input_prompt = """
You are a civil engineer. Please describe the structure in the image and provide details such as its type,

1. Type of structure – Description
2. Materials used – Description
3. Dimensions – Description
4. Construction methods – Description
5. Notable features or engineering challenges – Description
"""

# Handle Submit
if submit:
    if uploaded_file is not None:
        try:
            with st.spinner("Analyzing structural details..."):
                # Prepare image and get response
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_text, image_data, input_prompt)
                
                st.subheader("Engineering Analysis Output")
                st.markdown(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an image before clicking 'Describe Structure'.")
