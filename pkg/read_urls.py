def get_urls():
    with open("./urls.txt") as f:
        lines = f.readlines()

    lines = [l.split()[0] for l in lines]

    # for line in lines:
    #     print(line)

    return lines
