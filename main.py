import streamlit as st
import sqlite3
from datetime import datetime

# Try to import matplotlib and handle the error if it fails
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    st.error("Matplotlib library is not installed. Please install it to view the graphs.")

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm trầm cảm", page_icon=":thought_balloon:", layout="wide")

# Tiêu đề
st.title("Trắc nghiệm trầm cảm")
st.write("Học viên: Kiến Văn")

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (name TEXT, date TEXT, level TEXT)''')

ten = st.text_input("Họ và tên:")
st.write("Xin chào,", ten)

# Các mức độ cảm xúc
Muc_do_cx = {
    "Rất tốt": "Bạn đang có trạng thái tinh thần rất ổn định và tích cực. Hãy tiếp tục duy trì điều này!",
    "Bình thường": "Bạn có một trạng thái tinh thần trung bình. Hãy chăm sóc bản thân và cân nhắc thư giãn thêm.",
    "Căng thẳng nhẹ": "Bạn có dấu hiệu căng thẳng nhẹ. Thử nghỉ ngơi, tập thể dục hoặc trò chuyện với bạn bè.",
    "Căng thẳng nặng": "Bạn có thể đang chịu áp lực lớn. Hãy tìm cách giảm bớt công việc và chăm sóc sức khỏe tinh thần.",
    "Buồn bã, tuyệt vọng": "Bạn có dấu hiệu trầm cảm nghiêm trọng. Hãy tìm đến sự hỗ trợ từ người thân hoặc chuyên gia tâm lý."
}

# Tạo cột cho các mức lựa chọn
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    b1 = st.button("Rất tốt")
with col2:
    b2 = st.button("Bình thường")
with col3:
    b3 = st.button("Căng thẳng nhẹ")
with col4:
    b4 = st.button("Căng thẳng nặng")
with col5:
    b5 = st.button("Buồn bã, tuyệt vọng")

# Hiển thị kết quả
if b1:
    with st.expander("Rất tốt"):
        st.write(":smile: " + Muc_do_cx["Rất tốt"])
        c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (ten, str(datetime.now()), "Rất tốt"))
        conn.commit()
if b2:
    with st.expander("Bình thường"):
        st.write(":neutral_face: " + Muc_do_cx["Bình thường"])
        c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (ten, str(datetime.now()), "Bình thường"))
        conn.commit()
if b3:
    with st.expander("Căng thẳng nhẹ"):
        st.write(":worried: " + Muc_do_cx["Căng thẳng nhẹ"])
        c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (ten, str(datetime.now()), "Căng thẳng nhẹ"))
        conn.commit()
if b4:
    with st.expander("Căng thẳng nặng"):
        st.write(":anguished: " + Muc_do_cx["Căng thẳng nặng"])
        c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (ten, str(datetime.now()), "Căng thẳng nặng"))
        conn.commit()
if b5:
    with st.expander("Buồn bã, tuyệt vọng"):
        st.write(":cry: " + Muc_do_cx["Buồn bã, tuyệt vọng"])
        c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (ten, str(datetime.now()), "Buồn bã, tuyệt vọng"))
        conn.commit()

# Thanh bên hiển thị kết quả
with st.sidebar:
    st.title("Kết quả trắc nghiệm")
    if b1:
        st.write(":smile: Bạn đã chọn: Rất tốt")
    if b2:
        st.write(":neutral_face: Bạn đã chọn: Bình thường")
    if b3:
        st.write(":worried: Bạn đã chọn: Căng thẳng nhẹ")
    if b4:
        st.write(":anguished: Bạn đã chọn: Căng thẳng nặng")
    if b5:
        st.write(":cry: Bạn đã chọn: Buồn bã, tuyệt vọng")

    st.write("Nếu cần hỗ trợ, hãy liên hệ người thân hoặc chuyên gia tâm lý.")

    # Lọc kết quả theo ngày
    st.header("Lọc kết quả theo ngày")
    start_date = st.date_input("Từ ngày")
    end_date = st.date_input("Đến ngày")
    if st.button("Lọc"):
        c.execute("SELECT * FROM results WHERE date BETWEEN ? AND ?", (start_date, end_date))
        filtered_results = c.fetchall()
        for result in filtered_results:
            st.write(result)

    # Hiển thị đồ thị về tình trạng cảm xúc theo thời gian
    st.header("Đồ thị tình trạng cảm xúc")
    if 'plt' in globals():
        c.execute("SELECT date, level FROM results")
        data = c.fetchall()
        dates = [datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S.%f') for d in data]
        levels = [d[1] for d in data]
        plt.plot(dates, levels)
        st.pyplot(plt)
    else:
        st.write("Matplotlib library is not available. Please install it to view the graphs.")

# Bản quyền
st.write('[© 2024 - Bản quyền thuộc về Ngvan](https://www.facebook.com/profile.php?id=100073017864297) <a href="https://www.facebook.com/profile.php?id=100073017864297" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" width="20"></a>', unsafe_allow_html=True)
