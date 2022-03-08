# 1. Описание:

Проект сервиса API YAMDB.
Позволяет писать ревью на произведения и выставлять им оценки,
а так же комментировать ревью других авторов.
Для неавторизованных пользователей API доступен только для чтения.

# 2. Установка:

### Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/DIABLik666/api_yamdb.git
```
```
cd api_yamdb
```

### Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```

### Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

### Выполнить миграции:
```
python3 manage.py migrate
```

### Запустить проект:
```
python3 manage.py runserver
```