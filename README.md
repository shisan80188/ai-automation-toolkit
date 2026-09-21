# ai-automation-toolkit

Production-ready Python tools for AI workflow automation: LLM/API integration,
web scraping, and task automation with clean, tested code.

## Features

- **`llm_client.py`** — Thin wrapper around OpenAI-compatible chat APIs with
  retries, timeouts, and a minimal dependency footprint.
- **`web_scraper.py`** — Dependency-light scraper with polite defaults,
  realistic headers, and configurable delays.

## Requirements

- Python 3.9+
- `requests`, `beautifulsoup4`

```bash
pip install requests beautifulsoup4
```

## Usage

```python
from llm_client import LLMClient

client = LLMClient(model="gpt-4o-mini")
print(client.chat([{"role": "user", "content": "Hello!"}]))
```

## License

MIT
