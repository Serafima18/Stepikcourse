| Тип  | Название                   | md type    | Кто делает   |
| ---- |----------------------------|------------| ------------ |
| text | теория                     | TEXT       | Ксения и все |
|      | численная задача           | NUMBER     | Александра   |
|      | текстовая задача           | STRING     | Татьяна      |
|      | выбор 1 или многих         | QUIZ       | Татьяна      |
|      | задача на программирование | TASKINLINE | Александра   |
|      | вставка пропусков          | SPACE      |    |


Скрипт|	Назначение |	Пример использования
get_token.py	| Получение токена доступа	| python get_token.py
create_lesson.py	| Создание нового урока	| python create_lesson.py --title "Новый урок"
create_text_step.py	| Добавление текстового шага	| python create_text_step.py --lesson 123 --position 1
update_step_text.py	| Обновление текстового шага	| python update_step_text.py --url https://stepik.org/lesson/123/step/1
create_choice_step.py	| Создание шага с выбором	| python create_choice_step.py --lesson 123 --position 2
update_choice_step.py	| Обновление шага с выбором	| python update_choice_step.py --url https://stepik.org/lesson/123/step/2
