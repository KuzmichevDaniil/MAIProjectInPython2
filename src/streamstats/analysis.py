from streamstats.parsers import parser_timestamp

levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def make_stats():
    """Создаём пустой словарь статистики с нулевыми счётчиками."""
    return {
        "total": 0,
        "by_level": {level: 0 for level in levels},
        "by_source": {},
        "top_error_sources": {},
        "first_timestamp": None,
        "last_timestamp": None,
        "skipped_invalid": 0,
    }
    
def analyzer(stats, event):
    """
    Учитывает одно событие в статистике. Изменяем stats.
    Обновляем общий счётчик total, счётчики по уровню by_level и источнику source,
    счётчик ошибок ERROR и CRITICAL по источникам для создания top-k
    и самую раннюю first_timestamp и самую позднюю временные метки last_timestamp.
    """
    stats["total"] += 1
    
    source = event["source"]
    stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
    
    level = event["level"]
    stats["by_level"][level] += 1
    
    if level in ["CRITICAL", "ERROR"]:
        stats["top_error_sources"][source] = stats["top_error_sources"].get(source, 0) + 1
        
    timestamp = event["timestamp"]
    if stats["first_timestamp"] == None or parser_timestamp(timestamp) < parser_timestamp(stats["first_timestamp"]):
        stats["first_timestamp"] = timestamp
    if stats["last_timestamp"] == None or parser_timestamp(timestamp) > parser_timestamp(stats["last_timestamp"]):
        stats["last_timestamp"] = timestamp
    
def top_error(err):
    "Создаем top-k для ошибок по источнику"
    srt = sorted(err.items(), reverse=True)
    return dict(srt)
    

def final_result(stats, skip_invalid = False):
    """
    Собираем итоговый отчёт из статистики.
    Поле skipped_invalid добавляется в отчёт только если программа запущена с флагом --skip-invalid.
    """
    result = {
        "total": stats["total"],
        "by_level": stats["by_level"],
        "by_source": stats["by_source"],
        "top_error_sources": top_error(stats["top_error_sources"]),        
        "first_timestamp": stats["first_timestamp"],
        "last_timestamp": stats["last_timestamp"],
    }
    
    if skip_invalid:
        result["skipped_invalid"] = stats["skipped_invalid"]
    return result