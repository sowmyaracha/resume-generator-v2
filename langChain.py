#!/usr/bin/env python

from fastapi import FastAPI, Request
from httpx import request
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from fastapi.responses import RedirectResponse
import google.oauth2.id_token
import google_auth_oauthlib.flow
import json
import secrets

load_dotenv()


class Extract_JD(BaseModel):
    requires_citizenship : str = Field("Does the job require US citizenship? Answer yes, no or not sure.")
    profile_relevance : str = Field("Write a cover letter based on this job description and user profile")

model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model="llama-3.1-8b-instant",
)

parser = StrOutputParser()

user_bg = ''

def get_user_bg(email=None):
    if email:
        import json as _json
        profile_path = f"user_data/{email}.json"
        if os.path.exists(profile_path):
            with open(profile_path, "r") as pf:
                profile = _json.load(pf)
            skills = ", ".join(profile.get("skills", []))
            exps = "\n".join([f"{e.get('position','?')} at {e.get('company','?')} ({e.get('duration','?')})" for e in profile.get("work_experience", [])])
            projs = "\n".join([f"{p.get('title','?')}: {p.get('description','?')}" for p in profile.get("projects", [])])
            edus = "\n".join([f"{e.get('degree','?')} at {e.get('school','?')} ({e.get('duration','?')})" for e in profile.get("education", [])])
            name = profile.get("name", "")
            email_val = profile.get("email", "")
            phone = profile.get("phone", "")
            linkedin = profile.get("linkedin", "")
            summary = profile.get("summary", "")
            return f"Name: {name}\nEmail: {email_val}\nPhone: {phone}\nLinkedIn: {linkedin}\n\nSummary: {summary}\n\nSkills: {skills}\n\nWork Experience:\n{exps}\n\nProjects:\n{projs}\n\nEducation:\n{edus}"
    return user_bg

skills_template_content = '''

Given the user skills {skills}
rearrange the skills based on the Job description. Make it appealing to the recruiter.
output should be comma separated skills.
'''
projects_template_content = '''
This is a work that I did alone when I was free, {project_content}
Rewrite the description such that it is more aligned with job description so that I can put it in projects section of my resume.
Make it very appealing to the recruiter.
output should a single paragraph less than 100 words.
'''




# 1. Create prompt template
system_template = '''
given the professional background of the user, {user_bg}
Provided the job description: {jd}  
'''

system_template = PromptTemplate(
    template=system_template,
    input_variables=["user_bg","jd"]  # Corrected input variables definition
)

skills_template = PromptTemplate(
    template=f"{system_template.template}\n\n{skills_template_content}",
    input_variables=["user_bg", "jd", "skills"]
)
projects_template= PromptTemplate(
     template=f"{system_template.template}\n\n{projects_template_content}",
     input_variables=["user_bg","jd","project_content"]
)



# 2. Create model
from langchain_groq import ChatGroq

model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model="llama-3.1-8b-instant",
)

# 3. Create parser
parser = StrOutputParser()


def process_JD(jd:str, bg:str=None):
    if bg is None:
        bg = user_bg
    prompt = f"""
Given the professional background of the user:
{bg}

And this job description:
{jd}

Write a professional cover letter addressed to the hiring manager.
- Start with "Dear Hiring Manager,"
- Highlight the most relevant skills and experience that match the job
- Keep it to 3 short paragraphs
- End with "Sincerely," followed by the user's full name from their profile above
Only output the cover letter, nothing else.
"""
    response = model.invoke(prompt)
    return response.content


# 4. Define chain
def process_project_chain(jd: str, project_content: str):
    # Fill the prompt with user-provided data
    prompt = projects_template.format(user_bg = user_bg, jd=jd,project_content=project_content)
    print(prompt)
    response = model.invoke(prompt)
    return response.content

    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^Here\'s a rewritten.*?:\n*', '', text, flags=re.MULTILINE)
    return text

def process_skills_chain(jd:str,skills:str):
    prompt = skills_template.format(user_bg=user_bg,jd=jd,skills=skills)
    #print(prompt)
    response = model.invoke(prompt)
    return response.content

    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text

# FastAPI model to handle input from the request body
class InputData(BaseModel):
    jd: str
    project_content: str

class ResumeContent(BaseModel):
    skills:str

class ResumeSkills(BaseModel):
     jd:str
     skills:str

