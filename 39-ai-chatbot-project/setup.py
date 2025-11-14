from setuptools import setup, find_packages

setup(
    name="ai-chatbot",
    version="1.0.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=1.23.5',
        'scikit-learn>=1.2.2',
        'nltk>=3.8.1',
        'flask>=2.3.3',
        'flask-socketio>=5.3.6',
        'eventlet>=0.33.3',
        'python-dotenv>=1.0.0',
        'pandas>=1.5.3',
        'joblib>=1.3.2'
    ],
    python_requires='>=3.9',
)