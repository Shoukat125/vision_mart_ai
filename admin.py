import streamlit as st
from database import (init_db, admin_exists, signup_admin, login_admin,
                      get_security_question, verify_security_answer,
                      reset_password, get_username,
                      get_all_products, save_product)
from ui import apply_custom_ui

init_db()
apply_custom_ui()

SECURITY_QUESTIONS = [
    "What is your date of birth?",
    "Which city were you born?",
    "What is your favorite product?"
]

# ── Session State ──
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

# ── Header ──
st.markdown("""
<div class="header-card">
    <h1>Vision-Mart AI</h1>
    <p>Admin Panel</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════
# NOT LOGGED IN
# ════════════════════════════════
if not st.session_state.admin_logged_in:

    _, col, _ = st.columns([1, 1.2, 1])

    with col:

        # ── SIGNUP ──
        if not admin_exists() or st.session_state.auth_page == "signup":
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Create Admin Account</div>', unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Username likhein")
            password = st.text_input("Password", type="password", placeholder="Password likhein")
            confirm  = st.text_input("Confirm Password", type="password", placeholder="Password dobara likhein")
            question = st.selectbox("Security Question", SECURITY_QUESTIONS)
            answer   = st.text_input("Answer", placeholder="Security question ka jawab")

            if st.button("Create Account"):
                if not username or not password or not answer:
                    st.markdown('<div class="warn-box">Sab fields fill karein.</div>', unsafe_allow_html=True)
                elif password != confirm:
                    st.markdown('<div class="warn-box">Passwords match nahi kar rahe.</div>', unsafe_allow_html=True)
                elif len(password) < 6:
                    st.markdown('<div class="warn-box">Password kam az kam 6 characters ka hona chahiye.</div>', unsafe_allow_html=True)
                else:
                    if signup_admin(username, password, question, answer):
                        st.success("Account ban gaya! Ab login karein.")
                        st.session_state.auth_page = "login"
                        st.rerun()
                    else:
                        st.markdown('<div class="error-box">Account banana failed. Username already exist karta hai.</div>', unsafe_allow_html=True)

            if admin_exists():
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Back to Login"):
                    st.session_state.auth_page = "login"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ── RESET STEP 1 ──
        elif st.session_state.auth_page == "reset_step1":
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Reset Password</div>', unsafe_allow_html=True)

            username_input = st.text_input("Username", placeholder="Apna username likhein")

            if st.button("Next"):
                question = get_security_question(username_input)
                if question:
                    st.session_state.reset_username = username_input
                    st.session_state.reset_question = question
                    st.session_state.auth_page = "reset_step2"
                    st.rerun()
                else:
                    st.markdown('<div class="error-box">Username nahi mila.</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Login"):
                st.session_state.auth_page = "login"
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ── RESET STEP 2 ──
        elif st.session_state.auth_page == "reset_step2":
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Reset Password</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-box" style="text-align:left; margin-bottom:12px;">
                {st.session_state.reset_question}
            </div>
            """, unsafe_allow_html=True)

            answer_input     = st.text_input("Answer", placeholder="Apna jawab likhein")
            new_password     = st.text_input("New Password", type="password", placeholder="Naya password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Password dobara likhein")

            if st.button("Reset Password"):
                if not answer_input or not new_password:
                    st.markdown('<div class="warn-box">Sab fields fill karein.</div>', unsafe_allow_html=True)
                elif new_password != confirm_password:
                    st.markdown('<div class="warn-box">Passwords match nahi kar rahe.</div>', unsafe_allow_html=True)
                elif len(new_password) < 6:
                    st.markdown('<div class="warn-box">Password kam az kam 6 characters ka hona chahiye.</div>', unsafe_allow_html=True)
                elif verify_security_answer(st.session_state.reset_username, answer_input):
                    reset_password(st.session_state.reset_username, new_password)
                    st.success("Password reset ho gaya! Ab login karein.")
                    st.session_state.auth_page = "login"
                    st.rerun()
                else:
                    st.markdown('<div class="error-box">Galat jawab. Dobara try karein.</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Login"):
                st.session_state.auth_page = "login"
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ── LOGIN ──
        else:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Login</div>', unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Username likhein")
            password = st.text_input("Password", type="password", placeholder="Password likhein")

            if st.button("Login"):
                if login_admin(username, password):
                    st.session_state.admin_logged_in = True
                    st.session_state.logged_username = username
                    st.rerun()
                else:
                    st.markdown('<div class="error-box">Galat username ya password.</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Forgot Password?"):
                st.session_state.auth_page = "reset_step1"
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════
# LOGGED IN — ADMIN PANEL
# ════════════════════════════════
else:
    # ── Top Bar ──
    col_name, col_logout = st.columns([4, 1])
    with col_name:
        username = st.session_state.get("logged_username", "Admin")
        st.markdown(f'<p style="color:#8b949e; font-size:0.78rem; margin:0;">Logged in as <b style="color:#a5d6ff;">{username}</b></p>', unsafe_allow_html=True)
    with col_logout:
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.session_state.auth_page = "login"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Set Product Price ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Set Product Price</div>', unsafe_allow_html=True)

    try:
        with open("labels.txt", "r") as f:
            # ✅ FIX: Correct parse — works for 10+ classes too
            labels = []
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(" ", 1)
                    if len(parts) == 2:
                        name = parts[1].strip()
                        # ✅ FIX: "Background" typo filter — skip background class
                        if "background" not in name.lower() and "backgroud" not in name.lower():
                            labels.append(name)
    except:
        labels = []

    if labels:
        selected_product = st.selectbox("Product", labels, label_visibility="collapsed")
        existing = dict(get_all_products())
        current_price = existing.get(selected_product, 0.0)

        new_price = st.number_input(
            "Price (Rs.)",
            min_value=0.0,
            value=float(current_price),
            step=1.0,
            label_visibility="collapsed",
            placeholder="Price Rs. mein"
        )

        if st.button("Save Price"):
            save_product(selected_product, new_price)
            st.success(f"{selected_product} — Rs. {int(new_price)} saved!")
    else:
        st.markdown('<div class="error-box">labels.txt nahi mili.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── All Products & Prices ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">All Products & Prices</div>', unsafe_allow_html=True)

    products = get_all_products()
    if products:
        st.markdown("""
        <div class="history-header">
            <span style="flex:2">Product</span>
            <span style="flex:1">Price</span>
        </div>
        """, unsafe_allow_html=True)
        for name, price in products:
            st.markdown(f"""
            <div class="history-row">
                <span style="flex:2; color:#c9d1d9;">{name}</span>
                <span style="flex:1; color:#a5d6ff;">Rs. {int(price)}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">Abhi koi price save nahi ki.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div class="footer">
        <a href="/" target="_self" style="color:#a5d6ff; text-decoration:none;">Back to Scanner</a>
        &nbsp;|&nbsp; Shoukat Ali &nbsp;|&nbsp; AI & ML Specialist
    </div>
    """, unsafe_allow_html=True)
