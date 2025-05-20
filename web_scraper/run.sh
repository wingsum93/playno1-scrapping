echo "Activating virtual environment..."
source .venv/bin/activate

echo "Running scraper..."
python scraper/main.py

echo "Done."