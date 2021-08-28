def index_letter(text):
    for i in range(0, len(text)):
        if text[i].isalpha():
            return i

def rindex_letter(text):
    for i in reversed(range(0, len(text))):
        if text[i].isalpha():
            return i

def convert_string_to_query(title):
    query = title.lower()
    special_characters = "()'.?!® []"
    for character in special_characters:
        query = query.replace(character, "")
    return query