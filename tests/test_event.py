import pytest

from streamstats.errors import *
from streamstats.parsers import *


def event(**argum):
    """
    Возвращает корректное событие. 
    Аргумент argum заменяет поля в ev.
    """
    ev = {"timestamp": "2024-03-01T08:00:00", 
          "level": "INFO", "source": "web", 
          "message": "Сервер запущен"}
    ev.update(argum)
    return ev

def test_make_event_good():
    """
    Тест корректного события.
    Событие возвращается без изменений.
    """
    assert make_event(1, event(), "file") == event()
    
def test_make_event_bad_for_timestamp():
    """Неверная дата вызывает InvalidTimestampError."""
    with pytest.raises(InvalidTimestampError):
        make_event(1, event(timestamp = "вчера вечером"), "file")
    
def test_make_event_bad_for_level():
    """Неизвестный уровень TRACE вызывает InvalidLevelError."""
    with pytest.raises(InvalidLevelError):
        make_event(1, event(level = "TRACE"), "file")    
    
def test_make_event_bad_for_source():
    """Источник не строка, а число, следоваетльно, вызываем InvalidSourceError."""
    with pytest.raises(InvalidSourceError):
        make_event(1, event(source = 123), "file")