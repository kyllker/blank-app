import streamlit as st
import requests
from PIL import Image
import replicate
from io import BytesIO
import os

# Initialize Streamlit app
st.title("Image Transformation with Replicate")
st.write("Upload two image URLs, transform them using Replicate, and see the results!")

# Input fields for image URLs
image_url1 = st.text_input("Enter the first image URL:")
image_url2 = st.text_input("Enter the second image URL:")
category = st.text_input("Enter the category:")
output_filename = st.text_input("Enter the output_filename:")

# Button to trigger the process
if st.button("Generate New Image"):
    if image_url1 and image_url2:
        try:
            # Fetch the first image
            response1 = requests.get(image_url1)
            img1 = Image.open(BytesIO(response1.content))

            # Fetch the second image
            response2 = requests.get(image_url2)
            img2 = Image.open(BytesIO(response2.content))

            # Display the input images
            st.image(img1, caption="First Image", use_column_width=True)
            st.image(img2, caption="Second Image", use_column_width=True)

            # Call the Replicate model
            st.write("Processing images with Replicate...")
            payload = {
                "url_body": image_url1,
                "url_product": image_url2,
                "category": category,
                "output_filename": output_filename
            }
            os.environ["REPLICATE_API_TOKEN"] = "r8_Lr8gS9evl01O8EGLmGKtw8m7pGmdHT62paDIA"
            deployment = replicate.deployments.get("techml-mm/tryon")
            prediction = deployment.predictions.create(
                input=payload
            )
            prediction.wait()
            url_result = prediction.output.get('url_image')
            # Display the generated image
            response1 = requests.get(url_result)
            generated_img = Image.open(BytesIO(response1.content))
            st.image(generated_img, caption="Generated Image", use_column_width=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide valid URLs for both images.")
