[![Check code style](https://github.com/JetBrains-Research/formal-lang-course/actions/workflows/code_style.yml/badge.svg)](https://github.com/JetBrains-Research/formal-lang-course/actions/workflows/code_style.yml)
[![Code style](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)
---
# Formal Language Course

Курс по формальным языкам: шаблон структуры репозитория для выполнения домашних работ,
а также материалы курса и другая сопутствующая информация.

Актуальное:
- [Таблица с текущими результатами](https://docs.google.com/spreadsheets/d/18DhYG5CuOrN4A5b5N7-mEDfDkc-7BuXF3Qsu6HD-lks/edit?usp=sharing)
- [Список задач](https://github.com/JetBrains-Research/formal-lang-course/tree/main/tasks)
- [Стиль кода как референс](https://www.python.org/dev/peps/pep-0008/)
- [Материалы по курсу](https://github.com/JetBrains-Research/formal-lang-course/blob/main/docs/lecture_notes/Formal_language_course.pdf)
- [О достижимости с ограничениями в терминах формальных языков](https://github.com/JetBrains-Research/FormalLanguageConstrainedReachability-LectureNotes)

Технологии:
- Python 3.8+
- Pytest для unit тестирования
- GitHub Actions для CI
- Google Colab для постановки и оформления экспериментов
- Сторонние пакеты из `requirements.txt` файла
- Английский язык для документации или самодокументирующийся код

## Работа с проектом

- Для выполнения домашних практических работ необходимо сделать `fork` этого репозитория к себе в `GitHub`.
- Рекомендуется установить [`pre-commit`](https://pre-commit.com/#install) для поддержания проекта в адекватном состоянии.
  - Установить `pre-commit` можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit install
    ```
  - Отформатировать код в соответствии с принятым стилем можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit run --all-files
    ```
- Ссылка на свой `fork` репозитория размещается в [таблице](https://docs.google.com/spreadsheets/d/18DhYG5CuOrN4A5b5N7-mEDfDkc-7BuXF3Qsu6HD-lks/edit?usp=sharing) курса с результатами.
- В свой репозиторий необходимо добавить проверяющих с `admin` правами на чтение, редактирование и проверку `pull-request`'ов.

## Домашние практические работы

### Дедлайны

- **мягкий**: воскресенье 23:59
- **жёсткий**: среда 23:59

### Выполнение домашнего задания

- Каждое домашнее задание выполняется в отдельной ветке. Ветка должна иметь осмысленное консистентное название.
- При выполнении домашнего задания в новой ветке необходимо открыть соответствующий `pull-request` в `main` вашего `fork`.
- `Pull-request` снабдить понятным названием и описанием с соответствующими пунктами прогресса.
- Проверка заданий осуществляется посредством `review` вашего `pull-request`.
- Как только вы считаете, что задание выполнено, вы можете запросить `review` у проверяющего.
  - Если `review` запрошено **до мягкого дедлайна**, то вам гарантированна дополнительная проверка (до жёсткого дедлайна), позволяющая исправить замечания до наступления жёсткого дедлайна.
  - Если `review` запрошено **после мягкого дедлайна**, но **до жесткого дедлайна**, задание будет проверено, но нет гарантий, что вы успеете его исправить.
- Когда проверка будет пройдена, и задание **зачтено**, его необходимо `merge` в `main` вашего `fork`.
- Результаты выполненных заданий будут повторно использоваться в последующих домашних работах.

### Получение оценки за домашнюю работу

- Если ваша работа **зачтена** _до_ **жёсткого дедлайна**, то выполучаете **полный балл за домашнюю работу**.
- Если ваша работа **зачтена** _после_ **жёсткого дедлайна**, то вы получаете **половину полного балла за домашнюю работу**.

## Код

- Исходный код практических задач по программированию размещайте в папке `project`.
- Файлам и модулям даем осмысленные имена, в соответствии с официально принятым стилем.
- Структурируем код, используем как классы, так и отдельно оформленные функции. Чем понятнее код, тем быстрее его проверять и тем больше у вас будет шансов получить полный балл.

## Тесты

- Тесты для домашних заданий размещайте в папке `tests`.
- Формат именования файлов с тестами `test_[какой модуль\класс\функцию тестирует].py`.
- Для работы с тестами рекомендутеся использовать [`pytest`](https://docs.pytest.org/en/6.2.x/).
- Для запуска тестов необходимо из корня проекта выполнить следующую команду:
  ```shell
  python ./scripts/run_tests.py
  ```

## Эксперименты

- Для выполнения экспериментов потребуется не только код, но окружение и некоторая его настройка.
- В качестве окружения используем только [`Google Colab`](https://research.google.com/colaboratory/) ноутбуки. Для его создания требуется только учетная запись `Google`.
- Создаем ноутбук, ссылка на ноутбук также размещается в [таблице](https://docs.google.com/spreadsheets/d/18DhYG5CuOrN4A5b5N7-mEDfDkc-7BuXF3Qsu6HD-lks/edit?usp=sharing) курса.
- В `Google Colab` ноутбуке выполняется вся настройка, пишется код для экспериментов, подготовки отчетов и графиков.

[Экспериментальное исследование алгоритмов решения задачи достижимости с КС ограничениями
](https://colab.research.google.com/drive/1D0tcQlcSlNW4jl3vqxJIw0Hxpd3wzy_c?usp=sharing)


## Язык запросов к графам

### Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Path of path
  | List of string
  | List of int
  | List of bool

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)

lambda =
    Lambda of List<var> * expr
```

### Описание конкретного синтаксиса языка
```
PROGRAM -> STMT ; PROGRAM | eps
STMT -> VAR = EXPR | PRINT(EXPR)

LOWERCASE -> [a-z]
UPPERCASE -> [A-Z]
DIGIT -> [0-9]

INT -> 0 | [1-9] DIGIT*
STRING -> (_ | . | LOWERCASE | UPPERCASE) (_ | . | LOWERCASE | UPPERCASE | DIGIT)*
BOOL -> true | false
PATH -> " (/ | _ | . | LOWERCASE | UPPERCASE | DIGIT)+ "

VAR -> STRING
VAL ->
    INT
    | " STRING "
    | BOOL
    | PATH
    | LIST<INT>
    | LIST<" STRING ">
    | LIST<BOOL>

SET ->
    SET<INT>
    | SET<" STRING ">
    | range ( INT , INT )

EXPR -> VAR
EXPR -> VAL
EXPR -> GRAPH
GRAPH -> " STRING "
GRAPH -> set_start(SET, GRAPH)
GRAPH -> set_final(SET, GRAPH)
GRAPH -> add_start(SET, GRAPH)
GRAPH -> add_final(SET, GRAPH)

EXPR -> VERTEX | VERTICES
VERTEX -> INT
VERTICES -> SET<VERTEX> | range ( INT , INT )
VERTICES -> get_start(GRAPH)
VERTICES -> get_final(SET, GRAPH)

EXPR -> PAIR_OF_VERTICES
PAIR_OF_VERTICES -> SET<(INT, INT)>
PAIR_OF_VERTICES -> get_reachable(GRAPH)

VERTICES -> get_vertices(GRAPH)

EXPR -> EDGE | EDGES
EDGE -> (INT, " STRING ", INT) | (INT, INT, INT)
EDGES -> SET<EDGE>
EDGES -> get_edges(GRAPH)

EXPR -> LABELS
LABELS -> SET<INT> | SET<" STRING ">
LABELS -> get_labels(GRAPH)

EXPR -> map(LAMBDA, EXPR)
EXPR -> filter(LAMBDA, EXPR)
GRAPH -> load(" PATH ")
GRAPH -> intersect(GRAPH, GRAPH)
GRAPH -> concat(GRAPH, GRAPH)
GRAPH -> union(GRAPH, GRAPH)
GRAPH -> star(GRAPH, GRAPH)

LAMBDA -> (LIST<VAR> -> [BOOL_EXPR | EXPR])
BOOL_EXPR ->
    BOOL_EXPR or BOOL_EXPR
    | BOOL_EXPR and BOOL_EXPR
    | not BOOL_EXPR
    | BOOL
    | has_label(EDGE, " STRING ")
    | is_start(VERTEX)
    | is_final(VERTEX)
    | X in SET<X>

LIST<X> -> list(X [, X]*) | list()
SET<X> -> set(X [, X]*) | set()
```

### Пример программы
```
g = load("wine")

h = set_start(set_final(get_vertices(g), g)), range(1, 100))

l1 = union("l1", "l2")

q1 = star(union("type", l1))
q2 = concat("sub_class_of", l1)

res1 = intersect(g, q1)
res2 = intersect(g, q2)

print(res1)

s = get_start(g)

vertices = filter((list(v) -> v in s), get_edges(res1))

print(vertices)
```
## Структура репозитория

```text
.
├── .github - файлы для настройки CI и проверок
├── docs - текстовые документы и материалы по курсу
├── project - исходный код домашних работ
├── scripts - вспомогательные скрипты для автоматизации разработки
├── tasks - файлы с описанием домашних заданий
├── tests - директория для unit-тестов домашних работ
├── README.md - основная информация о проекте
└── requirements.txt - зависимости для настройки репозитория
```


## Контакты

- Семен Григорьев [@gsvgit](https://github.com/gsvgit)
- Егор Орачев [@EgorOrachyov](https://github.com/EgorOrachyov)
- Вадим Абзалов [@vdshk](https://github.com/vdshk)
