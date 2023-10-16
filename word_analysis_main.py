# "Dracula" book as a string
def readBook():
  f = open("dracula.txt", "r")
  s = f.read().replace("-", " ")
  f.close()
  return ''.join(c for c in s if c.isalnum() or c == " ")

# Read file
dracula = readBook()

# Split text by word and convert words to lowercase
words = [words.lower() for words in dracula.split()]

# Format Header
header = "Dracula by Bram Stoker\n -- Text Analytics --"
print(f"{header}\n")

# Find most common word
mostCommonWord = ""
maxCount = 0
wordCount = {}

for word in words:
  if word in wordCount:
    wordCount[word] += 1
  else:
    wordCount[word] = 1
    
  # Check if word in the word count is greater than max count
  if wordCount[word] > maxCount:
    maxCount = wordCount[word]
    mostCommonWord = word

print(f"The most common word is '{mostCommonWord}' appearing {maxCount} times\n")

# Unique four-letter words are in the book
fourLetterWords = []

# Append four letter words not already in list
for word in words:
  if (len(word) == 4 and word not in fourLetterWords):
    fourLetterWords.append(word)
    
print(f"There are {len(fourLetterWords)} unique 4 letter words\n")

# Words that shows up more than 500 times
wordsOver500 = []

for word in wordCount:
  if wordCount[word] > 500:
    wordsOver500.append(word)

# Return results
for word in wordsOver500:
  print(f"{word}: {wordCount[word]} times")
print("\n-- Analysis Complete --\n")