import pytest

from corporacreator import preprocessors


@pytest.mark.parametrize('locale, client_id, sentence, expected', [
    ('fr', '*', 'Faisons donc attention à utiliser les bons mots.', 'Faisons donc attention à utiliser les bons mots'),
    ('fr', '*', "bah 98%", "bah quatre vingt dix huit pourcent"),
    ('fr', '*', "prix au m2", "prix au mètre carré"),
    ('fr', '*', "prix au m²", "prix au mètre carré"),
    ('fr', '*', "10 m²", "dix mètre carré"),
    ('fr', '*', "2éme page", "deuxième page"),
    ('fr', '*', "donc, ce sera 299 € + 99 €", "donc ce sera deux cent quatre vingt dix neuf euros plus quatre vingt dix neuf euros"),
    ('fr', '*', "ok pour 18h", "ok pour dix huit heure"),
    ('fr', '*', '2 0 200', "deux zéro deux cents"),
    ('fr', '*', 'rue Coq-Héron au nº13', "rue Coq Héron au numéro treize"),
    ('fr', '*', "En comparaison, la Lune orbite en moyenne à 390 000 km de la Terre", "En comparaison la Lune orbite en moyenne à trois cent quatre vingt dix mille kilomètres de la Terre"),
    ('fr', '*', "le vendredi 13 mars à 11 h 10.", "le vendredi treize mars à onze heure dix"),
    ('fr', '*', "le 13 mars à 11 h.", "le treize mars à onze heure"),
    ('fr', '*', "Demain%2C il n’y aura plus d’entreprises", "Demain il n’y aura plus d’entreprises"),
    ('fr', '*', "À la 5è rue", "À la cinquième rue"),
    ('fr', '*', "Telle est la raison d’être du CICE.", "Telle est la raison d’être du C I C E"),
    ('fr', '*', "Tout le monde titrait sur « la bataille de l’ISF ». ", "Tout le monde titrait sur la bataille de l’I S F"),
    ('fr', '*', "Nous parlons de CDI saisonnier", "Nous parlons de C D I saisonnier"),
    ('fr', '*', "Nous nous accordons tous à dire que dix-huit milliards d’A P L, ce n’est pas tenable.", "Nous nous accordons tous à dire que dix huit milliards d’A P L ce n’est pas tenable"),
    ('fr', '*', "Quelques-uns seulement bénéficient du RSA.", "Quelques uns seulement bénéficient du R S A"),
    ('fr', '*', "Jean-Paul II.", "Jean Paul deux"),
    ('fr', '*', "nº deux", "numéro deux"),
    ('fr', '*', "Une capacité qui pourrait être équivalente à une production de 120 000T de poudre de lait /an.", "Une capacité qui pourrait être équivalente à une production de cent vingt mille tonnes de poudre de lait par an"),
    ('fr', '*', "30 euros/m2", "trente euros par mètre carré"),
])
def test_preprocessor(locale, client_id, sentence, expected):
    preprocessor = getattr(preprocessors, locale.replace('-', ''))
    assert expected == preprocessor(client_id, preprocessors.common(sentence))
