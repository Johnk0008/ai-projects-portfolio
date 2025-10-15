try:
    import flask
    import nltk
    import spacy
    import sklearn
    print("✅ All imports successful!")
    print(f"Flask version: {flask.__version__}")
    print(f"spaCy version: {spacy.__version__}")
    print("Setup completed successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")