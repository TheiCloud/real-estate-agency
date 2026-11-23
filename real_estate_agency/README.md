# Агентство недвижимости

Учебный проект по объектно-ориентированному программированию на Python.
Демонстрирует все ключевые темы ООП в одном приложении.

## Что внутри

- **Модели** — квартиры, студии, двухкомнатные, дома, пентхаусы, клиенты, агенты.
- **Сервисы** — хранение, сделки, аренда, уведомления, отчёты, комиссии.
- **Паттерны** — Factory, Singleton, Observer, Decorator, Adapter, Strategy.
- **База данных** — SQLite для сохранения объектов между запусками.
- **CLI** — командная строка для работы с системой.
- **Тесты** — pytest для моделей, сервисов, паттернов, базы данных, CLI и утилит.

## Установка

```bash
pip install -r requirements.txt
```

Требуется Python 3.10 или новее. Для установки пакета в режиме разработки:

```bash
pip install -e .
```

## Запуск

### Полное демо

```bash
python main.py
```

### Демо по частям

```bash
python examples/demo_basic.py
python examples/demo_services.py
python examples/demo_full.py
```

### CLI

```bash
# Добавить квартиру
python cli.py add --address "ул. Ленина, д. 10" --area 65 --price 8500000

# Добавить дом (для дома укажите число этажей)
python cli.py add --type house --address "ул. Садовая, д. 3" --area 200 --price 18000000 --floors 2

# Показать все
python cli.py list

# Найти
python cli.py find --address "ул. Ленина, д. 10"

# Продать
python cli.py sell --address "ул. Ленина, д. 10" --buyer "Петров"

# Сдать в аренду
python cli.py rent --address "ул. Ленина, д. 10" --tenant "Иванов" --days 30

# Подписать клиента
python cli.py subscribe --name "Иванов" --budget 10000000

# Отчёт
python cli.py report

# Сохранить в БД
python cli.py save

# Загрузить из БД
python cli.py load
```

CLI загружает сохранённые данные при запуске и автоматически сохраняет добавление,
продажу, аренду и подписки в `data/agency.db`. Команды `save` и `load` доступны
для ручного сохранения и повторной загрузки.

### Тесты

```bash
pytest tests/ -v
```

## Структура проекта

```
real_estate_agency/
│
├── src/real_estate/
│   ├── __init__.py
│   ├── interfaces/     — абстракции и миксины
│   ├── exceptions/     — собственные исключения
│   ├── utils/          — дескрипторы, валидаторы, логирование
│   ├── models/         — доменные объекты
│   ├── services/       — бизнес-логика
│   ├── patterns/       — паттерны проектирования
│   ├── database/       — работа с SQLite
│   └── cli/            — командная строка
│
├── tests/              — тесты pytest
├── examples/           — демо-скрипты
├── data/               — файлы базы данных
│
├── config.py           — настройки
├── main.py             — точка входа
├── cli.py              — CLI
├── README.md
├── requirements.txt
├── setup.py
└── .gitignore
```

## Архитектура

Проект разделён на слои:

1. **Интерфейсы** — контракты (ABC, Protocol).
2. **Исключения** — свои ошибки.
3. **Утилиты** — общие инструменты.
4. **Модели** — доменные объекты.
5. **Сервисы** — бизнес-логика.
6. **Паттерны** — решения типовых задач.
7. **База данных** — хранение.
8. **CLI** — интерфейс пользователя.

Слои зависят только от нижележащих. Изменение в одном слое не ломает другие.

## Что демонстрирует проект

| Главы | Тема | Где |
|-------|------|-----|
| 1–2 | Классы, инкапсуляция | Модели |
| 3–4 | Наследование, полиморфизм | Studio, House |
| 5–7 | Модификаторы, static, abstract | Интерфейсы |
| 8 | Композиция | Apartment, Building |
| 9–10 | Override, overload | Методы |
| 11–13 | Магические методы | Модели, Storage |
| 14–16 | property, classmethod, счётчик | Apartment |
| 17 | Исключения | exceptions |
| 18 | Агрегация, ассоциация | Storage |
| 19–20 | MRO, dataclass, миксин | Модели |
| 21–22 | slots, дескрипторы | Building, Apartment, utils |
| 23–24 | Метаклассы, Singleton | patterns |
| 25 | Factory | patterns |
| 26 | Observer | services |
| 27 | SRP | Разделение сервисов |
| 28 | Композиция и наследование | Apartment, Building, Penthouse |
| 29 | Копирование | Модели |
| 30 | Утиная типизация | describe |
| 31–33 | Итерация, индексация, with | Storage, DB |
| 34–35 | Strategy, OCP, LSP | commission |
| 36–37 | call, new | CommissionCalculator |
| 38–39 | Decorator, Adapter | patterns |
| 40 | ISP, DIP | interfaces |

## Лицензия

Учебный проект. Свободное использование.
