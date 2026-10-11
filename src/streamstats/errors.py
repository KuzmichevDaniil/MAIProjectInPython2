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