from utils import convert_cleaned_str
from process_overview_analysis_results import process_analysis_results
from constants import common_words
from tokenize_text import tokenize_text
from topic_modeling import topic_modeling
from part_of_speech_tags import extract_part_of_speech_tags
from sentiment_analysis import analyze_sentiment
from entity_by_type_analysis import analyze_entities_by_type
from summarize_text_nlp import summarize_text


def analyze_text_and_nlp(text):

    cleaned_text = convert_cleaned_str(text)

    process_analysis_results(cleaned_text, common_words)

    tokens_str, doc = tokenize_text(cleaned_text)

    extract_part_of_speech_tags(tokens_str, doc, view_all=False)

    analyze_sentiment(tokens_str, doc)

    topic_modeling(cleaned_text)

    analyze_entities_by_type(doc)

    summarize_text(tokens_str, doc)
