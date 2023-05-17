# Парсер сайта https://siriust.ru/
### Описание работы программы:
Основная логика:
1)  Запрашивает у пользователя логин и пароль
2)  Авторизовывается
3)  Собрает персональную информацию
4)  Собрает информацию по всем товарам, которые находятся в ИЗБРАННОМ


По каждому товару из избранного забирает:
1)  название
2)  цену
3)  рейтинг
4)  количество отзывов
5)  количество магазинов, в которых есть товар
6)  отзывы

Из персональных данных забирает:
1)  почта
2)  имя
3)  фамилия
4)  город

Вся собранная информация выводится в консоли и сохраняется в БД Sqlite3.
После успешного завершения программы в корне появится файл "siriust.db".


При разработке использовались библиотеки requests, lxml, sqlalchemy.


### Перед запуском программы:
1) Перейти в папку с проектом
2) Введите команды в консоли:

`python -m venv venv`

`venv\Scripts\activate.bat` - Для Windows

`source venv/bin/activate` - Для MacOS и Linux

`pip install requirements.txt` - Установить зависимости

### Запуск программы:

`python parser_siriust.py`

Программа попросит ввести Email и Password.

Тестовые данные:

Email: `test_siriust@rambler.ru`

Password: `HkMnx!8XqHTZLiC`