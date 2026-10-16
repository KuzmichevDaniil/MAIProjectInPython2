class StreamStatsErrors(Exception):
    pass

class UnknownFormat(StreamStatsErrors):
    def __init__(self, form):
        super().__init__(f"Ошибка, неизвестный формат {form}")
        
class FileNotFound(StreamStatsErrors):
    def __init__(self, file):
        super().__init__(f"Ошибка, файл {file} не найден!")
        
class UnsupportedExtention(StreamStatsErrors):
    def __init__(self, file):
        super().__init__(f"Ошибка, неподдерживаемое расширение файла {file}")
        
class DataError(StreamStatsErrors):
    def __init__(self):
        super().__init__("Несовместимый файл с форматом!")

class InvalidTimestampError(StreamStatsErrors):
    def __init__(self, err):
        super().__init__(err)
        
class InvalidLevelError(StreamStatsErrors):
    def __init__(self, err):
        super().__init__(err)
        
class InvalidSourceError(StreamStatsErrors):
    def __init__(self, err):
        super().__init__(err)
        
class InvalidMessageError(StreamStatsErrors):
    def __init__(self, err):
        super().__init__(err)
        
class FileExists(StreamStatsErrors):
    def __init__(self, file):
        super().__init__(f"Файл {file} уже существует!")
        
class MissingRequiredHeadings(StreamStatsErrors):
    def __init__(self, err):
        super().__init__(err)