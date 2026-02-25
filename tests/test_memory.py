import tempfile
import unittest
from pathlib import Path

from cody.memory import MemoryStore


class MemoryTests(unittest.TestCase):
    def test_short_term_memory_by_conversation_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MemoryStore(long_term_path=Path(tmp) / "long.json")
            store.append_short_term("c1", "user", "hello")
            store.append_short_term("c1", "assistant", "hi")
            store.append_short_term("c2", "user", "other")

            self.assertEqual(len(store.get_short_term("c1")), 2)
            self.assertEqual(len(store.get_short_term("c2")), 1)

    def test_long_term_summary_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "memory.json"
            store = MemoryStore(long_term_path=path)
            summary = {"topic": "phase1", "summary": "stored"}

            store.save_long_term_summary(summary)
            self.assertEqual(store.load_long_term_summary(), summary)

    def test_long_term_summary_requires_topic_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = MemoryStore(long_term_path=Path(tmp) / "memory.json")

            with self.assertRaises(ValueError):
                store.save_long_term_summary({"topic": "", "summary": "stored"})


if __name__ == "__main__":
    unittest.main()
