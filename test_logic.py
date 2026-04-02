import pytest
from logic import get_ai_response

def test_get_ai_response_valid_input(mocker):
    # # Mockiamo la chiamata a Ollama per non dipendere dal modello nei test
    # mock_ollama = mocker.patch('ollama.chat')
    # mock_ollama.return_value = {'message': {'content': 'Ciao, come posso aiutarti?'}}
    
    res = get_ai_response("What's the capital of the USA? Answer with only the city name")
    assert res == "Washington DC" or res == "Washington, D.C." or res == "Washington"  # Accettiamo entrambe le varianti

def test_get_ai_response_empty_input():
    # Testiamo un caso limite senza mock
    res = get_ai_response("")
    assert res == "Messaggio vuoto."