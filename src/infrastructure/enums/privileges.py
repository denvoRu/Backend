from enum import Enum


class Privileges(str, Enum):
    SEE_RATING = "rating"
    SEE_COMMENTS = "comments"
