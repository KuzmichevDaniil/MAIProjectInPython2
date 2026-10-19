# Лабораторная работа №2. Программирование на Python

>Потоковый анализатор логов в форматах CSV и JSONL с JSON-отчётом

---

## Что умеет программа

Программа читает файлы с событиями, считает по ним статистику и сохраняет отчёт в JSON.

- Читает файлы **по одной строке**, а не целиком
- Объединяет статистику **нескольких файлов**
- Поддерживает **кириллицу**
- Не изменяет исходные файлы

---

## Клонирование

```bash
git clone https://github.com/KuzmichevDaniil/MAIProjectInPython2.git
```

---

## Установка

```bash
pip install -e .
```

---

## Запуск

```text
python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl --output REPORT.json
python -m streamstats analyze INPUT --format jsonl --skip-invalid
```

| Параметр | Описание |
|---|---|
| `--format` | формат файлов: `csv` и/или `jsonl` |
| `--output` | куда сохранить отчёт (без него — вывод в консоль) |
| `--skip-invalid` | пропускать битые строки, а не останавливаться |

> ⚠️ Если файл отчёта уже существует, он **не перезаписывается** — программа выдаст ошибку.

---

## Формат данных

Каждое событие состоит из 4 обязательных полей:

| Поле | Что это |
|---|---|
| `timestamp` | дата и время (ISO 8601) |
| `level` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `source` | источник, не пустой |
| `message` | сообщение |

## Пример CSV

```csv
timestamp,level,source,message
2024-03-01T08:00:00,INFO,web,Сервер запущен
```

## Пример JSONL

```json
{"timestamp": "2024-03-01T08:04:20", "level": "ERROR", "source": "бд", "message": "Соединение потеряно"}
```

---

## Что считается

| Показатель | Описание |
|:---|:---|
| Всего событий | Общее число корректных событий |
| Число уровней | Число событий каждого уровня |
| По источникам | Число событий каждого источника |
| Топ-k ошибок по источникам | Источники с наибольшим числом (`ERROR` и `CRITICAL`) по источникам |
| Временной диапазон | Первая и последняя временная метка |
| Пропущено строк | Число строк, пропущенных в режиме `--skip-invalid` |

Если файлов несколько — статистика **складывается**. Пустой файл даёт **нулевой отчёт**.

---

## Пример отчёта

```json
{
    "total": 12,
    "by_level": {"DEBUG": 1, "INFO": 3, "WARNING": 1, "ERROR": 5, "CRITICAL": 2},
    "by_source": {"web": 2, "кэш": 1, "авторизация": 2, "бд": 3, "платежи": 4},
    "top_error_sources": {"платежи": 3, "бд": 3, "авторизация": 1},
    "first_timestamp": "2024-03-01T08:00:00",
    "last_timestamp": "2024-03-01T08:10:00Z"
}
```

---

## Структура проекта

```text
MAIProjectInPython2/
  pyproject.toml
  README.md
  src/streamstats/
    __init__.py
    __main__.py
    parsers.py
    analysis.py
    report.py
    errors.py
  tests/
    test_analysis.py
    test_cli.py
    test_event.py
    test_parsers.py
```

---

## Проверка

```bash
python -m pytest
python -m ruff check .
python -m streamstats --help
```