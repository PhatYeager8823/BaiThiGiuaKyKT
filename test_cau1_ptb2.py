import unittest
import math
import re
import datetime
import sys
import io

# --- PHẦN 1: IMPORT HÀM CẦN TEST ---
# Nếu bạn đã có file ptb2.py thực tế, hãy bỏ comment dòng dưới và xóa hàm dummy đi
# from ptb2 import giai_pt_bac2

# (Hàm giả lập để code chạy được ngay - Khi thi bạn xóa đoạn này đi nhé)
def giai_pt_bac2(a, b, c):
    if a == 0 and b == 0 and c == 0: return "Phương trình có vô số nghiệm"
    if a == 0 and b == 0: return "Phương trình vô nghiệm"
    if a == 0: return f"Phương trình bậc nhất, nghiệm x={-c/b}"
    delta = b*b - 4*a*c
    if delta < 0: return "Phương trình vô nghiệm thực"
    if delta == 0: return f"Phương trình có nghiệm kép x1=x2={-b/(2*a)}"
    x1 = (-b + math.sqrt(delta))/(2*a)
    x2 = (-b - math.sqrt(delta))/(2*a)
    return f"Phương trình có 2 nghiệm phân biệt x1={x1}, x2={x2}"

# --- PHẦN 2: CÁC HÀM HỖ TRỢ (HELPER) ---
def extract_numbers(text):
    """Hàm trích xuất số từ chuỗi kết quả (Chuẩn theo đáp án cô giáo)"""
    return [float(x) for x in re.findall(r"-?\d+\.\d+", text)]

# --- PHẦN 3: CLASS KIỂM THỬ (UNITTEST) ---
class TestGiaiPTB2(unittest.TestCase):
    
    # TC1: Vô số nghiệm
    def test_TC1_vo_so_nghiem(self):
        ket_qua = giai_pt_bac2(0, 0, 0)
        self.assertEqual(ket_qua, "Phương trình có vô số nghiệm")

    # TC2: Vô nghiệm (a=0, b=0, c!=0)
    def test_TC2_vo_nghiem(self):
        ket_qua = giai_pt_bac2(0, 0, 5)
        self.assertEqual(ket_qua, "Phương trình vô nghiệm")

    # TC3: Bậc nhất (a=0)
    def test_TC3_bac_nhat(self):
        res = giai_pt_bac2(0, 2, -4)
        # Kiểm tra chứa từ khóa
        self.assertIn("bậc nhất", res)
        # Kiểm tra giá trị số (x=2.0)
        nums = extract_numbers(res)
        self.assertTrue(len(nums) > 0, "Không tìm thấy số trong kết quả")
        self.assertTrue(math.isclose(nums[0], 2.0, rel_tol=1e-3))

    # TC4: Delta âm (Vô nghiệm thực)
    def test_TC4_delta_am(self):
        res = giai_pt_bac2(1, 2, 5)
        self.assertEqual(res, "Phương trình vô nghiệm thực")

    # TC5: Delta = 0 (Nghiệm kép)
    def test_TC5_nghiem_kep(self):
        res = giai_pt_bac2(1, 2, 1) # x = -1.0
        self.assertIn("nghiệm kép", res)
        nums = extract_numbers(res)
        self.assertTrue(len(nums) > 0)
        self.assertTrue(math.isclose(nums[0], -1.0, rel_tol=1e-3))

    # TC6: Delta > 0 (2 nghiệm phân biệt)
    def test_TC6_hai_nghiem_phan_biet(self):
        res = giai_pt_bac2(1, -3, 2) # Nghiệm 1.0 và 2.0
        self.assertIn("2 nghiệm phân biệt", res)
        nums = extract_numbers(res)
        
        # Kiểm tra xem có đủ 2 nghiệm 1.0 và 2.0 không
        has_1 = any(math.isclose(x, 1.0, rel_tol=1e-3) for x in nums)
        has_2 = any(math.isclose(x, 2.0, rel_tol=1e-3) for x in nums)
        self.assertTrue(has_1 and has_2, f"Kết quả mong đợi 1.0 và 2.0, nhận được {nums}")

    # TC7: Test case này CỐ TÌNH SAI để xem báo cáo hiện màu đỏ
    def test_TC7_demo_ket_qua_sai(self):
        # Thực tế: (0, 0, 0) trả về "Phương trình có vô số nghiệm"
        # Nhưng ta mong đợi sai là: "Phương trình vô nghiệm"
        res = giai_pt_bac2(0, 0, 0)
        
        # Câu lệnh này sẽ gây ra lỗi FAIL vì 2 chuỗi không giống nhau
        self.assertEqual(res, "Phương trình vô nghiệm", "Lỗi này là do tôi cố tình làm sai để test báo cáo!")

