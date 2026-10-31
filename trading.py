import streamlit as st

st.set_page_config(
    page_title="Kalkulator Entry Spot",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 Spot Entry Calculator")
st.caption("Target Rasio SL -10% & TP +30% dari Modal Per Trade (Spot / No Leverage)")

# --- Input Parameter ---
col_modal1, col_modal2 = st.columns(2)
with col_modal1:
    modal_per_trade = st.number_input(
        "Modal Sekali Trade ($)",
        min_value=1.0,
        value=10.0,
        step=10.0,
        format="%.2f",
        help="Basis modal awal yang dijadikan patokan -10% / +30%"
    )
with col_modal2:
    saldo_usdt = st.number_input(
        "Saldo USDT Cadangan ($)",
        min_value=0.0,
        value=50.0,
        step=10.0,
        format="%.2f",
        help="Saldo menganggur yang siap dipakai menambah entry"
    )

col_pct1, col_pct2 = st.columns(2)
with col_pct1:
    sl_teknikal = st.number_input(
        "Jarak SL Aset (%)",
        min_value=0.1,
        max_value=100.0,
        value=3.5,
        step=0.5,
        help="Titik Stop Loss dari harga beli"
    )
with col_pct2:
    tp_teknikal = st.number_input(
        "Jarak TP Aset (%)",
        min_value=0.1,
        value=10.5,
        step=0.5,
        help="Titik Take Profit dari harga beli"
    )

st.divider()

if modal_per_trade > 0 and sl_teknikal > 0:
    # 1. Target Nominal Kerugian (10% dari modal sekali trade)
    target_rugi_nominal = modal_per_trade * 0.10

    # 2. Total Entry yang dibutuhkan
    total_entry = target_rugi_nominal / (sl_teknikal / 100.0)

    # 3. Kebutuhan Tambahan Saldo
    tambahan_saldo = total_entry - modal_per_trade

    # Output Utama
    st.metric(
        label="Total Entry yang Harus Dipasang",
        value=f"${total_entry:,.2f}"
    )

    # Evaluasi Ketersediaan Modal
    total_dana_tersedia = modal_per_trade + saldo_usdt

    if tambahan_saldo > 0:
        if tambahan_saldo <= saldo_usdt:
            st.success(
                f"**Kesimpulan:** Ambil tambahan dari saldo USDT sebesar **\${tambahan_saldo:,.2f}** "
                f"(Sisa cadangan USDT: **\${saldo_usdt - tambahan_saldo:,.2f}**)."
            )
        else:
            kekurangan = tambahan_saldo - saldo_usdt
            st.error(
                f"**Kesimpulan:** Butuh tambahan **${tambahan_saldo:,.2f}**, tapi saldo USDT cuma ada **${saldo_usdt:,.2f}**. "
                f"Kurang **${kekurangan:,.2f}** lagi agar bisa pasang full entry."
            )
    elif tambahan_saldo == 0:
        st.info("**Kesimpulan:** Pas dengan modal sekali trade ($200), tidak perlu ambil dari saldo cadangan.")
    else:
        st.info(
            f"**Kesimpulan:** Cukup pasang **${total_entry:,.2f}** dari modal per trade. "
            f"Ada sisa modal per trade sebesar **${abs(tambahan_saldo):,.2f}**."
        )

    st.divider()

    # Rincian Validasi Nominal
    st.markdown("### Verifikasi Nominal Trade")
    c1, c2 = st.columns(2)
    with c1:
        rugi_nominal = total_entry * (sl_teknikal / 100.0)
        pct_rugi_modal = (rugi_nominal / modal_per_trade) * 100.0
        st.error(f"**Kalau Kena SL (-{sl_teknikal}%)**")
        st.write(f"Rugi: **-${rugi_nominal:,.2f}**")
        st.write(f"Efek ke modal per trade: **-{pct_rugi_modal:.1f}%**")

    with c2:
        untung_nominal = total_entry * (tp_teknikal / 100.0)
        pct_untung_modal = (untung_nominal / modal_per_trade) * 100.0
        st.success(f"**Kalau Kena TP (+{tp_teknikal}%)**")
        st.write(f"Profit: **+${untung_nominal:,.2f}**")
        st.write(f"Efek ke modal per trade: **+{pct_untung_modal:.1f}%**")

leverage_ekuivalen = 10 / sl_teknikal
st.write(
    f"Besaran Leverage: **<span style='color: #FFD700;'>{leverage_ekuivalen:.1f}x</span>**",
    unsafe_allow_html=True
)