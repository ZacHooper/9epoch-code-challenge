from models import vadar

def test_vader_analysis():
    sentence = 'The head of the United Nations says Ukraine has become "an epicentre of unbearable heartache and pain."'
    assert vadar.compound_score(sentence) > -1
    assert vadar.compound_score(sentence) < 1