# --- PHẦN 4: CHẠY TEST VÀ XUẤT HTML ---
if __name__ == '__main__':
    # 1. Nạp các test case từ class TestGiaiPTB2
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGiaiPTB2)
    
    # 2. Chạy test và hứng kết quả vào biến 'result'
    # stream=io.StringIO() giúp ẩn kết quả in ra màn hình console để tập trung vào file HTML
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2)
    result = runner.run(suite)
    
    # 3. Code xuất file HTML (Dựa trên mẫu bạn cung cấp)
    filename = "ketqua.html"
    with open(filename, "w", encoding="utf-8") as f:
        # --- HEADER ---
        f.write("""
        <html>
        <head>
            <meta charset='utf-8'>
            <title>Kết quả kiểm thử</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; background: #fafafa; }
                h1 { color: #2c3e50; border-bottom: 2px solid #34495e; padding-bottom: 10px; }
                .section-title { margin-top: 25px; color: #34495e; }
                ul { line-height: 1.7; }
                table { border-collapse: collapse; width: 100%; margin-top: 15px; }
                table, th, td { border: 1px solid #aaa; padding: 8px; }
                th { background: #e8e8e8; text-align: left; }
                .pass { color: green; font-weight: bold; }
                .fail { color: red; font-weight: bold; }
                .error { color: orange; font-weight: bold; }
                pre { white-space: pre-wrap; background: #f5f5f5; padding: 5px; }
            </style>
        </head>
        <body>
        """)
        
        # --- BODY REPORT ---
        f.write("<h1>BÁO CÁO KẾT QUẢ KIỂM THỬ</h1>\n")
        
        # Thời gian
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"<p><b>Thời gian chạy:</b> {now}</p>\n")
        
        # Thống kê số liệu từ biến result
        total = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        passed = total - failures - errors
        
        # Tổng quan
        f.write("<h2 class='section-title'>I. Thống kê tổng quan</h2>\n")
        f.write("<ul>\n")
        f.write(f"<li><b>Tổng số test chạy:</b> {total}</li>\n")
        f.write(f"<li><span class='pass'>PASS:</span> <span class='pass'>{passed}</span></li>\n")
        f.write(f"<li><span class='fail'>Failures:</span> <span class='fail'>{failures}</span></li>\n")
        f.write(f"<li><span class='error'>Errors:</span> <span class='error'>{errors}</span></li>\n")
        f.write("</ul>\n")
        
        # Chi tiết lỗi
        f.write("<h2 class='section-title'>II. Chi tiết lỗi</h2>\n")
        
        if failures == 0 and errors == 0:
            f.write("<p class='pass'>✔ Chúc mừng! Tất cả test case đều PASS.</p>\n")
        else:
            f.write("<table>\n")
            f.write("<tr><th>Loại lỗi</th><th>Tên test</th><th>Chi tiết</th></tr>\n")
            
            # Ghi lỗi Fail (Logic sai)
            for test, detail in result.failures:
                f.write("<tr>")
                f.write("<td class='fail'>FAIL</td>")
                f.write(f"<td>{test}</td>")
                f.write(f"<td><pre>{detail}</pre></td>")
                f.write("</tr>\n")
                
            # Ghi lỗi Error (Code lỗi)
            for test, detail in result.errors:
                f.write("<tr>")
                f.write("<td class='error'>ERROR</td>")
                f.write(f"<td>{test}</td>")
                f.write(f"<td><pre>{detail}</pre></td>")
                f.write("</tr>\n")
            
            f.write("</table>\n")
        
        f.write("</body></html>")
        
    print(f"Đã chạy xong {total} test case.")
    print(f"Xem kết quả chi tiết tại file: {filename}")