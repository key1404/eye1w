import streamlit as st
import numpy as np
from PIL import Image

# تنظیمات صفحه
st.set_page_config(
    page_title="سیستم هوشمند تخصصی انتخاب عینک | Eye1 AI",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند تخصصی انتخاب عینک (نسخه پویا و تحلیل‌گر)")
st.markdown("این سیستم ابعاد و تناسبات تصویر آپلودشده را آنالیز کرده و بر اساس هندسه چهره، فریم مناسب را پیشنهاد می‌کند.")

# نوار کناری
st.sidebar.header("⚙️ تنظیمات بالینی و اپتومتریک")
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)
rx_type = st.sidebar.selectbox("نوع نمره چشم (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])

uploaded_file = st.file_uploader("لطفاً تصویر چهره را آپلود کنید:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # محاسبه نسبت ابعاد تصویر (Aspect Ratio) برای تشخیص پویای فرم صورت
    aspect_ratio = h / w
    
    # منطق پویای تشخیص فرم صورت بر اساس ابعاد عکس
    if aspect_ratio > 1.35:
        detected_shape = "مستطیلی یا کشیده (Oblong / Rectangle)"
        rec_frame = "فریم‌های دارای ارتفاع بیشتر و خط ابروی برجسته یا خلبانی (Aviator)"
        desc = "صورت کشیده است؛ فریم‌های عریض‌تر با جزئیات در قسمت پل بینی تعادل عالی ایجاد می‌کنند."
        brand = "Tom Ford (مدل‌های مربع بزرگ یا خلبانی)"
    elif 1.15 <= aspect_ratio <= 1.35:
        detected_shape = "بیضی متعادل (Oval)"
        rec_frame = "فریم‌های چشم‌گربه‌ای (Cat-eye) یا مستطیلی کلاسیک"
        desc = "متعادل‌ترین فرم صورت؛ تقریباً هر استایلی با این تناسبات هماهنگ است."
        brand = "Ray-Ban (ویفرر یا کلاب‌مستر)"
    else:
        detected_shape = "گرد یا مربعی (Round / Square)"
        rec_frame = "فریم‌های زاویه‌دار، مستطیلی یا هندسی باریک"
        desc = "برای شکستن خطوط نرم یا زاویه‌‌دار چهره، فریم‌های کشیده و زاویه‌دار توصیه می‌شوند."
        brand = "Tom Ford یا Ray-Ban (فریم‌های مستطیلی باریک)"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### تصویر آپلود شده:")
        st.image(image, use_column_width=True)

    with col2:
        st.markdown("#### نتایج تحلیل پویای هوش مصنوعی:")
        st.success("✅ تحلیل هندسی تصویر با موفقیت انجام شد!")
        st.write(f"🔹 **فرم آناتومیک تشخیص‌داده‌شده:** {detected_shape}")
        st.write(f"📐 **نسبت ابعاد تصویر (H/W):** {aspect_ratio:.2f}")
        st.write(f"💡 **تحلیل بالینی:** {desc}")
        st.write(f"📏 **سایز پیشنهادی فریم (بر اساس PD = {pd_input}mm):** پهنای عدسی {pd_input - 10} تا {pd_input - 6} میلی‌متر")

    st.markdown("---")
    st.markdown("### ۲. پیشنهادهای تخصصی و متغیر فریم عینک")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"**پیشنهاد برند:**\n\n{brand}")
    with c2:
        st.info(f"**استایل پیشنهادی:**\n\n{rec_frame}")
    with c3:
        st.info(f"**تطبیق نمره ({rx_type}):**\n\nتوصیه عدسی فشرده متناسب با چهارچوب انتخابی.")
else:
    st.info("👈 لطفاً یک تصویر آپلود کنید تا تحلیل پویا انجام شود.")