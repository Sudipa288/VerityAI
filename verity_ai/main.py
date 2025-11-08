import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components
import random
import urllib.parse

st.set_page_config(
    page_title="VerityAI - Agriculture Chatbot",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LOGO_URL = "https://img.freepik.com/premium-vector/leaf-green-logo-symbol-vector_878729-987.jpg"

# ========================= GLOBAL CSS ========================= #
st.markdown("""
<style>
    /* Keep Streamlit header in DOM so the real sidebar button exists */
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    div.block-container { padding-top: 0 !important; }

    /* === Top Navbar === */
    .top-nav {
        position: fixed; top: 0; left: 0; width: 100%;
        background-color: #ffffff;
        padding: 10px 18px 6px;
        display: flex; flex-direction: column;
        z-index: 9999;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .top-title {
        font-size: 20px; font-weight: 700; color: #2d4b38;
        display: flex; align-items: center; gap: 10px;
    }
    .nav-logo {
        width: 40px; height: 40px; border-radius: 50%;
        object-fit: cover; border: 1px solid #ccd6cc;
    }
    .nav-toggle {
        font-size: 21px; font-weight: 900; border: none; background: none;
        cursor: pointer; color: #2d4b38; padding: 4px 8px; margin-right: 4px;
        transition: transform 0.25s ease;
    }
    .nav-toggle.rotated { transform: rotate(90deg); }
    .top-subtitle {
        font-size: 11px; color: #6f7f73; margin-top: -3px; padding-left: 48px; letter-spacing: 0.3px;
    }

    /* Push content below navbar */
    .stApp { padding-top: 95px !important; background-color: #f5f3ed; }

    /* Chat bubbles */
    .chat-message { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; }
    .user-message { background-color: #4a7c59; color: white; margin-left: 20%; }
    .assistant-message { background-color: white; border: 1px solid #c8d5b9; margin-right: 20%; }

    /* Suggestion cards */
    .suggestion-box {
        background-color: #ffffff; color: #3d5a40; padding: 1rem; border-radius: 10px;
        border: 1px solid #c8d5b9; cursor: pointer; margin-bottom: 0.7rem;
        text-align: center; font-weight: 600; height: 75px; display: flex;
        align-items: center; justify-content: center; transition: all 0.2s;
    }
    .suggestion-box:hover { border-color: #4a7c59; background-color: #f4f7f2; transform: scale(1.03); }

    /* Inputs */
    .stTextInput > div > div > input {
        background-color: white; color: #555 !important; border: 1px solid #c8d5b9;
    }
    .stTextInput > div > div > input::placeholder { color: #888 !important; }

    .stButton > button {
        background-color: #4a7c59; color: white; border: none; padding: 0.5rem 2rem; border-radius: 8px; cursor: pointer;
    }
    .stButton > button:hover { background-color: #3d5a40; }

    #location_input input { height: 32px !important; font-size: 0.8rem !important; padding: 4px 8px !important; }

    .loc-btn {
        padding: 6px 14px; border-radius: 8px; border: none; background-color: #d62828; color: white; font-weight: 600; cursor: pointer;
    }
    .loc-btn:hover { background-color: #a4161a; }
    .loc-status { margin-top: 6px; font-size: 12px; color: #2f3b2f; opacity: 0.9; }

    /* Sidebar styled menu */
    .menu-item, .submenu-title, .menu-leaf {
        display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 8px;
        cursor: pointer; user-select: none; text-decoration: none;
    }
    .menu-item:hover, .submenu-title:hover, .menu-leaf:hover { background: #ecf1ec; }
    .menu-icon { width: 20px; text-align: center; }
    .menu-divider { height: 1px; background: #e6ece6; margin: 8px 0; }
    .submenu-items { margin-left: 12px; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

# ========================= JS: Sidebar Toggle + Suggestion Fill ========================= #
st.markdown("""
<script>
function toggleSidebar(){
  const doc = window.parent ? window.parent.document : document;

  // Streamlit 1.51 toggle + fallbacks
  const selectors = [
    'button[data-testid="baseButton-headerNoPadding"]', // ✅ Streamlit 1.51
    'button[data-testid="baseButton-header"]',
    '[data-testid="sidebar-collapse-button"]',
    'button[aria-label="Toggle sidebar"]'
  ];
  let btn = null;
  for (const s of selectors){
    btn = doc.querySelector(s);
    if (btn) break;
  }

  const icon = document.getElementById('hamburgerIcon');
  if (btn){
    btn.click();
    if (icon) icon.classList.toggle('rotated');  // rotate on each toggle
  } else {
    console.warn('Sidebar toggle button not found for this Streamlit version.');
  }
}

function fillInput(value){
  const input = window.parent.document.querySelector('input[placeholder="Ask anything about agriculture..."]');
  if (input){
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
}
</script>
""", unsafe_allow_html=True)

# ========================= NAVBAR ========================= #
st.markdown(f"""
<div class="top-nav">
    <div class="top-title">
        <button id="hamburgerIcon" class="nav-toggle" onclick="toggleSidebar()">☰</button>
        <img src="{LOGO_URL}" class="nav-logo">
        VERITY AI
    </div>
    <div class="top-subtitle">YOUR FRIENDLY NEIGHBORHOOD AI</div>
</div>
""", unsafe_allow_html=True)

# ========================= SESSION STATE ========================= #
if 'chats' not in st.session_state:
    st.session_state.chats = [
        {"id": "1", "title": "Soil pH Testing", "messages": [], "created_at": datetime.now()},
        {"id": "2", "title": "Crop Rotation Tips", "messages": [], "created_at": datetime.now()}
    ]
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'location' not in st.session_state:
    st.session_state.location = ""
if 'nav_mode' not in st.session_state:
    st.session_state.nav_mode = "chat"
if 'convos_open' not in st.session_state:
    st.session_state.convos_open = False

# ========================= SIDEBAR (Styled Menu) ========================= #
with st.sidebar:
    st.markdown('<div class="menu-wrap">', unsafe_allow_html=True)

    # PROFILE (top)
    st.markdown(
        """
        <div class="menu-item" onclick="location.href='?nav=profile'">
            <span class="menu-icon">👤</span> <span>My Profile</span>
        </div>
        <div class="menu-divider"></div>
        """,
        unsafe_allow_html=True
    )

    # NEW CHAT
    st.markdown(
        """
        <div class="menu-item" onclick="location.href='?nav=new_chat'">
            <span class="menu-icon">➕</span> <span>New Chat</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # MY CONVERSATIONS (collapsible)
    arrow = "▾" if st.session_state.convos_open else "▸"
    st.markdown(
        f"""
        <div class="submenu-title" onclick="location.href='?nav=toggle_convos'">
            <span class="menu-icon">💬</span> <span>My Conversations</span>
            <span style="margin-left:auto;">{arrow}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.convos_open:
        st.markdown('<div class="submenu-items">', unsafe_allow_html=True)
        for chat in st.session_state.chats:
            chat_id = chat["id"]
            title = chat["title"]
            st.markdown(
                f"""
                <div class="menu-leaf" onclick="location.href='?nav=open_chat&chat_id={chat_id}'">
                    <span class="menu-icon">▸</span>
                    <span>{title}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)

    # LOGOUT (bottom)
    st.markdown(
        """
        <div class="menu-item" onclick="location.href='?nav=logout'">
            <span class="menu-icon">🚪</span> <span>Logout</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ========================= HANDLE NAVIGATION ========================= #
nav = st.query_params.get("nav")
chat_id_param = st.query_params.get("chat_id")

def _qp(val):
    if isinstance(val, list):
        return val[0]
    return val

if nav:
    nav = _qp(nav)
    if nav == "profile":
        st.session_state.nav_mode = "profile"
    elif nav == "new_chat":
        new_chat = {"id": str(datetime.now().timestamp()), "title": "New Chat",
                    "messages": [], "created_at": datetime.now()}
        st.session_state.chats.insert(0, new_chat)
        st.session_state.current_chat_id = new_chat["id"]
        st.session_state.nav_mode = "chat"
    elif nav == "open_chat":
        cid = _qp(chat_id_param)
        st.session_state.current_chat_id = cid
        st.session_state.nav_mode = "chat"
    elif nav == "toggle_convos":
        st.session_state.convos_open = not st.session_state.convos_open
    elif nav == "logout":
        for k in ["chats", "current_chat_id", "input_text", "location"]:
            if k in st.session_state: del st.session_state[k]
        st.session_state.nav_mode = "chat"
        st.session_state.convos_open = False

    st.query_params.clear()
    st.rerun()

# ========================= SUGGESTIONS (JS fillInput) ========================= #
def render_suggestions():
    st.markdown("""
    <h3 style="color:#2b7a3e; text-align:center; font-size:20px; font-weight:600; margin-top:25px;">
        Try asking about:
    </h3>
    """, unsafe_allow_html=True)

    pool = [
        "🍃 What's the best time to plant wheat?",
        "🍃 How do I improve soil fertility naturally?",
        "🍃 What are common pests affecting tomatoes?",
        "🍃 How much water does rice need daily?",
        "🍃 Which fertilizer is best for sugarcane?",
        "🍃 How do I prevent fungal disease in potatoes?",
        "🍃 What crops grow well in sandy soil?",
        "🍃 How to choose the right irrigation method?",
        "🍃 What are high-yield hybrid rice varieties?",
        "🍃 How do I detect nitrogen deficiency in crops?",
        "🍃 Best organic pest control methods?",
        "🍃 How to improve soil drainage in clay soil?",
        "🍃 How do I reduce water usage in irrigation?",
        "🍃 When should I harvest groundnut?",
        "🍃 How to manage weeds without chemicals?"
    ]
    suggestions = random.sample(pool, 4)

    for i in range(0, len(suggestions), 2):
        cols = st.columns(2)
        for j, text in enumerate(suggestions[i:i+2]):
            with cols[j]:
                # Escape single quotes for JS string
                encoded = text.replace("'", "\\'")
                st.markdown(
                    f"<div class='suggestion-box' onclick=\"fillInput('{encoded}')\">{text}</div>",
                    unsafe_allow_html=True
                )

# ========================= MAIN VIEW ========================= #
if st.session_state.nav_mode == "profile":
    st.markdown(f"""
    <div style="text-align:center; padding: 1.5rem;">
        <img src="{LOGO_URL}" style="width:90px; height:90px; border-radius:50%; margin-bottom: 12px;">
        <h2 style="color:#2d4b38; margin: 0;">My Profile</h2>
        <p style="color:#6b7c6e;">Profile page coming soon…</p>
    </div>
    """, unsafe_allow_html=True)
else:
    current_chat = next((c for c in st.session_state.chats if c["id"] == st.session_state.current_chat_id), None)

    if not current_chat or len(current_chat["messages"]) == 0:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem;">
            <img src="{LOGO_URL}" style="width:90px; height:90px; border-radius:50%; margin-bottom: 16px;">
            <h2 style="color: #4a7c59; margin-bottom: 6px;">Welcome to VerityAI</h2>
            <p style="color: #6b7c6e;">Your friendly neighborhood AI for all agricultural queries</p>
        </div>
        """, unsafe_allow_html=True)
        render_suggestions()
    else:
        for msg in current_chat["messages"]:
            if msg["role"] == "user":
                loc = f"<br><small>{msg.get('location','')}</small>" if msg.get("location") else ""
                st.markdown(f"<div class='chat-message user-message'>{msg['content']}{loc}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message assistant-message'>🌱 {msg['content']}</div>", unsafe_allow_html=True)

    # Location + input
    st.markdown('<label style="color: black; font-weight:600;">📍 Location (optional):</label>', unsafe_allow_html=True)
    lc1, lc2 = st.columns([5, 1])

    with lc1:
        location = st.text_input("", value=st.session_state.location,
                                 placeholder="Add your location",
                                 key="location_input", label_visibility="collapsed")

    with lc2:
        components.html("""
        <div>
          <button class="loc-btn" id="accessLocBtn">📍 Access Location</button>
          <div class="loc-status" id="locStatus"></div>
        </div>
        <script>
        (function() {
            const statusEl = document.getElementById('locStatus');
            const btn = document.getElementById('accessLocBtn');
            function setStatus(msg) { if (statusEl) statusEl.textContent = msg || ''; }
            function setLocationInput(value) {
              const el = window.parent.document.querySelector('input[placeholder="Add your location"]');
              if (el) {
                el.value = value;
                el.dispatchEvent(new Event('input', { bubbles: true }));
              }
            }
            async function reverseGeocode(lat, lon) {
              const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;
              const resp = await fetch(url);
              const data = await resp.json();
              const a = data.address || {};
              const parts = [a.city || a.town || a.village || a.county, a.state, a.country].filter(Boolean);
              return parts.join(", ");
            }
            function getLocation() {
              if (!navigator.geolocation) return setStatus("Geolocation not supported.");
              setStatus("Detecting location…");
              navigator.geolocation.getCurrentPosition(async (pos) => {
                const lat = pos.coords.latitude, lon = pos.coords.longitude;
                setStatus("Resolving address…");
                const place = await reverseGeocode(lat, lon);
                setLocationInput(place);
                setStatus("✅ Location added");
              }, () => setStatus("Location access denied."), { enableHighAccuracy: true });
            }
            btn.addEventListener("click", getLocation);
        })();
        </script>
        """, height=70)

    mc1, mc2 = st.columns([5, 1])
    with mc1:
        user_input = st.text_input("Message", value=st.session_state.input_text,
                                   placeholder="Ask anything about agriculture...",
                                   label_visibility="collapsed", key="message_input")
    with mc2:
        send_button = st.button("Send 📤", use_container_width=True)

    if send_button and user_input.strip():
        if not current_chat:
            new_chat = {"id": str(datetime.now().timestamp()),
                        "title": user_input[:30] + ("..." if len(user_input) > 30 else ""),
                        "messages": [], "created_at": datetime.now()}
            st.session_state.chats.insert(0, new_chat)
            st.session_state.current_chat_id = new_chat["id"]
            current_chat = new_chat

        user_msg = {"role": "user", "content": user_input, "location": location or None}
        ai_msg = {"role": "assistant",
                  "content": f"I'd be happy to help you with \"{user_input}\". "
                             f"{f'Based on your location ({location}), ' if location else ''}"
                             f"this is a simulated response."}

        for chat in st.session_state.chats:
            if chat["id"] == current_chat["id"]:
                chat["messages"].extend([user_msg, ai_msg])
                if len(chat["messages"]) == 2:
                    chat["title"] = user_input[:30] + ("..." if len(user_input) > 30 else "")
                break

        st.session_state.input_text = ""
        st.session_state.location = ""
        st.rerun()
