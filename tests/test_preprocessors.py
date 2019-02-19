import pytest

from corporacreator import preprocessors


@pytest.mark.parametrize('locale, client_id, sentence, expected', [
    ('fr', '*', 'Faisons donc attention à utiliser les bons mots.', 'faisons donc attention à utiliser les bons mots'),
    ('fr', '*', "bah 98%", "bah quatre vingt dix huit pourcent"),
    ('fr', '*', "prix au m2", "prix au mètre carré"),
    ('fr', '*', "prix au m²", "prix au mètre carré"),
    ('fr', '*', "10 m²", "dix mètre carré"),
    ('fr', '*', "2éme page", "deuxième page"),
    ('fr', '*', "donc, ce sera 299 € + 99 €", "donc ce sera deux cent quatre vingt dix neuf euros plus quatre vingt dix neuf euros"),
    ('fr', '*', "ok pour 18h", "ok pour dix huit heure"),
    ('fr', '*', '2 0 200', "deux zéro deux cents"),
    ('fr', '*', 'rue Coq-Héron au nº13', "rue coq héron au numéro treize"),
    ('fr', '*', "En comparaison, la Lune orbite en moyenne à 390 000 km de la Terre", "en comparaison la lune orbite en moyenne à trois cent quatre vingt dix mille kilomètres de la terre"),
])
def test_preprocessor(locale, client_id, sentence, expected):
    preprocessor = getattr(preprocessors, locale.replace('-', ''))
    assert expected == preprocessor(client_id, preprocessors.common(sentence))
