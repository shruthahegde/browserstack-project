from Project import main

def test_articles_pipeline_1():
    translated_titles = main()
    assert isinstance(translated_titles, list)
    assert len(translated_titles) >= 3 