# Запросы для grade-book степика
## <u>Что знаю</u>: 
### Работа с информацией о пользователе
Структура https-запроса:
**https://stepik.org/api/users?ids%5B%5D=user_id**
> Вместо **user_id** нужно подставить id конкретного пользователя

В json-формате мы получим словарь, в котором по ключу "user" хранится список словарей. Вид хранимого словаря:

``` json
{   
    "id": int,
    "profile": int - на примере(в докуметации str),
    "is_private": bool,
    "is_active": bool,
    "is_guest": bool,
    "is_organization": bool,
    "is_author": bool,
    "short_bio": str,
    "details": str,
    "first_name": str,
    "last_name": str,
    "full_name": str,
    "alias": str,
    "avatar": str,
    "cover": str,
    "city": str,
    "knowledge": int,
    "knowledge_rank": int,
    "reputation": int,
    "reputation_rank": int,
    "join_date": str,
    "social_profiles": str,
    "solved_steps_count": int,
    "created_courses_count": int,
    "created_lessons_count": int,
    "issued_certificates_count":int,
    "followers_count": int
}
```

<b> Пример: </b>\
Запрос: 
**https://stepik.org/api/users?ids\%5B\%5D=944335224&ids%5B%5D=496655886**
Ответ на него:
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "users": [
        {
            "id": 496655886,
            "profile": 496655886,
            "is_private": false,
            "is_active": true,
            "is_guest": false,
            "is_organization": false,
            "is_author": false,
            "short_bio": "",
            "details": "",
            "first_name": "Марков",
            "last_name": "Александр",
            "full_name": "Марков Александр",
            "alias": null,
            "avatar": "https://cdn.stepik.net/media/users/496655886/1688392595-CVWqA5o/avatar.png",
            "cover": null,
            "city": null,
            "knowledge": 860,
            "knowledge_rank": 129919,
            "reputation": 0,
            "reputation_rank": null,
            "join_date": "2022-05-22T14:26:43Z",
            "social_profiles": [],
            "solved_steps_count": 860,
            "created_courses_count": 0,
            "created_lessons_count": 0,
            "issued_certificates_count": 0,
            "followers_count": 0
        }
    ]
}
```

### Работа с информацией по grade-book

Мы получим все оценки всех студентов. Структура https-запроса:
**https://stepik.org/api/course-grades?course=course_id&is_teacher=false&klass=klass_id&order=-score%2C-id&page=1&search=**
> Вместо **course_id** нужно подставить id курса\
  Вместо **klass_id** нужно подставить id класса

В json-формате мы получим словарь, в котором по ключу "user" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "course": int - на примере(в документации str),
    "user": int - на примере(в документации str),
    "results": dict - на примере(в документации str),
    "score": int - на примере(в документации str),
    "rank": int,
    "rank_max": int,
    "rank_position": int,
    "users_count": int,
    "is_teacher": bool,
    "date_joined": str,
    "last_viewed": str,
    "certificate_issue_date": str,
    "certificate_issue_regular_date": str,
    "certificate_issue_distinction_date": str,
    "certificate_update_date": str,
    "certificate_url": str
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/course-grades?course=188376&is_teacher=false&klass=62475&order=-score%2C-id&page=1&search=**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "course-grades": [
        {
            "id": 29959369,
            "course": 188376,
            "user": 540290205,
            "results": {},
            "score": 0.0,
            "rank": null,
            "rank_max": null,
            "rank_position": null,
            "users_count": null,
            "is_teacher": false,
            "date_joined": "2024-09-14T19:24:48Z",
            "last_viewed": null,
            "certificate_issue_date": null,
            "certificate_issue_regular_date": null,
            "certificate_issue_distinction_date": null,
            "certificate_update_date": null,
            "certificate_url": null
        }
    ]
}
```

### Работа с информацией по шагу
Получить информацию по шагу можно с помощью этого https-запроса:
**https://stepik.org/api/steps?ids%5B%5D=step_id**
> Вместо **step_id** нужно подставить id шага

