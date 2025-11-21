import os
import json
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import storage
from contextlib import contextmanager
from google.oauth2 import service_account

load_dotenv()


@contextmanager
def create_database_connection(conn_str: str):
    conn = psycopg2.connect(
        conn_str
    )
    yield conn
    conn.close()


@contextmanager
def create_cursor(conn):
    cur = conn.cursor()
    yield cur
    cur.close()


class LoadToPostgres():
    def __init__(self, read_from_cache=False):
        self.cache_file = "books_test.json"
        self.load_date = datetime.now().strftime("%Y-%m-%d")
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.read_from_cache = read_from_cache
        self.file_name = f"load_date={self.load_date}/daily_parition_books.json"
        self.conn_str = f"""
            host={os.getenv("HOST")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")} port={os.getenv("PORT")} dbname={os.getenv("DB_NAME")}
        """

        keyfile_path = "/Users/arthurjunfujimoto/Documents/xccelerated/bootcamp/pink-flamingos-elt-project/ae-de-project-2025-9b9ea7fe449d.json"
        gcp_credentials = service_account.Credentials.from_service_account_file(keyfile_path)
        self.gc_client = storage.Client(credentials=gcp_credentials)

    def read_file(self):
        if self.read_from_cache:
            return self.read_cache()
        
        bucket = self.gc_client.bucket(self.bucket_name)
        blob = bucket.blob(self.file_name)
        return blob.download_as_bytes().decode()

    def read_cache(self) -> list:
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_data(self, file: list) -> list:
        clean_books = []

        for book in file:
            volume_id = book["id"]
            volume_info = book["volumeInfo"]
            sales_info = book["saleInfo"]

            clean_books.append(dict(
                volume_id = volume_id,
                title = volume_info["title"],
                main_author = volume_info["authors"][0],
                publisher = volume_info.get("publisher", None),
                published_date = volume_info["publishedDate"],
                description = volume_info["description"],
                page_count = volume_info["pageCount"],
                print_type = volume_info["printType"],
                main_category = volume_info["categories"][0],
                language = volume_info["language"],
                thumbnail = volume_info["imageLinks"]["thumbnail"],
                sales_country = sales_info["country"],
                saleability = sales_info["saleability"],
                is_ebook = sales_info["isEbook"]
            ))

        return clean_books

    def load(self, data: list):
        create_table = """
            CREATE TABLE IF NOT EXISTS books (
                volume_id VARCHAR PRIMARY KEY,
                title VARCHAR(500),
                main_author VARCHAR(100),
                publisher VARCHAR(100),
                published_date VARCHAR(40),
                description TEXT,
                page_count INT,
                print_type VARCHAR(30),
                main_category VARCHAR(30),
                language VARCHAR(4),
                thumbnail VARCHAR(1000),
                sales_country VARCHAR(4),
                saleability VARCHAR(15),
                is_ebook BOOLEAN,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NULL
            );
        """
        self.execute_query(query=create_table)

        upsert_query = """
            INSERT INTO books (
                    volume_id, title, main_author, publisher, published_date, description, page_count,
                    print_type, main_category, language, thumbnail, sales_country, saleability, is_ebook, 
                    created_at, updated_at
            )
            VALUES (
                %(volume_id)s, %(title)s, %(main_author)s, %(publisher)s, %(published_date)s, %(description)s, %(page_count)s,
                %(print_type)s, %(main_category)s, %(language)s, %(thumbnail)s, %(sales_country)s,
                %(saleability)s, %(is_ebook)s, now(), now()
            )
            ON CONFLICT (volume_id) DO UPDATE SET
            title = EXCLUDED.title,
            main_author = EXCLUDED.main_author,
            publisher = EXCLUDED.publisher,
            published_date = EXCLUDED.published_date,
            description = EXCLUDED.description,
            page_count = EXCLUDED.page_count,
            print_type = EXCLUDED.print_type,
            main_category = EXCLUDED.main_category,
            language = EXCLUDED.language,
            thumbnail = EXCLUDED.thumbnail,
            sales_country = EXCLUDED.sales_country,
            saleability = EXCLUDED.saleability,
            is_ebook = EXCLUDED.is_ebook,
            created_at = EXCLUDED.created_at,
            updated_at = now()
        """
        self.execute_query(query=upsert_query, params=data)

    def execute_query(self, query: str, params: list = [None]):
        with create_database_connection(self.conn_str) as conn, create_cursor(conn) as cur:
            for row in params:
                cur.execute(query, row)
            conn.commit()

    def execute(self):
        file = self.read_file()
        data = self.parse_data(file=file)
        self.load(data=data)


if __name__ == "__main__":
    lp = LoadToPostgres(read_from_cache=True)
    lp.load()
