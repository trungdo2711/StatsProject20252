import math
from statsmodels.stats.contingency_tables import mcnemar

import math

import math

def custom_mcnemar(X, Y, exact=True, correction=True):
    n = len(X)
    a = b = c = d = 0
    for i in range(n):
        if X[i] == 1 and Y[i] == 1: a += 1
        elif X[i] == 1 and Y[i] == 0: b += 1
        elif X[i] == 0 and Y[i] == 1: c += 1
        else: d += 1
            
    diff = abs(b - c)
    total = b + c
    chi_square = 0.0
    
    if total == 0:
        chi_square = 0.0
        p_value = 1.0 

    elif exact == True and total < 25: 
        chi_square = float(min(b, c)) 
        k = min(b, c)
        p_value_one_tailed = 0.0
        for i in range(k + 1):
            p_value_one_tailed += math.comb(total, i) * (0.5 ** total)
        p_value = min(1.0, 2.0 * p_value_one_tailed) 
        
    else: 
        if correction == True:
            # Dùng Chi-square có hiệu chỉnh Yates
            adjusted_diff = diff - 1.0 
            chi_square = (adjusted_diff ** 2) / total
        else:
            # Dùng Chi-square tiêu chuẩn (Không hiệu chỉnh)
            chi_square = (diff ** 2) / total
            
        p_value = 1.0 - math.erf(math.sqrt(chi_square / 2.0))
        
    return chi_square, p_value, [[a, b], [c, d]]

# ---------------------------------------------------------
# 2. KIỂM THỬ VÀ SO SÁNH
# ---------------------------------------------------------
# Tạo dữ liệu giả lập (Output của 2 mô hình phân loại)
# Cố tình tạo b + c < 25 để test hiệu chỉnh Yates
y_pred_model_A = [1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
y_pred_model_B = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1]

# Chạy hàm custom
custom_chi, custom_p, contingency_table = custom_mcnemar(y_pred_model_A, y_pred_model_B, exact=False, correction=True)

# Chạy thư viện Statsmodels
# exact=False: Ép dùng Chi-square thay vì Binomial
# correction=True: Bật hiệu chỉnh Yates (- 0.5)
lib_result = mcnemar(contingency_table, exact=False, correction=True)

# ---------------------------------------------------------
# 3. IN KẾT QUẢ ĐỐI CHIẾU
# ---------------------------------------------------------
print("--- KẾT QUẢ HÀM TỰ CODE ---")
print(f"Chi-square: {custom_chi:.5f}")
print(f"P-value:    {custom_p:.5f}")
print("-" * 30)
print("--- KẾT QUẢ TỪ THƯ VIỆN STATSMODELS ---")
print(f"Chi-square: {lib_result.statistic:.5f}")
print(f"P-value:    {lib_result.pvalue:.5f}")
print("-" * 30)

# Kiểm tra xem kết quả có khớp nhau hoàn toàn không
if abs(custom_chi - lib_result.statistic) < 1e-5 and abs(custom_p - lib_result.pvalue) < 1e-5:
    print("✅ XÁC NHẬN: Code của bạn khớp 100% với thư viện chuẩn!")
else:
    print("❌ CÓ SAI LỆCH")