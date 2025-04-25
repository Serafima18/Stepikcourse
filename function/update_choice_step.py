from classes import StepText, StepikAPI

def update_step_content(step_url: str, new_content: str):
    """
    Обновляет содержимое текстового шага
    
    Args:
        step_url: URL шага (например, "https://stepik.org/lesson/123/step/1")
        new_content: Новое HTML-содержимое
    """
    token = StepikAPI.get_token()
    
    # Получаем текущий заголовок шага (можно изменить, если нужно)
    current_title = "Теория"  # Или получить автоматически через API
    
    updated_step = StepText(
        step_id=0,  # ID будет получен из URL
        title=current_title,
        content=new_content
    )
    
    try:
        result = updated_step.update(step_url, token)
        print(f"Шаг {step_url} успешно обновлен!")
        return result
    except Exception as e:
        print(f"Ошибка при обновлении: {str(e)}")
        return None

if __name__ == "__main__":
    # Теория в шаге 1
    THEORY_STEP_URL = "https://stepik.org/lesson/1731206/step/2"  # Замените на ваш URL
    
    theory_content = """
    <h2>Теория: Сложение чисел</h2>
    <p>Сложение - это базовая математическая операция.</p>
    
    <h3>Основные понятия:</h3>
    <ul>
        <li><strong>Слагаемые</strong> - числа, которые складываются</li>
        <li><strong>Сумма</strong> - результат сложения</li>
    </ul>
    
    <h3>Пример:</h3>
    <p>3 + 5 = 8</p>
    <p>Где:
        <br>3 - первое слагаемое
        <br>5 - второе слагаемое
        <br>8 - сумма
    </p>
    """
    
    update_step_content(THEORY_STEP_URL, theory_content)