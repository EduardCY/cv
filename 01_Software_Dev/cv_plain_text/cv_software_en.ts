/**
 * @fileoverview Typed definition of Eduard Criollo Yule's Professional Resume
 * for Software Development, Artificial Intelligence, and Data Science (English Edition).
 * 
 * @module SoftwareResumeEN
 * @author Eduard Criollo Yule
 * @version 2.1.0
 * @see {'../../data/profile_software_en.json'} SSOT Data Source
 */

export interface ContactInfo {
  phone: string;
  email: string;
  location: string;
  platzi: string;
  github: string;
  linkedin: string;
}

export interface AcademicMetric {
  id: string;
  badge: string;
  title: string;
  score: string;
  level: string;
  breakdown: string;
  institution: string;
  date: string;
}

export interface EducationEntry {
  degree: string;
  institution: string;
  period: string;
  status: string;
  location: string;
  highlights: string[];
}

export interface ExperienceEntry {
  role: string;
  organization: string;
  period: string;
  location: string;
  responsibilities: string[];
  technologies: string[];
}

export interface SkillCategory {
  category: string;
  skills: string[];
}

export interface LanguageProficiency {
  language: string;
  level: string;
  certification?: string;
  notes: string;
}

export interface SoftwareProfile {
  personal: {
    name: string;
    headline: string;
    subtitle: string;
    location: string;
    contact: ContactInfo;
    summary_hook: string;
  };
  metrics: AcademicMetric[];
  education: EducationEntry[];
  experience: ExperienceEntry[];
  skills_matrix: Record<string, SkillCategory>;
  soft_skills: string[];
  languages: LanguageProficiency[];
}

