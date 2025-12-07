import os
import sys
import unittest
from unittest.mock import MagicMock, patch

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from llm import LLM


class TestLLMIntegration(unittest.TestCase):
    @patch("llm.OpenAI")
    def test_answer_calls_client_with_expected_prompt(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "```output```"
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion

        model = LLM(api_key="test-key", api_model="test-model", max_retries=1)
        response = model.answer("ls", log_history=["whoami", "root"])

        self.assertEqual(response, "output")

        mock_openai.assert_called_once()
        mock_client.chat.completions.create.assert_called_once()
        _, kwargs = mock_client.chat.completions.create.call_args
        self.assertEqual(kwargs["model"], "test-model")

        messages = kwargs["messages"]
        self.assertGreaterEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "whoami")
        self.assertIn("### Task", messages[-1]["content"])
        self.assertIn("ls", messages[-1]["content"])


if __name__ == "__main__":
    unittest.main()