В json-формате мы получим словарь, в котором по ключу "steps" хранится список словарей. Вид хранимого словаря:

``` json
{
    "id": int,
    "lesson": int - на примере(в документации str), - урок, к которому прикреплен шаг
    "position": int, - позиция шага в уроке, т.е. какой он по счету (1, 2, ...)
    "status": str,
    "block": dict , - описан ниже
    "actions": dict - на примере(в документации str),
    "progress": str,
    "subscriptions": list - на примере(в документации str),
    "instruction": str,
    "session": str,
    "instruction_type": str,
    "viewed_by": int - на примере(в документации str),
    "passed_by": int - на примере(в документации str),
    "correct_ratio": str,
    "worth": int - на примере(в документации str),
    "is_solutions_unlocked": bool,
    "solutions_unlocked_attempts": int,
    "has_submissions_restrictions": bool,
    "max_submissions_count": int,
    "variation": int - на примере(в документации str),
    "variations_count": int - на примере(в документации str),
    "is_enabled": bool,
    "needs_plan": str,
    "create_date": str,
    "update_date": str,
    "discussions_count": int - на примере(в документации str),
    "discussion_proxy": str,
    "discussion_threads": list - на примере(в документации str)
},
```

Структура block:
``` json
{
    "name": str, - тип урока
    "text": str, - текст, который сопровождает урок
    "video": str,
    "options": str,
    "subtitle_files": list - на примере(в документации str),
    "is_deprecated": bool - на примере(в документации str)
}
```

