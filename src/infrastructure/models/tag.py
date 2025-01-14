from typing import Literal


GoodTag = Literal[
    "полезно", 
    "понятно", 
    "интересно", 
    "атмосфера", 
    "общение", 
    "организация"
]


BadTag = Literal[
    "непонятно", 
    "неинтересно", 
    "недостаточно", 
    "перегружено", 
    "нет общения", 
    "организация"
]


Tag = Literal[GoodTag, BadTag]
