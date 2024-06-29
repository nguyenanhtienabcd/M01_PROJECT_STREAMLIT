import streamlit as st  # type: ignore

# ĐỊNH NGHĨA MỘT HÀM ĐỌC DỮ LIỆU TỪ FILE


def open_file(uploaded_file):
    if uploaded_file is None:
        return
    # đọc file txt, chuyển đổi kiểu dữ liệu byte sang str
    read_file = uploaded_file.read().decode('utf-8')
    # chuyển đổi một chuỗi thành 1 list
    processed_file = read_file.replace('\n', ' ').lower().split()
    words = sorted(list(set(processed_file)))
    return words


# ĐỊNH NGHĨA MỘT HÀM ĐỌC levenshtein_distance


def levenshtein_distance(source, target):
    n_source = len(source) + 1
    m_target = len(target) + 1
    # tạo ra ma trận nxm với các phần tử bên trong là số 0
    dp = [[0] * (m_target) for _ in range(n_source)]

    # update lại hàng 0 và cột 0 của ma trận dp
    for i in range(n_source):
        dp[i][0] = i
    for j in range(m_target):
        dp[0][j] = j

    # tính toán khoảng cách levenshtein
    for i in range(1, n_source):
        for j in range(1, m_target):
            # so sánh ký tự thứ i-1 của source và ký tự thứ j-1 của target
            if source[i-1] == target[j-1]:
                cost = 0
            else:
                cost = 1
            d_del = dp[i-1][j] + 1  # delete
            d_ins = dp[i][j-1] + 1  # insert
            d_sub = dp[i-1][j-1] + cost  # subtituation
            # tìm giá trị nhỏ nhất của 3 công thứ trên
            dp[i][j] = min(d_del, d_ins, d_sub)
    result = dp[n_source-1][m_target-1]
    return result


def main(vocab):
    st.title('Word correction using Levenshtein Distance')
    word = st.text_input('word:', value='Bok')
    if st.button('compute'):
        levenshtein_dis = dict()
        for each_word in vocab:
            # tạo một dict() chứa khoảng cách levenshtein so với từ gốc
            levenshtein_dis[each_word] = levenshtein_distance(word, each_word)
        # sắp xếp theo thứ tụ từ thấp đến cao theo khoảng cách levenstein
        sorted_levenshtein = dict(
            sorted(levenshtein_dis.items(), key=lambda x: x[1]))
        # tạo một list chứa các key đã được sort trong dict
        sorted_levenshtein_lst = list(sorted_levenshtein.keys())
        min_levenshtein = sorted_levenshtein_lst[0]  # Lấy phần tử đầu tiên
        st.write('correct word:', min_levenshtein)
        col1, col2 = st.columns(2)
        col1 . write('Vocabulary')
        col1 . write(vocab)

        col2 . write('distances')
        col2 . write(sorted_levenshtein)


if __name__ == '__main__':
    # tải file .txt từ bên ngoài vào
    uploaded_file = st.file_uploader('Upload file .txt', type='txt')
    vocab = open_file(uploaded_file)    # gọi hàm xử lý file
    main(vocab)
