import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BACKEND_URL = "http://localhost:8000"  

def upload_file():
    """Блок загрузки файла"""
    uploaded_file = st.file_uploader(
        "Загрузите ZIP-архив с Excel-файлами", 
        type="zip",
        help="Архив должен содержать файлы в формате ГГГГ.xlsx (например: 2020.xlsx)"
    )
    
    if uploaded_file:
        return uploaded_file
    return None


def process_file(uploaded_file):
    """Отправка файла на бэкенд и обработка результатов"""
    with st.spinner("Обработка данных..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(
                f"{BACKEND_URL}/process_zip",
                files=files
            )
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame.from_dict(data, orient='index', columns=['Выручка'])
                df.index = df.index.astype(int)
                df.sort_index(inplace=True)
                return df
            else:
                st.error(f"Ошибка обработки файла: {response.json().get('detail', 'Неизвестная ошибка')}")
                return None
                
        except Exception as e:
            st.error(f"Ошибка соединения с сервером: {str(e)}")
            return None


def create_plot(df):
    """Отображение графика"""
    
    fig = px.line(
        df, 
        x=df.index, 
        y="Выручка",
        title="Динамика выручки по годам",
        labels={"index": "Год", "Выручка": "Выручка, руб."},
        markers=True,
        line_shape="linear",
        template="plotly_white"
    )
    fig.update_traces(line_color="#4CAF50", line_width=3)
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Год",
        yaxis_title="Выручка (руб.)",
        font=dict(family="Arial", size=12))
    return fig 


def llm_analysis(df):
    """Отображение анализа данных"""    
    response = requests.post(
        f"{BACKEND_URL}/get-analysis",  # или ваш URL API
        json={"data": df['Выручка'].to_dict()},
        timeout=20
    )
    
    if response.status_code == 200:
        analysis = response.json().get("analysis", "")
        return analysis

    
def main():
    st.set_page_config(page_title="Анализ динамики выручки компании")
    st.title("Анализ динамики выручки компании")
    uploaded_file = upload_file()

    if uploaded_file:
        df = process_file(uploaded_file)
        if df is not None:
            st.plotly_chart(create_plot(df), use_container_width=True)
            st.subheader('Аналитический отчет')
            analysis = llm_analysis(df)
            if analysis:
                blocks = analysis.split('block')
                with st.expander('Основные показатели'):
                        st.markdown(blocks[0])
                with st.expander('Анализ динамики'):
                        st.markdown(blocks[1])
                with st.expander('Итоговые выводы'):
                        st.markdown(blocks[2])
                
if __name__=='__main__':
    main()