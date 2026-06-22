import streamlit as st
import datetime
import base64
import os

# Import team modules safely
from models import SocialPost
from storage import Storage
from caption import CaptionGenerator
from scheduler import PostScheduler
import regex

# --- 1. CONFIG & SYSTEM ELEVATION ---
st.set_page_config(
    page_title="Social Post Manager", 
    page_icon="📅", 
    layout="wide"
)

# --- 2. MULTI-WEIGHT CUSTOM FONT INJECTION (GILROY PRO BOLD & REGULAR) ---
def inject_system_typography():
    bold_path = "assets/Gilroy-Bold.ttf"
    regular_path = "assets/Gilroy-Regular.ttf"
    css_injection = "<style>"
    
    if os.path.exists(bold_path):
        with open(bold_path, "rb") as f:
            bold_b64 = base64.b64encode(f.read()).decode()
        css_injection += f"""
            @font-face {{
                font-family: 'Gilroy-Bold';
                src: url(data:font/ttf;base64,{bold_b64}) format('truetype');
            }}
        """
    if os.path.exists(regular_path):
        with open(regular_path, "rb") as f:
            regular_b64 = base64.b64encode(f.read()).decode()
        css_injection += f"""
            @font-face {{
                font-family: 'Gilroy-Regular';
                src: url(data:font/ttf;base64,{regular_b64}) format('truetype');
            }}
        """
    css_injection += """
        html, body, h1, h2, h3, strong, button, .stMetric div, 
        div[data-testid="stHeader"] h1, div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h3, .stButton>button p,
        div[data-testid="stFormSubmitButton"] button p {
            font-family: 'Gilroy-Bold', sans-serif !important;
            letter-spacing: -0.02em !important;
            font-weight: 700 !important;
        }
        label, .stTextInput label, .stSelectbox label, .stDateInput label,
        .stTimeInput label, .stTextArea label, .stFileUploader label,
        p[data-testid="stWidgetLabel"], div[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] span, .stTabs [data-baseweb="tab"] div p,
        .stTabs [data-baseweb="tab"] {
            font-family: 'Gilroy-Bold', sans-serif !important;
            letter-spacing: -0.01em !important;
            font-weight: 700 !important;
        }
        input, select, textarea, .stCaption, ::placeholder, div[data-testid="stNotification"] p {
            font-family: 'Gilroy-Regular', sans-serif !important;
            letter-spacing: -0.01em !important;
        }
        p, span { font-family: 'Gilroy-Regular', sans-serif; letter-spacing: -0.01em; }
        input::placeholder, textarea::placeholder { font-family: 'Gilroy-Regular', sans-serif !important; opacity: 0.75; }
        div[data-testid="stFileUploaderDropzone"] button { font-family: 'Gilroy-Bold', sans-serif !important; }
        div[data-testid="stFileUploaderDropzone"] button small,
        div[data-testid="stFileUploaderDropzone"] button span,
        div[data-testid="stFileUploaderDropzone"] button div {
            font-family: 'Gilroy-Bold', sans-serif !important;
            letter-spacing: 0px !important;
        }
    </style>
    """
    st.markdown(css_injection, unsafe_allow_html=True)

inject_system_typography()

