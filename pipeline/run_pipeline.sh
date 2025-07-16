# run_pipeline.sh
#!/bin/bash

echo "Step 1: Scraping Telegram data..."
python pipeline/scrape_telegram_data.py

echo "Step 2: Load raw data to Postgres..."
python pipeline/load_to_postgres.py

echo "Step 3: Run dbt transformations..."
cd telegram_project
dbt run
cd ..

echo "Step 4: YOLO enrichment..."
python pipeline/run_yolo_enrichment.py
