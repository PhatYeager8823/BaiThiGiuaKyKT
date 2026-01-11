import pytest
import pyodbc
import os

# --- CẤU HÌNH TÊN FILE KẾT QUẢ ---
FILE_CAU_2_1 = "Ketqua_cau2.txt"
FILE_CAU_2_2 = "Ketqua_22.txt"

# --- 1. FIXTURE & HÀM HỖ TRỢ ---

@pytest.fixture(scope="session", autouse=True)
def setup_files():
    """Tự động xóa nội dung file kết quả cũ khi bắt đầu chạy"""
    # Xóa/Tạo mới file cho câu 2.2
    with open(FILE_CAU_2_2, "w", encoding="utf-8") as f:
        f.write("=== BÁO CÁO KẾT QUẢ TEST STORE PROCEDURE (CÂU 2.2) ===\n\n")
    # File câu 2.1 sẽ được ghi đè trong hàm test nên không cần xóa ở đây

@pytest.fixture(scope="function")
def db_cursor():
    """Kết nối CSDL"""
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=YOUR_SERVER_NAME;'  # <--- SỬA TÊN SERVER CỦA BẠN Ở ĐÂY
        'Database=QuanLyDiem;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    yield cursor
    conn.close()

def exec_sp(cursor, sp_name):
    """Chạy Store Procedure và trả về list dictionary"""
    cursor.execute(f"EXEC {sp_name}")
    try:
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except pyodbc.ProgrammingError:
        return []

def setup_dummy_data(cursor):
    """Làm sạch và tạo dữ liệu giả (Reset Data)"""
    # 1. Xóa dữ liệu cũ (Theo thứ tự: Con/Cháu xóa trước -> Cha xóa sau)
    cursor.execute("DELETE FROM KETQUA")
    cursor.execute("DELETE FROM SINHVIEN")
    cursor.execute("DELETE FROM MONHOC")
    cursor.execute("DELETE FROM LOP")
    
    # 2. Tạo dữ liệu mới (Theo thứ tự: Cha trước -> Con sau)
    cursor.execute("INSERT INTO LOP VALUES ('L01', '16DTH3', 50)")
    cursor.execute("INSERT INTO LOP VALUES ('L02', 'KHAC', 50)")
    
    cursor.execute("INSERT INTO MONHOC VALUES ('MH01', N'Cơ sở dữ liệu', 3)")
    cursor.execute("INSERT INTO MONHOC VALUES ('MH02', N'Mạng máy tính', 3)")
    
    cursor.execute("INSERT INTO SINHVIEN VALUES ('SV01', N'Nguyen A', '2000-01-01', 'HCM', 'L01')")
    cursor.execute("INSERT INTO SINHVIEN VALUES ('SV02', N'Tran B', '2000-02-02', 'HN', 'L01')")
    cursor.execute("INSERT INTO SINHVIEN VALUES ('SV03', N'Le C', '2000-03-03', 'DN', 'L02')")
    
    cursor.commit()

def ghi_log_2_2(tencase, trangthai, chitiet=""):
    """Hàm ghi log riêng cho file Ketqua_22.txt"""
    with open(FILE_CAU_2_2, "a", encoding="utf-8") as f:
        f.write(f"Test Case: {tencase}\n")
        f.write(f"Kết quả: {trangthai}\n")
        if chitiet: f.write(f"Chi tiết: {chitiet}\n")
        f.write("-" * 40 + "\n")

# --- 2. TEST CASE CÂU 2.1 (TRÙNG KHÓA) ---

def test_cau2_1_trung_khoa(db_cursor):
    """Test chèn trùng mã SV và ghi lỗi ra file Ketqua_cau2.txt"""
    setup_dummy_data(db_cursor) # Đảm bảo đã có SV01
    
    ma_trung = 'SV01'
    print(f"\nĐang test trùng mã: {ma_trung}")

    try:
        # Cố tình chèn trùng
        db_cursor.execute(f"INSERT INTO SINHVIEN VALUES ('{ma_trung}', N'Test Trùng', '2000-01-01', 'HCM', 'L01')")
        db_cursor.commit()
        pytest.fail("Lỗi: Hệ thống không bắt lỗi trùng khóa!")
        
    except pyodbc.IntegrityError as e:
        # Bắt lỗi thành công -> Ghi ra file
        with open(FILE_CAU_2_1, "w", encoding="utf-8") as f:
            f.write("--- KẾT QUẢ CÂU 2.1: KIỂM TRA LỖI TRÙNG KHÓA ---\n")
            f.write(f"Mã trùng: {ma_trung}\n")
            f.write(f"Kết quả: Đã bắt được lỗi (PASS)\n")
            f.write(f"Thông báo từ SQL: {str(e)}\n")
        
        assert os.path.exists(FILE_CAU_2_1)

