# import pytest
# from unittest.mock import patch, mock_open, MagicMock
# # from flaskr.wikimusic import get_wikipedia_articles, get_iframe_spotify_songs
# from .wikimusic import get_wikipedia_articles, get_iframe_spotify_songs


# @patch("wikimusic.get_wikipedia_article")
# def test_get_wikipedia_articles(mock_get_wikipedia_article):
#     mock = MagicMock()
#     mock.get.return_value = MagicMock()
#     mock.get.return_value.json.return_value.__enter__.return_value = {
#         "query": {
#             "search": {
#                 "title": "new song"
#             }
#         }
#     }

#     mock_get_wikipedia_article.return_value = "new article"

#     articles = get_wikipedia_articles("black bird", mock)
#     assert articles == ["new article"]
