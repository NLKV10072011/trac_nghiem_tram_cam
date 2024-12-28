import streamlit as st
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm trầm cảm", page_icon=":thought_balloon:", layout="wide")

# Tiêu đề
st.title("Trắc nghiệm trầm cảm")
st.write("Học viên: Kiến Văn")

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect('results.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS results (name TEXT, date TEXT, level TEXT, email TEXT)''')

ten = st.text_input("Họ và tên:")
email = st.text_input("Email của bạn:")
st.write("Xin chào,", ten)

# Các mức độ cảm xúc
Muc_do_cx = {
    "Rất tốt": "Bạn đang có trạng thái tinh thần rất ổn định và tích cực. Hãy tiếp tục duy trì điều này!",
    "Bình thường": "Bạn có một trạng thái tinh thần trung bình. Hãy chăm sóc bản thân và cân nhắc thư giãn thêm.",
    "Căng thẳng nhẹ": "Bạn có dấu hiệu căng thẳng nhẹ. Thử nghỉ ngơi, tập thể dục hoặc trò chuyện với bạn bè.",
    "Căng thẳng nặng": "Bạn có thể đang chịu áp lực lớn. Hãy tìm cách giảm bớt công việc và chăm sóc sức khỏe tinh thần.",
    "Buồn bã, tuyệt vọng": "Bạn có dấu hiệu trầm cảm nghiêm trọng. Hãy tìm đến sự hỗ trợ từ người thân hoặc chuyên gia tâm lý.",
    "Vui vẻ": "Bạn đang trong trạng thái rất vui vẻ và hạnh phúc!"
}

# Câu hỏi trắc nghiệm và các lựa chọn
questions = [
    "Trong tuần qua, bạn cảm thấy tinh thần của mình như thế nào?",
    "Trong tuần qua, bạn có cảm thấy căng thẳng, mệt mỏi không?",
    "Bạn có cảm thấy cuộc sống có ý nghĩa và mục đích không?",
    "Bạn có dễ dàng cảm thấy hạnh phúc hoặc vui vẻ không?"
]

# Câu trả lời tương ứng với mỗi câu hỏi
answers = [
    ["Rất tốt", "Bình thường", "Căng thẳng nhẹ", "Căng thẳng nặng", "Buồn bã, tuyệt vọng"],
    ["Rất tốt", "Bình thường", "Căng thẳng nhẹ", "Căng thẳng nặng", "Buồn bã, tuyệt vọng"],
    ["Rất tốt", "Bình thường", "Căng thẳng nhẹ", "Căng thẳng nặng", "Buồn bã, tuyệt vọng"],
    ["Rất tốt", "Bình thường", "Căng thẳng nhẹ", "Căng thẳng nặng", "Buồn bã, tuyệt vọng"]
]

# Hiển thị các câu hỏi và lựa chọn
responses = []
for idx, question in enumerate(questions):
    response = st.radio(question, answers[idx])
    responses.append(response)

# Hàm gửi email
def send_email(recipient_email, subject, body):
    sender_email = "your_email@gmail.com"  # Thay bằng email của bạn
    sender_password = "your_app_password"  # Mật khẩu ứng dụng nếu có bật xác thực 2 bước
    
    # Cấu hình thư
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Thêm nội dung email
    msg.attach(MIMEText(body, 'plain'))
    
    # Gửi email qua SMTP server của Gmail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email đã được gửi thành công!")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

# Gửi kết quả trắc nghiệm qua email
def send_test_results(email, name, responses):
    subject = f"Kết quả trắc nghiệm trầm cảm của {name}"
    body = f"Chào {name},\n\nKết quả trắc nghiệm trầm cảm của bạn:\n"
    for idx, response in enumerate(responses):
        body += f"- Câu hỏi {idx+1}: {response}\n"
    body += "\nCảm ơn bạn đã tham gia!"
    send_email(email, subject, body)

# Khi người dùng hoàn thành trắc nghiệm, hiển thị kết quả và gửi email
if st.button("Gửi kết quả"):
    if ten and email:
        # Lưu kết quả vào cơ sở dữ liệu
        c.execute("INSERT INTO results (name, date, level, email) VALUES (?, ?, ?, ?)", (ten, str(datetime.now()), str(responses), email))
        conn.commit()
        
        # Gửi kết quả qua email
        send_test_results(email, ten, responses)
        
        # Thông báo kết quả đã được gửi
        st.success("Kết quả trắc nghiệm đã được gửi qua email!")
    else:
        st.error("Vui lòng nhập đầy đủ tên và email.")

# Thanh bên hiển thị kết quả
with st.sidebar:
    st.title("Kết quả trắc nghiệm")
    st.write("Kết quả của bạn đã được ghi lại và gửi qua email.")
    st.write("Nếu cần hỗ trợ, hãy liên hệ người thân hoặc chuyên gia tâm lý.")
