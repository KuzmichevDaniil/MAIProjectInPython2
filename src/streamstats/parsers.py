import csv
import json
from datetime import UTC, datetime

from streamstats.errors import *


def parser_csv(file):
    """
    Читаем CSV файл построчно.
    Разделитель (',', '|', ';', '\t' (табуляция)) определяется по первой строке (samp).
    Для каждой записи возвращаем пару (номер_строки, словарь).
    Если запись повреждена, вместо словаря возвращаем None. 
    Пустой файл ничего не отдаёт.
    Рейзим MissingRequiredHeadings, если отсутсвуют обязательные заголовки.
    """
    with file.open(mode='r', encoding="utf-8") as fl:
        
        samp = fl.readline()
        if not samp:
            return 
        
        fl.seek(0)
        sep = csv.Sniffer().sniff(samp, delimiters=[',', '|', ';', '\t'])
        reader_csv = csv.DictReader(fl, delimiter=sep.delimiter)
        
        filednames_arr = [flname for flname in ['timestamp', 'level', 'source', 'message'] if flname not in reader_csv.fieldnames]
        if filednames_arr:
            raise MissingRequiredHeadings(f"Пропущены обязательные заголовки в файле {fl.name}: " + f"{', '.join(filednames_arr)}")
        
        for line in reader_csv:
            if None in line or all(value == '' for value in line.values()):
                yield reader_csv.line_num, None
            else:
                yield reader_csv.line_num, line

def parser_jsonl(file):
    """
        Читаем JSONL файл построчно.
        Для каждой строки возвращаем пару (номер_строки, словарь).
        Если строка не является корректным JSON объектом, вместо словаря возвращаем None. 
        Пустые строки пропускаются.
        """
    with file.open(mode='r', encoding='utf-8') as fl:        
        for num_line, line in enumerate(fl, start=1):
            if not line.strip():
                continue
            try:
                line = json.loads(line)
            except json.JSONDecodeError:
                line = None
            if isinstance(line, dict):
                yield num_line, line
            else:
                yield num_line, None

def parser_timestamp(ts):
    """
    Превращаем строку ISO 8601 в datetime в часовом поясе UTC.
    Рейзим ValueError, если строка не соответствует формату в make_event.
    """
    timestamp = datetime.fromisoformat(ts)
    if timestamp.tzinfo == None:
        return timestamp.replace(tzinfo=UTC)
    else:
        return timestamp.astimezone(UTC)

def make_event(num, raw: dict[str, str], file):
    """
    Проверяем запись и возвращаем событие в виде словаря.
    num и file нужны только для сообщений об ошибках.
    Если raw равен None, или поле timestamp, level, source или message
    некорректно, рейзим ошибку.
    """
    if raw is None:
        raise InvalidEvent(file, num)
    
    timestamp = raw.get("timestamp")
    level = raw.get("level")
    source = raw.get("source")
    message = raw.get("message")
    
    if not isinstance(timestamp, str) or not timestamp:
        raise InvalidTimestampError(f"Некорректная дата в файле {file}! Строка номер {num}.")
    
    try:
        parser_timestamp(timestamp)
    except ValueError:
        raise InvalidTimestampError(f"Неверный формат времени {timestamp} в файле {file}! Строка номер {num}.")
    
    if not isinstance(level, str) or not level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise InvalidLevelError(f"Некорректный уровень {level} в файле {file}! Строка номер {num}.")
    
    elif not isinstance(source, str) or not source:
        raise InvalidSourceError(f"Некорректный источник {source} в файле {file}! Строка номер {num}.")
    
    elif not isinstance(message, str):
        raise InvalidMessageError(f"Некорректное сообщение {message} в файле {file}! Строка номер {num}.")
    
    return {"timestamp": timestamp,
            "level": level,
            "source": source,
            "message": message}