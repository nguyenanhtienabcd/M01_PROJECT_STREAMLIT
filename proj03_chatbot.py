import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


def generate_respond(prmpt, email, passw):
    # đăng nhập vào hugchat
    sing_in = Login(email, passw)
    cookies = sing_in.login()
    # tạo chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prmpt)


def main():
    st.title('Chatbot')

    # tạo một sidebar để đăng nhập
    with st.sidebar:
        st.title('Huggingchat account')
        hf_mail = st.text_input('E-mail:')
        hf_pass = st.text_input('Password:', type='password')
        if not (hf_mail and hf_pass):
            st. warning('Please enter your account !')
        else:
            st. success('Proceed to entering your prompt message !')

    # tạo một danh sách ghi lại lịch sử các câu lệnh và câu trả lời
    if 'messages' not in st.session_state.keys():   # kiểm tra chuỗi 'message' có trong key ko?
        st.session_state['messages'] = [
            {'user': 'assistant', 'content': 'How can I help you?'}]

    for messages in st.session_state['messages']:
        # st.chat_message để hiển thị các tin nhắn trong lịch sử với vai trò tương ứng ('user' hoặc 'assistant').
        with st.chat_message(messages['user']):
            # sẽ ghi ra câu trả lời content (ghi lại trên màn hình)
            st.write(messages['content'])

    # câu lệnh này kiểm tính truly
    # input_chat sẽ bị khóa nếu 1 trong hf_mail hoặc hf_pass là rỗng
    # not(true and true) = false -----> disabled = True
    # nếu promt KHÔNG rỗng (not None, '', ()...) thực hiện lệnh dưới (NGƯỢC LẠI: nếu prompt rỗng thì ko thực thi lệnh bên dưới)
    if promt := st.chat_input(disabled=not (hf_mail and hf_pass)):
        st.session_state['messages'].append(
            {'user': 'user', 'content': promt})
        with st.chat_message('user'):
            st.write(promt)

        #### TẠO CÂU TRẢ LỜI BẰNG HUGCHAT ###
        # kiểm tra phần tử cuối cùng của list và key của phần tử đó
        # mục đích để người viết/ trả lời cuối cùng phải là 'assistant'
        if st.session_state['messages'][-1]['user'] != " assistant ":
            with st.chat_message('assistant'):
                # mục đích là hiển thị đang load câu trả lời
                with st.spinner('Thinking...'):
                    response = generate_respond(promt, hf_mail, hf_pass)
                    st.write(response)
                # mục đích tạo một dict() mới
            messages = {'user': 'assistant', 'content': response}
            # chèn cả cụm dict() này vào lịch sử chat
            st.session_state['messages'].append(messages)


if __name__ == '__main__':
    main()
