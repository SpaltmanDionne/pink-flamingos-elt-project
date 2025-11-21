import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()


class ExtractLoad():
    def __init__(self, read_from_cache=False):
        self.base_url = os.getenv("GOOGLE_BOOKS_BASE_URL")
        self.cache_file = "books_test.json"
        self.load_date = datetime.now().strftime("%Y-%m-%d")
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.read_from_cache = read_from_cache
        
        self.query_params = {
            "q": "subject:romance",
            "orderBy": "relevance",
            "maxResults": 10,
            "key": os.getenv("API_KEY")
        }

        keyfile_path = "/Users/arthurjunfujimoto/Documents/xccelerated/bootcamp/pink-flamingos-elt-project/ae-de-project-2025-9b9ea7fe449d.json"
        gcp_credentials = service_account.Credentials.from_service_account_file(keyfile_path)
        self.gc_client = storage.Client(credentials=gcp_credentials)

    def extract(self) -> list:
        start_index = 0
        books = []

        while start_index < 10:
            print(f"Initializing extracting for index starting at: {start_index}")
            self.query_params["startIndex"] = start_index
            res = requests.get(self.base_url, params=self.query_params)

            if res.status_code != 200:
                raise Exception
            
            json_res = res.json()
            items = json_res.get("items", [])
            if not items:
                break

            books.extend(items)
            start_index += len(items)
        
        print(f"Extract finalized. Total {len(books)} books were collected.")
        return books

    def load(self, books: list):
        file_name = f"load_date={self.load_date}/daily_parition_books.json"

        print("Loading json file to Google Cloud Storage.")
        bucket = self.gc_client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(books, default=str))
        print("Data loaded.")

    def el(self):
        if self.read_from_cache:
            print("Reading from cache.")
            data = self.read_cache()
        else:
            data = self.extract()

        self.load(books=data)
        self.save_cache(books=data)

    def save_cache(self, books: list):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(books, f, indent=2, ensure_ascii=False)

    def read_cache(self) -> list:
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":
    el = ExtractLoad(read_from_cache=True)
    el.el()