import streamlit as st
import urllib.parse
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Pithampur Property Portal", layout="wide", page_icon="🏢")

# Initializing Database & Leads in Session State
if 'db_data' not in st.session_state:
    st.session_state.db_data = {
        "Dream City (Kalibillod)": {
            "images": [
                "https://images.unsplash.com/photo-1564013799919-ab600027ffc6",
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c"
            ],
            "location_text": "Near Pithampur Industrial Area, Kalibillod, Madhya Pradesh",
            "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3684.0759328224095!2d75.6395155!3d22.6453!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjLCbDM3JzQzLjEiTiA3NSczOCcyMi4zIkU!5e0!3m2!1sen!2sin!4v1721500000000!5m2!1sen!2sin",
            "map_link": "https://maps.google.com/?q=22.6453,75.6421",
            "videos": [],
            "plots": [
                {"no": "24", "size": "1037 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "90", "size": "1200 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "95", "size": "1200 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "101", "size": "1212 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "103", "size": "400 sqft", "status": "Available", "price": "Call for Price"}
            ]
        }
    }

if 'leads' not in st.session_state:
    st.session_state.leads = []

db_data = st.session_state.db_data

# Navigation State Manager
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# ----------------- SIDEBAR ADMIN PANEL -----------------
st.sidebar.title("🔐 Owner Control Panel")
admin_mode = st.sidebar.checkbox("Admin Mode On Karein")

if admin_mode:
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password == "admin123":
        st.sidebar.success("Welcome! Aap control panel me hain.")
        
        # --- NEW SECTION: CUSTOMER LEADS ---
        st.sidebar.subheader("📊 Customer Leads (Enquiries)")
        if not st.session_state.leads:
            st.sidebar.info("Abhi koi nayi lead nahi aayi hai.")
        else:
            for idx, lead in enumerate(st.session_state.leads):
                st.sidebar.markdown(f"""
                **Lead #{idx+1}**
                * 👤 **Naam:** {lead['name']}
                * 📞 **Phone:** {lead['phone']}
                * 📍 **Colony:** {lead['colony']}
                * 🕒 **Time:** {lead['time']}
                ---
                """)
        
        st.sidebar.write("---")
        # --- MEDIA & PLOT UPDATES ---
        st.sidebar.subheader("🔄 Update Details")
        colony_to_edit = st.sidebar.selectbox("Colony Chunein:", list(db_data.keys()))
        
        if colony_to_edit:
            current_images = ", ".join(db_data[colony_to_edit].get("images", []))
            updated_images = st.sidebar.text_area("Colony Images (Comma separated):", current_images)
            current_videos = ", ".join(db_data[colony_to_edit].get("videos", []))
            updated_videos = st.sidebar.text_area("Colony Videos (Comma separated):", current_videos)
            
            if st.sidebar.button("Save Media Updates"):
                db_data[colony_to_edit]["images"] = [img.strip() for img in updated_images.split(",") if img.strip()]
                db_data[colony_to_edit]["videos"] = [vid.strip() for vid in updated_videos.split(",") if vid.strip()]
                st.sidebar.success("Media update ho gaya!")
                st.rerun()
    else:
        if password:
            st.sidebar.error("Wrong Password!")

# ----------------- PAGE 1: USER HOME PAGE -----------------
if st.session_state.current_page == "Home":
    st.title("🏢 Pithampur Property Portal")
    st.subheader("Hamari Active Locations Aur Available Plots")
    st.write("---")

    cols = st.columns(3)
    col_index = 0

    for colony_name, data in db_data.items():
        with cols[col_index % 3]:
            main_img = data["images"][0] if data.get("images") else "https://images.unsplash.com/photo-1564013799919-ab600027ffc6"
            st.image(main_img, use_container_width=True)
            st.subheader(colony_name)
            st.caption(f"📍 {data['location_text']}")
            if st.button(f"View Details ->", key=colony_name):
                st.session_state.current_page = colony_name
                st.rerun()
            st.write("---")
        col_index += 1

# ----------------- PAGE 2: COLONY DETAIL PAGE -----------------
else:
    colony_name = st.session_state.current_page
    if colony_name in db_data:
        colony_data = db_data[colony_name]

        if st.button("⬅️ Back to Home"):
            st.session_state.current_page = "Home"
            st.rerun()

        st.title(f"📍 {colony_name}")
        st.write(f"**Location:** {colony_data['location_text']}")
        st.write("---")

        # Media Sections (Photos & Videos)
        images_list = colony_data.get("images", [])
        if images_list:
            st.subheader("🖼️ Site Photos Gallery")
            selected_img = st.select_slider("Photos slide karein", options=list(range(1, len(images_list) + 1)))
            st.image(images_list[selected_img - 1], use_container_width=True)
            st.write("---")

        videos_list = colony_data.get("videos", [])
        if videos_list:
            st.subheader("📺 Colony Real Site Video Views")
            v_cols = st.columns(2)
            for v_idx, v_url in enumerate(videos_list):
                with v_cols[v_idx % 2]:
                    st.video(v_url)
            st.write("---")

        # Map and Grid Layout
        col_left, col_right = st.columns([1, 1.2])
        with col_left:
            st.subheader("🗺️ Location Map")
            st.components.v1.iframe(colony_data["map_embed_url"], height=350)

        with col_right:
            st.subheader("🟢 Live Plot Layout Grid")
            plot_cols = st.columns(3)
            for idx, plot in enumerate(colony_data["plots"]):
                with plot_cols[idx % 3]:
                    st.markdown(f"""
                        <div style="background-color: #2ecc71; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px;">
                            <h4 style="margin:0;">Plot {plot['no']}</h4>
                            <p style="margin:5px 0 0 0; font-size:13px;">Size: {plot['size']}</p>
                            <span style="font-size:11px; background: rgba(0,0,0,0.15); padding: 2px 5px; border-radius:3px;">{plot['status']}</span>
                        </div>
                        """, unsafe_allow_html=True)

        # --- THE TRUST-BASED LEAD FORM ---
        st.write("---")
        st.subheader("📞 Request Site Visit / Callback")
        st.write("Agar aap is property me interested hain, toh apni details chhodein. Hamari team aapse turant baat karegi.")
        
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            c_name = st.text_input("Aapka Naam (Full Name)", placeholder="Eg. Rahul Sharma")
            c_phone = st.text_input("Mobile Number", placeholder="Eg. 98765xxxxx")
            
            if st.button("Submit Callback Request 📩"):
                if c_name and c_phone:
                    # Save lead locally
                    new_lead = {
                        "name": c_name,
                        "phone": c_phone,
                        "colony": colony_name,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.leads.append(new_lead)
                    st.success("✅ Aapki request submit ho gayi hai! Hum jald hi aapse sampark karenge.")
                else:
                    st.error("Kripya Naam aur Mobile Number dono bharein!")

        # Direct Actions
        st.write("---")
        whatsapp_number = "+919876543210" # Apna real number yahan daal dena bhai
        custom_message = f"Hello! Mujhe '{colony_name}' me plots ki enquiry karni hai."
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={urllib.parse.quote(custom_message)}"
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 18px; cursor: pointer; font-weight: bold;">💬 Direct Chat on WhatsApp</button></a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a href="tel:{whatsapp_number}"><button style="width: 100%; background-color: #1a1a1a; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 18px; cursor: pointer; font-weight: bold;">📞 Direct Call Now</button></a>', unsafe_allow_html=True)
