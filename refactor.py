def make_asterisk(text, word):
    return text.replace(word, "*" * len(word))


def alert_text(text):
    if text.count("*") > 5:
        print("More than five *")


if __name__ == "__main__":
    text = """Because he's the hero Gotham deserves but not the one it needs right now.
So we will hunt him, because he can take it. Because he's not out hero.
He is a silent guardian, a watchful protector... a dark knight."""

    word1 = "hero"
    word2 = "silent"

    # TODO: 4. Consider general usage
    # TODO: 3. Substitute algorithm

    # TODO: 2. Extract method, remove duplicated code
    # Censor `word1` from `text`
    text = make_asterisk(text, word1)

    alert_text(text)

    # TODO: 2. Extract method, remove duplicated code
    # Censor `word2` from `text`
    text = make_asterisk(text, word2)

    alert_text(text)

    # Print result `text`
    print(text)
