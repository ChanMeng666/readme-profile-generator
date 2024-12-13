import streamlit as st
from pathlib import Path
import re
import urllib.parse

def load_template(template_path):
    """加载 README 模板文件"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_template_variables(template_content):
    """从模板中提取所有变量"""
    pattern = r'\{\{(\w+)\}\}'
    return sorted(list(set(re.findall(pattern, template_content))))

def encode_url_safe(text):
    """将文本中的空格转换为 URL 安全的格式"""
    return urllib.parse.quote(text).replace('+', '%20')

def replace_template_variables(template_content, variables_dict):
    """替换模板中的所有变量，对特定字段进行 URL 编码"""
    url_encode_fields = ['full_name', 'bio']  # 需要 URL 编码的字段
    
    for key, value in variables_dict.items():
        if key in url_encode_fields and value:
            # 对特定字段进行 URL 编码
            encoded_value = encode_url_safe(value)
            template_content = template_content.replace(f'{{{{{key}}}}}', encoded_value)
        else:
            # 其他字段正常替换
            template_content = template_content.replace(f'{{{{{key}}}}}', value)
    
    return template_content

def create_badge(text, color="blue"):
    """创建技能徽章
    将空格替换为下划线，以确保徽章正确显示
    """
    # 处理空格
    text = text.strip()
    badge_text = text.replace(" ", "_")
    badge_logo = text.lower().replace(" ", "-")  # logo 使用连字符
    
    return f"![{text}](https://img.shields.io/badge/-{badge_text}-{color}?style=for-the-badge&logo={badge_logo}&logoColor=white)"

def process_skills(skills_text):
    """处理技能列表文本
    分割文本并生成徽章
    """
    if not skills_text:
        return ""
    
    # 分割技能并移除空白项
    skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
    # 生成徽章
    return " ".join([create_badge(skill) for skill in skills])

def create_project_fields(col, project_num):
    """创建单个项目的输入字段"""
    st.subheader(f"项目 {project_num}")
    project_data = {
        f'project_{project_num}_name': st.text_input(f"项目 {project_num} 名称", value="My Awesome Project", key=f"name_{project_num}"),
        f'project_{project_num}_link': st.text_input(f"项目 {project_num} 链接", value="#", key=f"link_{project_num}"),
        f'project_{project_num}_image': st.text_input(f"项目 {project_num} 图片", value="/path/to/project.png", key=f"image_{project_num}"),
        f'project_{project_num}_github': st.text_input(f"项目 {project_num} GitHub", value="#", key=f"github_{project_num}"),
        f'project_{project_num}_live': st.text_input(f"项目 {project_num} 演示链接", value="#", key=f"live_{project_num}"),
        f'project_{project_num}_point_1': st.text_input(f"项目 {project_num} 要点 1", value="Feature 1", key=f"point1_{project_num}"),
        f'project_{project_num}_point_2': st.text_input(f"项目 {project_num} 要点 2", value="Feature 2", key=f"point2_{project_num}"),
        f'project_{project_num}_point_3': st.text_input(f"项目 {project_num} 要点 3", value="Feature 3", key=f"point3_{project_num}")
    }
    return project_data

def create_project_html(project_num):
    """生成单个项目的 HTML 模板"""
    return f'''<td width="50%">
<h3 align="center">{{{{project_{project_num}_name}}}}</h3>
<div align="center">  
<a href="{{{{project_{project_num}_link}}}}" target="_blank">
<img src="{{{{project_{project_num}_image}}}}" width="50%" alt="{{{{project_{project_num}_name}}}}"/>
</a>
<br>
<br>
<p>
<a href="{{{{project_{project_num}_github}}}}" target="_blank">
<img src="https://img.shields.io/badge/View_on_GitHub-2ea44f?style=for-the-badge&logo=github"/>
</a>
<a href="{{{{project_{project_num}_live}}}}" target="_blank">
<img src="https://img.shields.io/badge/Live_Demo-brightgreen?style=for-the-badge&logo=vercel"/>
</a>
</p>
<p align="left">
• {{{{project_{project_num}_point_1}}}}<br>
• {{{{project_{project_num}_point_2}}}}<br>
• {{{{project_{project_num}_point_3}}}}
</p>
</div>
</td>'''

def generate_projects_section(num_projects):
    """生成项目展示区域的 HTML"""
    projects_html = []
    for i in range(0, num_projects, 2):
        row_html = f'''<tr>
{create_project_html(i + 1)}
{create_project_html(i + 2) if i + 1 < num_projects else ""}
</tr>'''
        projects_html.append(row_html)
    return "\n".join(projects_html)

def main():
    st.set_page_config(
        page_title="GitHub README Profile Generator",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("GitHub README Profile Generator")
    st.markdown("### 生成你的个性化 GitHub Profile README")

    # 加载默认模板
    template_path = Path("README_template.md")
    template_content = load_template(template_path)
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("基本信息")
        
        # 基本信息表单
        full_name = st.text_input("姓名", value="Chan Meng")
        bio = st.text_input("个人简介", value="A minimalist")
        github_username = st.text_input("GitHub 用户名", value="ChanMeng666")
        
        # 社交链接
        st.subheader("社交链接")
        portfolio_link = st.text_input("作品集链接", value="https://chanmeng.live/")
        linkedin_link = st.text_input("LinkedIn 链接", value="https://www.linkedin.com/in/chanmeng666/")
        
        # 日常行为
        st.subheader("日常行为")
        daily_routine_1 = st.text_input("日常行为 1", value="code")
        daily_routine_2 = st.text_input("日常行 2", value="eat")
        daily_routine_3 = st.text_input("日常行为 3", value="sleep")
        daily_routine_4 = st.text_input("日常行为 4", value="repeat")
        
        # 项目信息
        st.subheader("项目展示")
        num_projects = st.number_input("项目数量", min_value=1, max_value=10, value=2)
        
        # 存储所有项目数据
        all_project_data = {}
        for i in range(1, num_projects + 1):
            project_data = create_project_fields(col1, i)
            all_project_data.update(project_data)
        
        # 技能徽章
        st.subheader("技能栈")
        core_skills = st.text_area("核心技能 (用逗号分隔)", 
            value="React,Python,TypeScript,Machine Learning")
        frontend_skills = st.text_area("前端技能 (用逗号分隔)", 
            value="HTML5,CSS3,JavaScript,React Native")
        backend_skills = st.text_area("后端技能 (用逗号分隔)", 
            value="Node.js,MySQL,MongoDB")

        # 生成徽章
        core_skills_badges = process_skills(core_skills)
        frontend_skills_badges = process_skills(frontend_skills)
        backend_skills_badges = process_skills(backend_skills)

        # 其他信息
        st.subheader("其他信息")
        footer_text = st.text_area("页脚文本", value="Thanks for visiting my GitHub profile! Feel free to connect or check out my projects.")

        # 更新变量字典，加入项目数据
        variables = {
            'full_name': full_name or '',
            'bio': bio or '',
            'github_username': github_username,
            'portfolio_link': portfolio_link,
            'linkedin_link': linkedin_link,
            'daily_routine_1': daily_routine_1,
            'daily_routine_2': daily_routine_2,
            'daily_routine_3': daily_routine_3,
            'daily_routine_4': daily_routine_4,
            'core_skills_badges': core_skills_badges,
            'frontend_skills_badges': frontend_skills_badges,
            'backend_skills_badges': backend_skills_badges,
            'footer_text': footer_text,
            **all_project_data  # 添加所有项目数据
        }

        # 动态生成项目部分的模板内容
        template_content = template_content.replace(
            "<!-- Featured Projects Section -->",
            f'''<!-- Featured Projects Section -->
<table>
{generate_projects_section(num_projects)}
</table>'''
        )

        # 生成预览内容
        preview_content = replace_template_variables(template_content, variables)

    with col2:
        st.subheader("预览")
        st.markdown(preview_content, unsafe_allow_html=True)
        
        if st.button("复制全部内容"):
            st.code(preview_content, language="markdown")
            st.success("内容已复制到剪贴板!")

if __name__ == "__main__":
    main()
