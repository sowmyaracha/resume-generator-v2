from pylatex import Document, Section, Subsection, Itemize, Command, NoEscape,Hyperref
from pylatex.utils import bold

# Define the resume content
resume_content = {
    "name": "Sowmya Racha",
    "email": "sowmyar2024@gmail.com",
    "phone": "8178259725",
    "linkedin": "https://www.linkedin.com/in/sowmya-racha-a30678183/",
    "skills": [
    "C/C++", "Java", "Python", "SQL", "C#", "HTML", "CSS", "JavaScript", "RAG", "LangChain", "LangGraph", "AI Agents", "Chatbots", "LLM", "Llama3", "PyTorch", "Kafka", "CUDA", "PySpark", "Scala", "MLOps", "ETL", "Java Spring", "Microservices", "Maven", "GIT", "AWS", "EC2", "S3", "SageMaker", "Machine Learning", "Neural Networks", "TensorFlow", "ScikitLearn", "OpenCV", "Pandas", "matplotlib", "HuggingFace", "Diffusion models", "Transformers", "GCN", "Virtual Reality", "Unity3D", "Blender", "React", "NodeJS"
]
,
    "work_experience": [
        {
            "company": "Rich Products Corporation",
            "location": "Remote, USA",
            "duration": "Jan 2025 - Mar 2026",
            "position": "Software Engineer – AI",
            "achievements": [
                "Developed scalable RESTful APIs and microservices using Java, Spring Boot, and Kafka in a distributed microservices architecture, supporting high-volume product and order processing workflows."
                "Implemented OAuth2/JWT authentication and role-based access control (RBAC) using Spring Security, securing 20+ APIs across multiple services."
                "Designed event-driven architecture using Apache Kafka, enabling real-time inventory and order processing across distributed systems."
                "Deployed cloud-native applications on AWS (EC2, RDS, S3) using Docker and implemented CI/CD pipelines using Jenkins, reducing deployment time by 40%."
                "Improved application performance and database performance by 30% through query optimization, indexing, and backend performance tuning."
                "Built Angular single-page applications integrated with REST APIs, improving user workflow efficiency by 25%."
                "Accelerated development velocity by integrating GitHub Copilot and agentic AI tools into daily engineering workflows, improving code quality, test coverage, and delivery speed across microservices projects."
                "Collaborated with cross-functional teams including QA, DevOps, and product owners to deliver scalable features on time in Agile sprints."
                ]
        },
        {
            "company": "USAA- American Insurance and Financial Company",
            "location": "Hyderabad, India",
            "duration": "Aug 2021 - Feb 2024",
            "position": "Fullstack Software Engineer",
            "achievements": [
                "Developed and maintained scalable microservices and REST/GraphQL APIs processing 10M+ daily transactions using Node.js, PostgreSQL, and MongoDB."
                "Improved backend performance by 25% through query optimization and system performance tuning."
                "Built responsive React applications using Redux and TypeScript, improving user engagement by 40%."
                "Implemented CI/CD pipelines and automated deployments, reducing release time by 30%."
                "Participated in system design, code reviews, and production deployments in an Agile/Scrum environment."
                "Integrated secure authentication and authorization mechanisms using JWT and OAuth standards for customer-facing applications."

            ]
        },
        {
            "company": "Quesite",
            "location": "Hyderabad, India",
            "duration": "Aug 2020 - May 2021",
            "position": "Software Developer",
            "achievements": [
                "Developed enterprise web applications using AngularJS, Core Java, and REST APIs for employee management and payroll systems."
                "Implemented client-side validation and exception handling, reducing data entry errors by 20%."
                "Designed SQL stored procedures, triggers, and scheduled jobs, automating payroll processing workflows."
                "Applied object-oriented design principles and modular architecture, improving code maintainability."
                "Used Git and worked in an Agile development environment." 
            ]
        }
    ],
    "projects": [
        {
            "title": "Automatic resume generator",
            "description": "Given Job descripton and user's current resume, it creates a new resume specific to the job. It rearranges the skills and highlights the main keywords given in the job description."
        },
        
        {
            "title": "AI agent for diet",
            "description": "Using LangChain, designed an AI agent chatbot to analyze and assist users using diet data stored in a PostgreSQL database. The AI agent can retrieve and process dietary information through various tools, including date-specific queries and custom SQL executions. Additionally, a user-friendly interface, built with Express.js, provides RESTful API endpoints to add, retrieve, update, and delete user meal records. The AI agent intelligently interacts with this database, ensuring accurate and responsive dietary tracking, while the UI facilitates seamless data management in real-time."
        },
        {
            "title": "Automatic YouTube Shorts generator",
            "description": "Developed an automatic YouTube short video generator using AI. The content, images, and voice are generated using LLMs, Diffusion models, and text-to-speech models from the Huggingface hub."
        },
        {
            "title": "Breast Cancer Detection",
            "description": "Used Pytorch to train extended VGG11 vision model on CBIS-DDSM dataset to classify breast cancer into 3 classes. After training on A100 GPU for few hours, the trained model accuracies were Train Accuracy: 71.34% , Validation Accuracy: 74.30%."
        },
        {
            "title": "Virtual Reality based Earth/Moon explorer",
            "description": "Developed a Virtual Reality (VR) application in Unity 3D using C# to explore Earth/Moon in VR. Used REST API to get geospatial data (height maps) of Earth and the Moon from usgs.gov, and converted the geospatial data into 3D models within the application. People can visit almost any place on Earth and the Moon in VR."
        },
        {
            "title": "Diffusion model to generate faces",
            "description": "Created a diffusion model using the Huggingface Diffusers library. Trained a UNet2D model from scratch on the MetFaces dataset using Google Colab Pro to generate human faces resembling works of art."
        },
        {
            "title": "Automatic Job applications",
            "description": "I am using LLMs and webdriver to apply to jobs automatically. The LLM reads the source HTML and screenshot of the webpage to identify what needs to be filled. I am sending random keys into text fields to identify which text field corresponds to which information. (for example, I send xyz to \"first name\" field, I ask the LLM what is the text within \"first name\" field, based on that we can map the input field to 'first name' dictionary entry, which contains my first name, I send the correct key now). Predefined questions are given to LLM and I process the responses to fill my details in a job application."
        }
    ],
    "education": [
        {
            "school": "University of Texas at Arlington",
            "location": "Texas, USA",
            "duration": "Jan 2024 - Dec 2025",
            "degree": "M.S. in Mathematics and Computer Science",
            "gpa": "3.9/4.0",
            "specialization": "Big Data and Machine Learning"
        },
        {
            "school": "Srinidhi Institute of Science and Technology",
            "location": "Hyderabad, India",
            "duration": "Aug 2017 - May 2021",
            "degree": "B.Tech in Computer Science",
        }
    ]
}
def main():
    # Create the LaTeX document with reduced margins
    doc = Document(page_numbers=False, geometry_options={"top": "0.75in", "bottom": "0.75in", "left": "0.75in", "right": "0.75in"})


    doc.packages.append(NoEscape(r'\usepackage{hyperref}'))

    # Add the name and contact information
    with doc.create(Section(resume_content["name"], numbering=False)):
        doc.append(NoEscape(f"{resume_content['email']} | {resume_content['phone']} | "))
        #doc.append(NoEscape(f"Portfolio | {resume_content['portfolio']} | {resume_content['linkedin']}"))
        portfolio_link = f"\\href{{{resume_content['portfolio']}}}{{Portfolio | }}"
        linkedin_link = f"\\href{{{resume_content['linkedin']}}}{{LinkedIn}}"

        doc.append(NoEscape(f"{portfolio_link} | {linkedin_link}"))

    # Add the skills section
    with doc.create(Section("Skills", numbering=False)):
        for i in range(len(resume_content["skills"])-1):
            skill = resume_content["skills"][i]
            doc.append(skill+", ")
        doc.append(resume_content["skills"][-1])

    # Add the work experience section
    with doc.create(Section("Work Experience", numbering=False)):
        for experience in resume_content["work_experience"]:
            with doc.create(Subsection(f"{experience['company']} | {experience['location']}", numbering=False)):
                doc.append(NoEscape(f"{experience['duration']}"))
                doc.append("\n")
                doc.append(bold(experience["position"]))
                with doc.create(Itemize()) as item_list:
                    for achievement in experience["achievements"]:
                        item_list.add_item(achievement)

    # Add the projects section
    with doc.create(Section("Project Work", numbering=False)):
        for project in resume_content["projects"]:
            with doc.create(Subsection(project["title"], numbering=False)):
                doc.append(project["description"])

    # Add the education section
    with doc.create(Section("Education", numbering=False)):
        for edu in resume_content["education"]:
            with doc.create(Subsection(f"{edu['school']} | {edu['location']}", numbering=False)):
                doc.append(NoEscape(f"{edu['duration']}"))
                doc.append("\n")
                doc.append(bold(edu["degree"]))
                if "gpa" in edu:
                    doc.append(NoEscape(f"GPA: {edu['gpa']}"))
                if "specialization" in edu:
                    doc.append(NoEscape(f"Specialty areas: {edu['specialization']}"))

    # Generate the PDF
    doc.generate_pdf("resume", clean_tex=True)
if __name__ == "__main__":
    main()
