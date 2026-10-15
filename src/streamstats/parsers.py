import json
import csv

from datetime import datetime, UTC
from streamstats.errors import *

def parser_csv(file):
    with file.open(mode='r', encoding="utf-8") as fl:
        for line in enumerate(csv.DictReader(fl), start=1):
            yield line[1]

def parser_jsonl(file):
    with file.open(mode='r', encoding='utf-8') as fl:
        for line in enumerate(fl, start=1):
            yield json.loads(line[1])

def parser_timestamp(ts):
    timestamp = datetime.fromisoformat(ts)
    if timestamp.tzinfo == None:
        return timestamp.replace(tzinfo=UTC)
    else:
        return timestamp.astimezone(UTC)

def make_event(raw: dict[str, str]):
    timestamp = raw.get("timestamp")
    level = raw.get("level")
    source = raw.get("source")
    message = raw.get("message")
    
    if not isinstance(timestamp, str) or not timestamp:
        raise InvalidTimestampError("Некорректная дата!")
    
    try:
        parser_timestamp(timestamp)
    except StreamStatsErrors:
        raise InvalidTimestampError(f"Неверный формат времени {timestamp}")
    
    if not isinstance(level, str) or not level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise InvalidLevelError("Некорректный уровень!")
    
    elif not isinstance(source, str) or not source:
        raise InvalidSourceError("Некорректный источник!")
    
    elif not isinstance(message, str):
        raise InvalidMessageError("Некорректное сообщение!")
    
    return {"timestamp": timestamp,
            "level": level,
            "source": source,
            "message": message}