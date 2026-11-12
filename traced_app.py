"""
traced_app.py
--------------
A single-file LangChain + OpenAI application with optional .env support.

LangSmith tracing is controlled ONLY by environment variables.
There is deliberately no LangSmith tracing code, callback, or decorator here.

Setup:
    1. Create a file named .env in the same folder as this script.
    2. Add OPENAI_API_KEY, LANGSMITH_API_KEY, LANGSMITH_TRACING,
       LANGSMITH_PROJECT, and optionally LANGSMITH_ENDPOINT.
    3. Install dependencies:
           python -m pip install langchain langchain-openai langsmith python-dotenv
    4. Run:
           python traced_app.py

Never commit your .env file or share its contents.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    # Load variables from the .env file in the same directory as this script.
    # override=False means already-defined OS/shell environment variables win.
    env_file = Path(__file__).resolve().parent / ".env" # Scripts\traced_app.py
    load_dotenv(dotenv_path=env_file, override=False)

    # Check required settings without printing or exposing secret values.
    required_keys = ("OPENAI_API_KEY", "LANGSMITH_API_KEY")
    missing = [key for key in required_keys if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + f". Add them to {env_file} or set them in your terminal."
        )

    tracing_enabled = os.getenv("LANGSMITH_TRACING", "").strip().lower()
    if tracing_enabled not in ("true", "1", "yes", "on"):
        raise RuntimeError(
            "LangSmith tracing is not enabled. Set LANGSMITH_TRACING=true "
            "in .env or in your terminal environment, then run again."
        )

    project_name = os.getenv("LANGSMITH_PROJECT")
    if not project_name:
        raise RuntimeError(
            "LANGSMITH_PROJECT is missing. Set a project name in .env "
            "so runs do not go into the default project."
        )

    print("Configuration check passed.")
    print("OpenAI API key: configured")
    print("LangSmith API key: configured")
    print(f"LangSmith tracing: {tracing_enabled}")
    print(f"LangSmith project: {project_name}")
    print("Secrets are not displayed.")

    # ChatOpenAI reads OPENAI_API_KEY from the process environment.
    # LangSmith tracing is activated automatically from environment variables.
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    prompts = [
        (
            "PROMPT 1 — Short factual explanation",
            "In no more than 80 words, explain what LangChain is "
            "and give one practical use case.",
        ),
        (
            "PROMPT 2 — Technical comparison",
            "Compare LangChain and LangSmith for a Python application. "
            "Explain their different purposes and describe how they work "
            "together. Present the answer in five concise bullet points.",
        ),
        (
            "PROMPT 3 — Detailed architecture",
            "You are a senior AI solutions architect. Design a practical "
            "Retrieval-Augmented Generation (RAG) application for an "
            "enterprise team using Python and LangChain. Explain the "
            "architecture in these sections: (1) document ingestion, "
            "(2) text splitting and metadata, (3) embedding generation, "
            "(4) vector database and retrieval, (5) prompt construction "
            "and answer generation, and (6) evaluation, observability, "
            "security, and deployment. For each section, describe its "
            "purpose and give one implementation recommendation. Finish "
            "with a numbered end-to-end data flow. Be specific but avoid "
            "inventing vendor capabilities.",
        ),
    ]

    # Each invoke() is a LangChain model run. With tracing enabled through
    # environment variables, LangSmith records each run automatically.
    for label, prompt in prompts:
        print("\n" + "=" * 80)
        print(label)
        print("=" * 80)
        print(f"\nPrompt:\n{prompt}\n")

        response = llm.invoke(prompt)

        print("Answer:")
        print(response.content)
        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()
