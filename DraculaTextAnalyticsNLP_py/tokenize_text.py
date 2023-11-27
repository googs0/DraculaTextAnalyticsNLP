from imports import threading, hashlib, logging, nlp, time
from utils import convert_cleaned_str

# Store text
tokenized_text_cache = {}

# Sync access to cache
tokenized_text_cache_lock = threading.Lock()


def get_tokens_info(cleaned_text):
    # Lock for thread safety
    with tokenized_text_cache_lock:
        # Calculate hash of cleaned text cache key
        text_hash = hashlib.md5(cleaned_text.encode()).hexdigest()

        # Check for tokens in cache
        if text_hash in tokenized_text_cache:
            logging.info(f"Tokens found in cache for text hash '{text_hash}'")
            return tokenized_text_cache[text_hash]

        logging.info(f"Creating tokens...")

        doc = nlp(cleaned_text)

        # Combine tokens into a space-separated str
        tokens_str = " ".join([token.text for token in doc])

        # Cache tokens info for future use
        tokenized_text_cache[text_hash] = (tokens_str, doc)
        logging.info(f"Added tokens to cache for text hash '{text_hash}'")

    return tokens_str, doc


def tokenize_text(text):
    logging.info("Tokenization started.")
    start_time = time.time()

    # Clean text and get tokens info
    cleaned_text = convert_cleaned_str(text)
    tokens_str, doc = get_tokens_info(cleaned_text)

    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Tokenization finished. Duration: {duration:.2f} seconds.\n")
    return tokens_str, doc
