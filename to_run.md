
1. `docker-compose up --build -d` from root.
2. from `frontend/` run `npm install` and `npm run dev`. access at `localhost:5173`.

3. Initial Setup:
- Go to the Feeds tab in the UI.
- Add a test feed (e.g., http://feeds.bbci.co.uk/news/rss.xml).
- The background worker will immediately fetch, parse, and analyze the news.
- Go to the Dashboard to see the incoming stream and sentiment analysis.