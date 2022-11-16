def censor_alert(text, *words, censor_char="*", threshold=5):
    for word in words:
        text = text.replace(word, censor_char * len(word))
        if text.count(censor_char) > threshold:
            print("More than %d %s" % (threshold, censor_char))

    return text


if __name__ == "__main__":
    text = """Because he's the hero Gotham deserves but not the one it needs right now.
So we will hunt him, because he can take it. Because he's not out hero.
He is a silent guardian, a watchful protector... a dark knight."""

    word1 = "hero"
    word2 = "silent"

    # TODO: 4. Consider general usage
    text = censor_alert(text, word1, word2)

    # Print result `text`
    print(text)
