maxcal = 0
maxcal2 = 0
maxcal3 = 0
curcal = 0
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            curcal += int(line)
        else:
            if curcal >= maxcal:
                maxcal3 = maxcal2
                maxcal2 = maxcal
                maxcal = curcal
            elif curcal >= maxcal2:
                maxcal3 = maxcal2
                maxcal2 = curcal
            elif curcal >= maxcal3:
                maxcal3 = curcal
            curcal = 0
print(maxcal + maxcal2 + maxcal3)
