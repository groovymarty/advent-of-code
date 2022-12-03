sum = 0
with open('input.txt') as f:
    lines = f.readlines()
    for i in range(0, len(lines), 3):
        elf1 = lines[i].strip()
        elf2 = lines[i+1].strip()
        elf3 = lines[i+2].strip()
        common_set = set(list(elf1)).intersection(set(list(elf2))).intersection(set(list(elf3)))
        if len(common_set) != 1:
            print(f"error, this group has {len(common_set)} common letters: {elf1}, {elf2}, {elf3}")
            break
        common_letter = list(common_set)[0]
        if "a" <= common_letter <= "z":
            sum += ord(common_letter) - ord("a") + 1
        elif "A" <= common_letter <= "Z":
            sum += ord(common_letter) - ord("A") + 27
        else:
            print(f"error, this group has invalid common letter {common_letter}: {elf1}, {elf2}, {elf3}")
            break
print(sum)
