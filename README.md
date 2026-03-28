Vision-Mart AI: Smart Product Recognition & Inventory System
<div align="center">
<img src="https://cdn-icons-png.flaticon.com/512/3081/3081648.png" width="120">
<h1>Vision-Mart AI</h1>
<p><b>Real-time Product Recognition (Mobile-Ready) + Automated Pricing & Inventory</b></p>
</div>

<div align="center">
<a href="#">
<img src="https://img.shields.io/badge/Hugging%20Face-Coming%20Soon-yellow?style=for-the-badge&logo=huggingface" alt="Live App">
</a>
<a href="#">
<img src="https://img.shields.io/badge/Streamlit-Deployment%20Pending-ff4b4b?style=for-the-badge&logo=streamlit" alt="Streamlit App">
</a>
<a href="#">
<img src="https://img.shields.io/badge/Status-Development%20Phase-blue?style=for-the-badge&logo=github" alt="Status">
</a>
</div>

Executive Summary
Vision-Mart AI ek cutting-edge computer vision solution hai jo retail products ko foran pehchanta hai aur unki prices database se fetch karta hai. Ye system khas tor par Mobile users ke liye design kiya gaya hai taake shop owners camera scan ke zariye inventory aur billing manage kar sakein.

Key Strategic Features
Real-time Recognition: TensorFlow aur Keras-based model jo products ko accurate labels ke saath classify karta hai.

Dynamic Database: SQLite integration jo har scan ki history, confidence level, aur total value track karti hai.

Admin Control: Secure Admin Panel jahan se products ki prices aur details update ki ja sakti hain.

UI/UX: Premium CSS-based dark theme jo mobile browser par ek asli app jaisa experience deti hai.

System Architecture
A. Computer Vision Layer
Model MobileNetV2 architecture par mabni hai jo low-power devices par bhi fast inference deta hai.

Image Processing: PIL (Pillow) aur ImageOps ke zariye images ko 224x224 dimensions mein normalize kiya jata hai.

Confidence Threshold: System sirf 70% se upar ki predictions ko valid maanta hai taake accuracy barkaraar rahe.

B. Data & Security Layer
Database: Persistent SQLite storage jo visionmart.db mein scans aur admin credentials save karta hai.

Auth: Admin login ke liye SHA-256 hashing use ki gayi hai taake security compromise na ho.

Technical Specifications
Frontend Framework: Streamlit (Layout: Wide, Theme: Dark).

Deep Learning: TensorFlow 2.x with Keras-model integration.

Language: Python 3.9+.

Key Dependencies: tensorflow, streamlit, pillow, numpy, sqlite3.

Repository Breakdown
app.py: Main execution engine aur scanner logic.

admin.py: Management dashboard for product and price control.

database.py: SQL logic aur authentication functions.

ui.py: Custom CSS components aur premium styling logic.

keras_model.h5: Trained AI model file.

Final Conclusion
Vision-Mart AI retail automation ki taraf ek bada kadam hai. Ye sirf ek scanner nahi balkay ek complete business intelligence tool hai jo sales history aur product performance ko track karne mein madad deta hai.

Developed by Shoukat Ali | AI Engineer & Data Analyst Specializing in Scalable Intelligent Systems.