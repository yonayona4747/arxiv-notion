from notion_client import Client
import logging

from utils import log_function_call, retry_on_exception, get_logger
import config

logger = get_logger(__name__)


class NotionWriter:
    def __init__(self, api_key, database_id):
        self.client = Client(auth=api_key)
        self.database_id = database_id

    @log_function_call
    @retry_on_exception(max_retries=3, exceptions=(Exception,))
    def write_entry(self, paper_info, summary, full_text):
        logger.info(f"Writing entry to Notion for paper: {paper_info['title']}")

        # サマリーから各セクションを抽出
        summary_sections = self._extract_summary_sections(summary)

        # Notionページの作成 (デバッグ出力追加)
        properties = {
            config.NOTION_COLUMNS["タイトル(英語)"]: {
                "title": [{"text": {"content": paper_info["title"]}}]
            },
            config.NOTION_COLUMNS["abstract"]: {
                "rich_text": [{"text": {"content": paper_info["abstract"]}}]
            },
            config.NOTION_COLUMNS["Index Term"]: {
                "multi_select": [
                    {"name": term} for term in self._extract_index_terms(full_text)
                ]
            },
            config.NOTION_COLUMNS["概要・目的"]: {
                "rich_text": [
                    {
                        "text": {
                            "content": summary_sections.get("論文の概要と目的", "")
                        }
                    }
                ]
            },
            config.NOTION_COLUMNS["先行研究との比較"]: {
                "rich_text": [
                    {
                        "text": {
                            "content": summary_sections.get(
                                "従来研究との比較・改善点", ""
                            )
                        }
                    }
                ]
            },
            config.NOTION_COLUMNS["核となる技術・手法"]: {
                "rich_text": [
                    {
                        "text": {
                            "content": summary_sections.get(
                                "核となる技術・手法", ""
                            )
                        }
                    }
                ]
            },
            config.NOTION_COLUMNS["有効性の検証方法"]: {
                "rich_text": [
                    {
                        "text": {
                            "content": summary_sections.get("有効性の検証方法", "")
                        }
                    }
                ]
            },
            config.NOTION_COLUMNS["議論すべき点"]: {
                "rich_text": [
                    {"text": {"content": summary_sections.get("議論すべき点", "")}}
                ]
            },
            config.NOTION_COLUMNS["次に読むべき論文"]: {
                "rich_text": [
                    {
                        "text": {
                            "content": summary_sections.get("次に読むべき論文", "")
                        }
                    }
                ]
            },
        }

        # デバッグ出力
        logger.debug("Notion page properties:")
        for key, value in properties.items():
            logger.debug(f"- {key}: {value}")

        new_page = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

        logger.debug(f"Successfully created Notion page for {paper_info['title']}")
        return new_page

    def _extract_summary_sections(self, summary):
        sections = {}
        current_section = None
        for line in summary.split("\n"):
            if any(
                line.strip().startswith(prompt)
                for prompt in config.OCHIAI_FORMAT.values()
            ):
                current_section = line.strip()
                sections[current_section] = ""
            elif current_section:
                sections[current_section] += line + "\n"
        return sections

    def _extract_index_terms(self, full_text):
        # "Index Term:" の行を探す
        for line in full_text.split('\n'):
            if line.startswith("**Index Term:"):
                # "Index Term:" の後ろ側を抽出
                index_terms_str = line[len("Index Term:"):].strip()
                # カンマで区切って空白削除
                terms = [term.strip() for term in index_terms_str.split(",")]
                return terms

        # "Index Term:" が見つからない場合は空リストを返す
        return []