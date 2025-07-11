pip install fastapi uvicorn

uvicorn main:app --reload

## Примеры curl-запросов и их ответов
### GET /review
**Запрос**
```bash
curl -X 'GET' \
  'http://localhost:8000/reviews' \
  -H 'accept: application/json'
```
**Ответ**
```json
[
  {
    "id": 1,
    "text": "хороший человек",
    "sentiment": "positive",
    "created_at": "2025-07-11T08:38:16.847674"
  },
  {
    "id": 2,
    "text": "плохой человек",
    "sentiment": "negative",
    "created_at": "2025-07-11T08:38:30.347451"
  },
  {
    "id": 3,
    "text": "человек",
    "sentiment": "neutral",
    "created_at": "2025-07-11T08:38:47.985456"
  }
]
```
### GET /review?sentiment=negative
**Запрос**
```bash
curl -X 'GET' \
  'http://localhost:8000/reviews?sentiment=negative' \
  -H 'accept: application/json'
```
**Ответ**
```json
[
  {
    "id": 2,
    "text": "плохой человек",
    "sentiment": "negative",
    "created_at": "2025-07-11T08:38:30.347451"
  }
]
```
### POST /review
**Запрос**
```bash
curl -X 'POST' \
  'http://localhost:8000/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Хороший человек"
}'
```
**Ответ**
```json
{
  "id": 9,
  "text": "хорошая компания",
  "sentiment": "positive",
  "created_at": "2025-07-11T09:10:50.894136"
}
```

