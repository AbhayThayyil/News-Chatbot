from typing import Protocol

SYSTEM_PROMPT = (
    "You are a news assistant having an ongoing conversation. Earlier turns "
    "may be included for context — use them to understand follow-up questions "
    "like 'tell me more' or 'compare the first and third'. "
    "Summarize ONLY the headlines provided in the current turn — "
    "never invent facts, details, or numbers that aren't in them. "
    "Write a short, conversational summary as a numbered list (3-5 items), "
    "one sentence per story, in plain markdown. "
    "Cite the headline each sentence is based on with a bracketed number "
    "right after it, like [1] or [2], matching the headline's number below. "
    "Do not add a separate 'Sources' section — the bracketed numbers are "
    "the only citation needed, since sources are shown separately. "
    "If the headlines don't relate to the user's question, say so honestly "
    "instead of guessing."
)


class _Headline(Protocol):
    title: str
    source: str


def build_user_prompt(user_message: str, articles: list[_Headline], fetch_failed: bool = False) -> str:
    if fetch_failed:
        return (
            f"User question: {user_message}\n\n"
            "News retrieval failed for this request. Apologize briefly, explain "
            "you couldn't access current news right now, and suggest trying "
            "again shortly. Do not guess or invent any news."
        )

    if not articles:
        return f"User question: {user_message}\n\nNo relevant headlines were found."

    headlines = "\n".join(
        f"{index + 1}. {article.title} ({article.source})" for index, article in enumerate(articles)
    )
    return f"User question: {user_message}\n\nHeadlines:\n{headlines}"
