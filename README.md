# 💳 Payments System

Backend сервис для обработки платежей и управления балансом организаций.

## 🚀 Функциональность

- Обработка входящих webhook-ов от банка
- Начисление средств на баланс организации по ИНН
- Ведение истории изменений баланса
- Защита от дублирования платежей

## 🔧 Технологии

- Python 3.9
- Django 4.2.17
- Django REST Framework
- SQLite (для разработки)

## 📝 API Endpoints

### POST `/api/webhook/bank/`

Принимает webhook от банка с информацией о платеже:

```json
{
  "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
  "amount": 145000,
  "payer_inn": "1234567890",
  "document_number": "PAY-328",
  "document_date": "2024-04-27T21:00:00Z"
}
```

### GET `/api/organizations/<inn>/balance/`

Возвращает текущий баланс организации по ИНН:

```json
{
  "inn": "1234567890",
  "balance": 145000
}
```

## 🏗️ Структура проекта

- `models.py` - модели данных (Organization, Payment, BalanceChange)
- `views.py` - обработчики API запросов
- `serializers.py` - сериализаторы для валидации данных
- `urls.py` - маршрутизация запросов

## 🚦 Запуск проекта

1. Создать виртуальное окружение:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Применить миграции:
```bash
python manage.py migrate
```

4. Запустить сервер:
```bash
python manage.py runserver
```
