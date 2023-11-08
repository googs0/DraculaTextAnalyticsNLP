import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rake_nltk import Rake
import gensim
from gensim import corpora
import pyLDAvis.gensim
from gensim.summarization import summarize
from gensim.summarization import keywords

# Load spaCy in English
nlp = spacy.load("en_core_web_sm")

# Initialize Rake for keyword extraction
r = Rake()

# Load Vader
nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()

# "Dracula" book as a string
def readBook():
  f = open("dracula.txt", "r")
  s = f.read().replace("-", " ")
  f.close()
  return ''.join(c for c in s if c.isalnum() or c == " ")

# Read file
dracula = readBook()
doc = nlp(dracula_text)

# Sentiment Analysis
sentiment = analyzer.polarity_scores(dracula_text)
print("Sentiment Analysis Result:\n")
print("Positive: {:.2%}".format(sentiment["pos"]))
print("Neutral: {:.2%}".format(sentiment["neu"]))
print("Negative: {:.2%}".format(sentiment["neg"])
      
# Keyword Extraction
r.extract_keywords_from_text(dracula_text)
keywords = r.get_ranked_phrases()
print("\nExtracted Keywords:")
for keyword in keywords:
  print(keyword)

# Topic Modeling
tokens = [token.text for token in doc if token.is_alpha]
dictionary = corpora.Dictionary([tokens])
corpus = [dictionary.doc2bow(tokens) for tokens in tokens]
lda_model = gensim.modelsLdaMode1(corpus, num_topics=10, id2word=dictionary)

topics = lda_model.print_topics()
print("\nLDA Topics:")
for topic in topics:
  print(topic)

# Text Summarization
summary = summarize(dracula_text, ratio=0.5)
print("\nSummary:")
print(summary)

# Part-of-speech tags
pos_tag = [(token.text, token.pos_) for token in doc]
print("\nPart of Speech Tags:")
for word, pos in pos_tag:
  print(f"{word} : {pos}")
  
# Initialize dictionary to store named entities by type
named_entities = {}
people = []
places = []
organizations = []

for ent in doc.ents:
  if ent.label_ not in named_entities:
    named_entities[ent.label_] = []
  named_entities[ent.label_].append(ent.text)
  
  if ent.label_ == "PERSON":
    people.append(ent.text)
  elif ent.label_ == "GPE":
    places.append(ent.text)
  elif ent.label_ == "ORG":
    organizations.append(ent.text)

# Print entities by type
for label, entities in named_entities.items():
  print(f"Named Entities of Type: '{label}'")
  for entity in set(entities):
    print(f"{entity}\n")

print("\nPeople:")
for person in set(people):
  print(person)
  
print("\nPlaces:")
for place in set(places):
  print(place)

print("\nOrganizations:")
for organization in set(organizations):
  print(organization)

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