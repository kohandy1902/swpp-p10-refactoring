def censor_alert(text, *words):
    for word in words:
        text = text.replace(word, "*" * len(word))
        if text.count("*") > 5:
            print("More than five *")


if __name__ == "__main__":
    text = """Because he's the hero Gotham deserves but not the one it needs right now.
So we will hunt him, because he can take it. Because he's not out hero.
He is a silent guardian, a watchful protector... a dark knight."""

    word1 = "hero"
    word2 = "silent"

    # TODO: 4. Consider general usage
    censor_alert(text, word1, word2)

    # Print result `text`
    print(text)
