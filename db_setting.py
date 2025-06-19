# DB操作用にsqlalchemyライブラリインポート
from sqlalchemy import create_engine

# DBの存在確認とDB作成を行うためにインポート
from sqlalchemy_utils import database_exists, create_database

# セッション定義用にインポート
from sqlalchemy.orm import sessionmaker, scoped_session

# モデル定義ファイルインポート
from db_model import Base

# 接続したいDBへの接続情報
user_name = "test"
password = "password"
host = "localhost"
database_name = "Tasks"

# バインディング
DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
    user_name,
    password,
    host,
    database_name,
)

# DBとの接続
ENGINE = create_engine(
    DATABASE,
    # 自動生成されたSQLを吐き出すようにする
    echo=True,
)

# session変数にsessionmakerインスタンスを格納
session = scoped_session(
    # ORマッパーの設定。自動コミットと自動反映はオフにする
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)
# DBが存在しなければ
if not database_exists(ENGINE.url):
    # DBを新規作成する
    create_database(ENGINE.url)

# 定義されているテーブルを一括作成
Base.metadata.create_all(bind=ENGINE)

# DB接続用のセッションクラス、インスタンスが作成されると接続する
Base.query = session.query_property()
