import streamlit as st
from pathlib import Path
import re
import urllib.parse

def load_template(template_path):
    """Load README template file"""
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
    """Create input fields for a single project"""
    st.subheader(f"Project {project_num}")
    project_data = {
        f'project_{project_num}_name': st.text_input(f"Project {project_num} Name", value="My Awesome Project", key=f"name_{project_num}"),
        f'project_{project_num}_link': st.text_input(f"Project {project_num} Link", value="#", key=f"link_{project_num}"),
        f'project_{project_num}_image': st.text_input(f"Project {project_num} Image URL", value="/path/to/project.png", key=f"image_{project_num}"),
        f'project_{project_num}_github': st.text_input(f"Project {project_num} GitHub Repository", value="#", key=f"github_{project_num}"),
        f'project_{project_num}_live': st.text_input(f"Project {project_num} Live Demo", value="#", key=f"live_{project_num}"),
        f'project_{project_num}_point_1': st.text_input(f"Project {project_num} Feature 1", value="Key feature or achievement", key=f"point1_{project_num}"),
        f'project_{project_num}_point_2': st.text_input(f"Project {project_num} Feature 2", value="Important functionality", key=f"point2_{project_num}"),
        f'project_{project_num}_point_3': st.text_input(f"Project {project_num} Feature 3", value="Technical highlight", key=f"point3_{project_num}")
    }
    return project_data

def create_project_html(project_num):
    """Generate HTML template for a single project"""
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
    """Generate HTML for the projects showcase section"""
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
    st.markdown("### Create Your Personalized GitHub Profile README")
    
    # Add introduction and tutorial
    st.info("""
    👋 Welcome! This tool helps you create an awesome GitHub profile README.md file in a few simple steps.
    
    **How to use this generator:**
    1. Fill in the forms in each section on the left
    2. Preview your README in real-time on the right
    3. When satisfied, click 'Copy Content' and paste it into your GitHub profile repository
    
    **To create your GitHub profile README:**
    1. Create a new repository with the same name as your GitHub username
    2. Initialize it with a README.md file
    3. Paste the generated content and commit changes
    """)

    # Load default template
    template_path = Path("README_template.md")
    template_content = load_template(template_path)
    
    # Create two-column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Basic Information")
        st.markdown("""
        This section forms the header of your profile. Make it personal and engaging!
        - **Name**: Your full name or preferred display name
        - **Bio**: A brief introduction about yourself (1-2 sentences)
        - **GitHub Username**: Your GitHub handle (used for generating links)
        """)
        
        # Basic information form
        full_name = st.text_input("Full Name", value="Chan Meng")
        bio = st.text_input("Bio", value="A passionate developer exploring the digital frontier")
        github_username = st.text_input("GitHub Username", value="ChanMeng666")
        
        # Social Links
        st.subheader("Social Links")
        st.markdown("""
        Connect with visitors through your professional networks.
        Add your portfolio and LinkedIn URLs to showcase your work and experience.
        """)
        portfolio_link = st.text_input("Portfolio Website", value="https://chanmeng.live/")
        linkedin_link = st.text_input("LinkedIn Profile", value="https://www.linkedin.com/in/chanmeng666/")
        
        # Daily Routine
        st.subheader("Daily Routine")
        st.markdown("""
        Share your daily activities in a fun way! These will be displayed as an animated cycle.
        Example: code → learn → create → repeat
        """)
        daily_routine_1 = st.text_input("Activity 1", value="code")
        daily_routine_2 = st.text_input("Activity 2", value="learn")
        daily_routine_3 = st.text_input("Activity 3", value="create")
        daily_routine_4 = st.text_input("Activity 4", value="repeat")
        
        # Projects Section
        st.subheader("Featured Projects")
        st.markdown("""
        Showcase your best work! For each project, you'll need:
        - Project name
        - Project link (repository or demo)
        - Screenshot/preview image
        - GitHub repository link
        - Live demo link
        - Key features/highlights (3 points)
        """)
        num_projects = st.number_input("Number of Projects", min_value=1, max_value=10, value=2)
        
        # Store project data
        all_project_data = {}
        for i in range(1, num_projects + 1):
            project_data = create_project_fields(col1, i)
            all_project_data.update(project_data)
        
        # Skills Section
        st.subheader("Skills & Technologies")
        st.markdown("""
        List your technical skills separated by commas. They'll be converted into beautiful badges!
        Example: Python, JavaScript, React, Docker
        
        Tip: Group similar skills together for better organization.
        """)
        core_skills = st.text_area("Core Skills", 
            value="React,Python,TypeScript,Machine Learning")
        frontend_skills = st.text_area("Frontend Skills", 
            value="HTML5,CSS3,JavaScript,React Native")
        backend_skills = st.text_area("Backend Skills", 
            value="Node.js,MySQL,MongoDB")

        # Generate badges
        core_skills_badges = process_skills(core_skills)
        frontend_skills_badges = process_skills(frontend_skills)
        backend_skills_badges = process_skills(backend_skills)

        # Additional Information
        st.subheader("Footer Message")
        st.markdown("""
        Add a personal touch with a closing message to your profile visitors.
        This appears at the bottom of your profile README.
        """)
        footer_text = st.text_area("Footer Message", 
            value="Thanks for visiting my GitHub profile! Feel free to connect or check out my projects.")

        # Update variable dictionary, add project data
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
            **all_project_data  # Add all project data
        }

        # Dynamic generate project section template content
        template_content = template_content.replace(
            "<!-- Featured Projects Section -->",
            f'''<!-- Featured Projects Section -->
<table>
{generate_projects_section(num_projects)}
</table>'''
        )

        # Generate preview content
        preview_content = replace_template_variables(template_content, variables)

    with col2:
        st.subheader("Live Preview")
        st.markdown("""
        See how your README looks in real-time. 
        When you're ready, click 'Copy Content' below to get the markdown code.
        """)
        st.markdown(preview_content, unsafe_allow_html=True)
        
        if st.button("Copy Content"):
            st.code(preview_content, language="markdown")
            st.success("""
            Content copied! To update your GitHub profile:
            1. Go to your profile repository (username/username)
            2. Edit README.md
            3. Paste this content and commit changes
            """)

if __name__ == "__main__":
    main()
