import google.generativeai as genai
import json

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
                次のJSON形式に従って、以下の論文情報をまとめてください。
                なお、下記のjsonはわざと丸括弧を使っているので、出力するときには波括弧を用いよ。

                '''json
                (
                    "論文データ": (
                        "論文タイトル": "論文タイトル",
                        "著者": "著者",
                        "アブストラクト": "アブストラクト",
                        "キーワード": "キーワード",
                        "論文の概要と目的": "論文の概要と目的",
                        "従来研究との比較・改善点": "従来研究との比較・改善点",
                        "核となる技術・手法": "核となる技術・手法",
                        "有効性の検証方法": "有効性の検証方法",
                        "議論すべき点": "議論すべき点",
                        "次に読むべき論文": "次に読むべき論文"
                    )
                )
                '''
                
                論文タイトル、著者、アブストラクト には、与えられた論文の情報をそのまま出力してください。
                キーワードは論文中に「Keyword」や「Index Term」などがあればそれを抽出せよ。
                無い場合は、論文中から5～10個のキーワードを抽出せよ。
                キーワードはカンマ区切りにし、語を翻訳せず原文のまま記載すること。
                論文の概要と目的 から 次に読むべき論文 までは、それぞれ400字程度の日本語で要約してください。
                論文情報
                論文のタイトル: {paper_info['title']}
                著者: {', '.join(paper_info['authors'])}
                アブストラクト: {paper_info['abstract']}
                論文本文
                {full_text}
                要約項目
                {config.OCHIAI_FORMAT['キーワード']}
                {config.OCHIAI_FORMAT['論文の概要と目的']}
                {config.OCHIAI_FORMAT['従来研究との比較・改善点']}
                {config.OCHIAI_FORMAT['核となる技術・手法']}
                {config.OCHIAI_FORMAT['有効性の検証方法']}
                {config.OCHIAI_FORMAT['議論すべき点']}
                {config.OCHIAI_FORMAT['次に読むべき論文']}
            """

        response = self.model.generate_content(prompt)
        summary_str = response.text

        # summary_str = self._escape_json_string(summary_str)

        summary = json.loads(summary_str)

        # LLMの出力をログに記録
        logger.debug(f"LLM Output:\n{summary}") 

        logger.debug(f"Generated summary for {paper_info['title']}")
        return summary


    def _escape_json_string(self, json_str):
        # Pythonのフォーマット指定子と誤認識される可能性のある '"' をエスケープ
        escaped_str = json_str.replace('"', '\\"')
        return escaped_str