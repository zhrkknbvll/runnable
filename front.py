import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/pdd/predict/"

st.title("Распознавание дорожных знаков")

file = st.file_uploader("Загрузите фото знака", type=["jpg", "jpeg", "png"])

if file:
    st.image(file, width=250)

    if st.button("Определить"):
        try:
            with st.spinner("Подождите..."):
                response = requests.post(
                    API_URL,
                    files={"file": (file.name, file.getvalue(), file.type)},
                    timeout=130,
                )
        except requests.exceptions.ConnectionError:
            st.error("Сервер не запущен (запусти python main.py)")
        else:
            if response.status_code == 200:
                data = response.json()
                st.success(data["class_name"])
                st.write("Категория:", data["category"])
                st.write("Описание:", data["description"])
                st.write("Класс:", data["class_id"])
            else:
                st.error(response.json().get("detail", "Ошибка"))
