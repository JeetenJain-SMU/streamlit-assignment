import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Load pre-trained model (ensure the model path is correct and accessible)
model = load_model('mnist_digit_classifier.h5')

def load_and_preprocess_image(image):
    # Resize image to 28x28 pixels using LANCZOS resampling
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    # Convert image to grayscale
    image = ImageOps.grayscale(image)
    
    # Convert image to numpy array
    image_array = np.array(image)
    
    # Normalize the image array
    image_array = image_array / 255.0
    
    # Invert image colors if the digit is darker than the background
    if np.mean(image_array) > 0.5:  # if the background is lighter than the digit
        image_array = 1.0 - image_array
    
    # Expand dimensions to fit model input
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def predict_digit(image):
    # Preprocess the image
    processed_image = load_and_preprocess_image(image)
    # Predict the digit
    predictions = model.predict(processed_image)
    return np.argmax(predictions), max(predictions[0])

# Streamlit UI
st.title('Digit Recognition App')
uploaded_file = st.file_uploader("Upload an image of a digit", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    predicted_digit, confidence = predict_digit(image)
    st.write(f'Predicted Digit: {predicted_digit} with confidence {confidence:.2f}')

