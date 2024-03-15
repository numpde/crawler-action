from pathlib import Path
from markdown_crawler import md_crawl

url = "https://counter-resistance.org"
md_crawl(url, max_depth=2, num_threads=5, base_dir=str(Path(__file__).with_suffix('')))
