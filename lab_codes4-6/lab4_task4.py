# Лабораторная работа 4, задание 4. Типы файлов
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех типов файлов
class FileType(ABC):
    def __init__(self, fname):
        self.fname = fname  # Имя файла

    # Каждый тип файла должен реализовать эти методы
    @abstractmethod
    def open_action(self): ...

    @abstractmethod
    def size_bytes(self): ...

    @abstractmethod
    def preview(self): ...


# Класс текстового файла
class TextFile(FileType):
    def __init__(self, fname, lines, chars, encoding):
        super().__init__(fname)  # Вызываем конструктор родительского класса
        self.lines, self.chars, self.encoding = lines, chars, encoding

    # Возвращаем способ открытия текстового файла
    def open_action(self):
        return 'открыть в текстовом редакторе'

    # Рассчитываем размер по количеству символов и кодировке
    def size_bytes(self):
        return self.chars * (2 if self.encoding == 'UTF-16' else 1)

    # Возвращаем краткую информацию о файле
    def preview(self):
        return f'{self.lines} строк, {self.chars} символов ({self.encoding})'


# Класс изображения
class ImageFile(FileType):
    def __init__(self, fname, w, h, fmt, depth):
        super().__init__(fname)
        self.w, self.h, self.fmt, self.depth = w, h, fmt, depth

    def open_action(self):
        return 'показать в просмотрщике изображений'

    # Рассчитываем размер изображения по ширине, высоте и глубине цвета
    def size_bytes(self):
        raw = self.w * self.h * self.depth // 8
        return raw // 10 if self.fmt == 'JPEG' else raw  # Условное уменьшение для JPEG

    def preview(self):
        return f'{self.w}×{self.h}, {self.fmt}, {self.depth} бит'


# Класс аудиофайла
class AudioFile(FileType):
    def __init__(self, fname, secs, kbps, channels):
        super().__init__(fname)
        self.secs, self.kbps, self.channels = secs, kbps, channels

    def open_action(self):
        return 'воспроизвести в плеере'

    # Рассчитываем размер аудио по длительности и битрейту
    def size_bytes(self):
        return self.secs * self.kbps * 1000 // 8

    def preview(self):
        return f'{self.secs} с, {self.kbps} кбит/с, {self.channels}'


# Класс видеофайла
class VideoFile(FileType):
    def __init__(self, fname, secs, resolution, fps, codec):
        super().__init__(fname)
        self.secs, self.resolution, self.fps, self.codec = secs, resolution, fps, codec

    def open_action(self):
        return 'запустить видеоплеер'

    # Битрейт зависит от разрешения видео
    def size_bytes(self):
        rate = {'480p': 1.5, '720p': 4, '1080p': 8}[self.resolution]  # Мбит/с
        return int(self.secs * rate * 1_000_000 / 8)  # Переводим биты в байты

    def preview(self):
        return f'{self.secs} с, {self.resolution}, {self.fps} к/с, {self.codec}'


# Создаём список файлов разных типов
files = [
    TextFile('отчёт.txt', 120, 5400, 'UTF-8'),
    ImageFile('пейзаж.jpg', 4000, 3000, 'JPEG', 24),
    AudioFile('песня.mp3', 215, 192, 'стерео'),
    VideoFile('урок.mp4', 600, '720p', 30, 'H.264'),
]

# Переменная для хранения общего размера всех файлов
total = 0

# Выводим информацию о каждом файле
for f in files:
    mb = f.size_bytes() / 1_048_576  # Переводим байты в мегабайты
    total += f.size_bytes()  # Добавляем размер файла к общей сумме

    print(f'{f.fname:<12} {mb:8.2f} МБ | {f.open_action()} | {f.preview()}')

# Выводим суммарный объём всех файлов в мегабайтах
print(f'Суммарный объём: {total / 1_048_576:.2f} МБ')