import unittest
from engine.inference import generate

class TestPersona(unittest.TestCase):
    def test_persona_mentions_cridergpt(self):
        """Verify that the generated response maintains the CriderGPT persona."""
        response = generate("Who are you?")
        self.assertIn("CriderGPT", response)

if __name__ == "__main__":
    unittest.main()
