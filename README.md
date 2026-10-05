# style-analyzer-lite

文风分析小工具。统计平均句长、句长方差、词汇丰富度（type-token ratio）、标点习惯，输出文风画像。零第三方依赖。

## 指标

- 句子数、平均句长、句长标准差/方差；
- 词元总数、去重词数、**TTR（type-token ratio）**；
- 每句逗号/问号/感叹号频率；
- 一句话文风画像（节奏 + 用词）。

## 快速开始

```bash
python3 cli.py "今天天气很好。我们出门散步吧！你觉得怎么样？"
```

## 使用示例

```bash
# 分析文件
python3 cli.py -f essay.txt

# JSON 指标
python3 cli.py "……" --json
```

## 无 API Key 如何运行

本工具**完全不需要 API Key**，全部为本地统计。

## 目录结构

```
style-analyzer-lite/
├── analyzer.py   # 分句、句长、TTR、标点、画像
├── cli.py        # 命令行入口
├── tests/
│   └── test_analyzer.py
├── README.md
├── LICENSE
└── .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
