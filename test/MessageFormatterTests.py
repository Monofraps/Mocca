import unittest
import lib.MessageFormatter as MessageFormatter


class MoccaMessageFormatterTests(unittest.TestCase):
    def test_can_set_verbosity_level(self):
        MessageFormatter.set_verbosity(MessageFormatter.V_INFO)
        self.assertEqual(MessageFormatter.verbosity, MessageFormatter.V_INFO)

        MessageFormatter.set_verbosity(MessageFormatter.V_ERROR)
        self.assertEqual(MessageFormatter.verbosity, MessageFormatter.V_ERROR)

    def test_should_log_method(self):
        MessageFormatter.set_verbosity(MessageFormatter.V_ERROR)
        self.assertTrue(MessageFormatter._should_log(MessageFormatter.V_ERROR))
        self.assertFalse(MessageFormatter._should_log(MessageFormatter.V_INFO))
        self.assertFalse(MessageFormatter._should_log(MessageFormatter.V_DEBUG))

        MessageFormatter.set_verbosity(MessageFormatter.V_INFO)
        self.assertTrue(MessageFormatter._should_log(MessageFormatter.V_ERROR))
        self.assertTrue(MessageFormatter._should_log(MessageFormatter.V_INFO))
        self.assertFalse(MessageFormatter._should_log(MessageFormatter.V_DEBUG))

        MessageFormatter.set_verbosity(MessageFormatter.V_DEBUG)
        self.assertTrue(MessageFormatter._should_log(MessageFormatter.V_ERROR))
        self.assertTrue(MessageFormatter._should_log(MessageFormatter.V_INFO))
        self.assertTrue(MessageFormatter._should_log(MessageFormatter.V_DEBUG))
