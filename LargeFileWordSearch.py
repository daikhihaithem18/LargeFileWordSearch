import os
import re
import mmap

# Counter for the filtered words
counter = 0

# Word to filter (can use regular expressions)
word_to_filter = "lolipopftp\.lolipop\.jp"

# Compiled regex pattern for word matching
pattern = re.compile(word_to_filter)

# Function to filter words and write to a file
def filter(word):
    global counter
    if pattern.search(word):
        print("[+] Filtered: {} => {}".format(word_to_filter, word))
        counter += 1
        with open("filtered_words.txt", "a") as file:
            file.write("[{}] => {}\n".format(word_to_filter, word))

# Get the path from the user
path = raw_input("Enter the path to the file or folder you want to process: ")

def process_file(file_path):
    try:
        with open(file_path, "rb", 0) as file:
            mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            print("Processing file:", file_path)
            for match in re.finditer(word_to_filter.encode(), mmapped_file):
                word = mmapped_file[match.start() - 50:match.end() + 50].decode("utf-8")
                filter(word)
            mmapped_file.close()
    except IOError:
        print("File not found or could not be opened for:", file_path)
    except OSError:
        print("File or folder not found or could not be opened.")

if os.path.isdir(path):
    # Process all files in the folder
    for root, dirs, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            process_file(file_path)
elif os.path.isfile(path):
    # Process the single specified file
    process_file(path)
else:
    print("Invalid path. Please provide a valid file or folder path.")

print("Total Counter:", counter)
