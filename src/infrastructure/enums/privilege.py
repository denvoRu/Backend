from enum import Enum


class Privilege(str, Enum):
    SEE_RATING = "rating"
    SEE_COMMENTS = "comments"
