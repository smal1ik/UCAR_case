import sqlite3
from datetime import datetime
from enum import Enum
from typing import List

from fastapi import FastAPI
import aiosqlite

from pydantic import BaseModel


def init_db():
    with sqlite3.connect("reviews.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT NOT NULL,
              sentiment TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
        """)
        conn.commit()


class Sentiment(str, Enum):
    NEUTRAL = 'neutral'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'


class Review(BaseModel):
    id: int
    text: str
    sentiment: Sentiment
    created_at: str


class ReviewRequest(BaseModel):
    text: str


sentiment_dict = {'хорош': 'positive',
                  'люблю': 'positive',
                  'плохо': 'negative',
                  'ненавиж': 'negative'}


NAME_DB = 'reviews.db'

init_db()
app = FastAPI()


async def add_reviews_db(text: str, sentiment_review: str) -> (int, str):
    """
    Функция для добавления отзыва в базу данных
    """
    created_at = datetime.utcnow().isoformat()
    async with aiosqlite.connect(NAME_DB) as connection:
        cursor = await connection.execute("INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
                                (text, sentiment_review, created_at))
        await connection.commit()
    return cursor.lastrowid, created_at


async def get_reviews_db(sentiment: str | None = None) -> List[Review]:
    """
    Функция для получения отзывов из базы данных
    """
    async with aiosqlite.connect(NAME_DB) as connection:
        if sentiment is None:
            cursor = await connection.execute("SELECT * FROM reviews")
        else:
            cursor = await connection.execute("SELECT * FROM reviews WHERE sentiment = ?", (sentiment,))
        result = await cursor.fetchall()
    return [Review(id=row[0], text=row[1], sentiment=row[2], created_at=row[3]) for row in result]


def get_sentiment(text: str) -> str:
    """
    Вспомогательная функция для определения настроения отзыва
    """
    sentiment_review = 'neutral'
    text = text.lower()
    for word, sentiment in sentiment_dict.items():
        if word in text:
            sentiment_review = sentiment
            break
    return sentiment_review


@app.post("/reviews", response_model=Review)
async def add_review(request: ReviewRequest) -> Review:
    sentiment = get_sentiment(request.text)
    id_review, created_at = await add_reviews_db(request.text, sentiment)
    return Review(id=id_review,
                  text=request.text,
                  sentiment=sentiment,
                  created_at=created_at)


@app.get("/reviews")
async def get_reviews(sentiment: Sentiment | None = None) -> List[Review]:
    reviews = await get_reviews_db(sentiment)
    return reviews



