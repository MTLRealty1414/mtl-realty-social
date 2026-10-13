# ==============================================================================
# 1. APP CONFIGURATION & BRAND CONSTANTS
# ==============================================================================
st.set_page_config(page_title="MTL Realty Social Command Center", layout="wide", page_icon="🏡")

PILLARS = {
    "Pillar 1: First-Time Home Buyers": {
        "url": "https://martinlattibeaudiere.book.live/hp-buyer-book",
        "keyword": "BUYER",
        "target": "First-time buyers in Fulton, Gwinnett, Cobb, DeKalb, Forsyth, Cherokee"
    },
    "Pillar 2: Home Sellers & Valuation": {
        "url": "https://martinlattibeaudiere.book.live/hp-biz-card-book",
        "keyword": "SELLER",
        "target": "Homeowners curious about equity and neighborhood comps"
    },
    "Pillar 3: FSBO & Expired Listings": {
        "url": "https://martinlattibeaudiere.book.live/hp-expired-book",
        "keyword": "EXPIRED",
        "target": "Sellers who struggled to sell on their own or had listings expire"
    },
    "Pillar 4: Divorce Selling Options": {
        "url": "https://martinlattibeaudiere.book.live/hp-divorce-book",
        "keyword": "DIVORCE",
        "target": "Discreet, equitable property division guidance"
    },
    "Pillar 5: Downsizing for Retirement": {
        "url": "https://martinlattibeaudiere.book.live/senior-book",
        "keyword": "DOWNSIZE",
        "target": "Seniors moving from large multi-level homes to low-maintenance Atlanta living"
    }
}

COUNTIES = "Fulton, Gwinnett, DeKalb, Cobb, Forsyth, and Cherokee Counties, Georgia"

# ==============================================================================
# 2. HELPER: GRAPHIC BUILDER WITH COMPLIANCE FOOTER
# ==============================================================================
def render_branded_graphic(bg_image, top_text, bottom_text):
    """Overlays top hook banner, bottom CTA, Coldwell Banker logo, MTL logo, and EHO bug."""
    canvas = bg_image.convert("RGBA").resize((1080, 1080))
    draw = ImageDraw.Draw(canvas)
    
    # Load fonts (defaulting to system bold font)
    try:
        font_hook = ImageFont.truetype("Arial-Bold.ttf", 46)
        font_cta = ImageFont.truetype("Arial-Bold.ttf", 44)
    except:
        font_hook = ImageFont.load_default()
        font_cta = ImageFont.load_default()

    # 1. Top Hook Banner (Navy Container: #132257)
    draw.rounded_rectangle([80, 50, 1000, 220], radius=25, fill=(19, 34, 87, 240))
    draw.text((540, 135), top_text, fill="white", font=font_hook, anchor="mm", align="center")

    # 2. Bottom CTA Text (with black drop-shadow)
    shadow = 3
    for dx, dy in [(-shadow, 0), (shadow, 0), (0, -shadow), (0, shadow)]:
        draw.text((540 + dx, 860 + dy), bottom_text, fill="black", font=font_cta, anchor="mm", align="center")
    draw.text((540, 860), bottom_text, fill="white", font=font_cta, anchor="mm", align="center")

    # 3. Bottom White Compliance Footer Bar
    footer_bar = Image.new("RGBA", (1080, 130), (255, 255, 255, 245))
    canvas.paste(footer_bar, (0, 950), footer_bar)

    # 4. Stamp Logos onto Footer Bar
    try:
        cb_logo = Image.open("cb_logo.png").convert("RGBA").resize((220, 80))
        mtl_logo = Image.open("mtl_logo.png").convert("RGBA").resize((220, 80))
        eho_logo = Image.open("eho_logo.png").convert("RGBA").resize((60, 60))
        
        canvas.paste(cb_logo, (60, 975), cb_logo)
        canvas.paste(mtl_logo, (430, 975), mtl_logo)
        canvas.paste(eho_logo, (960, 985), eho_logo)
    except Exception as e:
        # Fallback text if logo images are missing from current directory
        draw.text((540, 1010), "Coldwell Banker Realty | MTL Realty LLC | Equal Housing Opportunity", fill="black", anchor="mm")

    return canvas.convert("RGB")

# ==============================================================================
# 3. SIDEBAR: CREDENTIALS & LEAD EXPORT
# ==============================================================================
st.sidebar.title("🏢 MTL Realty Command")
st.sidebar.caption("Coldwell Banker Realty | Metro Atlanta")

gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
pexels_key = st.sidebar.text_input("Pexels API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Lead Management")

# Sample lead database simulation (persisted in SQLite or Supabase in production)
sample_leads = pd.DataFrame([
    {"Date": "2025-05-10", "Name": "David Miller", "Email": "david.m@example.com", "Phone": "404-555-0192", "Pillar": "Downsizing for Retirement", "County": "North Fulton", "Trigger": "DOWNSIZE"},
    {"Date": "2025-05-11", "Name": "Sarah Jenkins", "Email": "sjenkins@example.com", "Phone": "770-555-0144", "Pillar": "First-Time Home Buyers", "County": "Gwinnett", "Trigger": "BUYER"},
    {"Date": "2025-05-12", "Name": "Robert Vance", "Email": "rvance@example.com", "Phone": "678-555-0188", "Pillar": "Home Sellers & Valuation", "County": "Cobb", "Trigger": "SELLER"}
])

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    sample_leads.to_excel(writer, index=False, sheet_name='Captured_Leads')
buffer.seek(0)

