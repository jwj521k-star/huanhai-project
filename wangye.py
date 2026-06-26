import streamlit as st
import pandas as pd
import datetime
import os

# =============================================
# 1. 网页基础配置
# =============================================
st.set_page_config(page_title="寰海青衿·关东焕新", layout="wide")

# =============================================
# 2. 本地 CSV 存储函数
# =============================================
DATA_FILE = "submissions.csv"


def save_to_csv(data_dict):
    """将数据追加到本地 CSV 文件"""
    if not os.path.exists(DATA_FILE):
        df_empty = pd.DataFrame(columns=["提交时间", "业务类型", "姓名", "国家", "联系方式"])
        df_empty.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

    existing_df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    new_row = pd.DataFrame([data_dict])
    updated_df = pd.concat([existing_df, new_row], ignore_index=True)
    updated_df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    return True


# =============================================
# 3. 页面标题区
# =============================================
st.title("寰海青衿·关东焕新 🌍")
st.subheader("一站式：留学指南 | 关东文旅 | 甄选好物")
st.write("面向东北三省及内蒙古自治区的国际青年共创平台")

# =============================================
# 4. 侧边栏：管理员入口（需要密码）
# =============================================
with st.sidebar:
    st.header("🔐 管理员入口")

    # 设置管理员密码（你可以改成自己的密码）
    ADMIN_PASSWORD = "huanhai2026"

    # 初始化 session_state
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    # 密码输入
    if not st.session_state.admin_authenticated:
        password = st.text_input("请输入管理员密码", type="password")
        if st.button("登录"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("✅ 验证成功！")
                st.rerun()
            else:
                st.error("❌ 密码错误！")
    else:
        # 验证通过后显示数据
        st.success("✅ 已登录")
        if st.button("🚪 退出登录"):
            st.session_state.admin_authenticated = False
            st.rerun()

        st.markdown("---")

        if st.button("🔄 刷新并查看所有数据"):
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
                st.dataframe(df)
                st.caption(f"共 {len(df)} 条记录")
                csv = df.to_csv(index=False, encoding="utf-8-sig")
                st.download_button("📥 下载数据 CSV", csv, "submissions.csv", "text/csv")
            else:
                st.info("暂无数据，等待第一条提交。")

        st.markdown("---")
        st.caption("💡 数据保存在本地的 submissions.csv 文件中")

# =============================================
# 5. 三大业务标签页（保持不变，对所有人开放）
# =============================================
tab1, tab2, tab3 = st.tabs(["🎓 青衿留学", "❄️ 关东文旅", "🛍️ 甄选商贸"])

# ---------- 标签页1：留学 ----------
with tab1:
    st.header("来华留学咨询与定制")
    st.write("请留下您的基本信息，获取最新奖学金政策及入学指导：")

    with st.form("留学咨询表单"):
        name = st.text_input("您的姓名 / Name")
        country = st.text_input("来自国家 / Country")
        contact = st.text_input("联系方式 / Contact Info (Email / WeChat / WhatsApp)")
        submitted = st.form_submit_button("提交咨询 / Submit")

        if submitted:
            if name and contact:
                payload = {
                    "提交时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "业务类型": "留学咨询",
                    "姓名": name,
                    "国家": country,
                    "联系方式": contact
                }
                save_to_csv(payload)
                st.success("✅ 提交成功！我们的专属顾问将在24小时内联系您。")
                st.balloons()
            else:
                st.error("⚠️ 姓名和联系方式为必填项哦！")

# ---------- 标签页2：文旅 ----------
with tab2:
    st.header("东北特色文旅路线")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("❄️ 冰雪奇观深度游")
        st.write("哈尔滨冰雪大世界 - 雪乡 - 亚布力")
        with st.expander("查看冰雪路线详情 👉"):
            st.markdown("""
            **✨ 行程亮点：**
            - 2至6人精致小团，全程纯玩无购物
            - 提供优先入园、专属交通与外语导游服务
            - 沉浸式体验哈尔滨冰雪与长白山天池
            """)
            with st.form("snow_tour_form"):
                snow_contact = st.text_input("留个联系方式，获取双语行程单：")
                snow_submitted = st.form_submit_button("立即获取")
                if snow_submitted:
                    if snow_contact:
                        payload = {
                            "提交时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "业务类型": "文旅-冰雪游",
                            "姓名": "",
                            "国家": "",
                            "联系方式": snow_contact
                        }
                        save_to_csv(payload)
                        st.success("✅ 行程单已发送至您的联系方式！")
                    else:
                        st.error("⚠️ 请填写联系方式哦！")

    with col2:
        st.subheader("🌿 广袤草原与民俗探秘")
        st.write("内蒙古东部草原 - 延吉朝鲜族风情")
        with st.expander("查看民俗路线详情 👉"):
            st.markdown("""
            **✨ 行程亮点：**
            - 深度游玩呼伦贝尔、满洲里、阿尔山
            - 沉浸式感受草原自然风貌与游牧民俗文化
            - 支持独立小包团出行，随心定制行程
            """)
            with st.form("grass_tour_form"):
                grass_contact = st.text_input("留个联系方式，获取双语行程单：")
                grass_submitted = st.form_submit_button("立即获取")
                if grass_submitted:
                    if grass_contact:
                        payload = {
                            "提交时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "业务类型": "文旅-草原游",
                            "姓名": "",
                            "国家": "",
                            "联系方式": grass_contact
                        }
                        save_to_csv(payload)
                        st.success("✅ 行程单已发送至您的联系方式！")
                    else:
                        st.error("⚠️ 请填写联系方式哦！")

# ---------- 标签页3：商贸 ----------
with tab3:
    st.header("跨境好物与民间推荐官计划")
    st.write("加入我们的共创计划，分享东北源头智造与轻工好物。")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://picsum.photos/300/200?random=1", caption="基础日用轻工品")
        st.caption("东北轻纺产业带直供")
    with col2:
        st.image("https://picsum.photos/300/200?random=2", caption="新能源与智能终端")
        st.caption("契合一带一路市场需求")
    with col3:
        st.image("https://picsum.photos/300/200?random=3", caption="特色农副产品")
        st.caption("长白山/大兴安岭原产地")

    st.write("---")
    with st.expander("💼 申请成为民间推荐官，了解分佣机制 👉"):
        st.markdown("""
        **✨ 推荐官专属权益：**
        - **零门槛启动**：无需囤货，一键代发，全程物流跟踪
        - **丰厚佣金**：畅享真实利润分成，把社交流量变成收益
        - **专属支持**：提供跨境电商选品指导与多语种营销素材
        """)
        with st.form("ambassador_form"):
            amb_name = st.text_input("如何称呼您？ / Name")
            amb_country = st.text_input("您的母国是哪里？ / Home Country")
            amb_contact = st.text_input("联系方式 / Contact Info (WeChat/Email)")
            amb_submitted = st.form_submit_button("立即提交申请 / Apply Now")
            if amb_submitted:
                if amb_name and amb_contact:
                    payload = {
                        "提交时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "业务类型": "商贸推荐官申请",
                        "姓名": amb_name,
                        "母国": amb_country,
                        "联系方式": amb_contact
                    }
                    save_to_csv(payload)
                    st.success("✅ 申请已提交！商贸团队将尽快与您对接。")
                    st.balloons()
                else:
                    st.error("⚠️ 姓名和联系方式为必填项哦！")

# =============================================
# 6. 底部信息
# =============================================
st.write("---")
st.caption("© 2026 寰海青衿·关东焕新 | 让留学生成为东北振兴的民间力量")