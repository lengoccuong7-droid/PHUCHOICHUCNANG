import unittest

from clinical_engine import analyze_case
from diagnostic_audit import CATALOGUE, run_bidirectional_audit, render_audit_report


class DiagnosticAuditTests(unittest.TestCase):
    def setUp(self):
        self.shoulder = {
            "region": "Khớp vai", "reason": "Đau vai khi nâng tay",
            "history": "Đau vai phải khi dang tay, đau về đêm",
            "site": "Mặt ngoài vai", "radiation": "Không lan",
            "inspection": "Không biến dạng", "palpation": "Đau vùng dưới mỏm cùng",
            "rom_mmt": "ROM chủ động đau, ROM thụ động bảo tồn; Jobe đau nhưng chưa ghi yếu cơ",
            "tests": {"Neer Test": "Dương tính (+)", "Hawkins-Kennedy": "Dương tính (+)",
                      "Jobe Test (Empty Can)": "Chưa làm / Âm tính (-)"},
            "red_flags": {},
        }

    def test_catalogue_covers_nine_regions(self):
        self.assertEqual(len(CATALOGUE), 9)

    def test_every_region_can_be_audited_without_crashing(self):
        for region in CATALOGUE:
            case = dict(self.shoulder)
            case["region"] = region
            audit = run_bidirectional_audit(case, analyze_case(case))
            self.assertEqual(audit["region"], region)
            self.assertTrue(audit["reverse"])

    def test_forward_and_reverse_are_both_produced(self):
        base = analyze_case(self.shoulder)
        audit = run_bidirectional_audit(self.shoulder, base)
        self.assertTrue(audit["forward"])
        self.assertTrue(audit["reverse"])
        self.assertIn("Đau liên quan chóp xoay", [x["name"] for x in audit["forward"]])

    def test_legacy_test_value_is_unknown_not_negative(self):
        audit = run_bidirectional_audit(self.shoulder, analyze_case(self.shoulder))
        self.assertIn("Jobe Test (Empty Can)", audit["unknown_tests"])
        self.assertTrue(any("gộp" in x for x in audit["contradictions"]))

    def test_history_radiation_mismatch_is_flagged(self):
        case = dict(self.shoulder)
        case["history"] = "Đau lan xuống tay và tê ngón tay"
        case["radiation"] = "Không lan, không tê"
        audit = run_bidirectional_audit(case, analyze_case(case))
        self.assertTrue(any("mô tả lan/tê" in x for x in audit["contradictions"]))

    def test_red_flag_blocks_routine_conclusion(self):
        case = dict(self.shoulder)
        base = analyze_case(case)
        base["red_flags"] = ["Cờ đỏ kiểm thử"]
        audit = run_bidirectional_audit(case, base)
        self.assertIn("ƯU TIÊN AN TOÀN", audit["overall"])

    def test_report_is_text(self):
        audit = run_bidirectional_audit(self.shoulder, analyze_case(self.shoulder))
        report = render_audit_report(audit)
        self.assertIn("ĐỐI SOÁT CHẨN ĐOÁN HAI CHIỀU", report)


if __name__ == "__main__":
    unittest.main()
