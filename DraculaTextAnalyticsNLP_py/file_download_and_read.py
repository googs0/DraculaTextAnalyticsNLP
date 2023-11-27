from imports import requests, logging
from utils import convert_cleaned_str


def download_text(url, local_filename):
    try:
        # Download content from URL
        response = requests.get(url)
        response.raise_for_status()

        # Save to local file
        with open(local_filename, 'wb') as file_handle:
            file_handle.write(response.content)

        logging.info(f"File '{local_filename}' downloaded and saved successfully.\n")
        return True

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred during download: {http_err}")
        return False
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An unexpected error occurred during download: {req_err}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False


def read_text(local_filename):
    try:
        with open(local_filename, 'r', encoding='utf-8') as file:
            text = file.read().replace("-", " ")

            cleaned_text = convert_cleaned_str(text)

        return cleaned_text

    except Exception as e:
        logging.error(f"An error occurred during text reading: {e}")
        return None


def download_and_read_text(url, local_filename):
    try:
        if download_text(url, local_filename):
            # Read and preprocess the content from the local file
            cleaned_text = read_text(local_filename)
            return cleaned_text

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
