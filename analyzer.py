"""style-analyzer-lite — 文风分析。

统计平均句长、句长方差、词汇丰富度（type-token ratio）、标点习惯等，输出画像。
零第三方依赖。
"""
from __future__ import annotations

import math
import re
from collections import Counter

_EN_RE = re.compile(r"[a-zA-Z]+")


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？.!?])", text)
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> list[str]:
    toks = _EN_RE.findall(text.lower())
    toks += re.findall(r"[\u4e00-\u9fff]", text)
    return toks


def analyze_style(text: str) -> dict:
    sents = _split_sentences(text)
    lengths = [len(re.sub(r"[\s。！？.!?]", "", s)) for s in sents]
    n_sent = len(lengths)
    avg_len = sum(lengths) / n_sent if n_sent else 0.0
    var = (sum((l - avg_len) ** 2 for l in lengths) / n_sent) if n_sent else 0.0

    tokens = _tokenize(text)
    total_tok = len(tokens)
    unique_tok = len(set(tokens))
    ttr = unique_tok / total_tok if total_tok else 0.0

    punct = Counter(ch for ch in text if ch in "，。！？、；：,.!?;:\"'\"'（）()")
    per_sent = n_sent if n_sent else 1

    comma = (punct.get("，", 0) + punct.get(",", 0)) / per_sent
    question = (punct.get("？", 0) + punct.get("?", 0)) / per_sent
    exclaim = (punct.get("！", 0) + punct.get("!", 0)) / per_sent

    return {
        "sentence_count": n_sent,
        "avg_sentence_len": round(avg_len, 2),
        "sentence_len_variance": round(var, 2),
        "sentence_len_std": round(math.sqrt(var), 2),
        "total_tokens": total_tok,
        "unique_tokens": unique_tok,
        "type_token_ratio": round(ttr, 3),
        "punct_per_sentence": {
            "comma": round(comma, 2),
            "question": round(question, 2),
            "exclaim": round(exclaim, 2),
        },
        "punct_counts": dict(punct),
    }


def style_persona(profile: dict) -> str:
    avg = profile["avg_sentence_len"]
    ttr = profile["type_token_ratio"]
    if avg > 40:
        rhythm = "句子偏长，行文绵密"
    elif avg < 15:
        rhythm = "句子短促，节奏明快"
    else:
        rhythm = "句长适中，张弛有度"
    if ttr > 0.6:
        vocab = "用词丰富多变"
    elif ttr < 0.3:
        vocab = "用词重复度较高"
    else:
        vocab = "用词稳定常规"
    return f"{rhythm}；{vocab}（TTR={ttr}）。"


def report(text: str) -> str:
    p = analyze_style(text)
    lines = [
        "=== 文风画像 ===",
        f"句子数：{p['sentence_count']}",
        f"平均句长：{p['avg_sentence_len']} 字符　句长标准差：{p['sentence_len_std']}",
        f"词元总数：{p['total_tokens']}　去重词：{p['unique_tokens']}　TTR：{p['type_token_ratio']}",
        f"每句标点：逗号 {p['punct_per_sentence']['comma']}，"
        f"问号 {p['punct_per_sentence']['question']}，"
        f"感叹号 {p['punct_per_sentence']['exclaim']}",
        f"画像：{style_persona(p)}",
    ]
    return "\n".join(lines)
