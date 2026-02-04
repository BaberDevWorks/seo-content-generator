import streamlit as st
import requests
import json
import time

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="SEO Article Generator", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px 30px;
        border-radius: 15px;
        margin-bottom: 40px;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .header-title {
        font-size: 3em;
        font-weight: 800;
        margin: 0;
        padding: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1.15em;
        opacity: 0.95;
        margin: 15px 0 0 0;
        font-weight: 300;
    }
    
    /* Input form styling */
    .input-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #f0f2f6 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 40px;
        border-left: 6px solid #667eea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .input-label {
        font-size: 0.95em;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Right sidebar styling */
    .sidebar-section {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8ebf0 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-title {
        font-size: 1.25em;
        font-weight: 700;
        margin-bottom: 18px;
        color: #667eea;
        letter-spacing: -0.3px;
    }
    
    .keyword-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #5568d3 100%);
        color: white;
        padding: 8px 14px;
        border-radius: 25px;
        margin: 6px 6px 6px 0;
        font-size: 0.85em;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
    }
    
    .meta-item {
        margin-bottom: 18px;
        padding-bottom: 18px;
        border-bottom: 1px solid #d0d5e0;
    }
    
    .meta-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .meta-label {
        font-weight: 700;
        color: #667eea;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .meta-value {
        margin-top: 8px;
        color: #2c3e50;
        font-size: 0.95em;
        line-height: 1.4;
    }
    
    /* Article content styling */
    .article-container {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        line-height: 1.7;
    }
    
    .article-container h1 {
        font-size: 2.2em;
        margin-bottom: 20px;
        color: #2c3e50;
        font-weight: 800;
    }
    
    .article-container h2 {
        font-size: 1.7em;
        margin-top: 30px;
        margin-bottom: 15px;
        color: #34495e;
        font-weight: 700;
    }
    
    .article-container h3 {
        font-size: 1.3em;
        margin-top: 20px;
        margin-bottom: 12px;
        color: #4a5f7f;
        font-weight: 700;
    }
    
    .article-container p {
        color: #555;
        font-size: 0.98em;
        margin-bottom: 15px;
    }
    
    /* Generating indicator */
    .generating-badge {
        display: inline-block;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 10px 16px;
        border-radius: 25px;
        font-size: 0.9em;
        font-weight: 600;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(132, 250, 176, 0.25);
    }
    
    .divider {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #d0d5e0, transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">🧠 SEO Content Generator</div>
    <div class="header-subtitle">Create SEO-optimized articles with metadata, keywords, and strategic linking</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col_label1, col_label2, col_label3, col_label4 = st.columns([2, 1, 1, 1])
    with col_label1:
        st.markdown('<div class="input-label">📌 Topic / Keyword</div>', unsafe_allow_html=True)
    with col_label2:
        st.markdown('<div class="input-label">📊 Word Count</div>', unsafe_allow_html=True)
    with col_label3:
        st.markdown('<div class="input-label">🌐 Language</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        topic = st.text_input(
            "Topic / Primary Keyword",
            "Best productivity tools for remote teams in 2025",
            help="Enter the main topic for the article",
            label_visibility="collapsed"
        )
    
    with col2:
        target_word_count = st.number_input(
            "Word Count",
            value=500,
            min_value=500,
            max_value=5000,
            step=100,
            help="Target word count",
            label_visibility="collapsed"
        )
    
    with col3:
        language = st.selectbox(
            "Language",
            ["en", "es", "fr", "de", "it"],
            help="Article language",
            label_visibility="collapsed"
        )
    
    with col4:
        generate_button = st.button("🚀 Generate", use_container_width=True, type="primary", key="generate_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)

if generate_button:
    try:
        print(f"\n🔵 [FRONTEND] User clicked Generate")
        print(f"🔵 [FRONTEND] Topic: {topic}")
        print(f"🔵 [FRONTEND] Word count: {target_word_count}")
        print(f"🔵 [FRONTEND] Language: {language}")
        
        response = requests.post(
            f"{BACKEND_URL}/jobs",
            json={"topic": topic, "language": language, "target_word_count": target_word_count},
            timeout=10
        )
        response.raise_for_status()
        job = response.json()
        
        print(f"🔵 [FRONTEND] Job created: {job.get('id')}")
        
        st.session_state["job_id"] = job["id"]
        st.session_state["generation_started"] = True
        st.session_state["topic"] = topic

        try:
            with st.spinner("⏳ Generating your article... This may take a minute"):
                progress = st.progress(0)
                run_resp = requests.post(f"{BACKEND_URL}/jobs/{job['id']}/run", timeout=300)
                run_resp.raise_for_status()

                final_result = None
                for i in range(60):
                    time.sleep(1)
                    progress.progress(min(100, int((i + 1) / 60 * 100)))
                    try:
                        res = requests.get(f"{BACKEND_URL}/jobs/{job['id']}/result", timeout=10)
                        if res.status_code == 200:
                            final_result = res.json()
                            break
                    except requests.exceptions.RequestException:
                        pass

                if final_result:
                    st.session_state["last_result"] = final_result
                else:

                    st.warning("Generation started. If results don't appear, refresh or check backend logs.")
        except requests.exceptions.RequestException as e:
            print(f"❌ [FRONTEND] Run request error: {str(e)}")
            st.error(f"❌ Failed to run generation: {str(e)}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ [FRONTEND] Request error: {str(e)}")
        st.error(f"❌ Failed to start generation: {str(e)}")
    except Exception as e:
        print(f"❌ [FRONTEND] Unexpected error: {str(e)}")
        st.error(f"❌ Unexpected error: {str(e)}")

if "job_id" in st.session_state:
    job_id = st.session_state["job_id"]
    print(f"🔵 [FRONTEND] Checking job result for: {job_id}")
    
    try:
        response = requests.get(f"{BACKEND_URL}/jobs/{job_id}/result", timeout=10)
        result = response.json()
        
        print(f"🔵 [FRONTEND] Result status: {result.get('status')}")
        print(f"🔵 [FRONTEND] Result detail: {result.get('detail')}")
        
        if result.get("status") == "pending" or result.get("status") == "running":
            st.markdown('<div class="generating-badge">⏳ Generating your article...</div>', unsafe_allow_html=True)
            st.info(f"📋 {result.get('detail', 'Processing...')}")
            
            progress = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.1)
                progress.progress(min(i, 99))
            
            time.sleep(10)
            st.rerun()
        
        elif result.get("status") == "failed":
            st.error("❌ Generation Failed")
            error_msg = result.get("detail") or result.get("error", "Unknown error occurred")
            st.error(f"**Error Details:** {error_msg}")
            
            with st.expander("🔧 Troubleshooting"):
                st.write("- Check your OpenAI API key in `.env`")
                st.write("- Ensure you have sufficient API credits")
                st.write("- Check backend logs for detailed error messages")
                st.write("- Try a simpler topic first")
        
        else:
            col_article, col_sidebar = st.columns([3, 1], gap="large")
            
            with col_article:
                for block in result.get("content", []):
                    if block["type"] == "heading":
                        level = block.get("level", 2)
                        text = block.get("text", "")
                        if level == 1:
                            st.markdown(f"# {text}")
                        elif level == 2:
                            st.markdown(f"## {text}")
                        elif level == 3:
                            st.markdown(f"### {text}")
                        else:
                            st.markdown(f"#### {text}")
                            
                    elif block["type"] == "paragraph":
                        st.write(block.get("text", ""))
                        
                    elif block["type"] == "list":
                        for item in block.get("items", []):
                            st.write(f"• {item}")
                
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### 🔗 Links & References")
                
                col_internal, col_external = st.columns(2)
                
                with col_internal:
                    st.markdown("**Internal Links:**")
                    for link in result.get("internalLinks", []):
                        anchor = link.get('anchorText', 'Link')
                        target = link.get('targetPage', '#')
                        st.markdown(f"- [{anchor}]({target})")
                
                with col_external:
                    st.markdown("**External References:**")
                    for ref in result.get("externalReferences", []):
                        url = ref.get('url', '#')
                        context = ref.get('context', 'Reference')
                        domain = url.split('/')[2] if len(url.split('/')) > 2 else url
                        st.markdown(f"- [{domain}]({url})")
                        st.caption(f"_{context}_")
                
                st.markdown("---")
                col_structured, col_raw = st.columns(2)
                
                # with col_structured:
                #     with st.expander("📋 Structured Data (JSON-LD)"):
                #         st.json(result.get("structuredData", {}))
                
                # with col_raw:
                #     with st.expander("🔬 View Full JSON"):
                #         st.json(result)
            
            with col_sidebar:
                st.markdown("### 📊 SEO Info")
                
                st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-title">📝 Metadata</div>', unsafe_allow_html=True)
                
                if result.get("meta"):
                    st.markdown('<div class="meta-item">', unsafe_allow_html=True)
                    st.markdown('<div class="meta-label">Title Tag</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="meta-value">{result["meta"].get("title", "N/A")}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="meta-item">', unsafe_allow_html=True)
                    st.markdown('<div class="meta-label">Meta Description</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="meta-value">{result["meta"].get("description", "N/A")}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-title">🎯 Primary Keywords</div>', unsafe_allow_html=True)
                
                primary_kws = result.get("keywords", {}).get("primary", [])
                if primary_kws:
                    keywords_html = ""
                    for kw in primary_kws:
                        keywords_html += f'<span class="keyword-badge">{kw}</span>'
                    st.markdown(f'<div>{keywords_html}</div>', unsafe_allow_html=True)
                else:
                    st.write("No primary keywords")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-title">🔍 Secondary Keywords</div>', unsafe_allow_html=True)
                
                secondary_kws = result.get("keywords", {}).get("secondary", [])
                if secondary_kws:
                    keywords_html = ""
                    for kw in secondary_kws:
                        keywords_html += f'<span class="keyword-badge" style="background: linear-gradient(135deg, #764ba2 0%, #6a3f8a 100%);">{kw}</span>'
                    st.markdown(f'<div>{keywords_html}</div>', unsafe_allow_html=True)
                else:
                    st.write("No secondary keywords")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
                content_text = " ".join([b.get("text", "") for b in result.get("content", []) if b.get("type") == "paragraph"])
                word_count = len(content_text.split())
                st.metric("📊 Word Count", word_count)
                st.markdown('</div>', unsafe_allow_html=True)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ [FRONTEND] Request error: {str(e)}")
        st.error(f"❌ Error fetching result: {str(e)}")
    except Exception as e:
        print(f"❌ [FRONTEND] Unexpected error: {str(e)}")
        st.error(f"❌ Unexpected error: {str(e)}")

