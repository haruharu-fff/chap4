# sqlalchemyライブラリから使用する型などをインポート
from sqlalchemy import Column, Integer, String, DateTime, Text
import json

# Baseクラス作成用にインポート
from sqlalchemy.ext.declarative import declarative_base

# Baseクラスを作成
Base = declarative_base()


# Baseクラスを継承したモデルを作成
class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20))
    deadline = Column(DateTime)
    memo = Column(String(140))
    children = Column(Text, nullable=False, default="[]")

    def title_name(self):
        return f"{self.title}"

    def set_children(self, list_of_str: list):
        self.children = json.dumps(list_of_str)

    def get_children(self):
        return json.loads(self.children or "[]")
