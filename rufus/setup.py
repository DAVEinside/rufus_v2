# setup.py

from setuptools import setup, find_packages

setup(
    name='Rufus',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.8.5',
        'beautifulsoup4==4.12.2',
        'langchain==0.0.250',
        'openai==0.27.10',
        'python-dotenv==1.0.0',
    ],
    description='Rufus: Intelligent Web Crawler for RAG Pipelines',
    author='nimit dave',
    author_email='nimitdave3001@gmail.com.com',
    url='https://github.com/DAVEinside/rufus_v2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
