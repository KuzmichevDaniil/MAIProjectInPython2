class StreamStatsErrors(Exception):
    pass

class UnknownFormat(StreamStatsErrors):
    """В --format указан неизвестный формат."""
    def __init__(self, form):
        super().__init__(f"Ошибка, неизвестный формат {form}")
        
class FileNotFound(StreamStatsErrors):
    """Входной файл не найден."""
    def __init__(self, file):
        super().__init__(f"Ошибка, файл {file} не найден!")
        
class UnsupportedExtention(StreamStatsErrors):
    """У входного файла расширение не .csv и не .jsonl."""
    def __init__(self, file):
        super().__init__(f"Ошибка, неподдерживаемое расширение файла {file}")
        
class DataError(StreamStatsErrors):
    """Файл не соответствует указанному формату."""
    def __init__(self):
        super().__init__("Несовместимый файл с форматом!")

class InvalidLineError(StreamStatsErrors):
    pass

class InvalidTimestampError(InvalidLineError):
    """Временная метка отсутствует или записана не в формате ISO 8601."""
    def __init__(self, err):
        super().__init__(err)
        
class InvalidLevelError(InvalidLineError):
    """Уровень события не из списка DEBUG, INFO, WARNING, ERROR, CRITICAL."""
    def __init__(self, err):
        super().__init__(err)
        
class InvalidSourceError(InvalidLineError):
    """Источник события отсутствует или пустой."""
    def __init__(self, err):
        super().__init__(err)
        
class InvalidMessageError(InvalidLineError):
    """Сообщение события не является строкой."""
    def __init__(self, err):
        super().__init__(err)
        
class FileExists(InvalidLineError):
    """Файл отчёта уже существует."""
    def __init__(self, file):
        super().__init__(f"Файл {file} уже существует!")
        
class MissingRequiredHeadings(InvalidLineError):
    """В CSV файле нет обязательных заголовков."""
    def __init__(self, err):
        super().__init__(err)
        
class InvalidEvent(InvalidLineError):
    """Строку не удалось превратить в событие."""
    def __init__(self, file, number):
        super().__init__(f"Неверное событие в файле {file}! Строка номер {number}.")