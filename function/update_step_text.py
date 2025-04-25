from classes import StepText, StepikAPI

def update_text_step(step_url: str, new_title: str, new_content: str):
    """
    Обновляет существующий текстовый шаг
    
    Args:
        step_url: Полный URL шага (например, "https://stepik.org/lesson/123/step/1")
        new_title: Новый заголовок шага
        new_content: Новое HTML-содержимое шага
    """
    # Получаем токен
    token = StepikAPI.get_token()
    
    # Создаем объект текстового шага с новыми данными
    updated_step = StepText(
        step_id=0,  # ID будет получен из URL
        title=new_title,
        content=new_content
    )
    
    try:
        # Обновляем шаг
        result = updated_step.update(step_url, token)
        
        print("Текстовый шаг успешно обновлен!")
        print(f"Новый заголовок: {new_title}")
        print(f"Ссылка: {step_url}")
        
        return result
        
    except Exception as e:
        print(f"Ошибка при обновлении шага: {str(e)}")
        return None

if __name__ == "__main__":
    # Пример использования
    STEP_URL = "https://stepik.org/lesson/1731206/step/1"  # Замените на URL вашего шага
    
    new_content = """
    <h2>Обновленный текстовый шаг</h2>
    <p>Этот шаг был успешно обновлен через API Stepik.</p>
    <ul>
        <li>Новый пункт 1</li>
        <li>Новый пункт 2</li>
    </ul>
    <p><em>Обновленное содержимое</em> с HTML-разметкой.</p>
    """
    
    update_result = update_text_step(
        step_url=STEP_URL,
        new_title="Обновленный текстовый шаг",
        new_content=new_content
    )