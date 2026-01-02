import streamlit as st
import pandas as pd
import os
from datetime import datetime


# --- 파비콘 X, 브라우저 명 ---
st.set_page_config(
    page_title="업무 기록_Lordnine",
    page_icon="🌟"
)


# --- 설정 및 암호 ---
EXCEL_FILE = 'Py1.xlsx'
PASSWORD = "0421" # 로그인 암호
SOURCE_FOLDER = "DHM_업무기록"

# 엑셀 초기화 함수
def init_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['날짜', '분류', '내용', '태그', '비고'])
        df.to_excel(EXCEL_FILE, index=False)

# 암호 확인 함수
def check_password():
    """암호가 맞으면 True를 반환합니다."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # 로그인 화면 UI
    st.title("🔒 암호 입력")
    password_input = st.text_input("암호를 입력하세요", type="password")
    
    if st.button("로그인"):
        if password_input == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("암호가 틀렸습니다.")
    return False

# 폴더 내 모든 엑셀 파일 불러와서 합치기
def load_all_excel_files(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return pd.DataFrame()
    all_files = os.listdir(folder_path)
    excel_files = [f for f in all_files if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        return pd.DataFrame()
    df_list = []
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        try:
            temp_df = pd.read_excel(file_path)
            df_list.append(temp_df)
        except Exception as e:
            st.warning(f"{file} 파일 읽기 오류: {e}")
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()
        
# --- 메인 로직 시작 ---
st.set_page_config(page_title="보안 엑셀 매니저", layout="wide")

if check_password():
    # 로그인 성공 시에만 아래 코드가 실행됩니다.
    init_excel()
    
    # 상단 로그아웃 버튼 (선택 사항)
    if st.sidebar.button("로그아웃"):
        st.session_state["password_correct"] = False
        st.rerun()
    st.image("https://yt3.googleusercontent.com/D1nWjc4h1lP25Mxa0Y8mfmyE5OUszgEgeqqd_xxSwtE37TZv2CvD-VhuiXUsZAopSTTFmnwgmw=s900-c-k-c0x00ffffff-no-rj", width=30)
    st.title("DHM 업무 기록")

    # 데이터 불러오기
    try:
        df = pd.read_excel(EXCEL_FILE)
    except:
        df = pd.DataFrame(columns=['날짜', '내용', '태그'])

    # 사이드바: 입력 기능
    with st.sidebar:
        st.header("📝 새로운 데이터 입력")
        new_content = st.text_area("내용을 입력하세요")
        new_tag = st.selectbox("카테고리", ["이슈", "공지", "기타"])
        
        if st.button("엑셀에 저장하기"):
            if new_content.strip():
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_row = pd.DataFrame([[now, new_content, new_tag]], columns=['날짜', '내용', '태그'])
                updated_df = pd.concat([df, new_row], ignore_index=False)
                updated_df.to_excel(EXCEL_FILE, index=False)
                st.success("성공적으로 저장되었습니다!")
                st.rerun()

    # 메인 화면: 검색 기능
    st.subheader("🔍 검색 및 조회")
    search_term = st.text_input("검색어를 입력하세요")

    if search_term:
        res = df[df['내용'].str.contains(search_term, na=False, case=False)]
        st.write(f"총 {len(res)}건의 결과가 있습니다.")
        st.table(res) # 경고창을 줄이기 위해 table 사용
    else:
        st.write("전체 데이터 목록:")
        st.dataframe(df, width=1000) # 가로 너비 설정