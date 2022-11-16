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
    tmp = text
    while word1 in tmp:
        tmp = (
            tmp[: tmp.find(word1)]
            + "*" * len(word1)
            + tmp[tmp.find(word1) + len(word1) :]
        )
    text = tmp

    if text.count("*") > 5:
        print("More than five *")

    # TODO: 2. Extract method, remove duplicated code
    # Censor `word2` from `text`
    tmp = text
    while word2 in tmp:
        tmp = (
            tmp[: tmp.find(word2)]
            + "*" * len(word2)
            + tmp[tmp.find(word2) + len(word2) :]
        )
    text = tmp

    if text.count("*") > 5:
        print("More than five *")

    # Print result `text`
    print(text)
