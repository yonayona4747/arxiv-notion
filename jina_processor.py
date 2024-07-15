import requests

from utils import log_function_call, retry_on_exception, get_logger

logger = get_logger(__name__)


class JinaProcessor:
    def __init__(self, api_key):
        self.api_key = api_key

    @log_function_call
    @retry_on_exception(max_retries=3, exceptions=(requests.RequestException,))
    def get_full_text(self, paper_info):
        logger.info(f"Processing paper: {paper_info['title']}")

        # Try HTML version first
        html_url = f"https://r.jina.ai/{paper_info['html_url']}"
        logger.debug(f"######{paper_info['html_url']}")

        response = self._make_request(html_url)
        if response.status_code == 200:
            logger.debug(
                f"Successfully retrieved HTML content for {paper_info['title']}"
            )
            return response.text

        # If HTML fails, try PDF version
        pdf_url = f"https://r.jina.ai/{paper_info['pdf_url']}"
        response = self._make_request(pdf_url)
        if response.status_code == 200:
            logger.debug(
                f"Successfully retrieved PDF content for {paper_info['title']}"
            )
            return response.text

        logger.error(f"Failed to retrieve content for {paper_info['title']}")
        return None

    @log_function_call
    def _make_request(self, url):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # response = requests.get(url, headers=headers, timeout=30)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response