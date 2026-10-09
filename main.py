import feedparser
import datetime
from typing import List, Dict

# Simulated LLM ranking function (replace with real API call)
def rank_articles(articles: List[Dict], query: str = "AI trends") -> List[Dict]:
    # Simple heuristic: prioritize items with query words in title/summary
    query_words = set(query.lower().split())
    scored = []
    for a in articles:
        text = (a.get('title', '') + ' ' + a.get('summary', '')).lower()
        score = sum(1 for w in query_words if w in text)
        scored.append((score, a))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for score, a in scored if score > 0][:5]

def fetch_rss(url: str, limit: int = 20) -> List[Dict]:
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:limit]:
        articles.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'summary': entry.get('summary', '')[:200],
            'published': entry.get('published', '')
        })
    return articles

def generate_daily_digest(feeds: List[str], topic: str) -> str:
    all_articles = []
    for url in feeds:
        all_articles.extend(fetch_rss(url))
    top = rank_articles(all_articles, topic)
    if not top:
        return "No relevant articles found today."
    lines = [f"# Daily Digest - {datetime.date.today().isoformat()}", f"**Topic**: {topic}\n"]
    for i, a in enumerate(top, 1):
        lines.append(f"{i}. [{a['title']}]({a['link']})")
        lines.append(f"   {a['summary']}\n")
    return "\n".join(lines)

if __name__ == "__main__":
    # Example: use a tech news RSS feed
    sample_feeds = [
        "https://hnrss.org/frontpage",
        "https://feeds.feedburner.com/TechCrunch"
    ]
    digest = generate_daily_digest(sample_feeds, topic="AI")
    print(digest)
    # In real implementation, save to file or send via email/webhook
}