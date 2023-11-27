import multiprocessing
import time
import requests
from gensim import corpora
from gensim.models import LdaMulticore
from collections import Counter
import spacy
from textblob import TextBlob
from concurrent.futures import ThreadPoolExecutor
import threading
import logging
import log_config
import hashlib
from nltk.sentiment import SentimentIntensityAnalyzer
from gensim.models import CoherenceModel
from collections import defaultdict
import re

log_config.setup_logging()

# Load spaCy
nlp = spacy.load("en_core_web_lg")