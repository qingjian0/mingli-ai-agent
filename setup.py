
from setuptools import setup, find_packages

setup(
    name="mingli-ai-agent",
    version="0.1.0",
    description="MingLi AI Agent - 企业级术数推理命理智能体",
    author="qingjian0",
    author_email="qingjian0@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "redis>=5.0.0",
        "langchain>=0.2.0",
        "openai>=1.0.0",
        "lunardate>=0.2.0",
        "pytest>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest-asyncio>=0.23.0",
            "httpx>=0.27.0",
            "mkdocs>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "mingli=src.cli.main:cli",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
