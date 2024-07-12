# Scheduling
EXECUTION_TIME = "02:00"  # HH:MM format

# arXiv settings
ARXIV_CATEGORIES = ["cs.AI", "cs.CL"]
ARXIV_MAX_RESULTS = 100
ARXIV_SORT_BY = "submittedDate"
ARXIV_SORT_ORDER = "descending"

# API keys
NOTION_API_KEY = ""
JINA_API_KEY = ""
LLM_API_KEY = ""

# Notion settings
NOTION_DATABASE_ID = ""

# LLM settings
LLM_MODEL = "gpt-3.5-turbo"
LLM_MAX_TOKENS = 1000
LLM_TEMPERATURE = 0.7

# Ochiai format prompts
OCHIAI_FORMAT = {
    "論文の概要と目的": "どのような内容ですか？論文の概要と目的を述べなさい。",
    "従来研究との比較・改善点": "先行研究をどのように改善していますか？この研究が先行研究をどのように強化または改善しているかを説明する。",
    "核となる技術・手法": "核となる技術や方法は何か？論文で導入または改善された主な技術や方法について説明してください。",
    "有効性の検証方法": "その有効性はどのように検証されましたか？新規または改良された技術・方法の有効性を検証するために用いた方法を詳述する。",
    "議論すべき点": "議論すべき点はあるか？限界、含意、論争などの論点があれば強調する。",
    "次に読むべき論文": "次に読むべき論文は何ですか？引用文献から次に読むべき論文を提案し、引用番号と論文タイトルを示す。",
}

# API request settings
API_REQUEST_TIMEOUT = 30
API_RETRY_ATTEMPTS = 3

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = "arxiv_summarizer.log"

# System settings
MAX_CONCURRENT_TASKS = 5
CACHE_DIR = "./cache"

# Error handling settings
MAX_RETRIES = 3
RETRY_DELAY = 5

# Output format settings
SUMMARY_MAX_LENGTH = 500
