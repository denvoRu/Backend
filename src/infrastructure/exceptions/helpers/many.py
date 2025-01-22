
def to_many_form(word: str):
    """
    Return word in many form
    """
    return word + "es" if word[-1].lower() == "s" else "s"