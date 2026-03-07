"""Simple tests for OpenAI API calls via MyBotWrapper."""
import os

import pytest

from vocqgen.chat import MyBotWrapper
from vocqgen.parser import ParserBase


def _has_api_key():
    return bool(os.environ.get("OPENAI_API_KEY"))


class _EchoParser(ParserBase):
    """Minimal parser for tests: prompt asks for a short reply, returns raw text."""
    task_name = "echo"
    response_format = "text"

    def compose_prompt(self, inputs):
        self.inputs = inputs
        return inputs.get("prompt", "Reply with exactly: OK")


@pytest.mark.skipif(not _has_api_key(), reason="OPENAI_API_KEY not set")
def test_mybotwrapper_returns_content():
    """Use MyBotWrapper to call the API and assert a non-empty text response."""
    parser = _EchoParser()
    bot = MyBotWrapper(parser=parser, model="gpt-5-mini", temperature=0)
    result = bot.run(inputs={"prompt": "Reply with exactly: OK"})
    assert result["success"]
    assert "result" in result
    assert result["result"] is not None
    assert isinstance(result["result"], str)
    assert len(result["result"].strip()) > 0


@pytest.mark.skipif(not _has_api_key(), reason="OPENAI_API_KEY not set")
def test_mybotwrapper_parse_response():
    """Use MyBotWrapper with a prompt that expects a numeric answer."""
    parser = _EchoParser()
    bot = MyBotWrapper(parser=parser, model="gpt-4o-mini", temperature=0)
    result = bot.run(
        inputs={"prompt": "What is 1+1? Reply with one digit only."}
    )
    assert result["success"]
    assert "2" in result["result"]
