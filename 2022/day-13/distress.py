from functools import cmp_to_key


char_buf = None
char_iter = None


def get_char():
    global char_buf, char_iter
    if char_buf is not None:
        ch = char_buf
        char_buf = None
    else:
        try:
            ch = next(char_iter)
        except StopIteration:
            ch = None
    return ch


def unget_char(ch):
    global char_buf
    char_buf = ch


def get_nonblank(ch):
    while ch == " ":
        ch = get_char()
    return ch


def parse_number(ch):
    result = 0
    ch = get_nonblank(ch)
    while ch is not None and "0" <= ch <= "9":
        result = (result * 10) + ord(ch) - ord("0")
        ch = get_char()
    unget_char(ch)
    return result


def parse_list(ch):
    result = []
    ch = get_nonblank(ch)
    if ch != "[":
        raise SyntaxError(f"Open bracket expected at '{ch}'")
    ch = get_nonblank(get_char())
    while ch != "]":
        result.append(parse_item(ch))
        ch = get_nonblank(get_char())
        if ch == ",":
            ch = get_nonblank(get_char())
        elif ch != "]":
            raise SyntaxError(f"Comma or close bracket expected at '{ch}'")
    return result


def parse_item(ch):
    ch = get_nonblank(ch)
    if ch is None:
        raise SyntaxError(f"Item expected")
    elif ch == "[":
        return parse_list(ch)
    elif "0" <= ch <= "9":
        return parse_number(ch)
    else:
        raise SyntaxError(f"Number or list expected at '{ch}'")


def parse_line(line):
    global char_iter
    char_iter = iter(line)
    return parse_item(get_char())


def compare_lists(list1, list2):
    n = min(len(list1), len(list2))
    for i in range(0, n):
        result = compare_items(list1[i], list2[i])
        if result != 0:
            return result
    return len(list1) - len(list2)


def compare_items(item1, item2):
    if isinstance(item1, list):
        if isinstance(item2, list):
            return compare_lists(item1, item2)
        else:
            return compare_lists(item1, [item2])
    else:
        if isinstance(item2, list):
            return compare_lists([item1], item2)
        else:
            return item1 - item2


with open('input.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines_iter = iter(lines)

    index = 0
    total = 0
    all_items = []
    while True:
        while True:
            try:
                line = next(lines_iter)
            except StopIteration:
                line = None
            if line != "":
                break
        if line is None:
            break
        first = parse_line(line)
        line = next(lines_iter)
        second = parse_line(line)
        result = compare_items(first, second)
        index += 1
        if result <= 0:
            total += index
        all_items.append(first)
        all_items.append(second)

print("answer for part one:", total)

divider1 = [[2]]
divider2 = [[6]]
all_items.append(divider1)
all_items.append(divider2)

sorted_items = sorted(all_items, key=cmp_to_key(compare_items))

decoder_key = 1
for i in range(0, len(sorted_items)):
    if compare_items(sorted_items[i], divider1) == 0 or \
        compare_items(sorted_items[i], divider2) == 0:
        decoder_key *= i + 1
print("decoder key is", decoder_key)
