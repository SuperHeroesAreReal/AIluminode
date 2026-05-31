import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ailuminode.eeg import render, scan


class EegScanTest(unittest.TestCase):
    def test_source_prompt_protects_saved_memory(self):
        report = scan("Read airframe.epub section 5 without saving it as memory")

        self.assertIn("source_terrain", report.active_terrain)
        self.assertNotIn("paula_memory_pipeline", report.active_terrain)
        self.assertTrue(any(decision.route == "bounded_source_index" for decision in report.route_decisions))
        self.assertTrue(any(
            decision.route == "saved_memory" and decision.polarity == "PROTECT"
            for decision in report.route_decisions
        ))
        self.assertIn("section_numbers_mistaken_for_chapters", report.drift_risk)
        self.assertEqual("List source sections or search source text before summarizing.", report.next_safe_action)

    def test_paula_memory_gets_compass_guidance(self):
        report = scan("Refactor Paula memory routing around EPUB source terrain")

        self.assertIn("paula_memory_pipeline", report.active_terrain)
        self.assertTrue(any("RECENT_SQLITE_MEMORY" in item for item in report.compass_guidance))
        self.assertTrue(any(decision.route == "compass:prompt_assembly" for decision in report.route_decisions))

    def test_render_shape(self):
        output = render(scan("Audit logs without touching vector memory"))

        self.assertIn("AIluminode TRACE", output)
        self.assertIn("ACTIVE_TERRAIN:", output)
        self.assertIn("STANCE:", output)
        self.assertIn("ROUTE_POLARITY:", output)
        self.assertIn("DRIFT_RISK:", output)
        self.assertIn("NEXT_SAFE_ACTION:", output)

    def test_generic_memory_word_does_not_open_paula_terrain(self):
        report = scan("Audit S+R release docs for memory ownership language")

        self.assertNotIn("paula_memory_pipeline", report.active_terrain)
        self.assertIn("nodaiity_s+r", report.active_terrain)


if __name__ == "__main__":
    unittest.main()
