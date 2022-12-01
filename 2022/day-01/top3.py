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
                # new greatest, demote old greatest to 2nd greatest, and old 2nd greatest to third
                maxcal3 = maxcal2
                maxcal2 = maxcal
                maxcal = curcal
            elif curcal >= maxcal2:
                # new second greatest, demote old 2nd greatest to 3rd then save new 2nd
                maxcal3 = maxcal2
                maxcal2 = curcal
            elif curcal >= maxcal3:
                # new third greatest, just save it
                maxcal3 = curcal
            curcal = 0
print(maxcal + maxcal2 + maxcal3)
