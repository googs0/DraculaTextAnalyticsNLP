from imports import logging, multiprocessing
from file_download_and_read import download_and_read_text
from analyze_text_and_nlp import analyze_text_and_nlp


# Header and Setup
text_title = "Dracula"
author = "Bram Stoker"
header = f"{text_title} by {author}\n -- Text Analytics --\n"
logging.info(header)

dracula_url = "https://raw.githubusercontent.com/googs0/DraculaTextAnalyticsNLP/main/assets/txt/dracula.txt"
local_filepath = "dracula.txt"
dracula = download_and_read_text(dracula_url, local_filepath)


def main():
    multiprocessing.freeze_support()
    analyze_text_and_nlp(dracula)


if __name__ == "__main__":
    main()
