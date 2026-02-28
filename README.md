# Hotel Booking Service

Простой REST API сервис для управления номерами отеля и бронированиями.

## Стек

- Python 3.12
- Django 6
- Django REST Framework
- MySQL 8.0
- Docker / Docker Compose

---

## Быстрый старт

```bash
git clone https://github.com/Giggs-11/project_mu
cd my_project_mu

docker-compose up --build -d

docker-compose exec web python manage.py migrate
```

Сервис доступен по адресу: `http://localhost:8000`

---

## API

### Номера отеля

#### Создать номер

```
POST /rooms/create/
```

Параметры (form-data):

| Параметр | Тип | Описание |
|----------|-----|----------|
| description | string | Описание номера |
| price_per_night | decimal | Цена за ночь |



---

#### Список номеров

```
GET /rooms/list/?sort=price_asc
```

Параметры (query string):

| Параметр | Значения | По умолчанию |
|----------|----------|--------------|
| sort | `price_asc`, `price_desc`, `date_asc`, `date_desc` | `date_asc` |



---

#### Удалить номер

```
DELETE /rooms/<room_id>/delete/
```

Удаляет номер и все его бронирования.



---

### Бронирования

#### Создать бронь

```
POST /bookings/create/
```

Параметры (form-data):

| Параметр | Тип | Описание |
|----------|-----|----------|
| room_id | int | ID номера отеля |
| date_start | string | Дата начала (YYYY-MM-DD) |
| date_end | string | Дата окончания (YYYY-MM-DD) |



Если номер уже занят на указанные даты:
```json
{"error": "Номер уже забронирован на эти даты"}
```

---

#### Список броней номера

```
GET /bookings/list/?room_id=1
```


---

#### Удалить бронь

```
DELETE /bookings/<booking_id>/delete/
```


---

## Обработка ошибок

Все ошибки возвращаются в формате JSON:

```json
{"error": "описание ошибки"}
```

| HTTP код | Причина |
|----------|---------|
| 400 | Неверные параметры запроса, пересечение дат |
| 404 | Номер или бронь не найдены |

---

## Архитектурные решения

**Проверка пересечения дат** реализована через SQL-запрос с условием overlap:
```
date_start < new_date_end AND date_end > new_date_start
```
Защита от race condition обеспечена через `SELECT FOR UPDATE` внутри транзакции.

**Индексы БД:**
- `Room`: по `price_per_night`, по `created_at` — для сортировки
- `Booking`: составной `(room, date_start)` — для выборки броней номера, `(date_start, date_end)` — для проверки overlap
