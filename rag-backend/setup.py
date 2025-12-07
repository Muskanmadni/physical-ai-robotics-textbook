from setuptools import setup, find_packages

setup(
    name="rag-backend",
    version="0.1.0",
    description="RAG Backend for AI Textbook Application",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "qdrant-client>=1.7.1",
        "pydantic>=2.5.0,<3.0.0",
        "python-dotenv==1.0.0",
        "pytest>=7.4.3",
        "httpx>=0.25.2",
        "cohere>=4.36",
        "google-generativeai>=0.8.4",
        "mangum>=0.17.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.0.0",
            "flake8>=6.0.0"
        ]
    },
    python_requires=">=3.8",
)