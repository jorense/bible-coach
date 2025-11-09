"""Core coaching logic for the Bible Coach application."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from typing import List, Sequence


_STOPWORDS = {
    "the",
    "and",
    "of",
    "to",
    "a",
    "in",
    "that",
    "is",
    "for",
    "with",
    "on",
    "as",
    "be",
    "by",
    "he",
    "she",
    "they",
    "them",
    "his",
    "her",
    "their",
    "it",
    "was",
    "are",
    "you",
    "your",
    "i",
    "me",
    "my",
    "we",
    "our",
    "us",
    "will",
    "shall",
    "not",
    "but",
    "have",
    "has",
    "had",
    "so",
    "at",
    "from",
    "this",
    "these",
    "those",
    "an",
    "who",
    "whom",
    "which",
    "into",
    "out",
    "up",
    "down",
    "over",
    "under",
    "about",
    "what",
    "when",
    "where",
    "why",
    "how",
    "also",
}


@dataclass
class KeywordHighlights:
    """Structured keyword information derived from a passage."""

    primary: List[str]
    repeated: List[str]
    verses: List[str]

    def summary(self) -> str:
        if not self.primary:
            return "Key themes emerge from your passage."
        keywords = ", ".join(self.primary)
        return f"Key themes that stood out: {keywords}."


class BibleCoach:
    """Creates conversation responses that coach the user through OIA."""

    def respond(self, messages: Sequence[dict[str, str]]) -> str:
        """Generate the coach response based on the conversation history."""
        if not messages:
            return self._intro_message()

        stage = self._determine_stage(messages)
        latest_user_message = self._latest_user_message(messages)

        if stage == "intro":
            return self._invite_observation()
        if stage == "observation":
            highlights = self._extract_keywords(latest_user_message)
            return self._observation_response(latest_user_message, highlights)
        if stage == "interpretation":
            highlights = self._extract_keywords(self._gather_passages(messages))
            return self._interpretation_response(latest_user_message, highlights)
        if stage == "application":
            highlights = self._extract_keywords(self._gather_passages(messages))
            return self._application_response(latest_user_message, highlights)

        return self._follow_up_response(latest_user_message)

    def _intro_message(self) -> str:
        return (
            "Hello! I'm your Bible Coach. Let's walk through Observation, "
            "Interpretation, and Application together. Share the passage "
            "you're studying so we can begin."
        )

    def _invite_observation(self) -> str:
        return (
            "Great! To start with *Observation*, paste the Bible verse or "
            "passage you're reading. We'll look for repeated ideas, "
            "contrasts, and key details."
        )

    def _observation_response(self, passage: str, highlights: KeywordHighlights) -> str:
        repeated = (
            ", ".join(highlights.repeated)
            if highlights.repeated
            else "Pay attention to repeated words and ideas."
        )
        focus = highlights.summary()
        return (
            "Observation focus:\n"
            f"- {focus}\n"
            f"- Repeated or emphasized words: {repeated}\n\n"
            "Guided questions:\n"
            "1. What is happening in this passage?\n"
            "2. What do you learn about God or the people involved?\n"
            "3. Are there commands, promises, or warnings?\n\n"
            "When you're ready, tell me what you think the passage means so we can move into Interpretation."
        )

    def _interpretation_response(self, reflection: str, highlights: KeywordHighlights) -> str:
        key_summary = highlights.summary()
        prompts = self._reflection_prompts(reflection)
        return (
            "Interpretation insights:\n"
            f"- {key_summary}\n"
            "- Consider how the key themes fit into the broader story of Scripture.\n\n"
            "Reflection prompts:\n"
            f"1. {prompts[0]}\n"
            f"2. {prompts[1]}\n"
            f"3. {prompts[2]}\n\n"
            "Share how you sense God speaking through this meaning, and we'll craft a personal Application."
        )

    def _application_response(self, reflection: str, highlights: KeywordHighlights) -> str:
        actions = self._application_actions(highlights, reflection)
        return (
            "Application coaching:\n"
            "- Turn your interpretation into a specific next step.\n"
            "- Invite accountability by sharing your plan with someone you trust.\n\n"
            "This week you could:\n"
            f"1. {actions[0]}\n"
            f"2. {actions[1]}\n"
            f"3. {actions[2]}\n\n"
            "Let me know how it goes or ask follow-up questions—I'm here to keep coaching you."
        )

    def _follow_up_response(self, message: str) -> str:
        prompts = self._reflection_prompts(message)
        return (
            "Keep applying God's Word:\n"
            f"- {prompts[0]}\n"
            f"- {prompts[1]}\n"
            f"- {prompts[2]}\n"
            "Feel free to share progress or start a new passage anytime."
        )

    def _determine_stage(self, messages: Sequence[dict[str, str]]) -> str:
        assistant_messages = [m["content"].lower() for m in messages if m["role"] == "assistant"]
        if not any(m["role"] == "user" for m in messages):
            return "intro"
        if not any("observation focus" in text for text in assistant_messages):
            return "observation"
        if not any("interpretation insights" in text for text in assistant_messages):
            return "interpretation"
        if not any("application coaching" in text for text in assistant_messages):
            return "application"
        return "follow_up"

    def _latest_user_message(self, messages: Sequence[dict[str, str]]) -> str:
        for message in reversed(messages):
            if message.get("role") == "user":
                return message.get("content", "").strip()
        return ""

    def _gather_passages(self, messages: Sequence[dict[str, str]]) -> str:
        passages: List[str] = []
        for message in messages:
            if message.get("role") == "user":
                passages.append(message.get("content", ""))
        return "\n".join(passages)

    def _extract_keywords(self, text: str) -> KeywordHighlights:
        tokens = re.findall(r"[A-Za-z']+", text.lower())
        filtered = [token for token in tokens if token not in _STOPWORDS]
        counter = Counter(filtered)
        primary = [word.capitalize() for word, _ in counter.most_common(3)]
        repeated = [word for word, count in counter.items() if count > 1]

        verses = self._extract_references(text)
        return KeywordHighlights(primary=primary, repeated=repeated, verses=verses)

    def _extract_references(self, text: str) -> List[str]:
        pattern = re.compile(r"([1-3]?\s?[A-Za-z]+\s\d+:\d+(?:-\d+)?)")
        return [match.strip() for match in pattern.findall(text)]

    def _reflection_prompts(self, message: str) -> List[str]:
        keywords = self._extract_keywords(message).primary
        base = [
            "What does this reveal about God's character?",
            "How does this passage point to Jesus or the gospel?",
            "Where might there be tension between this truth and your current habits?",
        ]
        if not keywords:
            return base
        prompts = [
            f"What do you learn about {keywords[0]} here?",
            f"How does this shape your view of {keywords[1] if len(keywords) > 1 else keywords[0]}?",
            f"How could focusing on {keywords[-1]} transform your relationships?",
        ]
        return prompts

    def _application_actions(self, highlights: KeywordHighlights, reflection: str) -> List[str]:
        base_actions = [
            "Write a prayer asking God to help you live this out.",
            "Share your insight with a friend or small group.",
            "Set a reminder to revisit this passage later this week.",
        ]
        if not highlights.primary:
            return base_actions

        focus = highlights.primary[0]
        custom_actions = [
            f"Identify one habit that reflects {focus.lower()} and practice it today.",
            f"Encourage someone who needs to hear about {focus.lower()}.",
            f"Note a situation this week where you can display {focus.lower()} intentionally.",
        ]
        if "pray" in reflection.lower():
            custom_actions[0] = "Turn your reflection into a written prayer and revisit it tomorrow."
        return custom_actions


__all__ = ["BibleCoach", "KeywordHighlights"]
