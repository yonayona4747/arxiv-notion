import google.generativeai as genai
import logging

from utils import log_function_call, retry_on_exception, get_logger
import config

logger = get_logger(__name__)


class LLMSummarizer:
    def __init__(self, api_key, model="gemini-pro"):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    @log_function_call
    @retry_on_exception(max_retries=3, exceptions=(Exception,))
    def summarize(self, full_text, paper_info):
        logger.info(f"Summarizing paper: {paper_info['title']}")

        prompt = f"""
        論文のタイトル: {paper_info['title']}
        著者: {', '.join(paper_info['authors'])}
        アブストラクト: {paper_info['abstract']}

        以下の論文本文を要約してください。要約は日本語で、各項目について400字程度にしてください。
        また、要約は以下の形式に従ってください：

        {config.OCHIAI_FORMAT['論文の概要と目的']}
        {config.OCHIAI_FORMAT['従来研究との比較・改善点']}
        {config.OCHIAI_FORMAT['核となる技術・手法']}
        {config.OCHIAI_FORMAT['有効性の検証方法']}
        {config.OCHIAI_FORMAT['議論すべき点']}
        {config.OCHIAI_FORMAT['次に読むべき論文']}

        論文本文:
        {full_text}
        """

        response = self.model.generate_content(prompt)
        summary = response.text

        # LLMの出力をログに記録
        logger.debug(f"LLM Output:\n{summary}") 

        logger.debug(f"Generated summary for {paper_info['title']}")
        return summary