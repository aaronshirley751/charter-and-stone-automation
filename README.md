# Clone the repo
# Create virtual env
python -m venv venv
# Activate venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the publisher
python src/auto_publisher.py
