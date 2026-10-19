import json

from streamstats.parsers import *


def event():
    """Возвращает одно корректное событие."""
    return {"timestamp": "2024-03-01T08:02:30",
            "level": "ERROR",
            "source": "бд",
            "message": "Таймаут запроса"}
    
def test_parse_csv(tmp_path):
    """parser_csv читает все строки файла и возвращает верные значения полей."""
    file = tmp_path / "events.csv"
    file.write_text("timestamp,level,source,message\n"
                    "2024-03-01T08:02:30,ERROR,бд,Таймаут запроса\n"
                    "2024-03-01T08:00:00,INFO,web,Сервер запущен\n"
                    "2024-03-01T08:00:05,DEBUG,кэш,Кэш прогрет\n"
                    "2024-03-01T08:10:00Z,CRITICAL,платежи,Шлюз недоступен\n", encoding="utf-8")
    line = list(parser_csv(file))
    assert line[0][1]["timestamp"] == "2024-03-01T08:02:30"
    assert line[1][1]["level"] == "INFO"
    assert line[2][1]["source"] == "кэш"
    assert line[3][1]["message"] == "Шлюз недоступен"
    
def test_parse_jsonl(tmp_path):
    """parser_jsonl читает строку и возвращает верные значения поля."""
    file = tmp_path / "events.jsonl"
    file.write_text(json.dumps(event()) + "\n", encoding="utf-8")
    line = list(parser_jsonl(file))
    assert line[0][1]["timestamp"] == "2024-03-01T08:02:30"
    assert line[0][1]["level"] == "ERROR"
    assert line[0][1]["source"] == "бд"
    assert line[0][1]["message"] == "Таймаут запроса"
    
def test_jsonl_empty_file(tmp_path):
    """Тест пустого JSONL файла."""
    file = tmp_path / "empty.jsonl"
    file.write_text("", encoding="utf-8")
    assert list(parser_jsonl(file)) == []
    
def test_csv_empty_file(tmp_path):
    """Тест пустого CSV файла."""
    file = tmp_path / "empty.csv"
    file.write_text("", encoding="utf-8")
    assert list(parser_csv(file)) == []
    
def test_unicode_for_jsonl(tmp_path):
    """
    Тест unicode. 
    Кириллица в JSONL сохраняется без искажения.
    """
    file = tmp_path / "unic.jsonl"
    file.write_text(json.dumps(event(), ensure_ascii=False) + "\n", encoding="utf-8")
    ev = list(parser_jsonl(file))
    assert ev[0][1]["source"] == "бд"
    assert ev[0][1]["message"] == "Таймаут запроса"
    
def test_unicode_for_csv(tmp_path):
    """
    Тест unicode.
    Кириллица в CSV сохраняется без искажения.
    """
    file = tmp_path / "unic.csv"
    file.write_text("timestamp,level,source,message\n"
                    "2024-03-01T08:00:05,DEBUG,кэш,Кэш прогрет\n"
                    "2024-03-01T08:10:00Z,CRITICAL,платежи,Шлюз недоступен\n", encoding="utf-8")
    line = list(parser_csv(file))
    assert line[0][1]["source"] == "кэш"
    assert line[1][1]["message"] == "Шлюз недоступен"