class GenerateResumeInput(BaseModel):
    skills: str
    projects:list

class ExtractJDInput(BaseModel):
    jd:str

class ExtractResume(BaseModel):
    res:str

# 5. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SECRET_KEY'),
    https_only=False,
    same_site="lax",
    max_age=86400,
    session_cookie="resume_session"
)


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:8000/auth/callback')

@app.get("/auth/google")
async def google_login(request: Request):
    # If already logged in skip auth
    request.session.clear() 
    state = secrets.token_urlsafe(16)
    request.session['oauth_state'] = state
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&state={state}"
        f"&prompt=select_account"
        f"&access_type=online"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
async def google_callback(request: Request):
    try:
        state = request.query_params.get('state')
    
        code = request.query_params.get('code')
        import httpx
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'code': code,
                    'client_id': GOOGLE_CLIENT_ID,
                    'client_secret': GOOGLE_CLIENT_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'grant_type': 'authorization_code'
                }
            )
            token_data = token_response.json()
            
            userinfo_response = await client.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f"Bearer {token_data['access_token']}"}
            )
            user = userinfo_response.json()
        
        request.session['user'] = {
            'name': user.get('name'),
            'email': user.get('email'),
            'picture': user.get('picture')
        }
        response = RedirectResponse('/profile-setup', status_code=303)
        return response
    except Exception as e:
        print(f"OAuth error: {e}")
        return RedirectResponse('/login')


# 6. Create a route that accepts POST requests with the JD and project content
@app.post("/process")
async def process_input(input_data: InputData):
    # Get data from the request body
    jd = input_data.jd
    project_content = input_data.project_content
    
    # Run the chain with user-provided JD and project content
    output = process_project_chain(jd, project_content)
    return {"output": output}

@app.post("/process_jd")
async def process_jd(request: Request, input_data: ExtractJDInput):
    user = request.session.get('user')
    email = user['email'] if user else None
    jd = input_data.jd
    bg = get_user_bg(email)
    output = process_JD(jd, bg)
    return {"output": output}

jobDetails = []

