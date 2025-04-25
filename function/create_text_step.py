from classes import StepText, StepikAPI

def create_text_step_in_lesson(lesson_id: int, position: int, title: str, content: str):
    """
    Создает текстовый шаг в указанном уроке
    
    Args:
        lesson_id: ID существующего урока
        position: Позиция шага в уроке (начиная с 1)
        title: Заголовок шага
        content: HTML-содержимое шага
    """
    # Получаем токен
    token = StepikAPI.get_token()
    
    # Создаем объект текстового шага
    text_step = StepText(
        step_id=0,  # 0 - так как шаг новый
        title=title,
        content=content
    )
    
    try:
        # Создаем шаг в уроке
        result = text_step.create(lesson_id, position, token)
        step_id = result['step-sources'][0]['id']
        
        print(f"Текстовый шаг успешно создан!")
        print(f"ID шага: {step_id}")
        print(f"Предпросмотр: https://stepik.org/lesson/{lesson_id}/step/{position}")
        
        return step_id
        
    except Exception as e:
        print(f"Ошибка при создании шага: {str(e)}")
        return None

if __name__ == "__main__":
    # Пример использования
    LESSON_ID = 1731206  # Замените на ID вашего урока
    STEP_POSITION = 1    # Позиция шага в уроке
    
    step_content = """
    <h2>Добро пожаловать на новый шаг!</h2>
    <p>Это пример текстового шага, созданного через API Stepik.</p>
    <ul>
        <li>Пункт 1</li>
        <li>Пункт 2</li>
        <li>Пункт 3</li>
    </ul>
    <p>Вы можете использовать <strong>HTML-разметку</strong> для форматирования.</p>
    """
    
    created_step_id = create_text_step_in_lesson(
        lesson_id=LESSON_ID,
        position=STEP_POSITION,
        title="Новый текстовый шаг",
        content=step_content
    )