"""行为测试：避免把正常学术语言或零信号误报为AI/质量结论。"""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from check_writing import analyze, main


class WritingDiagnosticsTest(unittest.TestCase):
    def test_preserves_academic_terms_and_valid_distinction(self):
        report = analyze('机制是待解释的过程。范式用于界定理论前提。此处讨论的不是资源总量，而是分配规则。')
        self.assertEqual(report['signals'], [])
        self.assertIsNone(report['external_aigc']['rate'])

    def test_locates_claim_for_review_without_ai_verdict(self):
        report = analyze('# 标题\n\n本研究填补空白，具有重要意义。')
        self.assertEqual({x['line'] for x in report['signals']}, {3})
        self.assertEqual(len(report['signals']), 2)
        self.assertEqual(report['external_aigc']['status'], 'not_tested')

    def test_zero_signals_does_not_mean_argument_passed(self):
        report = analyze('本课题将研究问题，并完成研究。')
        self.assertEqual(report['metrics']['signal_count'], 0)
        self.assertNotIn('passed', report)
        self.assertNotIn('score', report)
        self.assertTrue(any('零命中' in s for s in report['limitations']))

    def test_priority_claim_with_topic_between_verb_and_object(self):
        report = analyze('本课题填补公共体育场地开放中断研究的空白。')
        self.assertEqual(len(report['signals']), 1)
        self.assertEqual(report['signals'][0]['kind'], 'priority_claim')

    def test_ignores_metadata_and_code_but_preserves_locations(self):
        report = analyze('> 综上所述\n```text\n具有重要意义\n```\n\n正文：综上所述。')
        self.assertEqual(len(report['signals']), 1)
        self.assertEqual(report['signals'][0]['line'], 6)

    def test_repeated_content_is_located(self):
        paragraph = '本课题拟比较不同管理安排中的开放记录，区分临时关闭、恢复开放与后续执行三个环节。'
        report = analyze(paragraph + '\n\n' + paragraph)
        duplicates = [x for x in report['signals'] if x['kind'] == 'repeated_line']
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]['line'], 3)

    def test_ordered_steps_remain_review_advice(self):
        report = analyze('首先校验资料目录，其次核对版本，最后记录差异。')
        self.assertEqual(report['signals'][0]['kind'], 'enumeration_chain')
        self.assertIn('可以保留', report['signals'][0]['review'])
        self.assertIsNone(report['external_aigc']['rate'])

    def test_cli_rejects_empty_or_binary_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, data in [('empty.md', b''), ('fake.docx', b'PK\x00\xff'), ('bad.txt', b'\xff')]:
                path = Path(directory) / name
                path.write_bytes(data)
                with patch.object(sys, 'argv', ['check_writing.py', str(path)]), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(), 2)


if __name__ == '__main__':
    unittest.main()
