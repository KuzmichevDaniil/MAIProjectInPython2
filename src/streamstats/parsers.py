import json
import csv

from datetime import datetime, UTC
from streamstats.errors import *

def parser_csv(file):
    with file.open(mode='r', encoding="utf-8") as fl:
        
        samp = fl.readline()
        fl.seek(0)
        sep = csv.Sniffer().sniff(samp, delimiters=[',', '|', ';', '\t'])
        reader_csv = csv.DictReader(fl, delimiter=sep.delimiter)
        
        filednames_arr = [flname for flname in ['timestamp', 'level', 'source', 'message'] if flname not in reader_csv.fieldnames]
        if filednames_arr:
            raise MissingRequiredHeadings(f"Пропущены обязательные заголовки в файле {fl.name}: " + f"{', '.join(filednames_arr)}")
        
        for line in enumerate(reader_csv, start=1):
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
    except ValueError:
        raise InvalidTimestampError(f"Неверный формат времени {timestamp}")
    
    if not isinstance(level, str) or not level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise InvalidLevelError(f"Некорректный уровень {level}!")
    
    elif not isinstance(source, str) or not source:
        raise InvalidSourceError(f"Некорректный источник {source}!")
    
    elif not isinstance(message, str):
        raise InvalidMessageError(f"Некорректное сообщение {message}!")
    
    return {"timestamp": timestamp,
            "level": level,
            "source": source,
            "message": message}