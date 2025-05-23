from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jsonsorter",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligent JSON file organizer based on content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jsonsorter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: File Formats :: JSON",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "jsonsorter=jsonsorter:main",
        ],
    },
)