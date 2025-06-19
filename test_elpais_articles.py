from Project import main

def test_articles_pipeline():
    translated_titles = main()
    assert len(translated_titles) == 5
    assert all(isinstance(title, str) for title in translated_titles)