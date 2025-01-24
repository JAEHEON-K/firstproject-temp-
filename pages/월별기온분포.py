import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit app title
st.title("12달의 기온 분포 박스플롯 시각화")

# File uploader
uploaded_file = st.file_uploader("데이터 파일을 업로드하세요:", type=["csv"])

# Cache the data loading function
@st.cache_data
def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

if uploaded_file is not None:
    try:
        # Load and inspect data
        data = load_data(uploaded_file)
        if data is None:
            st.stop()

        # 컬럼 이름 출력
        st.write("업로드된 데이터의 컬럼:")
        st.write(data.columns.tolist())

        # '날짜' 컬럼 확인 및 처리
        if '날짜' not in data.columns:
            st.error("데이터셋에 '날짜' 컬럼이 없습니다. CSV 파일을 확인해주세요.")
            st.stop()

        # Convert '날짜' to datetime
        data['날짜'] = pd.to_datetime(data['날짜'].str.strip(), format="%Y-%m-%d", errors='coerce')
        data = data.dropna(subset=['날짜'])  # Remove invalid dates
        data['월'] = data['날짜'].dt.month  # Extract the month

        # Melt data for interactive plotting
        melted_data = pd.melt(
            data,
            id_vars=['월'],
            value_vars=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'],
            var_name='기온유형',
            value_name='기온값'
        )

        # Plotly boxplot
        fig = px.box(
            melted_data,
            x="월",
            y="기온값",
            color="기온유형",
            title="12달의 기온 분포",
            labels={"월": "월", "기온값": "기온 (℃)", "기온유형": "기온 유형"},
            category_orders={"월": list(range(1, 13))}  # Ensure months are in order
        )
        fig.update_layout(
            xaxis=dict(title="월", tickmode="linear"),
            yaxis=dict(title="기온 (℃)"),
            boxmode='group'  # Group boxes by 기온유형
        )

        # Show plot
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"처리 중 오류가 발생했습니다: {e}")
else:
    st.warning("데이터 파일을 업로드해주세요.")
