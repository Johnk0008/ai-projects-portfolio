import nltk
import ssl
import os
import urllib.request

def fix_ssl_and_download_nltk():
    print("Fixing SSL certificate issues and downloading NLTK data...")
    
    # Bypass SSL verification (temporary solution for development)
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # Set NLTK data path to current directory
    nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
    os.makedirs(nltk_data_path, exist_ok=True)
    nltk.data.path.append(nltk_data_path)
    
    # Download required NLTK datasets
    required_datasets = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    
    for dataset in required_datasets:
        print(f"Downloading {dataset}...")
        try:
            nltk.download(dataset, download_dir=nltk_data_path)
            print(f"✅ Successfully downloaded {dataset}")
        except Exception as e:
            print(f"❌ Error downloading {dataset}: {e}")
            
            # Alternative download method
            try:
                print(f"Trying alternative method for {dataset}...")
                nltk.download(dataset, download_dir=nltk_data_path, quiet=False)
            except Exception as e2:
                print(f"Alternative method also failed for {dataset}: {e2}")

if __name__ == "__main__":
    fix_ssl_and_download_nltk()
    print("\nNLTK data download completed!")