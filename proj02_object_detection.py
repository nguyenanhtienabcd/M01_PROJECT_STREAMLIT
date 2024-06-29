import cv2
import numpy as np
from PIL import Image
import streamlit as st
import tempfile

st.title('Object detection for Image')  # tạo title cho trang thử nghiệm

model_file = st.file_uploader("Upload MODEL file:", type='.caffemodel')
prototxt_file = st.file_uploader(
    "Upload PROTOTXT file:", type=['txt', '.prototxt'])

# ----------Fault---------#
# Hàm st.file_uploader trả về các đối tượng tệp
# nhưng cv2.dnn.readNetFromCaffe yêu cầu các đường dẫn tệp dưới dạng chuỗi ký tự
# Do đó, khi bạn truyền đối tượng tệp trực tiếp, hàm này không thể xử lý và gây ra lỗi.
# --------solution--------#
# (NamedTemporaryFile) giúp bạn lưu nội dung của đối tượng tệp vào một tệp thực sự trên hệ thống tệp (filesystem)
# Sau đó, bạn có thể lấy đường dẫn của tệp tạm thời này và truyền cho hàm yêu cầu đường dẫn tệp.
# Các tệp tạm thời được tự động xoá sau khi chúng không còn được sử dụng
if prototxt_file and model_file:
    with tempfile.NamedTemporaryFile(delete=False) as prototxt_temp:
        # Tham số delete=False -> tệp tạm thời này không nên bị xóa tự động khi đối tượng tệp (file object) bị đóng
        prototxt_temp.write(prototxt_file.read())
        PROTOTXT = prototxt_temp.name

    with tempfile.NamedTemporaryFile(delete=False) as model_temp:
        model_temp.write(model_file.read())
        MODEL = model_temp.name


def process_image(image):
    blob = cv2.dnn . blobFromImage(cv2 . resize(
        image, (300, 300)), 0.007843, (300, 300), 127.5)
    net = cv2.dnn. readNetFromCaffe(PROTOTXT, MODEL)
    net . setInput(blob)
    detections = net. forward()
    return detections


def annotate_image(image, detections, confidence_threshold=0.5):
    # loop over the detections
    image_np = np.array(image)  # chuyển đôi ảnh thành một mảng bằng numpy
    (h, w) = image_np.shape[:2]  # lấy chiều rộng và chiều dài của ảnh
    for i in np. arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confidence_threshold:
            # extract the index of the class label from the ‘detections ‘,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            # idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np. array([w, h, w, h])
            (startx, starty, endx, endy) = box.astype("int")
            cv2 . rectangle(image_np, (startx, starty),
                            (endx, endy), 227, 2)
    return image_np


def main():

    upload_f = st.file_uploader('Upload image file', type=[
                                'png', 'jpg', 'jpeg'])   # tải file ảnh lên
    if upload_f is not None:
        # kiếm tra xem file tải lên có None không, nếu ko thì cho hiển thị ảnh
        st.image(upload_f, 'uploaded image')
        image = Image.open(upload_f)    # mở hình ảnh
        # chuyển đổi hình ảnh thành mảng dữ liệu nhiều chiều
        image_arr = np.array(image)
        detections = process_image(image_arr)   # phát hiện dữ liệu blackbox
        processed_image = annotate_image(image, detections)
        st.image(processed_image, 'processed image')


if __name__ == '__main__':
    main()
