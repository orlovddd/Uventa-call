import math
from typing import Tuple, Optional

def validate_inputs(length: float, max_post_spacing: float, sheet_width: float, overlap: float) -> Tuple[bool, Optional[str]]:
    """Validate input parameters for fence calculation."""
    if length <= 0:
        return False, "Длина участка должна быть положительным числом"
    if max_post_spacing <= 0:
        return False, "Расстояние между столбами должно быть положительным числом"
    if sheet_width <= 0:
        return False, "Ширина профлиста должна быть положительным числом"
    if overlap < 0:
        return False, "Нахлест не может быть отрицательным"
    if overlap >= sheet_width:
        return False, "Нахлест должен быть меньше ширины профлиста"
    return True, None

def calculate_fence_materials(length: float, max_post_spacing: float, sheet_width: float, overlap: float) -> Tuple[int, int, int, float]:
    """Calculate fence materials requirements."""
    # Расчет количества пролетов и столбов
    num_spans = math.ceil(length / max_post_spacing)
    actual_spacing = length / num_spans
    num_posts = num_spans + 1

    # Расчет общего количества листов
    effective_width = sheet_width - overlap  # Полезная площадь одного листа
    total_required_coverage = length  # Общая необходимая длина покрытия
    total_sheets = math.ceil(total_required_coverage / effective_width)  # Округляем вверх общее количество листов

    return num_posts, num_spans, total_sheets, actual_spacing
