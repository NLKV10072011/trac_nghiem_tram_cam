import streamlit as st
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm Trầm cảm", page_icon=":thought_balloon:", layout="wide")

# Tiêu đề và giới thiệu
st.title("Trắc nghiệm Trầm cảm - Hỗ trợ sức khỏe tinh thần")
st.write("Chào bạn, đây là công cụ giúp bạn đánh giá tình trạng tâm lý của mình. Hãy chia sẻ cảm xúc để chúng tôi có thể hỗ trợ bạn tốt hơn.")

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (name TEXT, date TEXT, level TEXT)''')

# Phần nhập tên
name = st.text_input("Tên người cần đánh giá:")

# Các câu hỏi đánh giá cảm xúc
questions = [
    ("Bạn cảm thấy mệt mỏi và thiếu năng lượng không?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có cảm thấy mình không còn hứng thú với các hoạt động bạn thường thích?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có thường xuyên cảm thấy buồn bã hoặc vô vọng?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có gặp khó khăn trong việc tập trung vào công việc hoặc các hoạt động khác?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có gặp khó khăn trong việc ngủ hoặc ngủ quá nhiều?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có cảm thấy mình vô dụng hoặc cảm thấy tội lỗi không giải thích được?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có cảm thấy lo âu hoặc khó kiểm soát cảm xúc của mình?", ["Không", "Thỉnh thoảng", "Có"]),
    ("Bạn có cảm thấy cô đơn và thiếu sự kết nối với người khác?", ["Không", "Thỉnh thoảng", "Có"]),
]

# Tạo giao diện cho các câu hỏi
responses = []
for question, options in questions:
    response = st.radio(question, options)
    responses.append(response)

# Đánh giá kết quả từ các câu trả lời
def evaluate_responses(responses):
    score = 0
    for response in responses:
        if response == "Có":
            score += 2
        elif response == "Thỉnh thoảng":
            score += 1
    if score >= 16:
        return "Cần sự hỗ trợ tâm lý", "Bạn có dấu hiệu trầm cảm nghiêm trọng. Hãy tìm đến sự hỗ trợ từ người thân hoặc chuyên gia tâm lý."
    elif score >= 10:
        return "Căng thẳng", "Bạn có dấu hiệu căng thẳng và cần chú ý đến sức khỏe tinh thần của mình."
    else:
        return "Tốt", "Bạn đang có trạng thái tinh thần ổn định. Tuy nhiên, hãy theo dõi và chăm sóc bản thân."

level, message = evaluate_responses(responses)

# Phần nhập email nhận kết quả
receiver_email = st.text_input("Nhập email nhận kết quả:")

# Thêm nút "Nộp bài"
submit_button = st.button("Nộp bài")

if submit_button:
    if name:
        # Lưu kết quả vào cơ sở dữ liệu, đảm bảo giá trị "level" hợp lệ
        if level in ["Tốt", "Căng thẳng", "Cần sự hỗ trợ tâm lý"]:
            c.execute("INSERT INTO results (name, date, level) VALUES (?, ?, ?)", (name, str(datetime.now()), level))
            conn.commit()
        else:
            st.error("Giá trị cảm xúc không hợp lệ. Vui lòng thử lại.")
            st.stop()  # Dừng lại nếu giá trị không hợp lệ

    # Hiển thị kết quả
    st.subheader(f"Tình trạng của {name}: {level}")
    st.write(message)

    # Hiển thị phần hỗ trợ tâm lý
    st.sidebar.title("Hỗ trợ và lời khuyên")
    if level == "Cần sự hỗ trợ tâm lý":
        st.sidebar.write("Bạn có thể liên hệ với các dịch vụ hỗ trợ tâm lý sau:")
        st.sidebar.write("- Đường dây nóng tâm lý: 1800-1234")
        st.sidebar.write("- Email hỗ trợ: support@mentalhealth.com")
        st.sidebar.write("Ngoài ra, bạn có thể tham gia các buổi thiền hoặc thở sâu để giảm căng thẳng:")
        st.sidebar.write("1. Bài tập thở 4-7-8: Hít vào 4 giây, giữ 7 giây, thở ra 8 giây.")
        st.sidebar.write("2. Thiền mindfulness: Hãy tập trung vào hơi thở và để tâm trí tĩnh lặng.")

    # Gửi email hỗ trợ
    email_button = st.button("Gửi kết quả qua email")
    if email_button:
        email_sent = send_email(name, level, message, receiver_email)
        if email_sent:
            st.success("Kết quả đã được gửi qua email!")
        else:
            st.error("Đã xảy ra lỗi khi gửi email. Vui lòng thử lại sau.")

    # Cập nhật biểu đồ tình trạng cảm xúc trong sidebar
    with st.sidebar:
        st.header("Đồ thị tình trạng cảm xúc")
        # Lọc kết quả theo ngày
        start_date = st.date_input("Từ ngày")
        end_date = st.date_input("Đến ngày")
        if st.button("Lọc"):
            c.execute("SELECT date, level FROM results WHERE date BETWEEN ? AND ?", (start_date, end_date))
            data = c.fetchall()

            # Khởi tạo dictionary với các mức độ hợp lệ
            level_counts = {
                "Tốt": 0,
                "Căng thẳng": 0,
                "Cần sự hỗ trợ tâm lý": 0
            }

            # Duyệt qua các giá trị level trong cơ sở dữ liệu
            for d in data:
                level_counts[d[1]] += 1

            # Vẽ biểu đồ
            fig, ax = plt.subplots()
            ax.bar(level_counts.keys(), level_counts.values(), color="skyblue")
            ax.set_title("Tình trạng cảm xúc của những người tham gia")
            ax.set_xlabel("Mức độ cảm xúc")
            ax.set_ylabel("Số lần chọn")
            st.pyplot(fig)

# Thanh bên hiển thị kết quả
with st.sidebar:
    st.title("Lịch sử kết quả")
    if name:
        st.write(f"Kết quả của {name}: {level}")
    st.write("Nếu cần hỗ trợ, hãy liên hệ người thân hoặc chuyên gia tâm lý.")

# Bản quyền
st.write('[© 2024 - Bản quyền thuộc về Ngvan](https://www.facebook.com/profile.php?id=100073017864297) <a href="https://www.facebook.com/profile.php?id=100073017864297" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" width="20"></a>', unsafe_allow_html=True)

# Hàm gửi email
def send_email(name, level, message, receiver_email):
    try:
        # Cấu hình thông tin email
        sender_email = "nlkienvan123456789@gmail.com"  # Địa chỉ email người gửi
        password = "Kv10072011"  # Mật khẩu tài khoản email người gửi
        subject = f"Kết quả trắc nghiệm trầm cảm của {name}"

        body = f"""
        Chào bạn,
        
        Kết quả trắc nghiệm trầm cảm của {name}:
        - Tình trạng: {level}
        - Thông điệp: {message}
        
        Nếu bạn cần sự hỗ trợ, hãy liên hệ với chuyên gia tâm lý hoặc người thân.

        Thân ái,
        Trắc nghiệm sức khỏe tinh thần.
        """

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Kết nối tới máy chủ Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        return True  # Trả về True nếu email gửi thành công
    except Exception as e:
        return False  # Trả về False nếu có lỗi xảy ra
