import streamlit as st
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm trầm cảm", page_icon=":thought_balloon:", layout="wide")

# Tiêu đề
st.title("Trắc nghiệm trầm cảm - Đánh giá tình trạng tâm lý của người khác")
st.write("Hãy giúp người khác đánh giá tình trạng tâm lý của họ.")

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (name TEXT, date TEXT, level TEXT)''')

name = st.text_input("Tên người cần đánh giá:")

# Các câu hỏi và lựa chọn trả lời
questions = [
    ("Bạn cảm thấy mệt mỏi và thiếu năng lượng không?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có cảm thấy mình không còn hứng thú với các hoạt động bạn thường thích?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có thường xuyên cảm thấy buồn bã hoặc vô vọng?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có gặp khó khăn trong việc tập trung vào công việc hoặc các hoạt động khác?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có gặp khó khăn trong việc ngủ hoặc ngủ quá nhiều?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có cảm thấy mình vô dụng hoặc cảm thấy tội lỗi không giải thích được?", ["Không", "Thỉnh thoảng", "Có"]),
]

# Tạo giao diện cho câu hỏi
responses = []
for question, options in questions:
    response = st.radio(question, options)
    responses.append(response)

# Xử lý kết quả
def evaluate_responses(responses):
    score = 0
    for response in responses:
        if response == "Có":
            score += 2
        elif response == "Thỉnh thoảng":
            score += 1
    if score >= 10:
        return "Cần sự hỗ trợ tâm lý", "Bạn có dấu hiệu trầm cảm nghiêm trọng. Hãy tìm đến sự hỗ trợ từ người thân hoặc chuyên gia tâm lý."
    elif score >= 6:
        return "Căng thẳng", "Bạn có dấu hiệu căng thẳng và cần chú ý đến sức khỏe tinh thần của mình."
    else:
        return "Tốt", "Bạn đang có trạng thái tinh thần ổn định. Tuy nhiên, hãy theo dõi và chăm sóc bản thân."

level, message = evaluate_responses(responses)

# Hiển thị kết quả
st.subheader(f"Tình trạng của {name}: {level}")
st.write(message)

# Lưu kết quả vào cơ sở dữ liệu
if name:
    c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (name, str(datetime.now()), level))
    conn.commit()

# Thanh bên hiển thị kết quả
with st.sidebar:
    st.title("Lịch sử kết quả")
    if name:
        st.write(f"Kết quả của {name}: {level}")
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
    c.execute("SELECT date, level FROM results")
    data = c.fetchall()
    dates = [datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S.%f') for d in data]
    levels = [d[1] for d in data]

    # Khởi tạo dictionary với các mức độ hợp lệ
    level_counts = {
        "Tốt": 0,
        "Căng thẳng": 0,
        "Cần sự hỗ trợ tâm lý": 0
    }

    # Duyệt qua các giá trị level trong cơ sở dữ liệu
    for level in levels:
        if level in level_counts:
            level_counts[level] += 1
        else:
            # Nếu level không có trong từ điển, bạn có thể ghi lại hoặc bỏ qua
            st.warning(f"Giá trị '{level}' không hợp lệ và bị bỏ qua.")

    # Vẽ biểu đồ
    fig, ax = plt.subplots()
    ax.bar(level_counts.keys(), level_counts.values(), color="skyblue")
    ax.set_title("Tình trạng cảm xúc của những người tham gia")
    ax.set_xlabel("Mức độ cảm xúc")
    ax.set_ylabel("Số lần chọn")
    st.pyplot(fig)

# Bản quyền
st.write('[© 2024 - Bản quyền thuộc về Ngvan](https://www.facebook.com/profile.php?id=100073017864297) <a href="https://www.facebook.com/profile.php?id=100073017864297" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" width="20"></a>', unsafe_allow_html=True)
