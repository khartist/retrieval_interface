import streamlit as st
from PIL import Image

st.title("Tải dữ liệu")
st.markdown("""
    ### Tải lên thông tin mới
    Nhập thông tin văn bản, tải lên hình ảnh.
""")

# Section for Text Input
st.header("Nhập liệu văn bản")
text_query = st.text_area("Nhập dữ liệu tại đây:")

# Section for Image Upload
st.header("Tải hình ảnh")
uploaded_image = st.file_uploader("Tải hình ảnh tại đây", type=["jpg", "jpeg", "png"])

# Display Text Input and Uploaded Content
if text_query:
    st.subheader("Nội dung văn bản đã nhập")
    st.write(text_query)

if uploaded_image is not None:
    st.subheader("Hình ảnh đã tải lên")
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Placeholder for future integration
st.header("Trạng thái")
st.markdown("""
    - **Tải dữ liệu lên cơ sở dữ liệu:** Tính năng đang được hoàn thiện.
""")
