def get_input():
    """read input return text"""
    # return sys.stdin.read()
    with open("inputs/text1.txt", encoding="utf-8") as f:
        return f.read()