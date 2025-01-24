import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'daily_temp.csv'
data = pd.read_csv(file_path)

# Preprocess the data
data['날짜'] = pd.to_datetime(data['날짜'])  # Convert '날짜' to datetime format
data['월'] = data['날짜'].dt.month         # Extract the month

# Streamlit app title
st.title("월별 기온 분포 박스플롯 시각화")

# Select month
month = st.selectbox("월을 선택하세요:", range(1, 13))

# Filter data for the selected month
filtered_data = data[data['월'] == month]

# Check if there is data for the selected month
if filtered_data.empty:
    st.warning("선택한 월에 대한 데이터가 없습니다.")
else:
    # Create a boxplot for the temperature data
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot([
        filtered_data['평균기온(℃)'].dropna(),
        filtered_data['최저기온(℃)'].dropna(),
        filtered_data['최고기온(℃)'].dropna()
    ],
    labels=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    
    ax.set_title(f"{month}월 기온 분포")
    ax.set_ylabel("기온 (℃)")
    
    # Display the plot
    st.pyplot(fig)
