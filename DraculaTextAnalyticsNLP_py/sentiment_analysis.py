from imports import nlp, TextBlob, SentimentIntensityAnalyzer, ThreadPoolExecutor, logging, time


# Single sentence sentiment analysis (primarily with TextBlob)
def process_task(sentence):
    sia = SentimentIntensityAnalyzer()
    blob = TextBlob(sentence)

    spacy_polarity = (blob.sentiment.polarity + 1) / 2

    sentiment = {
        'text': sentence,
        'spacy_polarity': spacy_polarity,
        'sia_compound': sia.polarity_scores(sentence)['compound'],
    }
    return sentiment


# Batch process sentences
def process_with_thread_pool_batched(sentences, batch_size=10, max_workers=None):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            batch_results = list(executor.map(process_task, batch))
            results.extend(batch_results)

    return results


# Sentiment analysis of batched sentences
def analyze_sentiment_batch(sentences, batch_size=10):
    results = process_with_thread_pool_batched(sentences, batch_size)

    return results


# Single sentence sentiment analysis (both TextBlob and SIA)
def analyze_sentence_sentiment(sentence):
    # TextBlob
    blob = TextBlob(sentence)
    blob_polarity = blob.sentiment.polarity
    blob_subjectivity = blob.sentiment.subjectivity

    # SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    sia_scores = sia.polarity_scores(sentence)
    sia_compound = sia_scores['compound']

    return {
        'text': sentence,
        'blob_polarity': blob_polarity,
        'blob_subjectivity': blob_subjectivity,
        'sia_compound': sia_compound,
    }


def analyze_sentiment(tokens_str, doc):
    logging.info("Initiating Sentiment Analysis\n")
    start_time = time.time()

    doc = doc if doc else nlp(tokens_str)
    sentences = [sent.text for sent in doc.sents]

    # Batch processing SentimentIntensityAnalyzer
    sentiment = process_with_thread_pool_batched(sentences)

    # Overall sentiment for the entire text
    overall_spacy_polarity = sum(sent['spacy_polarity'] for sent in sentiment) / len(sentiment)
    overall_sia_compound = sum(sent['sia_compound'] for sent in sentiment) / len(sentiment)

    # Subjectivity Analysis
    overall_subjectivity = get_subjectivity(tokens_str, doc)
    logging.info(f"Overall Subjectivity: {overall_subjectivity}\n")

    # Overall sentiment analysis results
    logging.info(
        f"Sentiment Analysis:\n"
        f"SpaCy Polarity: {overall_spacy_polarity}\n"
        f"SIA Compound: {overall_sia_compound}\n"
        f"Number of Sentences: {len(sentiment)}\n"
    )

    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Sentiment Analysis finished. Duration: {duration:.2f} seconds.\n")

    return sentiment


def get_subjectivity(tokens_str, doc):
    doc = doc if doc else nlp(tokens_str)

    # TextBlob
    sentences = [sent.text for sent in doc.sents]
    subjectivities = []

    for sentence in sentences:
        blob = TextBlob(sentence)
        subjectivity = blob.sentiment.subjectivity
        subjectivities.append(subjectivity)

    # Overall subjectivity for the entire text
    overall_subjectivity = sum(subjectivities) / len(subjectivities)

    # Most subjective and least subjective sentences
    most_subjective_sentence = max(sentences, key=lambda x: TextBlob(x).sentiment.subjectivity)
    least_subjective_sentence = min(sentences, key=lambda x: TextBlob(x).sentiment.subjectivity)

    # Count of subjective and objective sentences
    subjective_count = sum(subj > 0.5 for subj in subjectivities)
    objective_count = len(subjectivities) - subjective_count

    logging.info("TextBlob Subjectivity Analysis:")
    logging.info(f"Overall Subjectivity Score: {overall_subjectivity}")
    logging.info(f"Most Subjective Sentence: {most_subjective_sentence}")
    logging.info(f"Least Subjective Sentence: {least_subjective_sentence}")
    logging.info(f"Subjective Sentence Count: {subjective_count}")
    logging.info(f"Objective Sentence Count: {objective_count}\n")

    return overall_subjectivity
