# Fonction à tester (dans un fichier séparé, ex: example.py)
def addition(a, b):
    return a + b

# Test de la fonction
def test_addition():
    assert addition(2, 3) == 5
    assert addition(-1, 1) == 0
    assert addition(0, 0) == 0
