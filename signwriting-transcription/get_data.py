import hashlib
import os
import csv

import psycopg2
from dotenv import load_dotenv
from signwriting.formats.fsw_to_swu import fsw2swu
from signwriting.formats.swu_to_fsw import swu2fsw
from signwriting.tokenizer import normalize_signwriting
from tqdm import tqdm

load_dotenv()

def stable_hash(s):
    # Using python's hash function changes values between sessions
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

def get_split(pose: str):
    if pose == "19097be0e2094c4aa6b2fdc208c8231e.pose":
        return "test"

    rand = stable_hash(pose[:-len('.pose')]) % 100
    if rand > 98:
        return "test"

    if rand > 96:
        return "dev"

    return "train"


if __name__ == "__main__":
    print("Connecting to database")
    database = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST']
    )

    QUERY = """
    SELECT CONCAT("videoId", '.pose') as pose, "videoLanguage", start, "end", "text" 
    FROM captions 
    WHERE language = 'Sgnw'
    ORDER BY "videoId", start
    """

    cursor = database.cursor()
    with open('data.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([c.name for c in cursor.description] + ["split"])

        print("Executing query")
        cursor.execute(QUERY)
        num_rows = cursor.rowcount
        for row in tqdm(cursor):
            # Normalize the SWU
            swu = row[-1]
            fsw = swu2fsw(swu)
            normalized_fsw = normalize_signwriting(fsw)
            fixed_swu = fsw2swu(normalized_fsw)

            new_row = list(row[:-1]) + [fixed_swu, get_split(row[0])]
            writer.writerow(new_row)