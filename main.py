import streamlit as st
import sqlite3
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json  # Thêm thư viện JSON để chuyển đổi responses thành chuỗi JSON

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm trầm cảm", page_icon=":thought_balloon:", layout="wide")

# Tiêu đề
st.title("Trắc nghiệm trầm cảm")
st.write("Học viên: Kiến Văn")

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (name TEXT, date TEXT, level TEXT, email TEXT)''')

# Nhập thông tin của người dùng
ten = st.text_input("Họ và tên:")
email = st.text_input("Email:")

# Các câu hỏi trắc nghiệm
questions = {
    "Bạn cảm thấy như thế nào trong tuần qua?": ["Rất tốt", "Bình thường", "Căng thẳng nhẹ", "Căng thẳng nặng", "Buồn bã, tuyệt vọng"],
    "Bạn có cảm giác mệt mỏi trong công việc không?": ["Không", "Có chút mệt", "Mệt nhiều", "Cực kỳ mệt", "Không thể làm việc"],
    "Bạn có cảm thấy lo âu không?": ["Không", "Có một chút lo lắng", "Lo lắng thường xuyên", "Lo âu mạnh mẽ", "Lo âu rất lớn"]
}

responses = []  # Dùng để lưu các câu trả lời của người dùng

# Hiển thị câu hỏi trắc nghiệm
for question, options in questions.items():
    answer = st.radio(question, options)
    responses.append(answer)

# Chức năng gửi kết quả qua email
def send_test_results(email, name, responses):
    sender_email = "nlkienvan123456789@gmail.com"  # Địa chỉ email của bạn
    password = "Kv10072011"  # Mật khẩu email của bạn
    receiver_email = email  # Địa chỉ email người nhận (người dùng nhập)

    # Soạn nội dung email
    subject = "Kết quả trắc nghiệm trầm cảm"
    body = f"Chào {name},\n\nDưới đây là kết quả trắc nghiệm trầm cảm của bạn:\n\n"
    for i, response in enumerate(responses):
        body += f"{list(questions.keys())[i]}: {response}\n"
    body += "\nChúc bạn sức khỏe và tinh thần tốt!"

    # Tạo MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Kết nối đến SMTP server và gửi email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("Kết quả trắc nghiệm đã được gửi qua email!")
    except Exception as e:
        st.error(f"Không thể gửi email. Lỗi: {str(e)}")

# Gửi kết quả và lưu vào cơ sở dữ liệu
if st.button("Gửi kết quả"):
    if ten and email:
        # Chuyển đổi responses thành chuỗi JSON trước khi lưu vào cơ sở dữ liệu
        responses_json = json.dumps(responses)
        
        # Lưu kết quả vào cơ sở dữ liệu
        c.execute("INSERT INTO results (name, date, level, email) VALUES (?, ?, ?, ?)", (ten, str(datetime.now()), responses_json, email))
        conn.commit()
        
        # Gửi kết quả qua email
        send_test_results(email, ten, responses)
    else:
        st.error("Vui lòng nhập đầy đủ tên và email.")

# Hiển thị kết quả đã gửi
st.write("Kết quả của bạn sẽ được hiển thị ở đây sau khi gửi.")
