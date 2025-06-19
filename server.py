from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import db_model as m
import db_setting as s


# データ追加の際に使うデータクラスを作成
class Task(BaseModel):
    title: str
    deadline: datetime
    memo: str
    model_config = {
        "arbitrary_types_allowed": True,
    }


# データを返す際に使うデータクラスを作成
class TaskResponse(BaseModel):
    task_id: int
    title: str
    deadline: datetime
    memo: str
    child: Optional[str]

    class Config:
        orm_mode = True


class Child(BaseModel):
    child: Optional[str] = None


# インスタンスを作成
app = FastAPI()


# タスク追加の処理
@app.post("/tasks")
def add_tasks(data: Task):
    task = m.Tasks()
    session = s.session()
    session.add(task)
    try:
        task.title = data.title
        task.deadline = data.deadline
        task.memo = data.memo
        # DBに反映
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        # 正常、異常にかかわらずセッションを終了する
        session.close()


# タスク削除の処理
@app.delete("/tasks/{id}")
def delete_tasks(id: int):
    session = s.session()
    try:
        query = session.query(m.Tasks)
        query = query.filter(m.Tasks.task_id == id)
        query.delete()
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# 全タスク取得の処理
@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    session = s.session()
    result = session.query(m.Tasks).all()
    return result


# 検索したタスクを取得する処理
@app.get("/tasks/{title}")
def get_tasks(title: str):
    session = s.session()
    try:
        result = session.query(m.Tasks).filter(m.Tasks.title == title).first()
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return result
    finally:
        session.close()


# 指定したタスクに子タスクを追加する処理
@app.post("/tasks/{id}")
def add_children(id: int, data: Child):
    session = s.session()
    try:
        # 子タスクを追加
        session.query(m.Tasks).filter(m.Tasks.task_id == id).update(
            {"child": data.child}
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
