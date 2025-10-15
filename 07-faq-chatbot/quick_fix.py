import nltk
import ssl
import os

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Set NLTK data path
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

print("Downloading NLTK data...")

# Download required data
datasets = ['punkt', 'stopwords']
for dataset in datasets:
    print(f"Downloading {dataset}...")
    try:
        nltk.download(dataset, quiet=False)
        print(f"✅ {dataset} downloaded successfully")
    except Exception as e:
        print(f"❌ Failed to download {dataset}: {e}")

print("NLTK setup completed!")