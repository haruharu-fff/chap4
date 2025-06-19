# chatGPTによる出力(デバッグ用)
from db_setting import ENGINE
from db_model import Base


def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=ENGINE)
    print("Creating all tables...")
    Base.metadata.create_all(bind=ENGINE)
    print("Database reset complete.")


if __name__ == "__main__":
    reset_database()
