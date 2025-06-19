# sqlalchemyライブラリから使用する型などをインポート
from sqlalchemy import Column, Integer, String, DateTime

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
    child = Column(String(20))

    def title_name(self):
        return f"{self.title}"
