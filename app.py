import streamlit as st
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Pithampur Property Portal", layout="wide", page_icon="🏢")

# Direct Data inside Code (Everything controllable via Admin Panel)
if 'db_data' not in st.session_state:
    st.session_state.db_data = {
        "Dream City (Kalibillod)": {
            "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6", # Admin panel se change ho jayegi
            "location_text": "Near Pithampur Industrial Area, Kalibillod, Madhya Pradesh",
            "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3684.0759328224095!2d75.6395155!3d22.6453!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjLCbDM4JzQzLjEiTiA3NSczOCcyMi4zIkU!5e0!3m2!1sen!2sin!4v1721500000000!5m2!1sen!2sin",
            "map_link": "https://maps.google.com/?q=22.6453,75.6421",
            "video_url": "",  # YouTube link yahan aayega
            "plots": [
                {"no": "24", "size": "1037 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "90", "size": "1200 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "95", "size": "1200 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "101", "size": "1212 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "103", "size": "400 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "104", "size": "400 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "105", "size": "1200 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "106", "size": "1200 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "112", "size": "835 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "113", "size": "815 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "117", "size": "1435 sqft", "status": "Available", "price": "Call for Price"},
                {"no": "140", "size": "1581 sqft", "status": "Available", "price": "Call for Price"}
            ]
        }
    }

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
        st.sidebar.success("Welcome back! Aap control panel me hain.")
        
        st.sidebar.subheader("🔄 Update Details")
        colony_to_edit = st.sidebar.selectbox("Colony Chunein:", list(db_data.keys()))
        
        if colony_to_edit:
            # Main Banner Image Update
            current_image = db_data[colony_to_edit].get("image", "")
            updated_image = st.sidebar.text_input("Colony Image Link (URL):", current_image)
            
            # Video URL Update
            current_video = db_data[colony_to_edit].get("video_url", "")
            updated_video = st.sidebar.text_input("Colony Video Link (YouTube URL):", current_video)
            
            if st.sidebar.button("Save Media Updates"):
                db_data[colony_to_edit]["image"] = updated_image
                db_data[colony_to_edit]["video_url"] = updated_video
                st.sidebar.success("Media successfully update ho gaya!")
                st.rerun()
                
            st.sidebar.write("---")
            # Plot Status Update
            plots_list = [p["no"] for p in db_data[colony_to_edit]["plots"]]
            plot_to_edit = st.sidebar.selectbox("Plot No Chunein:", plots_list)
            new_status = st.sidebar.selectbox("Naya Status Chunein:", ["Available", "Booked", "Sold"])
            
            if st.sidebar.button("Update Plot Status"):
                for plot in db_data[colony_to_edit]["plots"]:
                    if plot["no"] == plot_to_edit:
                        plot["status"] = new_status
                        break
                st.sidebar.success(f"Plot {plot_to_edit} ab {new_status} ho gaya hai!")
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
            st.image(data["image"], use_container_width=True)
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

        # Live Video Section
        video_url = colony_data.get("video_url", "")
        if video_url:
            st.subheader("📺 Colony Real Site Video View")
            st.video(video_url)
            st.write("---")

        col_left, col_right = st.columns([1, 1.2])

        with col_left:
            st.subheader("🗺️ Location Map")
            st.components.v1.iframe(colony_data["map_embed_url"], height=350)
            
            st.markdown(f'''
                <a href="{colony_data['map_link']}" target="_blank">
                    <button style="width: 100%; background-color: #4285F4; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold;">📍 Open in Google Maps (Navigation)</button>
                </a>
            ''', unsafe_allow_html=True)

        with col_right:
            st.subheader("🟢 Live Plot Layout Grid (White Blocks)")
            plot_cols = st.columns(3)
            for idx, plot in enumerate(colony_data["plots"]):
                if plot["status"] == "Available":
                    bg_color = "#2ecc71"
                    text_color = "white"
                elif plot["status"] == "Booked":
                    bg_color = "#f1c40f"
                    text_color = "black"
                else:
                    bg_color = "#e74c3c"
                    text_color = "white"

                with plot_cols[idx % 3]:
                    st.markdown(
                        f"""
                        <div style="background-color: {bg_color}; color: {text_color}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 10px;">
                            <h4 style="margin:0;">Plot {plot['no']}</h4>
                            <p style="margin:5px 0 0 0; font-size:13px;">Size: {plot['size']}</p>
                            <p style="margin:2px 0 0 0; font-weight:bold;">{plot['price']}</p>
                            <span style="font-size:11px; background: rgba(0,0,0,0.15); padding: 2px 5px; border-radius:3px;">{plot['status']}</span>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

        # Contact Section
        st.write("---")
        st.subheader("📞 Interested in this Property?")
        
        whatsapp_number = "+919876543210" # WhatsApp number daal dena
        custom_message = f"Hello! Mujhe '{colony_name}' me plot no. ki enquiry karni hai."
        encoded_message = urllib.parse.quote(custom_message)
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 18px; cursor: pointer; font-weight: bold;">💬 Chat on WhatsApp</button></a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a href="tel:{whatsapp_number}"><button style="width: 100%; background-color: #1a1a1a; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 18px; cursor: pointer; font-weight: bold;">📞 Call Agent Now</button></a>', unsafe_allow_html=True)
    else:
        st.error("Colony not found.")
