from notion_client import Client

from utils import log_function_call, retry_on_exception, get_logger
import config

logger = get_logger(__name__)


class NotionWriter:
    def __init__(self, api_key, database_id):
        self.client = Client(auth=api_key)
        self.database_id = database_id

    @log_function_call
    @retry_on_exception(max_retries=3, exceptions=(Exception,))
    def write_entry(self, paper_info, summary, full_text):  # summaryはJSON形式
        logger.info(f"Writing entry to Notion for paper: {paper_info['title']}")

        paper_data = summary

        # Notionページの作成
        new_page = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                config.NOTION_COLUMNS["タイトル(英語)"]: {
                    "title": [{"text": {"content": paper_data["論文タイトル"]}}]  
                },
                config.NOTION_COLUMNS["abstract"]: {
                    "rich_text": [{"text": {"content": paper_data["アブストラクト"]}}]  
                },
                config.NOTION_COLUMNS["Index Term"]: {
                    "multi_select": [
                        {"name": term.strip()} for term in paper_data["キーワード"].split(",")
                    ]
                },
                config.NOTION_COLUMNS["概要・目的"]: {
                    "rich_text": [
                        {
                            "text": {
                                "content": paper_data["論文の概要と目的"]
                            }
                        }
                    ]
                },
                config.NOTION_COLUMNS["先行研究との比較"]: {
                    "rich_text": [
                        {
                            "text": {
                                "content": paper_data["従来研究との比較・改善点"] 
                            }
                        }
                    ]
                },
                config.NOTION_COLUMNS["核となる技術・手法"]: {
                    "rich_text": [
                        {
                            "text": {
                                "content": paper_data["核となる技術・手法"]
                            }
                        }
                    ]
                },
                config.NOTION_COLUMNS["有効性の検証方法"]: {
                    "rich_text": [
                        {
                            "text": {
                                "content": paper_data["有効性の検証方法"]
                            }
                        }
                    ]
                },
                config.NOTION_COLUMNS["議論すべき点"]: {
                    "rich_text": [
                        {"text": {"content": paper_data["議論すべき点"]}}  
                    ]
                },
                config.NOTION_COLUMNS["次に読むべき論文"]: {
                    "rich_text": [
                        {
                            "text": {
                                "content": paper_data["次に読むべき論文"] 
                            }
                        }
                    ]
                },
            },
        )

        logger.debug(f"Successfully created Notion page for {paper_info['title']}")
        return new_page