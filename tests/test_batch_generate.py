import pytest
from wordsmith import NarrativeGenerateError
from tests.fixtures import TestWordsmith


class TestProject(TestWordsmith):

    def setup(self):
        self.ws = super().initialize()

    def test_batch_generate_narrative(self):
        data = [{'a': i, 'b': i, 'c': i} for i in range(10)]
        expected_outputs = ['The value of A is {}.'.format(i)
                            for i in range(10)]
        narrs = self.ws.project('test').template('test').batch_narrative(data)
        narrs.generate()
        for expected, actual in zip(expected_outputs, narrs.narratives):
            assert expected == actual.text

    def test_bad_batch_generate_no_break(self):
        data = [
            {'a': 1, 'b': 1, 'c': 1},
            {'d': 1, 'e': 1},
            {'a': 1, 'b': 1, 'c': 1}
        ]
        narrs = self.ws.project('test').template('test').batch_narrative(data)
        narrs.break_on_error = False
        narrs.generate()
        expected_narratives = ['The value of A is 1.',
                               None,
                               'The value of A is 1.']
        actual_narratives = []
        for n in narrs.narratives:
            actual_narratives.append(n.text if n is not None else None)
        assert (expected_narratives == actual_narratives)\
            and (len(narrs.errors) == 1)

    def test_bad_batch_generate_break(self):
        with pytest.raises(NarrativeGenerateError):
            data = [
                {'a': 1, 'b': 1, 'c': 1},
                {'d': 1, 'e': 1},
                {'a': 1, 'b': 1, 'c': 1}
            ]
            narrs = self.ws.project('test')\
                .template('test').batch_narrative(data)
            narrs.break_on_error = True
            narrs.generate()

    def test_wordsmith_400_error(self):
        with pytest.raises(NarrativeGenerateError):
            data = {'not_a_valid_column': 0}
            self.ws.project('test')\
                .template('test').generate_narrative(data)
