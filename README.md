# API для базы данных YaMDb

## 1. [Описание](#1)
## 2. [Команды для запуска](#2)
## 3. [Техническая информация](#3)
## 4. [Об авторе](#4)

---
## 1. Описание <a id=1></a>

Проект предназначен для взаимодействия с API социальной сети YaMDb.
YaMDb собирает отзывы пользователей на различные произведения.

API предоставляет возможность взаимодействовать с базой данных по следующим направлениям:
  - авторизироваться
  - создавать свои отзывы и управлять ими (корректировать\удалять)
  - просматривать и комментировать отзывы других пользователей
  - просматривать комментарии к своему и другим отзывам
  - просматривать произведения, категории и жанры произведений

---
## 2. Команды для запуска <a id=2></a>

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/DIABLik666/api_yamdb.git
SSH: git clone git@github.com:DIABLik666/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
Linux: source venv/bin/activate
Windows: source venv/Scripts/activate
```

И установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Выполнить миграции:
```bash
python3 manage.py migrate
```

Запустить проект:
```bash
python3 manage.py runserver
```

Теперь доступность проекта можно проверить по адресу [http://localhost/admin/](http://localhost/admin/)

---
## 3. Техническая информация <a id=3></a>

Стек технологий: Python 3, Django, Django Rest, simple JWT.

---
## 4. Об авторе <a id=4></a>

Бормотов Алексей Викторович  
Python-разработчик (Backend)  
Россия, г. Кемерово  
E-mail: di-devil@yandex.ru  
Telegram: @DIABLik666

### Соавторы:
- [UfoNexus](https://github.com/UfoNexus)  
- [ATIMSRU](https://github.com/ATIMSRU)
