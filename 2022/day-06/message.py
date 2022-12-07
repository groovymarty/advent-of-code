with open('input.txt') as f:
    # get the input into a string, strip newline
    data = f.read().strip()
    # n is number of distinct characters counted so far
    n = 0
    # loop over the input, i is index of character being considered
    for i in range(0, len(data)):
        # assume it's distinct so add 1 to count
        n += 1
        # say n is 4, we need to check the past 3 chars and see if current character is a duplicate
        # if n is 3, check past 2 chars
        # if n is 2, check go back one and check
        # if n is 1, no need to check any
        # here is the range for each case:
        # n=4, range(3, 0, -1) returns 3, 2, 1
        # n=3, range(2, 0, -1) returns 2, 1
        # n=2, range(1, 0, -1) returns 1
        # n=1, range(0, 0, -1) returns empty list
        # loop over the range, j takes on the values returned by range as listed above
        for j in range(n-1, 0, -1):
            # look back from current character, i, to character j positions back.. is it a repeat of the same char?
            if data[i] == data[i-j]:
                # yes, this is the part that's hard to explain
                # we have to update n to account for the fact that the current char, i, matches char at i-j
                # the number of chars between these two points is i - (i - j) = j
                # then we have to consider are we off by 1, source of many bugs?
                # helps to draw a picture on paper, think out loud, and/or use test cases
                # we have a big test case with the input.txt file, proving the code here is correct
                n = j
        # if we found fourteen distinct chars in a row, break loop
        if n == 14:
            break
# i is index of last char processed, since index starts at 0 we have to add 1 to get correct result
print(i+1)
