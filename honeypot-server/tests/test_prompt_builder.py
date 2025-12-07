import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from llm import DEFAULT_FEW_SHOT_EXAMPLES, build_few_shot_prompt, select_examples


class TestPromptBuilder(unittest.TestCase):
    def test_select_examples_limits_length(self):
        examples = [
            {"command": "cmd1", "response": "out1"},
            {"command": "cmd2", "response": "out2"},
            {"command": "cmd3", "response": "out3"},
        ]
        selected = select_examples(examples, 2)
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected[0]["command"], "cmd1")
        self.assertEqual(selected[1]["command"], "cmd2")

    def test_build_few_shot_prompt_format(self):
        examples = [
            {"command": "ls", "response": "file1 file2"},
            {"command": "pwd", "response": "/home"},
        ]
        user_input = "whoami"
        prompt = build_few_shot_prompt("system", examples, user_input)

        self.assertIn("system", prompt)
        self.assertIn("### Example 1", prompt)
        self.assertIn("Input:\nls", prompt)
        self.assertIn("Output:\nfile1 file2", prompt)
        self.assertIn("### Example 2", prompt)
        self.assertFalse(prompt.strip().endswith("Output:"))
        self.assertIn("### Task", prompt)
        self.assertIn("Input:\nwhoami", prompt)

    def test_default_examples_non_empty(self):
        self.assertGreater(len(DEFAULT_FEW_SHOT_EXAMPLES), 0)


if __name__ == "__main__":
    unittest.main()
