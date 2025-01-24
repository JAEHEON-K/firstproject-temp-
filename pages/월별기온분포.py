import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit app title
st.title("12달의 기온 분포 박스플롯 시각화")


# Cache the data loading function
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    try:
        # Load and preprocess data
        data = load_data(uploaded_file)
        data['날짜'] = pd.to_datetime(data['날짜'], errors='coerce')  # Ensure '날짜' is datetime
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

    except KeyError as e:
        st.error(f"데이터에 필요한 컬럼이 없습니다: {e}")
else:
    st.warning("데이터 파일을 업로드해주세요.")
