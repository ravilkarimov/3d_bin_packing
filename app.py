import random
import streamlit as st
from src.types import Box
from src.plot import plot_boxes
from src.model import ThreeDimPacking


st.set_page_config(
    page_title="3D Bin Packing by Devs",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None)
st.title("3D Bin Packing by Devs")

B_COL1, B_COL2 = st.columns(2)
with B_COL1:

    st.subheader("Параметры главного параллелелипида")
    col1, col2, col3 = st.columns(3)
    with col1:
        width = st.number_input('Ширина', 1, 100, 10)
    with col2:
        height = st.number_input('Высота', 1, 100, 10)
    with col3:
        length = st.number_input('Длина', 1, 100, 10)
    box = Box(width, height, length)

    # TODO: add option to manually add rectangles
    st.subheader("Параметры случайной генерации параллелелипидов для упаковки")
    num_boxes = st.number_input('Количество коробок для генерации', 1, 50, 10)
    col1, col2 = st.columns(2)
    with col1:
        min_width = st.number_input('Мин ширина', 1, 100, 2)
    with col2:
        max_width = st.number_input('Макс ширина', 1, 100, 10)

    col1, col2 = st.columns(2)
    with col1:
        min_height = st.number_input('Миш высота', 1, 100, 2)
    with col2:
        max_height = st.number_input('Макс высота', 1, 100, 10)

    col1, col2 = st.columns(2)
    with col1:
        min_length = st.number_input('Мин длина', 1, 100, 2)
    with col2:
        max_length = st.number_input('Макс длина', 1, 100, 10)

    items = [Box(
        random.randint(min_width, max_width),
        random.randint(min_height, max_height),
        random.randint(min_length, max_length))
        for _ in range(num_boxes)
    ]
    with st.expander('Показать параметры сгенерированных коробок'):
        st.write(items)

with B_COL2:
    model = ThreeDimPacking(box, items)
    model.solve()
    positions: list[list[int]] = model.get_result()
    if positions:
        packed_boxes = []
        unpacked_boxes = []
        for i in range(num_boxes):
            x, y, z = positions[i]
            if -1 in (x, y, z):
                unpacked_boxes.append(i)
                continue
            items[i].set_position(x, y, z)
            packed_boxes.append(items[i])

        st.subheader("Результат оптимальной упаковки")
        if unpacked_boxes:
            st.info('Недостаточно места для коробок под номерами: %s' % (
                " ".join(map(str, unpacked_boxes))))
        fig = plot_boxes((box.width, box.height, box.length), packed_boxes)
        st.plotly_chart(fig)

        with st.expander('Показать параметры коробок после упаковки'):
            st.write(items)
    else:
        st.error('Решение не найдено')
