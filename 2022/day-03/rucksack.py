sum = 0
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        first_half = line[0: len(line)//2]
        second_half = line[len(line)//2:]
        first_set = set(list(first_half))
        second_set = set(list(second_half))
        common_set = first_set.intersection(second_set)
        if len(common_set) != 1:
            print(f"error, this line has {len(common_set)} common letters: {line}")
            break
        common_letter = list(common_set)[0]
        if "a" <= common_letter <= "z":
            sum += ord(common_letter) - ord("a") + 1
        elif "A" <= common_letter <= "Z":
            sum += ord(common_letter) - ord("A") + 27
        else:
            print(f"error, this line has invalid common letter {common_letter}: {line}")
            break
print(sum)