<b> Пример: </b>\
Запрос:
**https://stepik.org/api/steps?ids%5B%5D=4818237**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "steps": [
        {
            "id": 4818237,
            "lesson": 1140054,
            "position": 6,
            "status": "ready",
            "block": {
                "name": "number",
                "text": "<p>Напишите ответ.</p>\n\n<p>2 + 5 = ?</p>",
                "video": null,
                "options": {},
                "subtitle_files": [],
                "is_deprecated": false
            },
            "actions": {
                "submit": "#",
                "comment": "#"
            },
            "progress": "77-4818237",
            "subscriptions": [
                "31-77-4818237",
                "30-77-4818237"
            ],
            "instruction": null,
            "session": null,
            "instruction_type": null,
            "viewed_by": 624,
            "passed_by": 598,
            "correct_ratio": 0.9661290322580646,
            "worth": 1,
            "is_solutions_unlocked": false,
            "solutions_unlocked_attempts": 3,
            "has_submissions_restrictions": false,
            "max_submissions_count": 3,
            "variation": 1,
            "variations_count": 1,
            "is_enabled": true,
            "needs_plan": null,
            "create_date": "2023-12-03T22:41:31Z",
            "update_date": "2023-12-03T22:41:31Z",
            "discussions_count": 1,
            "discussion_proxy": "77-4818237-1",
            "discussion_threads": [
                "77-4818237-1"
            ]
        }
    ]
}
```


### Работа с информацией по уроку(lesson)
Получить информацию по уроку можно с помощью этого https-запроса:
**https://stepik.org/api/lessons?ids%5B%5D=lesson_id**
> Вместо **lesson_id** нужно подставить id урока

В json-формате мы получим словарь, в котором по ключу "lessons" хранится список словарей. Вид хранимого словаря:

``` json
{
    "id": int,
    "steps": list, - список шагов в уроке 
    "actions": str,
    "progress": str,
    "subscriptions": list - на примере(в документаци str),
    "viewed_by": int - на примере(в документаци str),
    "passed_by": int - на примере(в документаци str),
    "time_to_complete": int - на примере(в документаци str),
    "cover_url": str,
    "is_comments_enabled": bool,
    "is_exam_without_progress": bool - на примере(в документаци str),
    "is_blank": bool,
    "is_draft": bool,
    "is_orphaned": bool - на примере(в документаци str),
    "courses": list, - список курсов, где вставлен этот урок
    "units": list, - список юнитов, где вставлен этот урок
    "owner": int - на примере(в документаци str),
    "language": str,
    "is_featured": bool,
    "is_public": bool,
    "canonical_url": str,
    "title": str,
    "slug": str,
    "create_date": str,
    "update_date": str,
    "learners_group": str,
    "testers_group": str,
    "moderators_group": str,
    "assistants_group": str,
    "teachers_group": str,
    "admins_group": str,
    "discussions_count": int - на примере(в документаци str),
    "discussion_proxy": str,
    "discussion_threads": list - на примере(в документаци str),
    "epic_count": int,
    "abuse_count": int,
    "vote_delta": int,
    "vote": str,
    "lti_consumer_key": str,
    "lti_secret_key": str,
    "lti_private_profile": bool
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/lessons?ids%5B%5D=1140055**
Ответ на него
``` json
{
  "meta": {
    "page": 1,
    "has_next": false,
    "has_previous": false
  },
  "lessons": [
    {
      "id": 1140055,
      "steps": [],
      "actions": {

      },
      "progress": null,
      "subscriptions": [
        "31-76-1140055",
        "30-76-1140055"
      ],
      "viewed_by": 638,
      "passed_by": 582,
      "time_to_complete": 30,
      "cover_url": null,
      "is_comments_enabled": true,
      "is_exam_without_progress": false,
      "is_blank": false,
      "is_draft": false,
      "is_orphaned": false,
      "courses": [188376],
      "units": [1151730],
      "owner": 40761646,
      "language": "ru",
      "is_featured": false,
      "is_public": false,
      "canonical_url": "https://stepik.org/lesson/1140055/",
      "title": "Установим программы",
      "slug": "Установим-программы-1140055",
      "create_date": "2023-11-15T18:42:07Z",
      "update_date": "2023-12-04T23:52:33Z",
      "learners_group": null,
      "testers_group": null,
      "moderators_group": null,
      "assistants_group": null,
      "teachers_group": null,
      "admins_group": null,
      "discussions_count": 0,
      "discussion_proxy": null,
      "discussion_threads": [],
      "epic_count": 44,
      "abuse_count": 1,
      "vote_delta": 43,
      "vote": null,
      "lti_consumer_key": "",
      "lti_secret_key": "",
      "lti_private_profile": false
    }
  ]
}
```

### Работа с информацией по модулю(секции)
>Пояснение: в степике можно вставлять один урок во множество курсов, поэтому модуль хранит не сами уроки(lessons), а юниты, которые служат обвязкой для уроков.

Получить информацию по модулю можно с помощью этого https-запроса:
**https://stepik.org/api/sections?ids%5B%5D=module_id**
> Вместо **module_id** нужно подставить id модуля

В json-формате мы получим словарь, в котором по ключу "sections" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "course": int - на примере(в документации str), - id курса, которому принадлежит модуль
    "units": list - на примере(в документации str), - список юнитов курса
    "position": int, - номер модуля по счету
    "discounting_policy": str,
    "progress": str,
    "actions": str,
    "required_section": str,
    "required_percent": int,
    "is_requirement_satisfied": str,
    "is_exam": bool,
    "is_exam_without_progress": bool,
    "is_random_exam": bool,
    "exam_duration_minutes": int,
    "random_exam_problems_course": str,
    "random_exam_problems_count": int,
    "exam_session": str,
    "proctor_session": str,
    "description": str,
    "is_proctoring_can_be_scheduled": str,
    "title": str, - название
    "slug": str,
    "begin_date": str,
    "end_date": str,
    "soft_deadline": str,
    "hard_deadline": str,
    "grading_policy": str,
    "begin_date_source": str,
    "end_date_source": str,
    "soft_deadline_source": str,
    "hard_deadline_source": str,
    "grading_policy_source": str,
    "is_active": bool,
    "create_date": str,
    "update_date": str
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/sections?ids%5B%5D=365062**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "sections": [
        {
            "id": 365062,
            "course": 188376,
            "units": [
                1151731,
                1151953,
                1151954,
                1151955,
                1151956,
                1151957,
                1156657
            ],
            "position": 2,
            "discounting_policy": "no_discount",
            "progress": "79-365062",
            "actions": {},
            "required_section": null,
            "required_percent": 100,
            "is_requirement_satisfied": true,
            "is_exam": false,
            "is_exam_without_progress": false,
            "is_random_exam": false,
            "exam_duration_minutes": 120,
            "random_exam_problems_course": null,
            "random_exam_problems_count": 20,
            "exam_session": null,
            "proctor_session": null,
            "description": "",
            "is_proctoring_can_be_scheduled": false,
            "title": "Арифметика и переменные",
            "slug": "Арифметика-и-переменные-365062",
            "begin_date": null,
            "end_date": null,
            "soft_deadline": null,
            "hard_deadline": null,
            "grading_policy": "no_deadlines",
            "begin_date_source": null,
            "end_date_source": null,
            "soft_deadline_source": null,
            "hard_deadline_source": null,
            "grading_policy_source": null,
            "is_active": true,
            "create_date": "2023-11-15T18:42:08Z",
            "update_date": "2025-03-07T21:05:23Z"
        }
    ]
}
```

Чтоб получить уроки из юнитов, можно воспользоваться этим https-запросом:
**https://stepik.org/api/units?ids%5B%5D=unit_id**
> Вместо **unit_id** нужно подставить id юнита

В json-формате мы получим словарь, в котором по ключу "units" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "section": int - на примере(в документации str), - id модуля, которому принадлежит юнит
    "lesson": int - на примере(в документации str), - урок, с которым связан юнит
    "assignments": list - на примере(в документации str), - ???
    "position": int - номер юнита по счету в модуле,
    "actions": str,
    "progress": str,
    "begin_date": str,
    "end_date": str,
    "soft_deadline": str,
    "hard_deadline": str,
    "grading_policy": str,
    "begin_date_source": str,
    "end_date_source": str,
    "soft_deadline_source": str,
    "hard_deadline_source": str,
    "grading_policy_source": str,
    "is_active": bool,
    "create_date": str,
    "update_date": str
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/units?ids%5B%5D=1151731**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "units": [
        {
            "id": 1151731,
            "section": 365062,
            "lesson": 1140056,
            "assignments": [
                4749949,
                4750888,
                4750889,
                4750891,
                4750892,
                4750893,
                4750894,
                4800566
            ],
            "position": 1,
            "actions": {},
            "progress": null,
            "begin_date": null,
            "end_date": null,
            "soft_deadline": null,
            "hard_deadline": null,
            "grading_policy": "no_deadlines",
            "begin_date_source": null,
            "end_date_source": null,
            "soft_deadline_source": null,
            "hard_deadline_source": null,
            "grading_policy_source": null,
            "is_active": true,
            "create_date": "2023-11-15T18:42:10Z",
            "update_date": "2023-12-04T23:47:39Z"
        }
    ]
}
```

