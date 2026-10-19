from streamstats.analysis import *


def event(ts = "2024-03-01T08:04:20", level = "INFO", source = "кэш", message = "ок"):
    """Возвращает корректное событие. Любое поле можно заменить при вызове."""
    return {"timestamp": ts, "level": level, "source": source, "message": message}

def test_stats():
    """
    Проверяем статистику по четырём событиям: total, level,
    source, top_error_sources, first_timestamp и last_timestamp.
    """
    
    stats = make_stats()
    analyzer(stats, event("2024-03-01T08:05:00", "WARNING", "бд"))
    analyzer(stats, event("2024-03-01T08:05:30", "INFO", "шлюз", "Шлюз недоступен"))
    analyzer(stats, event("2024-03-01T08:05:10", "CRITICAL", "бд"))
    analyzer(stats, event("2024-03-01T08:05:25", "INFO", "web"))
    
    result = final_result(stats)
    assert result["total"] == 4
    assert result["by_level"]["INFO"] == 2
    assert result["by_source"] == {"бд": 2, "шлюз": 1, "web": 1}
    assert result["top_error_sources"] == {"бд": 1}
    assert result["first_timestamp"] == "2024-03-01T08:05:00"
    assert result["last_timestamp"] == "2024-03-01T08:05:30"