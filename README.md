# Техническое задание

## Проект

**Создание телеграм-бота для отображения финансовых данных из Таблицы**

## Цель

Разработка телеграм-бота, который будет использовать данные из таблицы, указанной ниже, и предоставлять пользователю информацию в виде графиков.

## Функциональные требования

### Подключение к базе данных

- Телеграм-бот должен отображать данные из Таблицы, содержащей финансовые данные.

### Меню выбора

- Бот должен иметь меню с выбором из 4 компаний, указанных в таблице.
- Для каждой компании должно быть доступно 4 информационных поля:
  - Доход компании
  - Расход компании
  - Прибыль компании
  - КПН компании

### Отображение данных

- При выборе компании и типа информации пользователь должен получать график с актуальной информацией из таблицы.

## Технические требования

### Интеграция с таблицей

- Использование данных из таблицы для отображения их по запросу в чате.

### Интерфейс телеграм-бота

- Реализация на Python с использованием библиотеки `python-telegram-bot` или аналогичной.
- Удобный и интуитивно понятный интерфейс с кнопками для выбора компании и типа информации.

### Данные в чате

- Обновление данных в телеграм-чате в реальном времени или с минимальной задержкой (1 минута).

### Дополнительно

- Должна быть возможность добавления новой компании через таблицу и ее дальнейшее отображение в чат-боте.

## Таблица с данными

Таблица с данными для примера доступна по следующей ссылке: [Таблица с данными](https://docs.google.com/spreadsheets/d/1w5MAeMSZZJ6_3_s2res3hJPcw2NJxNIaFV4lV0j7ePI/edit?usp=sharing)

## Примеры

![Пример графика 1](https://example.com/image1.png)
![Пример графика 2](https://example.com/image2.png)


