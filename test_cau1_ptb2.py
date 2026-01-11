import unittest
import math
import re
import pytest
import sys
from ptb2 import giai_pt_bac2

# --- PHẦN 2: HÀM HỖ TRỢ (Giữ nguyên) ---
def extract_numbers(text):
    return [float(x) for x in re.findall(r"-?\d+\.\d+", text)]

# --- PHẦN 3: CLASS KIỂM THỬ (Giữ nguyên logic test của bạn) ---
class TestGiaiPTB2(unittest.TestCase):
    
    def test_TC1_vo_so_nghiem(self):
        self.assertEqual(giai_pt_bac2(0, 0, 0), "Phương trình có vô số nghiệm")

    def test_TC2_vo_nghiem(self):
        self.assertEqual(giai_pt_bac2(0, 0, 5), "Phương trình vô nghiệm")

    def test_TC3_bac_nhat(self):
        res = giai_pt_bac2(0, 2, -4)
        self.assertIn("bậc nhất", res)
        nums = extract_numbers(res)
        self.assertTrue(len(nums) > 0)
        self.assertTrue(math.isclose(nums[0], 2.0, rel_tol=1e-3))

    def test_TC4_delta_am(self):
        self.assertEqual(giai_pt_bac2(1, 2, 5), "Phương trình vô nghiệm thực")

    def test_TC5_nghiem_kep(self):
        res = giai_pt_bac2(1, 2, 1)
        self.assertIn("nghiệm kép", res)
        nums = extract_numbers(res)
        self.assertTrue(len(nums) > 0)
        self.assertTrue(math.isclose(nums[0], -1.0, rel_tol=1e-3))

    def test_TC6_hai_nghiem_phan_biet(self):
        res = giai_pt_bac2(1, -3, 2)
        self.assertIn("2 nghiệm phân biệt", res)
        nums = extract_numbers(res)
        has_1 = any(math.isclose(x, 1.0, rel_tol=1e-3) for x in nums)
        has_2 = any(math.isclose(x, 2.0, rel_tol=1e-3) for x in nums)
        self.assertTrue(has_1 and has_2)

    # Test Case cố tình sai để xem màu đỏ trong báo cáo
    def test_TC7_demo_ket_qua_sai(self):
        res = giai_pt_bac2(0, 0, 0)
        self.assertEqual(res)

# --- PHẦN 4: TỰ ĐỘNG CHẠY VÀ XUẤT HTML (Thay đổi lớn nhất ở đây) ---
if __name__ == '__main__':
    print("⏳ Đang chạy kiểm thử PTB2 và tạo báo cáo HTML...")
    
    # Dùng lệnh này thay vì viết code HTML thủ công dài dòng
    # --self-contained-html: Giúp file HTML đẹp mà không cần file CSS đi kèm
    pytest.main(["-v", __file__, "--html=ketqua_ptb2.html", "--self-contained-html"])
    
    print("\n✅ Đã xong! Mở file 'ketqua_ptb2.html' để xem kết quả (Có màu đỏ FAIL).")