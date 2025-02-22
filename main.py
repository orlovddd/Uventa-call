import streamlit as st
import plotly.graph_objects as go
from calculator import validate_inputs, calculate_fence_materials
from datetime import datetime

def create_fence_visualization(num_posts: int, num_spans: int, actual_spacing: float):
    """Create a visual representation of the fence."""
    fig = go.Figure()

    # Add posts (including underground part)
    for i in range(num_posts):
        fig.add_trace(go.Scatter(
            x=[i * actual_spacing, i * actual_spacing],
            y=[-1.2, 1.8],  # From -1.2m (underground) to 1.8m above ground
            mode='lines',
            line=dict(color='brown', width=10),
            name='Столб' if i == 0 else None,
            showlegend=(i == 0)
        ))

        # Add horizontal bars between posts
        if i < num_posts - 1:
            # Upper bar at 1.75m
            fig.add_trace(go.Scatter(
                x=[i * actual_spacing, (i + 1) * actual_spacing],
                y=[1.75, 1.75],
                mode='lines',
                line=dict(color='brown', width=5),
                name='Поперечина' if i == 0 else None,
                showlegend=(i == 0)
            ))
            # Lower bar at 0.3m
            fig.add_trace(go.Scatter(
                x=[i * actual_spacing, (i + 1) * actual_spacing],
                y=[0.3, 0.3],
                mode='lines',
                line=dict(color='brown', width=5),
                showlegend=False
            ))

        # Add dashed line to show ground level
        if i == 0:
            fig.add_trace(go.Scatter(
                x=[0, (num_posts - 1) * actual_spacing],
                y=[0, 0],
                mode='lines',
                line=dict(color='black', width=1, dash='dash'),
                name='Уровень земли',
                showlegend=True
            ))

    # Add sheets with pattern
    for i in range(num_spans):
        # Create pattern with vertical lines
        x_pattern = []
        y_pattern = []
        num_lines = 15  # Increased number of lines for better density
        
        for j in range(num_lines):
            x_pos = i * actual_spacing + (j/num_lines) * actual_spacing
            x_pattern.extend([x_pos, x_pos, None])
            y_pattern.extend([0, 2, None])

        # Add patterned sheet
        fig.add_trace(go.Scatter(
            x=x_pattern,
            y=y_pattern,
            mode='lines',
            line=dict(color='green', width=1),
            fill=None,
            name='Профлист' if i == 0 else None,
            showlegend=(i == 0)
        ))
        
        # Add outline
        fig.add_trace(go.Scatter(
            x=[i * actual_spacing, i * actual_spacing, (i + 1) * actual_spacing, (i + 1) * actual_spacing],
            y=[0, 2, 2, 0],
            mode='lines',
            line=dict(color='green', width=2),
            fill='tonexty',
            fillcolor='rgba(0,255,0,0.1)',
            showlegend=False
        ))

    fig.update_layout(
        title="Схема забора",
        xaxis_title="Длина (м)",
        yaxis_title="Высота (м)",
        showlegend=True,
        height=400,  # Увеличим высоту для лучшей видимости подземной части
        margin=dict(l=50, r=50, t=50, b=50),
        yaxis=dict(
            range=[-1.4, 2.0],  # Расширим диапазон для отображения подземной части
            zeroline=False
        )
    )

    return fig

def save_calculation_to_history(length, max_post_spacing, sheet_width, overlap, num_posts, num_spans, total_sheets):
    """Save calculation results to history."""
    if 'calculation_history' not in st.session_state:
        st.session_state.calculation_history = []

    calculation = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'parameters': {
            'length': length,
            'max_post_spacing': max_post_spacing,
            'sheet_width': sheet_width,
            'overlap': overlap
        },
        'results': {
            'num_posts': num_posts,
            'num_spans': num_spans,
            'total_sheets': total_sheets,
            'caps': num_posts,
            'fasteners': total_sheets * 10
        }
    }

    st.session_state.calculation_history.insert(0, calculation)  # Add new calculation at the beginning

