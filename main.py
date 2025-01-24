import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정 (Mac: 'AppleGothic')
plt.rc('font', family='AppleGothic')  # Mac 사용자를 위한 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# Streamlit app title
st.title("월별 기온 분포 박스플롯 시각화")

# File uploader
uploaded_file = st.file_uploader("데이터 파일을 업로드하세요:", type=["csv"])

# Cache the data loading function
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    try:
        data = load_data(uploaded_file)
        
        # Preprocess the data
        data['날짜'] = pd.to_datetime(data['날짜'], errors='coerce')  # Ensure '날짜' is datetime
        data = data.dropna(subset=['날짜'])  # Remove invalid dates
        data['월'] = data['날짜'].dt.month  # Extract the month
        
        # Select month
        month = st.selectbox("월을 선택하세요:", range(1, 13))
        
        # Filter data for the selected month
        filtered_data = data[data['월'] == month]
        
        # Check if there is data for the selected month
        if filtered_data.empty:
            st.warning(f"{month}월에 대한 데이터가 없습니다.")
        else:
            # Prepare data for boxplot
            boxplot_data = [
                filtered_data['평균기온(℃)'].dropna(),
                filtered_data['최저기온(℃)'].dropna(),
                filtered_data['최고기온(℃)'].dropna(),
            ]
            
            # Check if all datasets are empty
            if all([len(temp) == 0 for temp in boxplot_data]):
                st.warning(f"{month}월의 기온 데이터가 없습니다.")
            else:
                # Create a boxplot for the temperature data
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.boxplot(
                    boxplot_data,
                    labels=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'],
                    patch_artist=True,  # Fill boxplot with color
                    boxprops=dict(facecolor='lightblue', color='blue'),
                    medianprops=dict(color='red'),
                )
                ax.set_title(f"{month}월 기온 분포", fontsize=16)
                ax.set_ylabel("기온 (℃)", fontsize=14)
                ax.grid(True, linestyle='--', alpha=0.6)
                
                # Display the plot
                st.pyplot(fig)
    except KeyError as e:
        st.error(f"데이터에 필요한 컬럼이 없습니다: {e}")
else:
    st.warning("데이터 파일을 업로드해주세요.")
