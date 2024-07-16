# arXiv論文要約 & Notion登録ツール

## 概要

このツールは、arXivから指定したカテゴリの最新論文情報を取得し、LLM (Gemini 1.5) を用いて要約を生成し、Notionデータベースに登録するツールです。 

## 機能

* arXivから指定されたカテゴリの最新論文情報を取得
* LLMを用いて論文の要約を生成 (落合フォーマット)
* Notionデータベースに論文情報と要約を登録

## 使い方

### 初期セットアップ
#### Notion
- Notion Integrationの作成
- Notion Integrationのシークレットキー取得
- Notionで新規DB作成し、次のようにカラムを設定する
  - カラム名 : タイプ
  - title : Title
  - Index Term : Multi-select
  - 概要・目的 : rich_text
  - 先行研究との比較 : rich_text
  - 核となる技術・手法 : rich_text
  - 有効性の検証方法 : rich_text
  - 議論すべき点 : rich_text
  - 次に読むべき論文 : rich_text
- NotionでDBのID取得
- NotionのDBとIntegrationの連携
#### Google AIStudio
- Google AIstudioへの登録
- Google AIstudioでのGemini APIキーの取得
#### Jina(※)
- (※ 必要があれば)
- [Jina](https://jina.ai/) でAPIキーの取得


### このプロジェクトの使い方

1.  `config.py` を編集し、必要なAPIキー、データベースID、arXivカテゴリなどを設定します。
2.  `pipenv install -r requirements.txt` を実行し、必要なライブラリをインストールします。
3.  `pipenv run python main.py` を実行すると、ツールが起動します。
4.  `--debug` オプションを付けて実行すると、デバッグモードで実行されます。

## 設定

`config.py` で以下の設定を行います。

*   `ARXIV_CATEGORIES`: arXivのカテゴリをリスト形式で指定します。
*   `NOTION_API_KEY`: Notion APIのトークンを指定します。
*   `NOTION_DATABASE_ID`: NotionデータベースのIDを指定します。
*   `JINA_API_KEY`: Jina AI APIのトークンを指定します。
*   `LLM_API_KEY`: 使用するLLMのAPIキーを指定します。

## TODO

*   実行時引数に日付を受け取るようにする
*   Dockerfileとdocker-compose.yamlの作成

## ライセンス

COPYLEFT