# --- 3. THEME LAYOUT INJECTION ---
st.markdown("""
    <style>
        .stButton>button { border-radius: 8px; padding: 0.5rem 1.5rem; }
        div[data-testid="stExpander"] { border: 1px solid rgba(49, 51, 63, 0.1); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 1rem; }
        div[data-testid="metric-container"] { background-color: rgba(49, 51, 63, 0.03); border: 1px solid rgba(49, 51, 63, 0.08); border-radius: 12px; padding: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- 4. ENGINE INITIALIZATION ---
db = Storage()
ai_engine = CaptionGenerator()
scheduler = PostScheduler(storage_instance=db)

if "posts" not in st.session_state:
    st.session_state.posts = db.load_posts()
if "draft_caption" not in st.session_state:
    st.session_state.draft_caption = ""
if "media_cache" not in st.session_state:
    st.session_state.media_cache = {}

# --- 5. HEADER ENVIRONMENT ---
col_title, col_logo = st.columns([8, 2], vertical_alignment="center")
with col_title:
    st.title("Social Media Post Manager")
    st.caption("Create, schedule, and manage your social media content pipeline.")
with col_logo:
    try:
        st.image("assets/ncair_logo.png", width=200)
    except Exception:
        st.caption("Logo Asset Missing")

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. SIDEBAR: AI CAPTION ASST ---
with st.sidebar:
    st.markdown("### 🤖 AI Caption Assistant")
    st.caption("Generate captions and hashtag bundles instantly.")
    topic = st.text_input("Topic", placeholder="e.g., new product launch")
    
    if st.button("Generate Caption", use_container_width=True):
        if topic:
            with st.spinner("AI is thinking..."):
                response = ai_engine.generate(topic)
                if "Error:" in response:
                    st.error(response, icon="❌")
                else:
                    st.session_state.draft_caption = response
        else:
            st.toast("⚠️ Enter a topic first.", icon="🔥")
            
    if st.session_state.draft_caption:
        st.markdown("---")
        st.text_area("Generated Caption (Copy this):", value=st.session_state.draft_caption, height=220)
        st.info("Copy this text into the form to fine-tune your post.", icon="ℹ️")

# --- 7. WORKSPACE MODULE ---
tab_create, tab_history = st.tabs(["📝 Create Post", "🗂️ Post History"])

with tab_create:
    with st.container(border=False):
        st.markdown("### Create a New Post")
        with st.form("create_post_form", clear_on_submit=True):
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                title = st.text_input("Post Title", placeholder="Enter post title...")
                platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter/X", "Facebook"])
            with col2:
                sched_date = st.date_input("Scheduled Date", min_value=datetime.date.today())
                sched_time = st.time_input("Scheduled Time")
                
            caption = st.text_area("Caption & Hashtags", placeholder="Paste your AI generated caption here...", height=150)
            uploaded_image = st.file_uploader("Attach Media Asset (Optional)", type=["png", "jpg", "jpeg"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn_1, col_btn_2 = st.columns([7, 3])
            with col_btn_2:
                submit = st.form_submit_button("Save Post", use_container_width=True, type="primary")
            
            if submit:
                str_date = sched_date.strftime("%Y-%m-%d")
                str_time = sched_time.strftime("%H:%M")
                
                try:
                    links_detected = regex.detect_links(caption)
                    hashtags_valid = regex.validate_hashtags(caption)
                    
                    saved_post_obj = scheduler.schedule_post(
                        title=title,
                        caption=caption,
                        platform=platform,
                        date_str=str_date,
                        time_str=str_time,
                        status="Scheduled"
                    )
                    
                    if uploaded_image and saved_post_obj:
                        st.session_state.media_cache[saved_post_obj.id] = uploaded_image
                    
                    st.session_state.posts = db.load_posts()
                    st.toast("Post processed and saved successfully!", icon="✅")
                    
                    if links_detected:
                        st.info(f"🔗 Link Scanner flagged URL asset: `{links_detected[0]}`")
                    if not hashtags_valid:
                        st.warning("🏷️ Optimization Warning: No hashtags were detected in this caption.")
                        
                except ValueError as validation_error:
                    st.error(f"Validation Failure: {validation_error}", icon="🚨")
                except Exception as storage_error:
                    st.error(f"Storage System Error: {storage_error}")

with tab_history:
    st.markdown("### Saved Posts")
    st.session_state.posts = db.load_posts()
    
    if not st.session_state.posts:
        st.info("No posts saved yet.", icon="📁")
    else:
        # --- AUTOMATIC PAST-DUE STATUS FLIPPER ---
        current_now = datetime.datetime.now()
        status_was_changed = False
        
        for post in st.session_state.posts:
            if post.status == "Scheduled":
                try:
                    p_date = datetime.datetime.strptime(post.scheduled_date, "%Y-%m-%d").date()
                    # Catch both HH:MM and HH:MM:SS gracefully
                    time_format = "%H:%M:%S" if ":" in post.scheduled_time and post.scheduled_time.count(":") == 2 else "%H:%M"
                    p_time = datetime.datetime.strptime(post.scheduled_time, time_format).time()
                    post_datetime = datetime.datetime.combine(p_date, p_time)
                    
                    if current_now >= post_datetime:
                        db.update_status(post.id, "Posted")
                        status_was_changed = True
                except Exception:
                    pass
                    
        if status_was_changed:
            st.session_state.posts = db.load_posts()
            
        # Metric Dashboards
        status_counts = {"Draft": 0, "Scheduled": 0, "Posted": 0}
        for p in st.session_state.posts:
            if p.status in status_counts:
                status_counts[p.status] += 1
            
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Draft", status_counts["Draft"])
        m_col2.metric("Scheduled", status_counts["Scheduled"])
        m_col3.metric("Posted", status_counts["Posted"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for idx, post in enumerate(st.session_state.posts):
            status_emoji = "⏳" if post.status == "Scheduled" else "📝" if post.status == "Draft" else "🚀"
            
            with st.expander(f"{status_emoji} {post.title} — {post.platform}"):
                col_view_1, col_view_2 = st.columns([7, 3], gap="large")
                with col_view_1:
                    st.markdown("**Scheduled Window:**")
                    st.caption(f"📅 {post.scheduled_date} at ⏰ {post.scheduled_time}")
                    st.markdown("**Caption:**")
                    st.text(post.caption)
                    
                    if post.id in st.session_state.media_cache:
                        st.markdown("<br>**Attached Media Asset Preview:**", unsafe_allow_html=True)
                        st.image(st.session_state.media_cache[post.id], width=350)
                        
                with col_view_2:
                    st.markdown("**Update Status**")
                    new_status = st.segmented_control(
                        "Status Options", 
                        options=["Draft", "Scheduled", "Posted"],
                        default=post.status,
                        key=f"status_{post.id}_{idx}",
                        label_visibility="collapsed"
                    )
                    if new_status and new_status != post.status:
                        db.update_status(post.id, new_status)
                        st.session_state.posts = db.load_posts()
                        st.rerun()
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️ Delete Post", key=f"del_{post.id}_{idx}", use_container_width=True):
                        if db.delete_post(post.id):
                            if post.id in st.session_state.media_cache:
                                del st.session_state.media_cache[post.id]
                            st.toast("Post removed from registry archive.", icon="🗑️")
                            st.session_state.posts = db.load_posts()
                            st.rerun()