from src.extract import split_sentences


def test_split_keeps_numbers_together():
    text = "Poverty fell to 2.6% in 2023. The base was 27.1% in 2011."
    sentences = split_sentences(text)
    assert len(sentences) == 2
    assert "2.6%" in sentences[0]