import os
import logging

import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent
from .tools import analyze_csv

# ── Setup ────────────────────────────────────────────────────────────────────

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.0-flash")

# ── Root Agent ───────────────────────────────────────────────────────────────

root_agent = Agent(
    name="data_analyst",
    model=model_name,
    description="A production-ready CSV analyst agent powered by Gemini on Google Cloud.",
    instruction="""
    You are the CSV Analyst Agent — an AI data analyst that produces
    structured Markdown reports from raw CSV data.

    When the user provides CSV text:
    1. Call the 'analyze_csv' tool with the full CSV text exactly as provided.
    2. Take the 'report' value from the tool's response.
    3. Return that report to the user exactly as-is — do not modify,
       shorten, reformat, or summarise it in any way.

    If the user sends a message without CSV data, politely ask them
    to paste their CSV text into the chat to begin analysis.
    """,
    tools=[analyze_csv],
)
