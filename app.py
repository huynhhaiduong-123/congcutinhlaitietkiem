import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Công cụ Tính Lãi Gửi Tiết Kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.write("Ứng dụng tính lãi suất tiết kiệm theo **Lãi Đơn** và **Lãi Kép** với các hình thức nhận lãi khác nhau.")

st.markdown("---")

# --- NHẬP DỮ LIỆU TỪ NGƯỜI DÙNG ---
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "1. Số tiền gửi (VND):",
        min_value=100000,
        value=100000000,
        step=1000000,
        format="%d"
    )
    
    ky_han_thang = st.number_input(
        "2. Kỳ hạn gửi (tháng):",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "3. Lãi suất (%/năm):",
        min_value=0.1,
        max_value=30.0,
        value=6.5,
        step=0.1
    )
    
    hinh_thuc_lanh = st.selectbox(
        "4. Hình thức nhận lãi:",
        options=["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"]
    )

loai_lai = st.radio(
    "5. Phương thức tính lãi:",
    options=["Lãi Đơn", "Lãi Kép"],
    horizontal=True,
    help="Lãi đơn: Tiền lãi định kỳ không nhập vào gốc. Lãi kép: Tiền lãi định kỳ được cộng vào gốc để tính lãi tiếp."
)

st.markdown("---")

# --- XỬ LÝ TÍNH TOÁN ---
def tinh_toan_lai(p, r_nam, t_thang, hinh_thuc, loai):
    r_thang = (r_nam / 100) / 12
    
    # Xác định số kỳ trả lãi (tính theo tháng)
    if hinh_thuc == "Lãnh lãi theo tháng":
        chu_ky = 1
        ten_ky = "tháng"
    elif hinh_thuc == "Lãnh lãi theo quý":
        chu_ky = 3
        ten_ky = "quý"
    else:  # Lãnh lãi cuối kỳ
        chu_ky = t_thang
        ten_ky = f"cuối kỳ ({t_thang} tháng)"
        
    so_ky = t_thang / chu_ky

    # Trường hợp Lãi Đơn
    if loai == "Lãi Đơn":
        tong_tien_lai = p * r_thang * t_thang
        
        if hinh_thuc == "Lãnh lãi theo tháng":
            lai_dinh_ky = p * r_thang * 1
        elif hinh_thuc == "Lãnh lãi theo quý":
            lai_dinh_ky = p * r_thang * 3
        else:
            lai_dinh_ky = tong_tien_lai
            
        tong_goc_va_lai = p + tong_tien_lai

    # Trường hợp Lãi Kép
    else:
        r_ky = r_thang * chu_ky  # Lãi suất theo từng chu kỳ nhận lãi
        tong_goc_va_lai = p * ((1 + r_ky) ** so_ky)
        tong_tien_lai = tong_goc_va_lai - p
        
        if hinh_thuc == "Lãnh lãi cuối kỳ":
            lai_dinh_ky = tong_tien_lai
        else:
            # Lãi kép thì tiền lãi mỗi kỳ sẽ tăng dần, hiển thị trung bình / kỳ
            lai_dinh_ky = tong_tien_lai / so_ky

    return lai_dinh_ky, tong_tien_lai, tong_goc_va_lai, ten_ky, so_ky

# Gọi hàm tính toán
lai_dinh_ky, tong_lai, tong_goc_lai, ten_ky, so_ky = tinh_toan_lai(
    so_tien_gui, lai_suat_nam, ky_han_thang, hinh_thuc_lanh, loai_lai
)

# --- HIỂN THỊ KẾT QUẢ ---
st.subheader("📊 Kết Quả Dự Tính")

res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    if loai_lai == "Lãi Kép" and hinh_thuc_lanh != "Lãnh lãi cuối kỳ":
        st.metric(
            label=f"Lãi trung bình /{ten_ky}:",
            value=f"{lai_dinh_ky:,.0f} VND"
        )
    else:
        st.metric(
            label=f"Tiền lãi định kỳ ({ten_ky}):",
            value=f"{lai_dinh_ky:,.0f} VND"
        )

with res_col2:
    st.metric(
        label="Tổng tiền lãi thu về:",
        value=f"{tong_lai:,.0f} VND"
    )

with res_col3:
    st.metric(
        label="Tổng gốc + lãi nhận được:",
        value=f"{tong_goc_lai:,.0f} VND"
    )

# Ghi chú thêm
if hinh_thuc_lanh != "Lãnh lãi cuối kỳ":
    st.caption(f"* Tổng thời gian gửi gồm **{so_ky:.1f}** chu kỳ nhận lãi ({ten_ky}).")
