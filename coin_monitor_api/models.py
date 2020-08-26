"""
These are not backed by a persistent DB
"""

from pydantic import BaseModel


class Coin(BaseModel):
    id: str
    name: str
    symbol: str
