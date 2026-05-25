import streamlit as st
import subprocess
import platform
import time
from pathlib import Path

# В Windows добавляем .exe, в Linux/Mac оставляем ./app
binary_name = "app.exe" if platform.system() == "Windows" else "app"
APP_BINARY = Path(__file__).parent / binary_name

st.set_page_config(page_title="Stack Overflow Search", layout="wide")
st.title("Stack Overflow Search")
st.caption("Инвертированный индекс на AVL / Red-Black / B-tree")

col_left, col_right = st.columns([3, 1])

with col_left:
    query = st.text_input("Поисковый запрос", placeholder="python list sort")

with col_right:
    tree_type = st.selectbox("Структура данных", ["avl", "rb", "btree"])

search_clicked = st.button("Найти", use_container_width=True)

if search_clicked:
    if not query.strip():
        st.warning("Введите запрос")
    elif not APP_BINARY.exists():
        st.error(f"Бинарник не найден: {APP_BINARY}\nСобери проект командой gcc из прошлого сообщения!")
    else:
        with st.spinner("Индексация и поиск..."):
            # Запускаем БЕЗ флага --json, так как наш C его не поддерживает
            proc = subprocess.run(
                [str(APP_BINARY), "search", f"--type={tree_type}", query],
                capture_output=True,
                text=True,
                encoding='utf-8', # Важно для кириллицы/спецсимволов
                timeout=600,       # Увеличил таймаут, так как данных много
            )

        if proc.returncode != 0:
            st.error(f"Ошибка выполнения (код {proc.returncode}):\n```\n{proc.stderr}\n```")
        else:
            # Выводим «сырой» текст из консоли Си-программы
            output = proc.stdout

            if "Найдено: 0 документов" in output or not output.strip():
                st.info("Ничего не найдено")
            else:
                # Рисуем красивую рамку с результатом
                st.markdown("### Результаты поиска")
                st.code(output, language="text")

            # Вывод логов для отладки внизу
            with st.expander("Техническая информация (Debug)"):
                st.text(f"Команда: {' '.join(proc.args)}")
                st.text(f"Размер вывода: {len(output)} байт")
