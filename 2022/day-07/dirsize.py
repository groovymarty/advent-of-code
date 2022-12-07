# A class to represent a file
# Every file has a name and a size
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

# A class to represent a directory
# Every directory has a name, a parent directory, a dictionary of files, and
# a dictionary of child directories
# We also keep track of the total size of the files in this directory,
# and there's a variable 'tot_size' used to help compute the required answers
class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.dirs = {}
        self.files = {}
        self.parent = parent
        self.file_size_sum = 0
        self.tot_size = 0

    def add_file(self, file):
        print(f"adding file {file.name} to {self.name}")
        self.files[file.name] = file
        self.file_size_sum += file.size

    def add_dir(self, dir):
        print(f"adding dir {dir.name} to {self.name}")
        self.dirs[dir.name] = dir

    def find_dir(self, name):
        return self.dirs[name] if name in self.dirs else None

    def calc_total_size(self):
        # return total size of files in this directory,
        # plus total sizes of all child directories, recursively
        self.tot_size = self.file_size_sum
        for child in self.dirs.values():
            self.tot_size += child.calc_total_size()
        return self.tot_size

    def calc_total_size_sum(self, max_threshold):
        # considering only directories up to the specified max size,
        # return sum of sizes of this directory and all child directories, recursively
        sum = 0
        if self.tot_size <= max_threshold:
            sum += self.tot_size
        for child in self.dirs.values():
            sum += child.calc_total_size_sum(max_threshold)
        return sum

    def find_smallest_dir(self, min_size):
        # considering only directories at least the specified min size,
        # return the smallest among this directory and all child directories, recursively
        smallest = self if self.tot_size >= min_size else None
        for child in self.dirs.values():
            child_smallest = child.find_smallest_dir(min_size)
            if child_smallest:
                if smallest:
                    if child_smallest.tot_size < smallest.tot_size:
                        smallest = child_smallest
                else:
                    smallest = child_smallest
        return smallest


root = Dir("/", None)
curdir = root


def process_command(command, response):
    global curdir
    print(f"doing {command}")
    parts = command.split()
    if len(parts) == 3 and parts[1] == "cd":
        if parts[2] == "/":
            curdir = root
        elif parts[2] == "..":
            curdir = curdir.parent
        else:
            curdir = curdir.find_dir(parts[2])
        if not curdir:
            print(f"command error: '{command}': directory {parts[2]} not found")
    elif len(parts) == 2 and parts[1] == "ls":
        for line in response:
            rparts = line.split()
            if len(rparts) == 2 and rparts[0] == "dir":
                dir = Dir(rparts[1], curdir)
                curdir.add_dir(dir)
            elif len(rparts) == 2:
                file = File(rparts[1], int(rparts[0]))
                curdir.add_file(file)
            else:
                print(f"command errorZ: '{command}': unrecognized response line: {line}")


with open('input.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    while len(lines) > 0:
        # get command and response lines
        command = lines.pop(0)
        response = []
        while len(lines) > 0 and lines[0][0] != "$":
            response.append(lines.pop(0))
        process_command(command, response)

root.calc_total_size()
print(f"answer to first part: {root.calc_total_size_sum(100000)}")

total_space = 70000000
update_size = 30000000
space_used = root.tot_size
space_left = total_space - space_used
space_needed = update_size - space_left

print(f"answer to second part: {root.find_smallest_dir(space_needed).tot_size}")
