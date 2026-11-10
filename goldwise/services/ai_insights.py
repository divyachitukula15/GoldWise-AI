import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from goldwise.services.market_analysis import compare_latest_rates

load_dotenv()

def generate_market_insights() -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY in .env")

    market_data = compare_latest_rates()
    if not market_data:
        return "Market data is not available yet."

    llm = ChatOpenAI(
        model="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.3,
    )
    prompt = f"""
    Analyze only this Kamareddy market data: {market_data}
    Write a short Telugu-English report using English letters only.
    Explain increases/decreases and observations. Do not predict prices.
    All rates are per 10 grams. Do not invent missing data.
    """
    return llm.invoke(prompt).content
