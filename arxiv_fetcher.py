import arxiv

from utils import log_function_call, retry_on_exception, get_logger

logger = get_logger(__name__)


class ArxivFetcher:
    def __init__(self, categories):
        self.categories = categories

    @log_function_call
    @retry_on_exception(max_retries=3, exceptions=(arxiv.HTTPError,))
    def fetch_latest_papers(self, max_results=100):  # max_results を引数に追加
        logger.info(f"Fetching papers for categories: {self.categories}")
        search = arxiv.Search(
            query=f"cat:{' OR '.join(self.categories)}",
            max_results=max_results,  # max_results を使用する
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        papers = []
        for result in search.results():
            paper = {
                "id": result.entry_id,
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "pdf_url": result.pdf_url,
                "html_url": f"https://arxiv.org/html/{result.get_short_id()}",
                "published": result.published,
            }
            papers.append(paper)
            logger.debug(f"Fetched paper: {paper['title']}")

        logger.info(f"Fetched {len(papers)} papers")
        return papers