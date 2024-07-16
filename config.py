# arXiv settings
ARXIV_CATEGORIES = ["cs.AI", "cs.AR", "cs.ET", "cs.LO", "eees.SP", "math.IT"]
ARXIV_MAX_RESULTS = 20
ARXIV_SORT_BY = "submittedDate"
ARXIV_SORT_ORDER = "descending"

# Jina settings
JINA_API_KEY = ""

# Notion settings
NOTION_API_KEY = ""
NOTION_DATABASE_ID = ""

# LLM settings
LLM_MODEL = "gemini-1.5-flash-latest"
LLM_API_KEY = ""
LLM_MAX_TOKENS = 1, 000, 000

# Ochiai format prompts
OCHIAI_FORMAT = {
    "キーワード": "論文本文中に「Index Term」があればそれを抜き出してください。無ければ、この論文を理解するために必要なキーワードを本文中から5個抽出してください。返答の中に「Index Term:...」の形式で出力してください。",
    "論文の概要と目的": "どのような内容ですか？論文の概要と目的を述べなさい。",
    "従来研究との比較・改善点": "先行研究をどのように改善していますか？この研究が先行研究をどのように強化または改善しているかを説明する。",
    "核となる技術・手法": "核となる技術や方法は何か？論文で導入または改善された主な技術や方法について説明してください。",
    "有効性の検証方法": "その有効性はどのように検証されましたか？新規または改良された技術・方法の有効性を検証するために用いた方法を詳述する。",
    "議論すべき点": "議論すべき点はあるか？限界、含意、論争などの論点があれば強調する。",
    "次に読むべき論文": "次に読むべき論文は何ですか？引用文献から次に読むべき論文を提案し、引用番号と論文タイトルを示す。",
}

# Notion columns mapping
NOTION_COLUMNS = {
    "タイトル(英語)": "title",
    "abstract": "abstract",
    "Index Term": "Index Term",
    "概要・目的": "概要・目的",
    "先行研究との比較": "先行研究との比較",
    "核となる技術・手法": "核となる技術・手法",
    "有効性の検証方法": "有効性の検証方法",
    "議論すべき点": "議論すべき点",
    "次に読むべき論文": "次に読むべき論文",
    "論文ID": "論文ID",
    "カテゴリ": "論文カテゴリ",
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
