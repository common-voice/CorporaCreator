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
    ('fr', '*', "le vendredi 13 mars à 11 h 10.", "le vendredi treize mars à onze heure dix"),
    ('fr', '*', "le 13 mars à 11 h.", "le treize mars à onze heure"),
    ('fr', '*', "Demain%2C il n’y aura plus d’entreprises", "demain il n'y aura plus d'entreprises"),
    ('fr', '*', "À la 5è rue", "à la cinquième rue"),
    ('fr', '*', "Telle est la raison d’être du CICE.", "telle est la raison d'être du c i c e"),
    ('fr', '*', "Tout le monde titrait sur « la bataille de l’ISF ». ", "tout le monde titrait sur la bataille de l'i s f"),
    ('fr', '*', "Nous parlons de CDI saisonnier", "nous parlons de c d i saisonnier"),
    ('fr', '*', "Nous nous accordons tous à dire que dix-huit milliards d’APL, ce n’est pas tenable.", "nous nous accordons tous à dire que dix huit milliards d'a p l ce n'est pas tenable"),
    ('fr', '*', "Quelques-uns seulement bénéficient du RSA.", "quelques uns seulement bénéficient du r s a"),
])
def test_preprocessor(locale, client_id, sentence, expected):
    preprocessor = getattr(preprocessors, locale.replace('-', ''))
    assert expected == preprocessor(client_id, preprocessors.common(sentence))
