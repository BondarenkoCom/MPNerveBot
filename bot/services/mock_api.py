from __future__ import annotations

import random
from datetime import date

from bot.services.schemas import DailyDigest, ReviewItem, SalesAnomaly, StockRisk


class MockMarketplaceClient:
    def _random(self, chat_id: int, marketplace: str) -> random.Random:
        seed = f"{chat_id}:{marketplace}:{date.today().isoformat()}"
        return random.Random(seed)

    def get_daily_digest(self, chat_id: int, marketplace: str) -> DailyDigest:
        rng = self._random(chat_id, marketplace)
        orders_count = rng.randint(44, 81)
        revenue_amount_rub = rng.randint(95_000, 185_000)
        stock_risks = [
            StockRisk(product_name="Футболка синяя XL", days_left=rng.randint(2, 5)),
            StockRisk(product_name="Чехол для телефона черный", days_left=rng.randint(1, 4)),
        ]
        unanswered_reviews_count = rng.randint(2, 6)

        return DailyDigest(
            marketplace_label="демо-режим",
            digest_date=date.today().isoformat(),
            orders_count=orders_count,
            orders_delta_percent=rng.randint(-12, 18),
            revenue_amount_rub=revenue_amount_rub,
            returns_count=rng.randint(1, 5),
            stock_risks=stock_risks,
            unanswered_reviews_count=unanswered_reviews_count,
            oldest_review_age_hours=rng.randint(18, 56),
            top_anomaly=SalesAnomaly(
                product_name="Футболка синяя XL",
                drop_percent=rng.randint(28, 47),
            ),
        )

    def get_unanswered_reviews(self, chat_id: int, marketplace: str) -> list[ReviewItem]:
        rng = self._random(chat_id, marketplace)
        reviews = [
            ReviewItem(
                review_id=f"demo-{index}",
                product_name=product_name,
                rating=rng.randint(2, 5),
                text=text,
                age_hours=rng.randint(12, 72),
            )
            for index, (product_name, text) in enumerate(
                [
                    ("Футболка синяя XL", "Размер подошел, но ткань могла быть плотнее."),
                    ("Чехол для телефона черный", "Доставка быстрая, но упаковка слабая."),
                    ("Кружка белая 350 мл", "Все нормально, хочу более яркую печать."),
                    ("Носки спортивные", "Удобные, но одна пара пришла с дефектом."),
                    ("Органайзер для стола", "Полезная вещь, инструкция неочевидная."),
                ],
                start=1,
            )
        ]
        reviews.sort(key=lambda item: item.age_hours, reverse=True)
        return reviews
