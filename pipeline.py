from db.models import init_db
from etl.extract import extract
from etl.transform import transform
from etl.load import load

def run_pipeline():
    print("=== Pipeline started ===")
    raw_data   = extract()
    clean_data = transform(raw_data)
    load(clean_data)
    print("=== Pipeline complete ===\n")

if __name__ == "__main__":
    init_db()
    run_pipeline()