@app.post("/save_to_csv")
async def save_to_csv(input_data: ExtractResume):
    res = input_data.res
    # save directly to CSV with just the resume content
    import csv
    with open("jobs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([res, "Waiting"])
    return

@app.post("/process_skills")
async def process_skills(input_data:ResumeSkills):
     
     jd = input_data.jd
     skills = input_data.skills
     print(jd,skills)
     output = process_skills_chain(jd,skills)
     return {"output":output}

@app.post("/processed_resume_content")
async def processed_resume_content(input_data:ResumeContent):
        skills = input_data.skills
        print(skills)

@app.get("/get-profile")
async def get_profile(request: Request):
    user = request.session.get('user')
    if not user:
        return {"error": "not logged in"}
    import json
    profile_path = f"user_data/{user['email']}.json"
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            return json.load(f)
    return {"error": "no profile found"}

@app.get("/")
async def UI(request: Request):
    if not request.session.get('user'):
        return RedirectResponse('/login')
    return RedirectResponse('/analyzer')

@app.get("/login")
async def login_page(request: Request):
    try:
        request.session.clear()
    except:
        pass
    return FileResponse("templates/login.html")

@app.get("/auth/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    request.session['user'] = {
        'name': user['name'],
        'email': user['email'],
        'picture': user['picture']
    }
    return RedirectResponse('/profile-setup')

@app.get("/auth/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    request.session['user'] = {
        'name': user['name'],
        'email': user['email'],
        'picture': user['picture']
    }
    return RedirectResponse('/profile-setup')

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse('/login')

@app.get("/profile-setup")
async def profile_setup(request: Request):
    if not request.session.get('user'):
        return RedirectResponse('/login')
    return FileResponse("templates/profile_setup.html")

@app.get("/user-info")
async def user_info(request: Request):
    user = request.session.get('user')
    if not user:
        return {"error": "not logged in"}
    return user

@app.post("/save-profile")
async def save_profile(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/login')
    data = await request.json()
    import json
    os.makedirs('user_data', exist_ok=True)
    with open(f"user_data/{user['email']}.json", 'w') as f:
        json.dump(data, f)
    return {"status": "saved"}


@app.get("/resume")
async def get_resume_content(request: Request):
    user = request.session.get('user')
    if user:
        import json
        profile_path = f"user_data/{user['email']}.json"
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = json.load(f)
            return {
                "skills": profile.get('skills', []),
                "projects": profile.get('projects', [])
            }
    return {
    }

@app.get("/populate_resumes")
async def get_resume_content():
    directory_path = 'resumes'
    files = os.listdir(directory_path)
    #print(files, "xyzz")
    return {
        "resumes": files
    }

@app.post("/generate_resume")
async def generate_resume(input_data: GenerateResumeInput):
    skills = input_data.skills
    projects = input_data.projects
    print(projects)
    
    return {"message": "Resume generated successfully"}

@app.get("/analyzer")
async def analyzer_page(request: Request):
    if not request.session.get('user'):
        return RedirectResponse('/login')
    return FileResponse("templates/analyzer.html")

class AnalyzeInput(BaseModel):
    jd: str

@app.post("/analyze")
async def analyze_resume(request: Request, input_data: AnalyzeInput):
    user = request.session.get('user')
    email = user['email'] if user else None
    jd = input_data.jd
    bg = get_user_bg(email)
    
    import json as _json, re
    profile = {}
    if email:
        profile_path = f"user_data/{email}.json"
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = _json.load(f)
    
    name = profile.get('name', 'Applicant')

    # Call 1 — scores and keywords
    prompt1 = f"""Analyze resume match. Respond ONLY with valid JSON.

USER PROFILE:
{bg}

JOB DESCRIPTION:
{jd}

JSON format:
{{
  "overall_score": <0-100>,
  "skills_score": <0-100>,
  "experience_score": <0-100>,
  "projects_score": <0-100>,
  "education_score": <0-100>,
  "present_keywords": ["15-20 short keywords from user profile skills and experience"],
  "missing_keywords": ["15-20 short keywords from JD not in profile"],
  "suggested_keywords": ["15-20 short keywords to strengthen profile for this role"]
}}
Return ONLY JSON."""

    # Call 2 — cover letter
    prompt2 = f"""Write a formal professional cover letter.

USER PROFILE:
{bg}

JOB DESCRIPTION:
{jd}

Requirements:
- Start with "Dear Hiring Manager,"
- Paragraph 1: Express strong interest in the role and company
- Paragraph 2: Highlight 3-4 specific skills and experiences from profile that match JD
- Paragraph 3: Mention 2 specific projects from profile relevant to this role
- Paragraph 4: Enthusiastic closing statement
- End with "Sincerely,\\n{name}"
- Minimum 250 words
- Formal professional tone

Return ONLY the cover letter text, no JSON."""

    # Call 3 — tailored projects
    projects = profile.get('projects', [])
    proj_text = "\n".join([f"- {p.get('title','')}: {p.get('description','')}" for p in projects])
    
    prompt3 = f"""Rewrite each project description to match this job description.

PROJECTS:
{proj_text}

JOB DESCRIPTION:
{jd}

For each project write 3-4 sentences using keywords from the JD. Make it compelling.

Respond ONLY with JSON:
{{
  "tailored_projects": [
    {{
      "title": "project title",
      "original": "original description",
      "tailored": "3-4 sentence rewrite using JD keywords"
    }}
  ]
}}"""

    try:
        r1 = model.invoke(prompt1)
        t1 = re.sub(r'^```json\s*', '', r1.content.strip())
        t1 = re.sub(r'\s*```$', '', t1)
        scores = _json.loads(t1)
    except:
        scores = {"overall_score":50,"skills_score":50,"experience_score":50,"projects_score":50,"education_score":50,"present_keywords":[],"missing_keywords":[],"suggested_keywords":[]}

    try:
        r2 = model.invoke(prompt2)
        cover_letter = r2.content.strip()
    except:
        cover_letter = f"Dear Hiring Manager,\n\nI am interested in this role.\n\nSincerely,\n{name}"

    try:
        r3 = model.invoke(prompt3)
        t3 = re.sub(r'^```json\s*', '', r3.content.strip())
        t3 = re.sub(r'\s*```$', '', t3)
        proj_result = _json.loads(t3)
        tailored_projects = proj_result.get('tailored_projects', [])
    except:
        tailored_projects = [{"title": p.get('title',''), "original": p.get('description',''), "tailored": p.get('description','')} for p in projects]

    return {
        **scores,
        "cover_letter": cover_letter,
        "tailored_projects": tailored_projects
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
