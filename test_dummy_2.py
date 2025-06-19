from Project import main

def test_articles_pipeline_2():
    translated_titles = main()
    for title in translated_titles:
        assert len(title) > 0 