### Работа с информацией по курсу

Получить информацию по курсу можно с помощью этого https-запроса:
**https://stepik.org/api/courses/course_id**
> Вместо **course_id** нужно подставить id курса

В json-формате мы получим словарь, в котором по ключу "courses" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "summary",
    "workload",
    "cover",
    "intro",
    "course_format",
    "target_audience",
    "certificate_footer",
    "certificate_cover_org",
    "is_certificate_issued",
    "is_certificate_auto_issued",
    "certificate_regular_threshold",
    "certificate_distinction_threshold",
    "instructors",
    "certificate",
    "requirements",
    "description",
    "sections": list, - список секций курса
    "total_units",
    "enrollment",
    "is_favorite",
    "actions",
    "progress",
    "first_lesson",
    "first_unit",
    "certificate_link",
    "certificate_regular_link",
    "certificate_distinction_link",
    "user_certificate",
    "referral_link",
    "schedule_link",
    "schedule_long_link",
    "first_deadline",
    "last_deadline",
    "subscriptions",
    "announcements",
    "is_contest",
    "is_self_paced",
    "is_adaptive",
    "is_idea_compatible",
    "is_in_wishlist",
    "last_step",
    "intro_video",
    "social_providers",
    "authors",
    "tags",
    "has_tutors",
    "is_enabled",
    "is_proctored",
    "proctor_url",
    "review_summary",
    "schedule_type",
    "certificates_count",
    "learners_count",
    "lessons_count",
    "quizzes_count",
    "challenges_count",
    "peer_reviews_count",
    "instructor_reviews_count",
    "videos_duration",
    "time_to_complete",
    "is_popular",
    "is_processed_with_paddle",
    "is_unsuitable",
    "is_paid",
    "price",
    "currency_code",
    "display_price",
    "default_promo_code_name",
    "default_promo_code_price",
    "default_promo_code_discount",
    "default_promo_code_is_percent_discount",
    "default_promo_code_expire_date",
    "continue_url",
    "readiness",
    "is_archived",
    "options",
    "price_tier",
    "position",
    "is_censored",
    "difficulty",
    "acquired_skills",
    "acquired_assets",
    "learning_format",
    "content_details",
    "issue",
    "course_type",
    "possible_type",
    "is_certificate_with_score",
    "preview_lesson",
    "preview_unit",
    "possible_currencies",
    "commission_basic",
    "commission_promo",
    "with_certificate",
    "child_courses",
    "child_courses_count",
    "parent_courses",
    "became_published_at",
    "became_paid_at",
    "title_en",
    "last_update_price_date",
    "owner",
    "language",
    "is_featured",
    "is_public",
    "canonical_url",
    "title",
    "slug",
    "begin_date",
    "end_date",
    "soft_deadline",
    "hard_deadline",
    "grading_policy",
    "begin_date_source",
    "end_date_source",
    "soft_deadline_source",
    "hard_deadline_source",
    "grading_policy_source",
    "is_active",
    "create_date",
    "update_date",
    "learners_group",
    "testers_group",
    "moderators_group",
    "assistants_group",
    "teachers_group",
    "admins_group",
    "discussions_count",
    "discussion_proxy",
    "discussion_threads",
    "lti_consumer_key",
    "lti_secret_key",
    "lti_private_profile"
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/courses/188376**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "courses": [
        {
            "id": 188376,
            "summary": "КУРС ОТКРЫВАЕТ ПО 1 МОДУЛЮ В НЕДЕЛЮ.\n\nПитон ...",
            "workload": "3 часа в неделю",
            "cover": "https://cdn.stepik.net/media/cache/images/courses/188376/cover_jqZRw1X/6b57db793df23a9a94ce8f62b5d36201.png",
            "intro": "",
            "course_format": "",
            "target_audience": "Для начинающих изучать программирование. Кому в школе не досталось информатики.",
            "certificate_footer": null,
            "certificate_cover_org": null,
            "is_certificate_issued": false,
            "is_certificate_auto_issued": false,
            "certificate_regular_threshold": null,
            "certificate_distinction_threshold": null,
            "instructors": [
                40761646
            ],
            "certificate": "",
            "requirements": "<p>Знание математики в рамках начальной школы.</p>",
            "description": "<p>КУРС В СТАДИИ ОТКРЫТИЯ. ...",
            "sections": [
                365061,
                365062,
                365713,
                371384,
                389712,
                371385,
                371386,
                371387,
                371388,
                371389,
                388364
            ],
            "total_units": 47,
            "enrollment": null,
            "is_favorite": false,
            "actions": {
                "view_reports": {
                    "enabled": false,
                    "needs_permission": "teach"
                },
                "edit_reports": {
                    "enabled": false,
                    "needs_permission": "teach"
                },
                "view_grade_book_page": {
                    "enabled": false,
                    "needs_permission": "assist"
                },
                "view_grade_book": {
                    "enabled": false,
                    "needs_permission": "assist"
                },
                "edit_lti": {
                    "enabled": false,
                    "needs_permission": "admin"
                },
                "edit_advanced_settings": {
                    "enabled": false,
                    "needs_permission": "teach"
                },
                "manage_permissions": {
                    "enabled": false,
                    "needs_permission": "admin"
                },
                "view_revenue": {
                    "enabled": false
                },
                "can_be_bought": {
                    "enabled": false
                },
                "can_be_price_changed": {
                    "enabled": true
                },
                "can_be_deleted": {
                    "enabled": false
                },
                "edit_tags": {
                    "enabled": false
                }
            },
            "progress": null,
            "first_lesson": 1140054,
            "first_unit": 1151729,
            "certificate_link": null,
            "certificate_regular_link": null,
            "certificate_distinction_link": null,
            "user_certificate": null,
            "referral_link": null,
            "schedule_link": null,
            "schedule_long_link": null,
            "first_deadline": null,
            "last_deadline": null,
            "subscriptions": [
                "31-78-188376",
                "30-78-188376"
            ],
            "announcements": [],
            "is_contest": false,
            "is_self_paced": true,
            "is_adaptive": false,
            "is_idea_compatible": false,
            "is_in_wishlist": false,
            "last_step": "78-188376",
            "intro_video": null,
            "social_providers": [],
            "authors": [
                40761646
            ],
            "tags": [
                1,
                2,
                3,
                42,
                55,
                56
            ],
            "has_tutors": false,
            "is_enabled": true,
            "is_proctored": false,
            "proctor_url": null,
            "review_summary": 187845,
            "schedule_type": "self_paced",
            "certificates_count": 0,
            "learners_count": 1226,
            "lessons_count": 47,
            "quizzes_count": 122,
            "challenges_count": 105,
            "peer_reviews_count": 0,
            "instructor_reviews_count": 0,
            "videos_duration": 0,
            "time_to_complete": 68120,
            "is_popular": true,
            "is_processed_with_paddle": false,
            "is_unsuitable": false,
            "is_paid": false,
            "price": null,
            "currency_code": null,
            "display_price": "-",
            "default_promo_code_name": null,
            "default_promo_code_price": null,
            "default_promo_code_discount": null,
            "default_promo_code_is_percent_discount": null,
            "default_promo_code_expire_date": null,
            "continue_url": "/course/188376/continue",
            "readiness": 0.9090909090909091,
            "is_archived": false,
            "options": {},
            "price_tier": null,
            "position": 1,
            "is_censored": false,
            "difficulty": "easy",
            "acquired_skills": [
                "Научитесь писать простейшие программы на python.",
                "Разделять код на логические блоки и оформлять их в виде функций.",
                "Поймете, что такое объект и класс и как на их основе строятся остальные конструкции языка."
            ],
            "acquired_assets": [
                "Необходимые знания для прохождения курсов по ИИ, ML и тп. Вложитесь в основы!",
                "Теорию, рассказанную простым языком.",
                "Обилие практики.",
                "Отвечающих на вопросы преподавателей."
            ],
            "learning_format": "<p>Теоретический ....</p>",
            "content_details": [],
            "issue": null,
            "course_type": "basic",
            "possible_type": null,
            "is_certificate_with_score": false,
            "preview_lesson": null,
            "preview_unit": null,
            "possible_currencies": [],
            "commission_basic": null,
            "commission_promo": null,
            "with_certificate": false,
            "child_courses": [],
            "child_courses_count": 0,
            "parent_courses": [],
            "became_published_at": "2023-11-27T18:08:11.020Z",
            "became_paid_at": null,
            "title_en": "Simple python: Volume 1, Basics",
            "last_update_price_date": null,
            "owner": 40761646,
            "language": "ru",
            "is_featured": false,
            "is_public": true,
            "canonical_url": "https://stepik.org/course/188376/",
            "title": "Простой python: том 1, основы",
            "slug": "Простой-python-том-1-основы-188376",
            "begin_date": null,
            "end_date": null,
            "soft_deadline": null,
            "hard_deadline": null,
            "grading_policy": "no_deadlines",
            "begin_date_source": null,
            "end_date_source": null,
            "soft_deadline_source": null,
            "hard_deadline_source": null,
            "grading_policy_source": "no_deadlines",
            "is_active": true,
            "create_date": "2023-11-15T17:57:21Z",
            "update_date": "2025-03-07T21:05:23Z",
            "learners_group": null,
            "testers_group": null,
            "moderators_group": null,
            "assistants_group": null,
            "teachers_group": null,
            "admins_group": null,
            "discussions_count": 0,
            "discussion_proxy": null,
            "discussion_threads": [],
            "lti_consumer_key": "",
            "lti_secret_key": "",
            "lti_private_profile": false
        }
    ],
    "enrollments": []
}
```


### Работа с информацией по классу

Получить информацию по классу можно с помощью этого https-запроса:
**https://stepik.org/api/classes/class_id**
> Вместо **class_id** нужно подставить id класса

В json-формате мы получим словарь, в котором по ключу "classes" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "course": int - на примере(в документации str), - id курса
    "owner": int - на примере(в документации str),
    "title": str,
    "description": str,
    "invitation_key": str,
    "is_access_restricted": bool - на примере(в документации str),
    "actions": dict - на примере(в документации str),
    "assistants_count": int,
    "students_count": int,
    "create_date": str,
    "update_date": str.
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/classes/62475**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "classes": [
        {
            "id": 62475,
            "course": 188376,
            "owner": 40761646,
            "title": "2024_3415_Рязань",
            "description": "2024 год, осень, 3415 группа, Рязань",
            "invitation_key": "448dea122c834f90cfb97bcc1c0c25651f48c354",
            "is_access_restricted": false,
            "actions": {
                "manage": false,
                "tutor": true,
                "assist": true
            },
            "assistants_count": 1,
            "students_count": 12,
            "create_date": "2024-09-14T17:59:59.250Z",
            "update_date": "2024-09-14T17:59:59.250Z"
        }
    ]
}
```

