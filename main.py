import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 경로
DATA_PATH = "daily_temp.csv"

# 데이터 로드
@st.cache
def load_data(path):
    return pd.read_csv(path)

data = load_data(DATA_PATH)

# 날짜 데이터를 날짜 형식으로 변환 및 월 열 추가
data['date'] = pd.to_datetime(data['date'])
data['month'] = data['date'].dt.month

# 제목과 설명 추가
st.title("월별 기온 분포 박스플롯")
st.write("월을 선택하면 해당 월의 기온 분포를 박스플롯으로 확인할 수 있습니다.")

# 월 선택 위젯
selected_month = st.selectbox("월을 선택하세요:", sorted(data['month'].unique()))

# 선택한 월의 데이터 필터링
month_data = data[data['month'] == selected_month]

# 박스플롯 그리기
if not month_data.empty:
    fig, ax = plt.subplots()
    ax.boxplot(month_data['temperature'], vert=True, patch_artist=True, labels=[f"{selected_month}월"])
    ax.set_title(f"{selected_month}월의 기온 분포")
    ax.set_ylabel("기온 (°C)")
    st.pyplot(fig)
else:
    st.warning("선택한 월에 해당하는 데이터가 없습니다.")
