import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from io import BytesIO
import tensorflow as tf
from database import init_db, get_price, add_scan, get_history, clear_history, get_stats
from ui import apply_custom_ui

# ── DepthwiseConv2D Patch ──
from tensorflow.python.keras.layers import DepthwiseConv2D
_orig_init = DepthwiseConv2D.__init__
def _patched_init(self, *args, **kwargs):
    kwargs.pop('groups', None)
    _orig_init(self, *args, **kwargs)
DepthwiseConv2D.__init__ = _patched_init

# ── Init ──
init_db()
apply_custom_ui()

# ── Model Load ──
@st.cache_resource
def load_resources():
    try:
        model = tf.keras.models.load_model("keras_model.h5", compile=False)
        with open("labels.txt", "r") as f:
            # ✅ FIX: Correct parse — "0 Surf Excel" → "Surf Excel" (10+ classes ke liye bhi kaam karta hai)
            labels = []
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(" ", 1)
                    if len(parts) == 2:
                        labels.append(parts[1].strip())
        return model, labels
    except Exception as e:
        return None, None

model, class_names = load_resources()

# ── Header ──
st.markdown("""
<div class="header-card">
    <h1>Vision-Mart AI</h1>
    <p>Smart Product Recognition System</p>
</div>
""", unsafe_allow_html=True)

# ── Stats Row ──
total_scans, total_value = get_stats()
unique = len(set(item[0] for item in get_history(limit=1000)))

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{total_scans}</div>
        <div class="stat-label">Total Scans</div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">Rs. {int(total_value)}</div>
        <div class="stat-label">Total Value</div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{unique}</div>
        <div class="stat-label">Unique Products</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Layout ──
col1, col2 = st.columns([1, 1], gap="medium")

# ── Left: Scan Area ──
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Scan Area</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Camera", "Upload Image"])
    img_file = None

    with tab1:
        camera_img = st.camera_input(" ")
        if camera_img:
            img_file = camera_img

    with tab2:
        uploaded_img = st.file_uploader(
            "Select image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if uploaded_img:
            # ✅ FIX: bytes ek baar read karo — display aur model dono ke liye
            img_bytes = uploaded_img.read()
            st.image(img_bytes, use_container_width=True)
            img_file = BytesIO(img_bytes)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Right: Analysis ──
with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

    if model is None:
        st.markdown('<div class="error-box">Model load nahi ho saka. keras_model.h5 check karein.</div>', unsafe_allow_html=True)

    elif img_file is not None:
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(img_file).convert("RGB")
        image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        with st.spinner("Analyzing..."):
            prediction = model.predict(data)
            index = np.argmax(prediction)
            # ✅ FIX: class_names already correctly parsed — direct use karein
            product_name = class_names[index]
            confidence_score = float(prediction[0][index])

        if confidence_score > 0.7:
            price = get_price(product_name)
            price_display = f"Rs. {int(price)}" if price is not None else "Price set nahi hai"
            price_val = price if price is not None else 0

            add_scan(product_name, price_val, round(confidence_score * 100))

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Detected Product</div>
                <div class="result-name">{product_name}</div>
                <div class="result-confidence">Confidence: {round(confidence_score * 100)}%</div>
                <div class="result-price">{price_display}</div>
            </div>
            """, unsafe_allow_html=True)

            if price is None:
                st.markdown('<div class="warn-box">Is product ki price set nahi hai. Admin Panel mein jaa kar price set karein.</div>', unsafe_allow_html=True)

            st.markdown('<div class="prob-title">All Predictions</div>', unsafe_allow_html=True)
            for i, label in enumerate(class_names):
                prob = float(prediction[0][i])
                pct = round(prob * 100)
                is_top = "top" if i == index else ""
                st.markdown(f"""
                <div class="prob-row">
                    <div class="prob-label">{label}</div>
                    <div class="prob-bar-bg">
                        <div class="prob-bar-fill {is_top}" style="width:{pct}%"></div>
                    </div>
                    <div class="prob-percent">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="warn-box">Confidence kam hai. Product ko qareeb aur clear rakhein.</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="info-box">Camera se photo lein ya image upload karein.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Scan History ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Scan History</div>', unsafe_allow_html=True)

history = get_history()

if history:
    if st.button("Clear History"):
        clear_history()
        st.rerun()

    st.markdown("""
    <div class="history-header">
        <span style="flex:2">Product</span>
        <span style="flex:1">Confidence</span>
        <span style="flex:1">Price</span>
        <span style="flex:1">Time</span>
    </div>
    """, unsafe_allow_html=True)

    for item in history:
        product, price, confidence, scanned_at = item
        time_str = scanned_at[11:16] if scanned_at else "--"
        price_str = f"Rs. {int(price)}" if price else "--"
        st.markdown(f"""
        <div class="history-row">
            <span style="flex:2; color:#c9d1d9;">{product}</span>
            <span style="flex:1; color:#3fb950;">{confidence}%</span>
            <span style="flex:1; color:#a5d6ff;">{price_str}</span>
            <span style="flex:1; color:#484f58;">{time_str}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="info-box">Abhi koi scan nahi kiya.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    Shoukat Ali &nbsp;|&nbsp; AI & ML Specialist &nbsp;|&nbsp;
    <a href="/admin" target="_self" style="color:#a5d6ff; text-decoration:none;">Admin Panel</a>
</div>
""", unsafe_allow_html=True)
