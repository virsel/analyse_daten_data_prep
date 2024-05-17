import unittest

from src.moduls.pipeline_de import txt_cleaning, spacy_tokenize

class TestTxtCleaning(unittest.TestCase):
    def test_remove_de(self):
        self.assertEqual("aufweist, wobei die Permanentmagnete eine Remanenz Br T aufweisen, und einen Umrichter, wobei eine", txt_cleaning(
        "85% aufweist, wobei die Permanentmagnete (11) eine Remanenz Br &gt; 1,25 T aufweisen, und - einen Umrichter (15), wobei eine <br />"))

    def test_remove_parentheses_content(self):
        self.assertEqual("Achsenlinie drehbar mit dem ersten Handgelenkelement gekoppelt ist, ein drittes", txt_cleaning("Achsenlinie (A2) drehbar mit dem ersten Handgelenkelement gekoppelt ist;ein drittes"))
    
    def test_special_chars_removal(self):
        self.assertEqual("Eine Interferenzbestimmungsvorrichtung umfassend: eine Erfassungseinheit, die sich.", txt_cleaning("Eine Interferenzbestimmungsvorrichtung (10) umfassend:eine Erfassungseinheit, die sich ...") )
    
    def test_duplicate_special_chars_removal(self):
        self.assertEqual("Offenbart wird ein Ende zu Ende Liefersystem, das Standardbehälter keltes AV Frachtverwaltungssystem, ein speziell entwickelter Roboter zum Beladen und Entladen von Paketen und Software zum Koordinieren der verschiedenen beteiligten Aufgaben.", txt_cleaning("Offenbart wird ein Ende-zu-Ende-Liefersystem, das Standardbehälter keltes AV-Frachtverwaltungssystem , ein speziell entwickelter Roboter zum Beladen und Entladen von Paketen und Software zum Koordinieren der verschiedenen beteiligten Aufgaben . "))
        
    def test_duplicate_special_chars_removal(self):
        self.assertEqual("vor einer Strahlungs und oder Objektquelle.", txt_cleaning("vor einer Strahlungs- und/oder Objektquelle (22)."))
        
class TestTokenizing(unittest.TestCase):
    def test_duplicate_special_chars_removal(self):
        self.assertEqual("vor einer Strahlungs und roboter oder Objektquelle.", spacy_tokenize("vor einer Strahlungs und roboter oder Objektquelle."))
        
    

if __name__ == '__main__':
    unittest.main()