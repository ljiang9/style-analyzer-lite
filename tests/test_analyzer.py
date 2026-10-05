"""style-analyzer-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyzer import analyze_style, style_persona, report  # noqa: E402


class TestMetrics(unittest.TestCase):
    def test_sentence_count(self):
        p = analyze_style("你好。世界！今天？")
        self.assertEqual(p["sentence_count"], 3)

    def test_avg_len(self):
        p = analyze_style("aaaa。bbbb。")
        self.assertEqual(p["avg_sentence_len"], 4.0)

    def test_ttr(self):
        p = analyze_style("the the the the cat")
        self.assertLess(p["type_token_ratio"], 0.6)

    def test_variance_zero_uniform(self):
        p = analyze_style("aaaaa。bbbbb。ccccc。")
        self.assertEqual(p["sentence_len_variance"], 0.0)

    def test_punct(self):
        p = analyze_style("你好，世界。好吗？")
        self.assertEqual(p["punct_counts"].get("？"), 1)


class TestPersona(unittest.TestCase):
    def test_persona_text(self):
        p = analyze_style("短。短。短。")
        self.assertIn("节奏明快", style_persona(p))

    def test_report(self):
        r = report("今天天气很好。我们出门吧！")
        self.assertIn("文风画像", r)


if __name__ == "__main__":
    unittest.main()
