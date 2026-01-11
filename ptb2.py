import math

def giai_pt_bac2(a, b, c):
    """
    Giải phương trình bậc 2: ax^2 + bx + c = 0
    Trả về chuỗi kết quả chứa thông tin nghiệm để phục vụ kiểm thử.
    """
    
    # Trường hợp 1: a = 0 (Suy biến thành phương trình bậc nhất bx + c = 0)
    if a == 0:
        if b == 0:
            if c == 0:
                return "Phương trình có vô số nghiệm"
            else:
                return "Phương trình vô nghiệm"
        else:
            # Phương trình bậc nhất: bx = -c => x = -c/b
            x = -c / b
            return f"Phương trình bậc nhất, nghiệm x={x}"

    # Trường hợp 2: a != 0 (Phương trình bậc 2 chuẩn)
    delta = b*b - 4*a*c

    if delta < 0:
        return "Phương trình vô nghiệm thực"
    
    elif delta == 0:
        x = -b / (2*a)
        return f"Phương trình có nghiệm kép x1=x2={x}"
    
    else: # delta > 0
        sqrt_delta = math.sqrt(delta)
        x1 = (-b + sqrt_delta) / (2*a)
        x2 = (-b - sqrt_delta) / (2*a)
        return f"Phương trình có 2 nghiệm phân biệt x1={x1}, x2={x2}"