# --- 3. TEST CASE CÂU 2.2 (STORE PROCEDURE) ---

def test_sp_happy_path(db_cursor):
    """2.2.1: Trường hợp chạy đúng"""
    setup_dummy_data(db_cursor)
    # SV02 điểm cao nhất (10)
    db_cursor.execute("INSERT INTO KETQUA VALUES ('SV01', 'MH01', 1, 8.0)")
    db_cursor.execute("INSERT INTO KETQUA VALUES ('SV02', 'MH01', 1, 10.0)")
    db_cursor.commit()

    try:
        result = exec_sp(db_cursor, 'sp_SV_DiemCSDL_CaoNhat_16DTH3')
        assert len(result) == 1
        assert result[0]['MASV'] == 'SV02' and result[0]['DIEM'] == 10.0
        ghi_log_2_2("Trường hợp đúng", "PASS", "Tìm thấy SV02 (10 điểm)")
    except AssertionError as e:
        ghi_log_2_2("Trường hợp đúng", "FAIL", str(e))
        raise e

def test_sp_lop_khong_ton_tai(db_cursor):
    """2.2.2: Tên lớp không tồn tại (Dùng Update tên lớp)"""
    setup_dummy_data(db_cursor)
    
    # Đổi tên lớp '16DTH3' thành 'XXX' -> SP tìm không ra
    db_cursor.execute("UPDATE LOP SET TENLOP = 'XXX' WHERE TENLOP = '16DTH3'")
    db_cursor.commit()

    try:
        result = exec_sp(db_cursor, 'sp_SV_DiemCSDL_CaoNhat_16DTH3')
        assert len(result) == 0
        ghi_log_2_2("Lớp không tồn tại", "PASS", "Trả về rỗng (Đúng)")
    except AssertionError as e:
        ghi_log_2_2("Lớp không tồn tại", "FAIL", str(e))
        raise e
    finally:
        # Trả lại tên cũ (Quan trọng)
        db_cursor.execute("UPDATE LOP SET TENLOP = '16DTH3' WHERE TENLOP = 'XXX'")
        db_cursor.commit()

def test_sp_mon_khong_ton_tai(db_cursor):
    """2.2.3: Tên môn không tồn tại (Dùng Update tên môn)"""
    setup_dummy_data(db_cursor)
    
    # Đổi tên môn -> SP tìm không ra
    db_cursor.execute("UPDATE MONHOC SET TENMH = N'XXX' WHERE MAMH = 'MH01'")
    db_cursor.commit()

    try:
        result = exec_sp(db_cursor, 'sp_SV_DiemCSDL_CaoNhat_16DTH3')
        assert len(result) == 0
        ghi_log_2_2("Môn không tồn tại", "PASS", "Trả về rỗng (Đúng)")
    except AssertionError as e:
        ghi_log_2_2("Môn không tồn tại", "FAIL", str(e))
        raise e
    finally:
        db_cursor.execute("UPDATE MONHOC SET TENMH = N'Cơ sở dữ liệu' WHERE MAMH = 'MH01'")
        db_cursor.commit()

def test_sp_nhieu_sv_cao_nhat(db_cursor):
    """2.2.4: Nhiều SV điểm cao bằng nhau"""
    setup_dummy_data(db_cursor)
    # Cả 2 đều 9 điểm
    db_cursor.execute("INSERT INTO KETQUA VALUES ('SV01', 'MH01', 1, 9.0)")
    db_cursor.execute("INSERT INTO KETQUA VALUES ('SV02', 'MH01', 1, 9.0)")
    db_cursor.commit()

    try:
        result = exec_sp(db_cursor, 'sp_SV_DiemCSDL_CaoNhat_16DTH3')
        assert len(result) == 2
        ghi_log_2_2("Nhiều SV điểm cao", "PASS", f"Tìm thấy {len(result)} SV")
    except AssertionError as e:
        ghi_log_2_2("Nhiều SV điểm cao", "FAIL", str(e))
        raise e