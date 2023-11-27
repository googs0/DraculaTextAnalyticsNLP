# All Constants 

COMMON_WORDS_AND_NUMBERS = {
    'a', 'about', 'after', 'again', 'all', 'am', 'an', 'and', 'any', 'at', 'as', 'are', 'away', 'back', 'bad', 'be',
    'been', 'before', 'but', 'by', 'came', 'can',  'chapter', 'come', 'could', 'did', 'do', 'down', 'each', 'even',
    'every', 'for', 'from', 'great', 'go', 'good', 'have', 'has', 'had', 'he', 'her', 'hers', 'here', 'him', 'his',
    'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'know', 'like', 'liked', 'look', 'looked', 'made', 'man', 'may',
    'me', 'my', 'more', 'myself',  'much', 'must', 'no', 'not', 'now', 'of', 'on', 'one', 'only', 'or', 'other', 'our',
    'ours', 'ourself', 'ourselves', 'out', 'over', 'own', 'said', 'saw', 'says', 'see', 'seemed', 'seems', 'seem',
    'shall', 'shalt', 'she', 'should', 'so', 'some', 'such', 'take', 'took', 'tell', 'than', 'that', 'the', 'then',
    'their', 'them', 'themselves', 'there', 'these', 'they', 'think', 'this', 'though', 'through', 'to', 'too', 'up',
    'us', 'very', 'was', 'way', 'we', 'well', 'went', 'were', 'what', 'when',  'where',  'which', 'who', 'whom', 'will',
    'with', 'woman', 'would', 'ye', 'yes', 'you', 'your', 'yours', 'yourself', 'yourselves',
}

COMMON_WORDS_AND_NUMBERS.update(str(num) for num in range(1, 100000))
COMMON_WORDS_AND_NUMBERS.update(chr(i) for i in range(ord('a'), ord('z') + 1))
common_words = frozenset(COMMON_WORDS_AND_NUMBERS)

# Process Analysis Results
TOP_WORDS_COUNT = 20
WORDS_OVER_THRESHOLD = 1000
