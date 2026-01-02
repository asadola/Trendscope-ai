from app.crawlers.runner import run_all_crawlers

events = run_all_crawlers()
print(f"Total events collected: {len(events)}")
print(events[:3])
