from langchain_openai import ChatOpenAI
from langchain.prompts import load_prompt
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime
import requests
import uuid

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

Prompt = load_prompt('template.json')
Image_prompt_template = load_prompt('image_template.json')

caption_chain = Prompt | model
image_chain = Image_prompt_template | model

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "caption" not in st.session_state:
    st.session_state.caption = None
if "image_path" not in st.session_state:
    st.session_state.image_path = None
if "show_preview" not in st.session_state:
    st.session_state.show_preview = False

def save_post(data):
    os.makedirs("output", exist_ok=True)
    file_path = "output/posts.json"
    try:
        with open(file_path, "r") as f:
            posts = json.load(f)
    except:
        posts = []
    posts.append(data)
    with open(file_path, "w") as f:
        json.dump(posts, f, indent=4)

def save_image_locally(image_url):
    os.makedirs("output/images", exist_ok=True)
    file_name = f"{uuid.uuid4()}.png"
    file_path = f"output/images/{file_name}"
    img_data = requests.get(image_url).content
    with open(file_path, "wb") as f:
        f.write(img_data)
    return file_path

st.header("AI Instagram Post Generator")
topic_input = st.text_input("TOPIC", placeholder='e.g. "Sunset yoga on a Beach"')
tone_input = st.selectbox("Select Tone", ["Professional", "Casual"])

if st.button("Generate Post"):
    if not topic_input:
        st.warning("Please enter a topic")
    else:
        with st.spinner("Generating your post..."):
            caption_result = caption_chain.invoke({
                "topic": topic_input,
                "tone": tone_input
            })
            caption = caption_result.content

            image_prompt_result = image_chain.invoke({
                "caption": caption,
                "topic": topic_input
            })
            image_prompt = image_prompt_result.content

            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024"
            )
            image_url = response.data[0].url
            local_image_path = save_image_locally(image_url)

            post_data = {
                "topic": topic_input,
                "tone": tone_input,
                "caption": caption,
                "image_url": local_image_path,
                "created_at": datetime.now().isoformat()
            }
            save_post(post_data)

            st.session_state.caption = caption
            st.session_state.image_path = local_image_path
            st.session_state.show_preview = False 

        st.success("✅ Post Generated!")


if st.session_state.caption and st.session_state.image_path:

    if not st.session_state.show_preview:

        st.image(st.session_state.image_path, use_container_width=True)
        st.write(st.session_state.caption)

        if st.button("📱 Preview Post"):
            st.session_state.show_preview = True
            st.rerun()

    else:

        st.markdown("### 📸 Instagram Preview")

        st.markdown("""
        <style>
        .post-card {
            border: 1px solid #dbdbdb;
            border-radius: 12px;
            max-width: 480px;
            margin: auto;
            background-color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            overflow: hidden;
        }
        .post-header {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            border-bottom: 1px solid #efefef;
        }
        .avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            margin-right: 12px;
            flex-shrink: 0;
        }
        .username {
            font-weight: 600;
            font-size: 14px;
            color: #000;
        }
        .actions {
            padding: 10px 15px 4px 15px;
            font-size: 22px;
        }
        .likes {
            padding: 0 15px;
            font-size: 14px;
            font-weight: 600;
            color: #000;
        }
        .caption-box {
            padding: 6px 15px 12px 15px;
            font-size: 14px;
            color: #000;
            line-height: 1.5;
        }
        .caption-box span {
            font-weight: 600;
            margin-right: 5px;
        }
        .comments {
            padding: 0 15px 10px 15px;
            font-size: 13px;
            color: #8e8e8e;
        }
        .timestamp {
            padding: 0 15px 12px 15px;
            font-size: 11px;
            color: #8e8e8e;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="post-card">', unsafe_allow_html=True)

        st.markdown("""
            <div class="post-header">
                <div class="avatar"></div>
                <div class="username">@Sanchit_Goel</div>
            </div>
        """, unsafe_allow_html=True)

        st.image(st.session_state.image_path, use_container_width=True)

        st.markdown(f"""
            <div class="actions">❤️ 🔖</div>
            <div class="likes">1,024 likes</div>
            <div class="caption-box">
                <span>@Sanchit_Goel</span>{st.session_state.caption}
            </div>
            <div class="comments">View all 128 comments</div>
            <div class="timestamp">{datetime.now().strftime("%B %d, %Y")}</div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("← Back to Post"):
            st.session_state.show_preview = False
            st.rerun()