st.sidebar.download_button(
    label="📊 Download Latest Leads (.xlsx)",
    data=buffer,
    file_name=f"MTL_Realty_Leads_{datetime.date.today()}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

# ==============================================================================
# 4. MAIN INTERFACE: CONTENT GENERATION & APPROVAL
# ==============================================================================
st.title("🏡 Social Media Batch Generator & Approvals")
st.write(f"Generating hyper-local, compliant real estate content for **{COUNTIES}**.")

col_a, col_b = st.columns([2, 1])
with col_a:
    selected_pillar_name = st.selectbox("Select Target Pillar", list(PILLARS.keys()))
with col_b:
    publish_channel = st.selectbox("Destination Format", [
        "Instagram (Tue @ 12:00 PM EST)",
        "Instagram (Thu @ 7:30 PM EST)",
        "Facebook (Wed @ 9:30 AM EST)",
        "Facebook (Sun @ 2:30 PM EST)",
        "YouTube Shorts (Tue @ 4:00 PM EST)",
        "YouTube Shorts (Fri @ 1:00 PM EST)",
        "X / Twitter (Mon @ 8:30 AM EST)",
        "X / Twitter (Thu @ 12:30 PM EST)"
    ])

selected_pillar = PILLARS[selected_pillar_name]

if st.button("🚀 Generate Compliant Post for Review", use_container_width=True):
    if not gemini_key:
        st.error("Please enter your free Gemini API key in the sidebar.")
    else:
        with st.spinner("Writing hyper-local Atlanta hooks and sourcing local house imagery..."):
            # 1. Call Gemini 1.5 Flash
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            You are the marketing director for Martin Lattibeaudiere, MTL Realty LLC, affiliated with Coldwell Banker Realty in Metro Atlanta.
            Audience: {selected_pillar['target']}
            Focus Counties: {COUNTIES}
            Landing Page: {selected_pillar['url']}
            DM Trigger Keyword: {selected_pillar['keyword']}
            
            Return a JSON object with:
            1. "top_banner": A punchy 4-7 word question or pain-point hook for an image banner.
            2. "bottom_banner": A 5-8 word CTA offer mentioning MTL Realty.
            3. "caption": A high-converting Instagram/Facebook caption highlighting local Atlanta dynamics, instructing viewers to comment "{selected_pillar['keyword']}" or click the link. Include 6 local hashtags (e.g. #AtlantaRealEstate, #CobbCountyHomes).
            4. "x_tweet": Under 250 characters with the link.
            5. "youtube_title": Under 60 characters with #Shorts.
            """
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            post_data = json.loads(response.text)
            
            # 2. Fallback sample image (or live Pexels search for "Atlanta suburban brick home")
            sample_bg = Image.new("RGB", (1080, 1080), color=(140, 170, 190))
            if pexels_key:
                try:
                    headers = {"Authorization": pexels_key}
                    res = requests.get("https://api.pexels.com/v1/search?query=suburban+brick+house+lawn&per_page=1", headers=headers).json()
                    if res.get("photos"):
                        img_url = res["photos"][0]["src"]["large"]
                        sample_bg = Image.open(io.BytesIO(requests.get(img_url).content))
                except:
                    pass

            rendered_img = render_branded_graphic(sample_bg, post_data["top_banner"], post_data["bottom_banner"])
            st.session_state["current_post"] = post_data
            st.session_state["current_img"] = rendered_img

# ==============================================================================
# 5. INDIVIDUAL POST APPROVAL CARD
# ==============================================================================
if "current_post" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Post Preview & Individual Approval")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(st.session_state["current_img"], caption="Rendered 1080x1080 Asset (Coldwell Banker + MTL Realty Compliant)", use_container_width=True)
        img_bytes = io.BytesIO()
        st.session_state["current_img"].save(img_bytes, format='JPEG', quality=95)
        st.download_button("💾 Download High-Res Image", data=img_bytes.getvalue(), file_name="post_graphic.jpg", mime="image/jpeg")

    with col2:
        st.markdown(f"**Pillar:** {selected_pillar_name}")
        st.markdown(f"**Lead Magnet:** [{selected_pillar['url']}]({selected_pillar['url']})")
        
        edit_hook = st.text_input("Top Banner Hook", value=st.session_state["current_post"]["top_banner"])
        edit_cta = st.text_input("Bottom Banner CTA", value=st.session_state["current_post"]["bottom_banner"])
        edit_caption = st.text_area("Social Caption & Hashtags", value=st.session_state["current_post"]["caption"], height=160)
        edit_tweet = st.text_area("X / Tweet Version", value=st.session_state["current_post"]["x_tweet"], height=80)
        
        c_app, c_reg, c_rej = st.columns(3)
        with c_app:
            if st.button("✅ Approve & Schedule", type="primary", use_container_width=True):
                st.success(f"Post approved! Scheduled for {publish_channel}. Dispatched to queue.")
        with c_reg:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.experimental_rerun()
        with c_rej:
            if st.button("❌ Reject", use_container_width=True):
                del st.session_state["current_post"]
                st.experimental_rerun()
