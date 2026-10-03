import streamlit as st
st.image("logo.jpg")
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Công cụ tính lãi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f7f9fc;
        border: 1px solid #e5e7eb;
        text-align: center;
    }

    .result-title {
        font-size: 16px;
        color: #666;
    }

    .result-value {
        font-size: 25px;
        font-weight: 700;
        margin-top: 8px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<div class="main-title">💰 CÔNG CỤ TÍNH LÃI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Tính lãi đơn và lãi kép cho khoản tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# =========================
# NHẬP THÔNG TIN
# =========================
st.markdown(
    '<div class="section-title">📋 Thông tin khoản tiền gửi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

with col2:
    hinh_thuc_nhan_lai = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    loai_lai = st.radio(
        "🧮 Phương pháp tính",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        horizontal=True
    )

    st.info(
        "💡 Lãi suất được nhập theo %/năm. "
        "Kỳ hạn được tính theo số tháng."
    )


# =========================
# NÚT TÍNH
# =========================
st.markdown("---")

calculate = st.button(
    "🧮 TÍNH TIỀN LÃI",
    type="primary",
    use_container_width=True
)


# =========================
# TÍNH TOÁN
# =========================
if calculate:

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Số kỳ nhận lãi
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_thang_moi_ky = 1
    elif hinh_thuc_nhan_lai == "Hàng quý":
        so_thang_moi_ky = 3
    else:
        so_thang_moi_ky = ky_han

    # =========================
    # TẠO CÁC KỲ TÍNH
    # =========================
    if hinh_thuc_nhan_lai == "Cuối kỳ":
        cac_ky = [ky_han]
    else:
        cac_ky = list(
            range(
                so_thang_moi_ky,
                ky_han + 1,
                so_thang_moi_ky
            )
        )

        # Nếu kỳ hạn không chia hết cho số tháng/kỳ
        if cac_ky[-1] != ky_han:
            cac_ky.append(ky_han)

    # =========================
    # TÍNH LÃI
    # =========================
    bang_du_lieu = []

    tong_lai = 0
    gia_tri_tai_dau_ky = tien_gui

    thang_truoc = 0

    for index, thang_hien_tai in enumerate(cac_ky, start=1):

        so_thang_trong_ky = thang_hien_tai - thang_truoc

        # Lãi suất của kỳ
        lai_suat_ky = lai_suat_nam * (so_thang_trong_ky / 12)

        # ---------------------------------
        # LÃI ĐƠN
        # ---------------------------------
        if loai_lai == "Lãi đơn":

            tien_lai_ky = tien_gui * lai_suat_ky
            gia_tri_cuoi_ky = gia_tri_tai_dau_ky + tien_lai_ky

        # ---------------------------------
        # LÃI KÉP
        # ---------------------------------
        else:

            gia_tri_cuoi_ky = (
                gia_tri_tai_dau_ky *
                (1 + lai_suat_ky)
            )

            tien_lai_ky = gia_tri_cuoi_ky - gia_tri_tai_dau_ky

        # =========================
        # XỬ LÝ NHẬN LÃI
        # =========================

        if loai_lai == "Lãi kép":

            # Với lãi kép, tiền lãi được nhập vào vốn
            # để tiếp tục sinh lãi ở kỳ tiếp theo.
            gia_tri_tai_dau_ky = gia_tri_cuoi_ky

        else:

            # Lãi đơn: vốn gốc không thay đổi
            gia_tri_tai_dau_ky = tien_gui

        tong_lai += tien_lai_ky

        bang_du_lieu.append({
            "Kỳ": index,
            "Thời điểm": f"Tháng {thang_hien_tai}",
            "Tiền đầu kỳ": gia_tri_tai_dau_ky
                if loai_lai == "Lãi kép"
                else tien_gui,
            "Tiền lãi kỳ này": tien_lai_ky,
            "Tổng lãi lũy kế": tong_lai
        })

        thang_truoc = thang_hien_tai

    # =========================
    # TỔNG TIỀN
    # =========================
    tong_tien = tien_gui + tong_lai


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.markdown(
        '<div class="section-title">📊 Kết quả tính toán</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💵 Tiền gốc</div>
                <div class="result-value">{format_money(tien_gui)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">📈 Tổng tiền lãi</div>
                <div class="result-value">{format_money(tong_lai)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💰 Tổng gốc + lãi</div>
                <div class="result-value">{format_money(tong_tien)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.markdown(
        '<div class="section-title">📝 Thông tin khoản gửi</div>',
        unsafe_allow_html=True
    )

    info_col1, info_col2, info_col3, info_col4 = st.columns(4)

    with info_col1:
        st.metric("Kỳ hạn", f"{ky_han} tháng")

    with info_col2:
        st.metric("Lãi suất", f"{lai_suat:.2f}%/năm")

    with info_col3:
        st.metric("Phương pháp", loai_lai)

    with info_col4:
        st.metric("Nhận lãi", hinh_thuc_nhan_lai)


    # =========================
    # TIỀN LÃI ĐỊNH KỲ
    # =========================
    st.markdown(
        '<div class="section-title">💸 Tiền lãi định kỳ</div>',
        unsafe_allow_html=True
    )

    if hinh_thuc_nhan_lai == "Cuối kỳ":
        st.success(
            f"Bạn nhận **{format_money(tong_lai)}** tiền lãi "
            f"vào cuối kỳ."
        )

    else:
        # Tính lãi kỳ chuẩn
        if loai_lai == "Lãi đơn":
            lai_dinh_ky = (
                tien_gui *
                lai_suat_nam *
                (so_thang_moi_ky / 12)
            )

            if hinh_thuc_nhan_lai == "Hàng tháng":
                text_ky = "mỗi tháng"
            else:
                text_ky = "mỗi quý"

            st.success(
                f"Tiền lãi **{text_ky}**: "
                f"**{format_money(lai_dinh_ky)}**"
            )

        else:
            # Với lãi kép, hiển thị lãi của kỳ đầu tiên
            lai_ky_dau = bang_du_lieu[0]["Tiền lãi kỳ này"]

            if hinh_thuc_nhan_lai == "Hàng tháng":
                text_ky = "tháng đầu tiên"
            else:
                text_ky = "quý đầu tiên"

            st.success(
                f"Tiền lãi **{text_ky}**: "
                f"**{format_money(lai_ky_dau)}**. "
                f"Do lãi kép, tiền lãi các kỳ sau sẽ thay đổi."
            )


    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.markdown(
        '<div class="section-title">📋 Chi tiết từng kỳ</div>',
        unsafe_allow_html=True
    )

    df = pd.DataFrame(bang_du_lieu)

    # Định dạng tiền
    df["Tiền đầu kỳ"] = df["Tiền đầu kỳ"].apply(format_money)
    df["Tiền lãi kỳ này"] = df["Tiền lãi kỳ này"].apply(format_money)
    df["Tổng lãi lũy kế"] = df["Tổng lãi lũy kế"].apply(format_money)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # =========================
    # CÔNG THỨC
    # =========================
    st.markdown(
        '<div class="section-title">📐 Công thức sử dụng</div>',
        unsafe_allow_html=True
    )

    if loai_lai == "Lãi đơn":

        st.latex(
            r"I = P \times r \times t"
        )

        st.write(
            "Trong đó:"
        )

        st.write(
            "- **I**: Tiền lãi\n"
            "- **P**: Tiền gốc ban đầu\n"
            "- **r**: Lãi suất năm\n"
            "- **t**: Thời gian gửi tính theo năm"
        )

    else:

        st.latex(
            r"A = P(1+r)^n"
        )

        st.write(
            "Trong đó:"
        )

        st.write(
            "- **A**: Tổng số tiền nhận được\n"
            "- **P**: Tiền gốc ban đầu\n"
            "- **r**: Lãi suất mỗi kỳ\n"
            "- **n**: Số kỳ tính lãi"
        )


    # =========================
    # GHI CHÚ
    # =========================
    st.markdown("---")

    st.caption(
        "⚠️ Đây là công cụ tính toán tham khảo. "
        "Lãi suất thực tế của ngân hàng có thể áp dụng quy tắc "
        "tính ngày, số ngày trong năm, cách làm tròn và điều kiện "
        "nhận lãi khác nhau."
    )
else:
    st.info(
        "👆 Nhập thông tin khoản tiền gửi ở phía trên "
        "và nhấn **TÍNH TIỀN LÃI** để xem kết quả."
    )
