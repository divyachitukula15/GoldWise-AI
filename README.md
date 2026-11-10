# GoldWise AI
### Agentic Gold & Silver Market Intelligence System

GoldWise AI is an AI-powered market intelligence system that tracks gold and silver prices in Kamareddy, analyzes historical price movements, and delivers automated market reports through Telegram.

It combines data engineering, financial analysis, LLM-powered insights, agentic workflows, and cloud database integration.

## Key Features

- **Multi-Metal Tracking:** Monitors 24K gold, 22K gold, and silver prices per 10 grams.
- **Market Data Extraction:** Collects historical rates from Upstox Kamareddy market pages.
- **Historical Analysis:** Calculates price differences, percentage changes, trends, averages, and volatility.
- **Cloud Database:** Stores historical rates and report snapshots in PostgreSQL.
- **AI-Powered Insights:** Uses an LLM to generate easy-to-understand Telugu-English market summaries.
- **Agentic Workflow:** Uses LangGraph to orchestrate the AI workflow and LangChain tools to retrieve market information.
- **Smart Notifications:** Sends a daily Telegram report and sends an additional report only when tracked prices change.


## Architecture

![GoldWise AI Architecture](assets/goldwise-architecture.png)


## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Data Extraction | Requests, BeautifulSoup |
| Database | PostgreSQL, Neon |
| AI / LLM | LangChain, OpenRouter |
| Agent Orchestration | LangGraph |
| Notifications | Telegram Bot API |
| Configuration | Python-dotenv |
| Testing | Pytest |
| Version Control | Git, GitHub |

## Project Structure

```text
GoldWise_AI/
│
├── goldwise/
│   ├── data/
│   │   └── upstox.py
│   ├── services/
│   │   ├── market_analysis.py
│   │   ├── change_detection.py
│   │   └── ai_insights.py
│   ├── agent/
│   │   ├── tools.py
│   │   └── workflow.py
│   ├── notifications/
│   │   └── telegram.py
│   ├── config.py
│   └── database.py
│
├── scripts/
│   ├── init_database.py
│   ├── fetch_market_data.py
│   ├── daily_report.py
│   └── change_report.py
│
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd GoldWise_AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`.

Configure:

```env
DATABASE_URL=your_neon_database_url

OPENROUTER_API_KEY=your_api_key

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Keep your `.env` file private. Never commit API keys, passwords, or tokens.

### 5. Initialize the database

```bash
python -m scripts.init_database
```

### 6. Fetch market data

```bash
python -m scripts.fetch_market_data
```

### 7. Generate the daily report

```bash
python -m scripts.daily_report
```

### 8. Check for price changes

```bash
python -m scripts.change_report
```

## Notification Strategy

| Schedule | Behaviour |
|---|---|
| 8:00 AM IST | Sends the daily market report |
| 4:00 PM IST | Sends a report only if a tracked rate changes |

The system maintains report snapshots in PostgreSQL to detect changes between reports.

## Testing

Run the test suite:

```bash
pytest
```

## Future Improvements

- Automated cloud scheduling using GitHub Actions.
- Jewellery shop retail-rate comparison.
- Advanced market trend analysis.
- Interactive market dashboard.
- Multi-agent market research and decision support.

## Important Note

Market rates are collected from Upstox and are used as informational benchmark rates. They may differ from actual jewellery shop selling prices due to taxes, making charges, and shop-specific premiums.

GoldWise AI is an informational project, not a financial advisory system.

---

**Built with Python, LangChain, LangGraph, PostgreSQL, and LLM-powered automation.**