def show_calculation_history():
    """Display calculation history."""
    if 'calculation_history' not in st.session_state or not st.session_state.calculation_history:
        st.info("История расчетов пуста")
        return

    st.subheader("📋 История расчетов")

    # Add buttons in the same row
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Очистить историю"):
            st.session_state.calculation_history = []
            st.experimental_rerun()
    
    for idx, calc in enumerate(st.session_state.calculation_history):
        with st.expander(f"Расчет от {calc['timestamp']}"):
            # Формируем текст для копирования
            copy_text = f"""
Расчет забора от {calc['timestamp']}
Параметры:
- Длина участка: {calc['parameters']['length']} м
- Расстояние между столбами: {calc['parameters']['max_post_spacing']} м
- Ширина профлиста: {calc['parameters']['sheet_width']} м
- Нахлест: {calc['parameters']['overlap']} м

Результаты:
- Количество столбов: {calc['results']['num_posts']} шт.
- Количество секций: {calc['results']['num_spans']} шт.
- Количество профлистов: {calc['results']['total_sheets']} шт.
- Количество поперечин: {calc['results']['num_spans'] * 2} шт.

Дополнительные материалы:
- Заглушки для столбов: {calc['results']['num_posts']} шт.
- Крепежные элементы: {calc['results']['total_sheets'] * 10} шт.
            """
            # Add copy button
            st.code(copy_text, language="text")
            st.button("📋 Копировать", key=f"copy_{idx}", help="Копировать результаты расчета")
            st.write("Параметры забора:")
            st.write(f"- Длина участка: {calc['parameters']['length']} м")
            st.write(f"- Расстояние между столбами: {calc['parameters']['max_post_spacing']} м")
            st.write(f"- Ширина профлиста: {calc['parameters']['sheet_width']} м")
            st.write(f"- Нахлест: {calc['parameters']['overlap']} м")

            st.write("Результаты:")
            st.write(f"- Количество столбов: {calc['results']['num_posts']} шт.")
            st.write(f"- Количество секций: {calc['results']['num_spans']} шт.")
            st.write(f"- Количество профлистов: {calc['results']['total_sheets']} шт.")
            
            st.write("Дополнительные материалы:")
            st.write(f"- Заглушки для столбов: {calc['results']['num_posts']} шт.")
            st.write(f"- Крепежные элементы: {calc['results']['total_sheets'] * 10} шт.")

def main():
    st.set_page_config(
        page_title="Калькулятор материалов для забора",
        page_icon="🏗️",
        layout="wide"
    )

    st.title("🏗️ Калькулятор материалов для забора из профлиста")

    # Добавляем описание
    st.markdown("""
    Этот калькулятор поможет рассчитать необходимое количество материалов для строительства забора.
    Введите параметры вашего участка и характеристики материалов ниже.
    """)

    # Создаем две колонки для ввода данных и вывода результатов
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📏 Параметры забора")

        length = st.number_input(
            "Длина участка (м)",
            min_value=0.0,
            value=10.0,
            step=0.1,
            help="Введите общую длину забора в метрах"
        )

        max_post_spacing = st.number_input(
            "Максимальное расстояние между столбами (м)",
            min_value=0.0,
            value=2.5,
            step=0.1,
            help="Рекомендуемое расстояние между столбами обычно составляет 2.5-3 метра"
        )

        sheet_width = st.number_input(
            "Ширина профлиста (м)",
            min_value=0.0,
            value=1.2,
            step=0.01,
            help="Стандартная ширина листа профнастила"
        )

        overlap = st.number_input(
            "Нахлест между профлистами (м)",
            min_value=0.0,
            value=0.05,
            step=0.01,
            help="Рекомендуемый нахлест между листами профнастила"
        )

    # Валидация введенных данных
    is_valid, error_message = validate_inputs(length, max_post_spacing, sheet_width, overlap)

    if not is_valid:
        st.error(error_message)
    else:
        # Расчет материалов
        num_posts, num_spans, total_sheets, actual_spacing = calculate_fence_materials(
            length, max_post_spacing, sheet_width, overlap
        )

        # Сохраняем результат в историю
        save_calculation_to_history(length, max_post_spacing, sheet_width, overlap,
                                      num_posts, num_spans, total_sheets)

        with col2:
            st.subheader("📊 Результаты расчета")

            # Создаем красивые метрики
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)

            col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
            with col_metrics1:
                st.metric("Количество столбов", f"{num_posts} шт.")
            with col_metrics2:
                st.metric("Количество секций", f"{num_spans} шт.")
            with col_metrics3:
                st.metric("Количество профлистов", f"{total_sheets} шт.")
            with col_metrics4:
                st.metric("Количество поперечин", f"{num_spans * 2} шт.")
            
            # Добавляем дополнительные материалы
            with st.expander("Дополнительные материалы"):
                st.write(f"• Заглушки для столбов: {num_posts} шт. (по 1 шт. на столб)")
                st.write(f"• Крепежные элементы: {total_sheets * 10} шт. (по 10 шт. на профлист)")

            # Дополнительная информация
            st.info(f"""
            📌 Расстояние между столбами: {max_post_spacing:.2f} м\n
            💡 Рекомендации:\n
            - Глубина установки столбов: от 1 до 2 м\n
            - Используйте металлические столбы сечением 60х60 мм\n
            - Не забудьте про крепежные элементы и заглушки для столбов
            """)

        # Визуализация забора
        st.subheader("🎨 Визуализация забора")
        fig = create_fence_visualization(num_posts, num_spans, actual_spacing)
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape'],
            'modeBarButtonsToRemove': [],
            'scrollZoom': True
        })

        # Показываем историю расчетов
        show_calculation_history()

if __name__ == "__main__":
    main()