export const SOFTWARE_PROFILE_DATA_EN: SoftwareProfile = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "_comment": "==============================================================================\n MASTER FILE: SOFTWARE DEVELOPMENT PROFILE (ENGLISH - SINGLE SOURCE OF TRUTH)\n Location: /data/profile_software_en.json\n Purpose: Centralize professional, academic, metrics, and technical skill data\n          for Eduard Criollo Yule in Software Engineering & AI.\n==============================================================================",
  "personal": {
    "name": "Eduard Criollo Yule",
    "headline": "Full Stack Developer & AI / Data Science Specialist",
    "subtitle": "Systems Engineering Student • C1 CEFR Accredited (Oxford University Press)",
    "location": "Cali, Valle del Cauca, Colombia",
    "photo": "../../data/img/FotoPerfil_01.JPG",
    "banner": "../../data/img/banner.jpg",
    "contact": {
      "phone": "+57 314 ••• ••••",
      "email": "eduardcriolloyule2004@gmail.com",
      "platzi": "https://platzi.com/@EduardYule/",
      "github": "https://github.com/EduardCY",
      "linkedin": "https://www.linkedin.com/in/eduard-criollo-yule/"
    },
    "social_links": [
      {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com/in/eduard-criollo-yule/",
        "icon": "linkedin",
        "label": "Professional LinkedIn Profile"
      },
      {
        "name": "GitHub",
        "url": "https://github.com/EduardCY",
        "icon": "github",
        "label": "Source Code & Repositories"
      },
      {
        "name": "Platzi",
        "url": "https://platzi.com/@EduardYule/",
        "icon": "platzi",
        "label": "Verified Learning Paths"
      },
      {
        "name": "Email",
        "url": "mailto:eduardcriolloyule2004@gmail.com",
        "icon": "email",
        "label": "Direct Contact"
      }
    ],
    "summary_hook": "Software Engineer specialized in designing and engineering Full Stack enterprise solutions, leveraging Spring Boot, Angular, FastAPI, Flask, and Java. I enhance my technical profile with solid expertise in Artificial Intelligence and Data Science, building predictive models and end-to-end data analytics pipelines.\n\nCurrently pursuing a Systems Engineering degree at Universidad Autónoma de Occidente, with rigorous foundations in relational database design and normalization (SQL), RESTful API design, and distributed scalable architectures. Certified with advanced English proficiency (C1 CEFR by Oxford University Press).\n\nDemonstrated leadership in technical coordination, infrastructure deployment, and incident management in fast-paced multidisciplinary environments, including the 2021 Junior Pan American Games."
  },
  "metrics": [
    {
      "id": "oopt",
      "badge": "Language Proficiency C1",
      "title": "Oxford Placement Test (OOPT)",
      "score": "93 / 120",
      "level": "C1 CEFR Level (Advanced Professional)",
      "breakdown": "Use of English: 93/C1 | Listening: 92/C1",
      "institution": "Oxford University Press / Colombo Americano",
      "date": "2021-09-13"
    },
    {
      "id": "fullstack_ai_cert",
      "badge": "Enterprise Accreditation",
      "title": "Full Stack & Artificial Intelligence",
      "score": "Triple Certification",
      "level": "Enterprise Architecture & Applied AI",
      "breakdown": "Spring Boot • Angular • FastAPI • Scikit-Learn",
      "institution": "Dev Senior Code (Miami, FL)",
      "date": "2025 - 2026"
    },
    {
      "id": "database_mastery",
      "badge": "Technical Foundation",
      "title": "Database Engineering & SQL",
      "score": "Advanced",
      "level": "Relational Data Modeling & Normalization",
      "breakdown": "PostgreSQL • MySQL • SQLite • Query Optimization",
      "institution": "Universidad Autónoma de Occidente",
      "date": "2022 - Present"
    }
  ],
  "experience": [
    {
      "role": "Technical Volunteer & Infrastructure Support",
      "organization": "I Junior Pan American Games Cali 2021",
      "company": "I Junior Pan American Games Cali 2021",
      "location": "Cali, Colombia",
      "period": "Nov 2021 – Dec 2021",
      "responsibilities": [
        "Delivered end-to-end technical support and logistical deployment across mission-critical technological infrastructure during international sports competitions.",
        "Assembled, diagnosed, and tested computing hardware and real-time network connectivity under high-concurrency conditions.",
        "Collaborated with broadcast engineers in live multi-camera transmissions, audio feeds, and multi-venue digital workflows.",
        "Demonstrated agility, multidisciplinary teamwork, and swift troubleshooting under strict operational timelines."
      ]
    }
  ],
  "education": [
    {
      "degree": "B.S. in Systems Engineering",
      "institution": "Universidad Autónoma de Occidente (UAO)",
      "period": "2022 – Present",
      "status": "In Progress (Active Student)",
      "location": "Cali, Colombia",
      "highlights": [
        "Core Focus: Software Architecture, Advanced Data Structures, Relational Databases (SQL), Operating Systems, and Distributed Computing.",
        "Exemplary academic record with active participation in advanced systems design and algorithmic research."
      ]
    },
    {
      "degree": "Technical Baccalaureate in Industrial Drafting",
      "institution": "Instituto Técnico Industrial San Juan Bosco",
      "period": "2014 – 2021",
      "status": "Graduated with Honors",
      "location": "Cali, Colombia",
      "highlights": [
        "Rigorous 7-year technical education in precision engineering drafting, spatial geometry, blueprint interpretation, and systematic analytical methodology."
      ]
    }
  ],
  "skills_matrix": {
    "ai_data": {
      "category": "Artificial Intelligence & Data Science",
      "skills": [
        "Machine Learning",
        "Scikit-Learn",
        "Predictive Modeling",
        "Scientific Python",
        "Pandas",
        "NumPy",
        "Data Preprocessing",
        "Supervised & Unsupervised Learning",
        "Business Analytics"
      ]
    },
    "backend": {
      "category": "Backend & Cloud Microservices",
      "skills": [
        "Java (17+)",
        "Spring Boot 3",
        "Python (3.11+)",
        "FastAPI",
        "Flask",
        "PHP",
        "RESTful APIs",
        "Layered Architecture",
        "Microservices",
        "JWT Auth",
        "Docker"
      ]
    },
    "database": {
      "category": "Database Engineering & Storage",
      "skills": [
        "Relational SQL",
        "Entity-Relationship Modeling",
        "Database Normalization (3NF)",
        "PostgreSQL",
        "PostGIS",
        "MySQL",
        "SQLite",
        "SQLAlchemy ORM",
        "Spring Data JPA"
      ]
    },
    "frontend": {
      "category": "Frontend & Reactive Systems",
      "skills": [
        "Angular",
        "TypeScript",
        "JavaScript (ES6+)",
        "React / Next.js",
        "Semantic HTML5",
        "Modern CSS (Variables/Grid/Flexbox)",
        "Tailwind CSS",
        "Responsive Design",
        "Accessibility (WCAG 2.1)"
      ]
    },
    "devops_tools": {
      "category": "DevOps, Tooling & Environments",
      "skills": [
        "Git & GitHub",
        "Docker Compose",
        "Kubernetes (k8s)",
        "Terraform (IaC)",
        "NGINX",
        "Linux / Bash",
        "Pip & Virtualenv",
        "VS Code",
        "Vagrant",
        "CI/CD Pipelines"
      ]
    }
  },
  "soft_skills": [
    "Critical & Analytical Thinking",
    "Structured Problem Solving",
    "Multidisciplinary Team Collaboration",
    "Assertive Technical Communication",
    "Agile Planning & Execution",
    "High Adaptability & Quick Learning"
  ],
  "languages": [
    {
      "language": "Spanish",
      "level": "Native",
      "certification": "Mother tongue"
    },
    {
      "language": "English",
      "level": "C1 (Advanced Professional)",
      "certification": "Oxford Placement Test (Score 93/120 — C1 CEFR)"
    }
  ]
};
