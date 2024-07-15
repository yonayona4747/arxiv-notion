import argparse
import logging

from arxiv_fetcher import ArxivFetcher
from jina_processor import JinaProcessor
from llm_summarizer import LLMSummarizer
from notion_writer import NotionWriter
import config
from utils import setup_logging, get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="arXiv paper summarizer and Notion writer"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    setup_logging(args.debug)

    try:
        arxiv_fetcher = ArxivFetcher(config.ARXIV_CATEGORIES)
        jina_processor = JinaProcessor(config.JINA_API_KEY)
        llm_summarizer = LLMSummarizer(config.LLM_API_KEY, config.LLM_MODEL)
        notion_writer = NotionWriter(config.NOTION_API_KEY, config.NOTION_DATABASE_ID)

        # DEBUGモードのチェック
        if args.debug:
            max_results = 1
        else:
            max_results = config.ARXIV_MAX_RESULTS

        papers = arxiv_fetcher.fetch_latest_papers(max_results=max_results)

        for paper in papers:
            try:
                full_text = jina_processor.get_full_text(paper)
                if full_text:
                    summary_json = llm_summarizer.summarize(full_text, paper)

                    logger.debug(f"#### sumamry_json : \n{summary_json}")
                    logger.info(f"{type(summary_json)}")

                    summary = summary_json["論文データ"]

                    logger.debug(f"#### summary : \n{summary}")
                    
                    # paper ではなく paper_info を渡す
                    notion_writer.write_entry(paper, summary, full_text)  
                else:
                    logger.warning(
                        f"Skipping paper due to missing full text: {paper['title']}"
                    )
            except Exception as e:
                logger.error(f"Error processing paper {paper['title']}: {str(e)}")

    except Exception as e:
        logger.error(f"An error occurred in the main process: {str(e)}")


if __name__ == "__main__":
    main()