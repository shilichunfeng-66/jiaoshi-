#!/usr/bin/env python
"""定位 Markdown/纯文本中的表达信号；不判定AI来源、论证质量或投稿资格。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

SIGNALS = [
    ('generic_opening', re.compile(r'随着[^。！？\n]{0,30}(?:发展|推进)'), '检查是否用具体问题或已核事实替代泛背景。'),
    ('empty_value', re.compile(r'具有重要(?:的理论|的实践|理论|实践)?意义|具有重要的理论意义和实践价值|提供(?:了)?有力支撑|奠定(?:了)?坚实基础|意义重大|影响深远'), '核对价值判断的具体对象、用途及依据。'),
    ('priority_claim', re.compile(r'填补[^。！？；\n]{0,40}空白|国际领先|国内首创|首次揭示'), '核对优先性或领先判断的检索与比较依据。'),
    ('generic_gap', re.compile(r'缺乏系统研究|缺少系统研究|研究不足|有待深入'), '核对研究缺口是否指明材料、争议或解释限制。'),
    ('generic_transition', re.compile(r'综上所述|由此可见|值得注意的是'), '检查连接关系是否真实，合理用法可保留。'),
]


def prose_lines(text):
    """保留原始行号；跳过Markdown标题、引用说明及围栏代码。"""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        mark = re.match(r'^(`{3,}|~{3,})', stripped)
        if mark:
            marker = mark.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None or re.match(r'^(?:#{1,6}\s|>)', stripped):
            continue
        yield number, line


def analyze(text):
    lines = list(prose_lines(text))
    signals = []
    for number, line in lines:
        for code, pattern, advice in SIGNALS:
            for match in pattern.finditer(line):
                signals.append({'kind': code, 'line': number, 'column': match.start() + 1,
                                'match': match.group(), 'context': line.strip(), 'review': advice})
        connectors = list(re.finditer(r'首先|其次|再次|最后', line))
        if len(connectors) >= 3:
            signals.append({'kind': 'enumeration_chain', 'line': number,
                            'column': connectors[0].start() + 1, 'match': '、'.join(m.group() for m in connectors),
                            'context': line.strip(), 'review': '核对是否为真实顺序；有序操作可以保留。'})
    seen = {}
    for number, line in lines:
        normalized = re.sub(r'\s+', '', line)
        if len(normalized) < 30:
            continue
        if normalized in seen:
            signals.append({'kind': 'repeated_line', 'line': number, 'column': 1,
                            'match': normalized[:60], 'context': line.strip(),
                            'review': f'与第 {seen[normalized]} 行重复，核对有无新增论证。'})
        else:
            seen[normalized] = number
    counts = {}
    for item in signals:
        counts[item['kind']] = counts.get(item['kind'], 0) + 1
    scanned = '\n'.join(line for _, line in lines)
    return {
        'scope': '仅扫描Markdown/纯文本可见正文行；跳过标题、引用块、围栏代码；不理解论证语义。',
        'external_aigc': {'status': 'not_tested', 'rate': None},
        'metrics': {'scanned_cjk_chars': len(re.findall(r'[\u4e00-\u9fff]', scanned)),
                    'signal_count': len(signals), 'by_kind': counts},
        'signals': signals,
        'limitations': ['命中仅为复核提示，不是问题定论。', '零命中不能证明自然、原创或论证合格。',
                        '字符数不含跳过区域，不可作为官方活页字数验收。',
                        '不核验文献、事实、匿名或材料获取条件。'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        raw = args.file.read_bytes()
        if args.file.suffix.lower() not in {'.md', '.txt'}:
            raise ValueError('仅支持UTF-8 Markdown或纯文本；DOCX/PDF请先完整提取正文与图表文字。')
        text = raw.decode('utf-8-sig')
        if not text.strip():
            raise ValueError('输入文件为空。')
    except (OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    result = analyze(text)
    result['file'] = str(args.file)
    result['sha256'] = hashlib.sha256(raw).hexdigest()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"表达复核信号：{result['metrics']['signal_count']} 处（非AI检测）")
        for item in result['signals']:
            print(f"{item['line']}:{item['column']} [{item['kind']}] {item['match']}；{item['review']}")
        print('第三方AI率：未检测。零信号不代表论证合格。')
    return 0  # 完成诊断，不表示质量通过


if __name__ == '__main__':
    raise SystemExit(main())
