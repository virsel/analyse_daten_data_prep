import unittest

from src._1_data_prepared_input.arrangement import extract_german_text


class TestTxtCleaning(unittest.TestCase):
    def test_remove_de(self):
        self.assertEqual(extract_german_text("[DE] SCHWEISSBRENNERSYSTEM MIT EINER WECHSELKUPPLUNG UND SCHWEISSBRENNER, BRENNERWECHSELSTATION, UND VERFAHREN ZUM AUFNEHMEN EINES SCHWEISSBRENNER EINES SCHWEISSBRENNERSYSTEM MIT EINEM SCHWEISSROBOTER ..."),
                         "SCHWEISSBRENNERSYSTEM MIT EINER WECHSELKUPPLUNG UND SCHWEISSBRENNER, BRENNERWECHSELSTATION, UND VERFAHREN ZUM AUFNEHMEN EINES SCHWEISSBRENNER EINES SCHWEISSBRENNERSYSTEM MIT EINEM SCHWEISSROBOTER ...")

if __name__ == '__main__':
    unittest.main()