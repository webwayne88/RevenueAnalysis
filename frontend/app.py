import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BACKEND_URL = "http://localhost:8000"  


def upload_zip_file():
    """Блок загрузки файла"""
    uploaded_file = st.file_uploader(
        "Загрузите ZIP-архив с Excel-файлами", 
        type="zip",
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
                f"{BACKEND_URL}/analyze",
                files=files
            )
            if response.status_code == 200:
                return response.json()
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


if __name__=='__main__':
    st.set_page_config(page_title="Анализ динамики выручки компании", layout="wide")
    st.title("Анализ динамики выручки компании")

    zip_file = upload_zip_file()

    if zip_file:
        data = process_file(zip_file)
        if data:
            df = pd.DataFrame(
                data["revenue_data"].items(),
                columns=["Год", "Выручка"]
            )
            df = df.set_index("Год")

            st.subheader("Динамика выручки по годам")
            st.plotly_chart(create_plot(df), use_container_width=True)

            st.subheader('Аналитический отчет')
            analysis = data["llm_response"]["analysis"]

            blocks = [block.strip() for block in analysis.split("---")]

            for block in blocks:
                if not block:
                    continue

                header = block.split("\n")[0].strip("*").strip()
                body = "\n".join(block.split("\n")[1:]).strip()
                
                with st.expander(header):
                    st.markdown(body)
            

