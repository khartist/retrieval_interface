import streamlit as st
from PIL import Image

st.title("Truy vấn thông tin")
st.markdown("""
    ### Tìm kiếm thông tin từ cơ sở dữ liệu
    Nhập thông tin bằng văn bản hoặc tải lên hình ảnh để bắt đầu tìm kiếm.
""")

# Section for Text Input
st.header("Truy vấn bằng văn bản")
text_query = st.text_area("Nhập tại đây:")

# Section for Image Upload
st.header("Truy vấn bằng hình ảnh")
uploaded_image = st.file_uploader("Tải hình ảnh tại đây", type=["jpg", "jpeg", "png"])

# Display Text Input and Image
if text_query:
    st.subheader("Text Query Preview")
    st.write(text_query)

if uploaded_image is not None:
    st.subheader("Uploaded Image Preview")
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Placeholder for future retrieval output
st.header("Kết quả truy vấn (Tính năng đang phát triển)")
st.markdown("""
    Kết quả truy vấn sẽ được hiển thị tại đây sau khi hệ thống hoàn thiện.
    Các kết quả có thể bao gồm văn bản, hình ảnh liên quan hoặc cả hai.
""")
st.button("Tìm kiếm")
