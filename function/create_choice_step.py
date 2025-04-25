from classes import StepText, StepikAPI

def create_text_task(lesson_id: int, position: int = 2):
    """
    Создает текстовую задачу в указанном уроке
    
    Args:
        lesson_id: ID урока
        position: Позиция шага (по умолчанию 2)
    """
    token = StepikAPI.get_token()
    
    task_content = """
    <h3>Текстовая задача</h3>
    <p>Решите следующую задачу:</p>
    <blockquote>
        У Пети было 5 яблок, а у Маши на 3 яблока больше. Сколько всего яблок у детей?
    </blockquote>
    <p>Напишите ответ в поле ниже:</p>
    """
    
    text_task = StepText(
        step_id=0,  # 0 для нового шага
        title="Текстовая задача",
        content=task_content
    )
    
    try:
        result = text_task.create(lesson_id, position, token)
        step_id = result['step-sources'][0]['id']
        
        print(f"Текстовая задача создана в шаге {position}!")
        print(f"ID шага: {step_id}")
        print(f"Ссылка: https://stepik.org/lesson/{lesson_id}/step/{position}")
        return step_id
        
    except Exception as e:
        print(f"Ошибка при создании задачи: {str(e)}")
        return None

if __name__ == "__main__":
    LESSON_ID = 1731206  # Замените на ID вашего урока
    
    # Создаем текстовую задачу в шаге 2
    create_text_task(LESSON_ID, position=2)