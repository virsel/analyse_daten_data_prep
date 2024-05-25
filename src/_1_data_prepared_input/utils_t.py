import unittest
from unittest.mock import patch
from utils import get_description
from wipo_ipc import Ipc

class TestGetDescription(unittest.TestCase):
    @patch('my_module.utils.Ipc')
    def test_valid_ipc(self, MockIpc):
        # Setup the mock
        mock_instance = MockIpc.return_value
        mock_instance.classe.description = 'Valid IPC description'
        
        # Test a valid IPC
        self.assertEqual(get_description('A01B'), 'Valid IPC description')
        MockIpc.assert_called_once_with('A01B')

    @patch('my_module.utils.Ipc')
    def test_empty_ipc(self, MockIpc):
        # Test with an empty string
        self.assertEqual(get_description(''), '')

    @patch('my_module.utils.Ipc')
    def test_attribute_error(self, MockIpc):
        # Setup the mock to raise an AttributeError
        mock_instance = MockIpc.return_value
        mock_instance.classe.description = 'Valid IPC description'
        mock_instance.section.description = 'Section description'
        
        mock_instance.classe.description.side_effect = AttributeError
        
        with patch('builtins.print') as mocked_print:
            self.assertEqual(get_description('A01B'), 'Section description')
            mocked_print.assert_called_once_with('attr err on A01B')

    @patch('my_module.utils.Ipc')
    def test_value_error(self, MockIpc):
        # Setup the mock to raise a ValueError
        MockIpc.side_effect = ValueError
        
        with self.assertRaises(ValueError):
            get_description('invalid_code')

if __name__ == '__main__':
    unittest.main()