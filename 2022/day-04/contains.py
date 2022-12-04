import re

n = 0
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        mr = re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line)
        if not mr:
            print(f"This line doesn't match the regex: {line}")
        start1 = int(mr.group(1))
        end1 = int(mr.group(2))
        start2 = int(mr.group(3))
        end2 = int(mr.group(4))
        if (start1 <= start2 and end2 <= end1) or (start2 <= start1 and end1 <= end2):
            n += 1
print(n)
