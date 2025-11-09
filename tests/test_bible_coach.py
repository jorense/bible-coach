import re

import pytest

from app.bible_coach import BibleCoach


@pytest.fixture()
def coach():
    return BibleCoach()


def test_intro_message(coach):
    response = coach.respond([])
    assert "Hello! I'm your Bible Coach" in response


def test_observation_stage(coach):
    messages = [{"role": "user", "content": "John 3:16 For God so loved the world."}]
    response = coach.respond(messages)
    assert "Observation focus" in response
    assert "John" in response or "God" in response


def test_interpretation_stage(coach):
    messages = [
        {"role": "user", "content": "John 3:16 For God so loved the world."},
        {"role": "assistant", "content": "Observation focus:\n- Key themes that stood out: God, Loved, World."},
        {"role": "user", "content": "It means God loves us and sent Jesus."},
    ]
    response = coach.respond(messages)
    assert "Interpretation insights" in response
    assert re.search(r"How does this shape your view of", response)


def test_application_stage(coach):
    messages = [
        {"role": "user", "content": "John 3:16 For God so loved the world."},
        {"role": "assistant", "content": "Observation focus:\n- Key themes that stood out: God, Loved, World."},
        {"role": "user", "content": "It means God loves us and sent Jesus."},
        {"role": "assistant", "content": "Interpretation insights:\n- Key themes that stood out: God, Loved, World."},
        {"role": "user", "content": "I will share God's love."},
    ]
    response = coach.respond(messages)
    assert "Application coaching" in response
    assert "This week you could" in response


def test_follow_up_stage(coach):
    messages = [
        {"role": "user", "content": "John 3:16 For God so loved the world."},
        {"role": "assistant", "content": "Observation focus:\n- Key themes that stood out: God, Loved, World."},
        {"role": "user", "content": "It means God loves us and sent Jesus."},
        {"role": "assistant", "content": "Interpretation insights:\n- Key themes that stood out: God, Loved, World."},
        {"role": "user", "content": "I will share God's love."},
        {"role": "assistant", "content": "Application coaching:\n- Turn your interpretation into a specific next step."},
        {"role": "user", "content": "I told my friend today."},
    ]
    response = coach.respond(messages)
    assert "Keep applying God's Word" in response