### Работа с учениками по классу

Получить информацию об учениках класса можно с помощью этого https-запроса:
**https://stepik.org/api/students?klass=class_id&page=1**
> Вместо **class_id** нужно подставить id класса

В json-формате мы получим словарь, в котором по ключу "students" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "klass": str,
    "user": str,
    "date_joined": str
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/students?klass=62475&page=1**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "students": [
        {
            "id": 762035,
            "klass": 62475,
            "user": 941539964,
            "date_joined": "2024-09-14T18:25:37.022Z"
        }
    ]
}
```

### Работа с информацией о посылках

Получить информацию о посылках для какого-то шага из класса можно с помощью этого https-запроса:
**https://stepik.org/api/submissions?klass=class_id&order=desc&page=1&step=step_id**
> Вместо **class_id** нужно подставить id класса\
Вместо **step_id** нужно подставить id шага

В json-формате мы получим словарь, в котором по ключу "students" хранится список словарей. Вид хранимого словаря:
``` json
{
    "id": int,
    "status": str,
    "score": float - на примере(в документации str),
    "hint": str,
    "feedback": str,
    "time": str,
    "reply": dict - на примере(в документации str),
    "reply_url": str,
    "attempt": int - на примере(в документации str),
    "session": str,
    "eta": int
}
```

<b> Пример: </b>\
Запрос: **https://stepik.org/api/submissions?klass=62475&order=desc&page=1&step=4584301**
Ответ на него
``` json
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "submissions": [
        {
            "id": 1277353101,
            "status": "correct",
            "score": 1.0,
            "hint": "",
            "feedback": "",
            "time": "2024-09-16T05:43:37Z",
            "reply": {
                "code": "class Gun:\n    pass\ntt = Gun()\nrevolver = Gun()\n\n\n\n\n",
                "language": "python3.10"
            },
            "reply_url": null,
            "attempt": 1192236951,
            "session": null,
            "eta": 0
        }
    ]
}
```
