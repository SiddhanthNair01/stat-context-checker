from src.extract import text_from_url, split_sentences

article = text_from_url("https://economictimes.indiatimes.com/markets/stocks/news/why-is-market-rising-today-sensex-soars-1500-pts-nifty-above-25700-major-factors-behind-rs-4-lakh-crore-gain/articleshow/136147698.cms")
print(article["title"], article["date"])
for s in split_sentences(article["text"])[:15]:
    print("-", s)