# 🤖 AI Resume Analyzer

A full-stack AI-powered web application that analyzes your resume against any job description and helps you stand out to recruiters.

🔗 **Live Demo:** https://resume-generator-v2-byfx.onrender.com
🔗 **GitHub:** https://github.com/sowmyaracha/resume-generator-v2

---

## 📌 Overview

AI Resume Analyzer takes your profile and a job description, then uses LLM-powered analysis to give you a detailed match score, identify keyword gaps, generate a tailored cover letter, and rewrite your project descriptions to better align with the role.

---

## ✨ Features

- 🔐 **Google OAuth Authentication** — Secure login with persistent user profiles
- 📊 **Overall Match Score** — See how well your profile matches the job description
- 🧩 **Section-wise Breakdown** — Individual scores for Skills, Experience, Projects, and Education
- 🔍 **Keyword Analysis** — Identifies present keywords, missing keywords, and suggested additions
- ✉️ **AI Cover Letter Generator** — Generates a personalized, formal cover letter
- 📝 **Tailored Project Descriptions** — Rewrites your projects to better match the job requirements
- 💾 **Persistent User Profiles** — Your profile is saved and pre-filled on every login

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI/LLM | LangChain, Groq (LLaMA 3.1 8B) |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Google OAuth 2.0 |
| Storage | JSON-based user profiles |
| Deployment | Render.com |

---

## 🚀 How It Works

1. **Login** — Sign in with your Google account
2. **Profile Setup** — Enter your skills, work experience, projects, and education (saved for future use)
3. **Paste Job Description** — Copy any job description from LinkedIn, Indeed, etc.
4. **Analyze** — Get instant AI-powered feedback:
   - Match score with section breakdown
   - Missing and suggested keywords
   - Tailored cover letter
   - Rewritten project descriptions

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Groq API Key ([get one free](https://console.groq.com))
- Google OAuth credentials ([Google Cloud Console](https://console.cloud.google.com))

### Installation

```bash
# Clone the repo
git clone https://github.com/sowmyaracha/resume-generator-v2.git
cd resume-generator-v2

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SECRET_KEY=your_secret_key
REDIRECT_URI=http://localhost:8000/auth/callback
```

### Run the App

```bash
python3 langChain.py
```

Open http://localhost:8000 in your browser.

---

## 📁 Project Structure

```
resume-generator-v2/
├── langChain.py          # Main FastAPI server
├── templates/
│   ├── login.html        # Google login page
│   ├── profile_setup.html # 3-step profile setup
│   └── analyzer.html     # Main resume analyzer page
├── user_data/            # User profiles (gitignored)
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (gitignored)
```

---

## 🌐 Deployment

This app is deployed on **Render.com** with automatic deployments from the `main` branch on GitHub.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ If you found this useful, please give it a star!
