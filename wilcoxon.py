import math
from scipy.stats import wilcoxon

# =========================================
# 1. CÁC HÀM TỰ CODE BẰNG PYTHON THUẦN
# =========================================

# Hàm tính CDF của phân phối chuẩn tắc (thay thế scipy.stats.norm)
def normal_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

# Hàm tính toán Wilcoxon hoàn chỉnh
def wilcoxon_manual(X, Y, apply_continuity = True, apply_tie_correction = True):
    diff = []
    for x, y in zip(X, Y):
        d = x - y
        if d != 0:
            sign = 1 if d > 0 else -1
            # Nạp một tuple gồm (trị tuyệt đối, dấu)
            diff.append((abs(d), sign)) 

    # Sắp xếp theo trị tuyệt đối
    diff.sort(key=lambda item: item[0])
    
    w_plus = 0
    w_minus = 0
    n = len(diff) 
    tie_penalty = 0
    
    # Bắt lỗi: Nếu 2 mảng không có điểm nào khác biệt
    if n == 0:
        return {"W": 0.0, "Z_score": 0.0, "p_value": 1.0}

    i = 0

    while i < n:
        j = i
        while j < n and diff[j][0] == diff[i][0]:
            j += 1

        t = j - i
        
        if apply_tie_correction and t > 1:
            tie_penalty += (t**3 - t) / 48

        sum_rank = sum(range(i + 1, j + 1))
        avg_rank = sum_rank / t

        for k in range(i, j):
            sign = diff[k][1]
            if sign == 1:
                w_plus += avg_rank
            elif sign == -1:
                w_minus += avg_rank
        
        i = j

    final_w = min(w_plus, w_minus)
    
    mu_w = n * (n + 1) / 4
    sigma_w = math.sqrt((n * (n + 1) * (2 * n + 1)) / 24 - tie_penalty)
    numerator = final_w - mu_w

    if apply_continuity:
        if numerator < 0:
            numerator += 0.5
        elif numerator > 0:
            numerator -= 0.5

    z_score = (numerator) / sigma_w
    
    p_value = 2 * normal_cdf(-abs(z_score))

    return {
        "W": final_w,
        "Z_score": z_score,
        "p_value": p_value
    }


# =========================================
# 2. CHẠY THỬ NGHIỆM VÀ SO SÁNH
# =========================================

# Dữ liệu thử nghiệm
X_test = [85, 70, 40, 65, 80, 75, 90]
Y_test = [75, 50, 50, 40, 80, 65, 80]

# Chạy cả 2 hàm
result_manual = wilcoxon_manual(X_test, Y_test,apply_continuity=False)
result_lib = wilcoxon(X_test, Y_test, method = "approx")

# In kết quả
print("==== KẾT QUẢ TỪ HÀM TỰ CODE (MANUAL) ====")
print(f"Giá trị W    : {result_manual['W']}")
print(f"Điểm Z-score : {result_manual['Z_score']:.4f}")
print(f"P-value      : {result_manual['p_value']:.4f}")

print("\n==== KẾT QUẢ TỪ THƯ VIỆN SCIPY ====")
print(f"Giá trị W    : {result_lib.statistic}")
print(f"P-value      : {result_lib.pvalue:.4f}")
print(f"Z-score      : {result_lib.zstatistic:.4f}")

print("\n==== KẾT LUẬN CUỐI CÙNG ====")
# Dựa trên kết quả tự code
if result_manual['p_value'] < 0.05:
    print("-> Bác bỏ H0: Có sự khác biệt có ý nghĩa thống kê giữa 2 nhóm (P-value < 0.05).")
else:
    print("-> Chấp nhận H0: Không đủ bằng chứng để nói có sự khác biệt (P-value >= 0.05).")