import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import qrcode
from io import BytesIO

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(page_title="智慧心灵 - 心理健康评估系统", layout="centered")
st.title("智慧心灵 - 心理健康评估系统")

# ==========================================
# 2. 侧边栏 (生成真实二维码)
# ==========================================
with st.sidebar:
    st.header("关于系统")
    st.info("本系统基于深度学习算法，对您的心理健康状态进行科学评估。")
    
    st.write("扫码分享给同学：")
    # 这里填入你的公网链接，目前先用演示链接
    url = "https://2soontest.streamlit.app/"
    
    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 将图片转为二进制以在 Streamlit 中显示
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # 显示二维码，宽度设置为 200 像素
    st.image(byte_im, caption="微信扫码进入系统", width=200)

# ==========================================
# 3. 问卷表单
# ==========================================
st.subheader("SCL-90 心理健康自评量表")
st.write("请根据最近一周的感觉评分 (1=没有, 2=很轻, 3=中等, 4=偏重, 5=严重)")

with st.form("scl90_form"):
    student_id = st.text_input("请输入你的学号")
    
    # 演示用的 10 道题
    q1 = st.radio("1. 头痛 (躯体化)", [1, 2, 3, 4, 5], horizontal=True)
    q2 = st.radio("2. 忘记性大 (强迫症状)", [1, 2, 3, 4, 5], horizontal=True)
    q3 = st.radio("3. 同异性相处时感到害羞不自在 (人际关系)", [1, 2, 3, 4, 5], horizontal=True)
    q4 = st.radio("4. 对事物不感兴趣 (抑郁)", [1, 2, 3, 4, 5], horizontal=True)
    q5 = st.radio("5. 神经过敏，心中不踏实 (焦虑)", [1, 2, 3, 4, 5], horizontal=True)
    q6 = st.radio("6. 容易烦恼和激动 (敌对)", [1, 2, 3, 4, 5], horizontal=True)
    q7 = st.radio("7. 害怕空旷的场所或街道 (恐怖)", [1, 2, 3, 4, 5], horizontal=True)
    q8 = st.radio("8. 感到大多数人都不可信任 (偏执)", [1, 2, 3, 4, 5], horizontal=True)
    q9 = st.radio("9. 感到孤独 (精神病性)", [1, 2, 3, 4, 5], horizontal=True)
    q10 = st.radio("10. 胃口不好 (其他)", [1, 2, 3, 4, 5], horizontal=True)
    
    submit = st.form_submit_button("提交评估")

# ==========================================
# 4. 结果处理与展示
# ==========================================
if submit:
    if not student_id:
        st.error("请填写学号！")
    else:
        st.success("评估完成！以下是您的专属心理健康报告：")
        
        answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        factors = ["躯体化", "强迫症状", "人际关系敏感", "抑郁", "焦虑", "敌对", "恐怖", "偏执", "精神病性", "其他"]
        scores = np.array(answers, dtype=float)
        
        # 绘制雷达图
        df_radar = pd.DataFrame(dict(r=scores, theta=factors))
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("### 您的因子得分雷达图")
            st.plotly_chart(fig)
            
        with col2:
            st.write("### 专家建议")
            max_score = max(answers)
            avg_score = sum(answers) / len(answers)
            
            if max_score <= 2:
                st.balloons()
                st.success("🌟 您的心理状态非常健康！请继续保持积极乐观的生活态度。")
            elif max_score == 3:
                st.info("💡 您近期可能存在轻微的情绪波动。建议多与朋友沟通，适当运动，注意休息。")
            else:
                st.warning("⚠️ 提示：您近期的心理压力较大。建议前往学校心理咨询中心寻求专业老师的帮助。")
            
            st.write(f"**平均得分：** {avg_score:.2f} 分")
            st.write("*(注：当前为界面演示模式，未接入深度聚类 AI 模型)*")
