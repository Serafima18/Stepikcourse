import requests
import re
from update_choice_step import update_choice_step, create_step

# Конфигурация
EDIT_LESSON_URL = "https://stepik.org/edit-lesson/1635418/step/2"
LESSON_ID = re.search(r'edit-lesson/(\d+)', EDIT_LESSON_URL).group(1)
BASE_LESSON_URL = f"https://stepik.org/lesson/{LESSON_ID}"
TOKEN = "NsLEBLUzgjQd7vwt8vqY8W0OZsQfgY"


MATH_PROBLEMS = [
    {
        'question': '<p>Сколько будет 1 + 1?</p>',
        'options': ['4', '8', '3', '2'],
        'correct': 3  # Индекс правильного ответа (нумерация с 0)
    }
]

def get_existing_steps(lesson_id, token):
    """Получает существующие шаги"""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://stepik.org/api/step-sources?lesson={lesson_id}',
        headers=headers
    )
    response.raise_for_status()
    return response.json().get('step-sources', [])

def main():
    print(f"Работаем с уроком ID: {LESSON_ID}")
    
    # Получаем шаги
    try:
        existing_steps = get_existing_steps(LESSON_ID, TOKEN)
        existing_positions = {step['position'] for step in existing_steps}
        print(f"Найдено шагов: {len(existing_steps)}")
    except Exception as e:
        print(f"Ошибка при получении шагов: {str(e)}")
        return

    # Обрабатываем задачи
    for i, problem in enumerate(MATH_PROBLEMS, start=1):
        step_url = f"{BASE_LESSON_URL}/step/{i}"
        
        # Если шага нет - создаем
        if i not in existing_positions:
            print(f"Создаем шаг {i}...")
            try:
                create_step(LESSON_ID, i, TOKEN)
                existing_positions.add(i)
                print(f"Шаг {i} создан")
            except Exception as e:
                print(f"Ошибка при создании шага: {str(e)}")
                continue
        
        # Обновляем шаг
        print(f"\nОбновляем задачу {i}:")
        try:
            result = update_choice_step(
                step_url=step_url,
                question=problem['question'],
                options=problem['options'],
                correct_option_index=problem['correct'],
                token=TOKEN
            )
            print("Успешно" if result else "Ошибка")
        except Exception as e:
            print(f"Ошибка обновления: {str(e)}")

if __name__ == "__main__":
    main()
