/**
 * @fileoverview Definición tipada de la Hoja de Vida y Perfil Profesional de Eduard Criollo Yule
 * para la carrera de Software Development, Inteligencia Artificial y Ciencia de Datos.
 * 
 * @module SoftwareResume
 * @author Eduard Criollo Yule
 * @version 2.1.0
 * @see {@link ../../data/profile_software.json} Fuente de datos madre
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

export const SOFTWARE_PROFILE_DATA: SoftwareProfile = {
  personal: {
    name: "Eduard Criollo Yule",
    headline: "Desarrollador Full Stack & Especialista en IA y Ciencia de Datos",
    subtitle: "Estudiante de Ingeniería de Sistemas • Acreditación C1 CEFR (Oxford)",
    location: "Cali, Valle del Cauca, Colombia",
    contact: {
      phone: "+57 314 ••• ••••",
      email: "eduardcriolloyule2004@gmail.com",
      platzi: "https://platzi.com/@EduardYule/",
      github: "https://github.com/EduardCY",
      linkedin: "https://www.linkedin.com/in/eduard-criollo-yule/"
    },
    summary_hook: "Desarrollador de Software con doble enfoque en arquitectura Full Stack empresarial (Spring Boot & Angular) y desarrollo de soluciones predictivas con Inteligencia Artificial y Ciencia de Datos. Estudiante activo de Ingeniería de Sistemas en la Universidad Autónoma de Occidente, con base técnica rigurosa en diseño y normalización de bases de datos relacionales SQL, construcción de APIs asíncronas de alto rendimiento con FastAPI / Flask / Java y dominio avanzado del idioma inglés (Nivel C1 certificado por Oxford University Press). Capacidad demostrada en coordinación técnica multidisciplinaria, despliegue de infraestructura y resolución de incidencias en certámenes internacionales (Juegos Panamericanos Juveniles 2021)."
  },
  metrics: [
    {
      id: "oopt",
      badge: "Dominio Lingüístico C1",
      title: "Oxford Placement Test (OOPT)",
      score: "93 / 120",
      level: "Nivel C1 CEFR (Avanzado Profesional)",
      breakdown: "Use of English: 93/C1 | Listening: 92/C1",
      institution: "Oxford University Press / Colombo Americano",
      date: "2021-09-13"
    },
    {
      id: "fullstack_ai_cert",
      badge: "Acreditación Empresarial",
      title: "Full Stack & Inteligencia Artificial",
      score: "Especialista Certificado",
      level: "Desarrollo Empresarial & Soluciones Inteligentes",
      breakdown: "Spring Boot • Angular • FastAPI • Scikit-Learn",
      institution: "Dev Senior Code (Miami, FL, USA)",
      date: "2025 - 2026"
    }
  ],
  education: [
    {
      degree: "Ingeniería de Sistemas",
      institution: "Universidad Autónoma de Occidente (UAO)",
      period: "2022 - Presente",
      status: "En curso",
      location: "Cali, Colombia",
      highlights: [
        "Énfasis en arquitectura de software distribuido, estructuras de datos y algoritmos avanzados.",
        "Modelado, diseño y normalización de bases de datos relacionales empresariales.",
        "Desarrollo de proyectos con metodologías ágiles e integración de componentes analíticos."
      ]
    },
    {
      degree: "Bachiller Técnico en Dibujo Técnico",
      institution: "Instituto Técnico Industrial San Juan Bosco",
      period: "2014 - 2021",
      status: "Graduado con Honores",
      location: "Cali, Colombia",
      highlights: [
        "Formación en diseño geométrico de precisión, dibujo industrial e interpretación técnica de planos.",
        "Desarrollo de pensamiento espacial, lógica matemática y disciplina analítica estructurada.",
        "Reconocimiento al mérito académico y distinciones por excelencia analítica."
      ]
    }
  ],
  experience: [
    {
      role: "Voluntario Técnico y Soporte Operativo de Infraestructura",
      organization: "Juegos Panamericanos Juveniles Cali 2021",
      period: "Noviembre 2021 - Diciembre 2021",
      location: "Cali, Colombia",
      responsibilities: [
        "Soporte técnico integral y despliegue logístico en operaciones clave de infraestructura tecnológica del certamen internacional.",
        "Montaje, diagnóstico, resolución de fallas y verificación de conectividad y equipos técnicos de red en tiempo real.",
        "Asistencia técnica operativa en transmisiones en vivo y monitoreo de sistemas audiovisuales multidisciplinarios para la cobertura del evento."
      ],
      technologies: ["Soporte Técnico de Red", "Hardware Diagnóstico", "Transmisión Audiovisual", "Coordinación Operativa"]
    }
  ],
  skills_matrix: {
    ai_data_science: {
      category: "Inteligencia Artificial & Ciencia de Datos",
      skills: ["Machine Learning", "Scikit-Learn", "Modelos Predictivos", "Ciencia de Datos", "NLP Básico", "Python Científico (Pandas, NumPy)", "FastAPI Microservicios"]
    },
    backend_architecture: {
      category: "Backend & Arquitectura de Microservicios",
      skills: ["Spring Boot 3", "Java Empresarial", "FastAPI Asíncrono", "Flask", "Python 3.11+", "PHP", "APIs RESTful", "Arquitectura por Capas", "Inyección de Dependencias"]
    },
    devops_cloud: {
      category: "Cloud, DevOps & DevSecOps",
      skills: ["Kubernetes (k8s)", "Terraform (IaC / HCL)", "Docker & Docker Compose", "GitHub Actions (CI/CD)", "NGINX (Canary Deployment / Ingress)", "Prometheus & Grafana", "OWASP ZAP"]
    },
    databases_persistence: {
      category: "Bases de Datos & Persistencia Relacional",
      skills: ["SQL Avanzado", "Diseño & Normalización Relacional", "PostgreSQL 15 (+ PostGIS)", "MySQL", "SQLite", "SQLAlchemy ORM (Async)", "Optimización de Consultas"]
    },
    frontend_ui: {
      category: "Frontend & Desarrollo Web",
      skills: ["React 19 / Next.js 14", "Angular", "TypeScript", "JavaScript ES6+", "PWA Serverless", "Tailwind CSS", "HTML5 Semántico", "CSS3 / Flexbox / Grid", "Diseño Responsivo"]
    },
    systems_low_level: {
      category: "Sistemas Operativos, Redes & Seguridad",
      skills: ["Linux Kernel (C Syscalls / Ring 0)", "Vagrant & Redes Virtuales", "Hardening Linux (IPTables / Fail2ban)", "Shell / Bash / PowerShell", "Git & GitHub", "VS Code", "Dibujo Técnico Industrial"]
    }
  },
  soft_skills: [
    "Pensamiento crítico y analítico",
    "Resolución estructurada de problemas complejos",
    "Trabajo en equipo multidisciplinario",
    "Comunicación técnica asertiva",
    "Planificación y gestión ágil de tareas",
    "Adaptabilidad y aprendizaje acelerado"
  ],
  languages: [
    {
      language: "Español",
      level: "Nativo",
      notes: "Lengua materna"
    },
    {
      language: "Inglés",
      level: "C1 Avanzado Profesional",
      certification: "Oxford Placement Test (Score 93/120 — CEFR C1)",
      notes: "Fluido en conversación técnica, comprensión auditiva y redacción técnica"
    }
  ]
};

export const SOFTWARE_ATS_PLAIN_TEXT: string = `==============================================================================
 EDUARD CRIOLLO YULE
 Desarrollador Full Stack • Especialista en IA & Data Science • Est. Ingeniería de Sistemas
==============================================================================
 Teléfono : +57 314 ••• ••••
 Correo   : eduardcriolloyule2004@gmail.com
 Ubicación: Cali, Valle del Cauca, Colombia
 LinkedIn : https://www.linkedin.com/in/eduard-criollo-yule/
 GitHub   : https://github.com/EduardCY
 Platzi   : https://platzi.com/@EduardYule/
 Idiomas  : Español (Nativo) | Inglés (C1 Avanzado - Oxford Placement Test 93/120)
------------------------------------------------------------------------------

[ PERFIL PROFESIONAL ]
------------------------------------------------------------------------------
Desarrollador de Software con doble enfoque en arquitectura Full Stack empresarial
(Spring Boot & Angular) y desarrollo de soluciones predictivas con Inteligencia
Artificial y Ciencia de Datos. Estudiante activo de Ingeniería de Sistemas en la
Universidad Autónoma de Occidente, con base técnica rigurosa en diseño y
normalización de bases de datos relacionales SQL, construcción de APIs asíncronas
de alto rendimiento con FastAPI / Flask / Java y dominio avanzado del idioma inglés
(Nivel C1 certificado por Oxford University Press). Capacidad demostrada en
coordinación técnica multidisciplinaria, despliegue de infraestructura y resolución
de incidencias en certámenes internacionales (Juegos Panamericanos Juveniles 2021).

[ ACREDITACIONES PROFESIONALES ]
------------------------------------------------------------------------------
* Oxford Placement Test (OOPT): 93 / 120 (Nivel C1 CEFR)
  Emisor: Oxford University Press / Colombo Americano
  Detalles: Use of English: 93/C1 | Listening: 92/C1

* Full Stack & Soluciones Inteligentes
  Emisor: Dev Senior Code (Miami, FL, USA)
  Detalles: Spring Boot • Angular • FastAPI • Scikit-Learn

[ PROYECTOS TÉCNICOS DESTACADOS (GITHUB @EduardCY) ]
------------------------------------------------------------------------------
* VeraMarket — Marketplace Universitario Geolocalizado (2025 - 2026)
  Subcategoría: Full Stack, Geolocalización & Microservicios
  Stack: FastAPI (Python 3.11+) • Next.js 14 • TypeScript • PostgreSQL + PostGIS • Docker Compose
  Métricas: Geolocalización PostGIS • Monorepo Desacoplado • PWA Mobile-First
  Descripción: Marketplace universitario con mapa interactivo del campus (UAO), FastAPI asíncrono, Next.js 14 y PostgreSQL PostGIS.
  Repositorio: Privado / Confidencial (Código disponible bajo solicitud técnica)

* Nexo — Plataforma de Rescate y Redistribución de Alimentos (2026)
  Subcategoría: PWA Serverless & Impacto Social
  Stack: TypeScript • Next.js / React • PWA Serverless • Tailwind CSS • Node.js
  Métricas: Bajo Impacto Operativo • Alta Eficiencia Social • Control de Cadena de Frío
  Descripción: PWA serverless para conectar restaurantes donantes de Cali con comedores comunitarios y coordinar rutas de transporte para voluntarios.
  Repositorio: Privado / Confidencial (Código disponible bajo solicitud técnica)

* SERVICIUDAD Cali — Sistema Empresarial con Despliegues Canarios (2026)
  Subcategoría: Arquitectura Empresarial & Despliegues Canarios
  Stack: Java 17+ • Spring Boot 3 • PostgreSQL • Docker Compose • NGINX Canary Proxy
  Métricas: Enrutamiento Ponderado 90/10 • Cero Downtime • Arquitectura Transaccional ACID
  Descripción: Sistema de gestión ciudadana con Spring Boot 3, PostgreSQL, Docker y despliegue canario ponderado en NGINX para cero caída de servicio.
  Repositorio: https://github.com/EduardCY/UAO-Software2-ServiCiudad-CanaryDeploy

* Infraestructura Cloud, Kubernetes & DevSecOps con OWASP ZAP (2026)
  Subcategoría: Infraestructura Cloud, IaC & DevSecOps
  Stack: Kubernetes (k8s) • Terraform (IaC / HCL) • Prometheus • Grafana • OWASP ZAP • NGINX Ingress
  Métricas: IaC Declarativo • Observabilidad en Tiempo Real • Auditoría DAST OWASP
  Descripción: Aprovisionamiento de red y clúster K8s con Terraform, observabilidad con Prometheus/Grafana y análisis de seguridad DAST con OWASP ZAP.
  Repositorio: https://github.com/EduardCY/UAO-DevOps-Kubernetes-Terraform-Pipeline

* Pipeline DevOps Integral CI/CD con Herramientas Libres (2026)
  Subcategoría: Automatización CI/CD & Cloud Delivery
  Stack: GitHub Actions • Docker • Node.js • Jest / Vitest • ESLint / Prettier • Render.com
  Métricas: Flujo CI/CD Automatizado • Zero-Intervention Deploy • Verificación Estricta
  Descripción: Pipeline automatizado de integración y entrega continua con validación de código, tests unitarios, build de imágenes Docker y deploy a Staging/Producción.
  Repositorio: https://github.com/EduardCY/UAO-DevOps-Pipeline-CI-CD

* Red Empresarial mediante Grafos & Optimización de Rutas (2026)
  Subcategoría: Estructuras de Datos Avanzadas & Algoritmos de Grafos
  Stack: React 19 • JavaScript ES6+ • Tailwind CSS 4 • Vite • Algoritmos Dijkstra / Prim / Kruskal
  Métricas: Cálculo de Rutas O(E log V) • Visualización de Topología Dinámica • React 19
  Descripción: Plataforma interactiva de modelado topológico y cálculo de rutas mínimas (Dijkstra) y árboles de recubrimiento mínimo (Prim/Kruskal).
  Repositorio: https://github.com/EduardCY/UAO-EDA2-Red-Empresarial-Grafos

* Investigación de Syscalls & Compilación del Kernel Linux (2026)
  Subcategoría: Sistemas Operativos de Bajo Nivel & Núcleo Linux
  Stack: C (Kernel Space) • Linux Kernel Source • glibc • Assembly • GRUB • Bash
  Métricas: Kernel Space (Ring 0) • Compilación de Kernel • Syscalls Personalizadas
  Descripción: Implementación de syscalls en C dentro del espacio de núcleo (Ring 0), modificación de sys_call_table y compilación cruzada del kernel Linux.
  Repositorio: https://github.com/EduardCY/UAO-SistemasOperativos-Kernel-Linux

* Laboratorio de Pentesting, Hardening & Redes Seguras con Vagrant (2026)
  Subcategoría: Ciberseguridad, Redes & Infraestructura Virtualizada
  Stack: Vagrant (IaC / Ruby) • VirtualBox • Ubuntu Linux • IPTables • Fail2ban • Bash
  Métricas: Entorno 100% Aislado y Reproducible • Hardening Linux • Segmentación de Red
  Descripción: Entorno de laboratorio virtualizado reproducible y aislado con Vagrant para pentesting ético y hardening Linux con IPTables y Fail2ban.
  Repositorio: https://github.com/EduardCY/UAO-SeguridadInformatica-Lab-Vagrant

* RIPS New 2025 — Motor de Validación y Procesamiento de Salud (2025 - 2026)
  Subcategoría: Ingeniería de Datos, Salud & Microservicios Asíncronos
  Stack: Python 3.11+ • FastAPI • Workers Asíncronos • PostgreSQL • SQLAlchemy ORM
  Métricas: Procesamiento Asíncrono por Lotes • Cumplimiento Normativo MinSalud
  Descripción: Ingesta, validación sintáctica/semántica y estructuración masiva de registros RIPS con workers asíncronos y PostgreSQL.
  Repositorio: Privado / Confidencial (Código disponible bajo solicitud técnica)

[ EDUCACIÓN ]
------------------------------------------------------------------------------
* Ingeniería de Sistemas (2022 - Presente)
  Institución: Universidad Autónoma de Occidente [En curso]
  Enfoque    : Arquitectura de software distribuido, estructuras de datos, cálculo y bases de datos

* Bachiller Técnico en Dibujo Técnico (2014 - 2021)
  Institución: Instituto Técnico Industrial San Juan Bosco [Graduado con Honores]
  Enfoque    : Diseño técnico de precisión, interpretación de planos y metodología analítica

[ EXPERIENCIA & COORDINACIÓN TÉCNICA ]
------------------------------------------------------------------------------
* Voluntario Técnico y Soporte Operativo — Juegos Panamericanos Juveniles Cali 2021
  Periodo: Noviembre 2021 - Diciembre 2021
  Responsabilidades:
   - Soporte técnico integral y despliegue logístico en operaciones clave de infraestructura tecnológica.
   - Montaje, diagnóstico y verificación de equipos y conectividad técnica de red en tiempo real.
   - Asistencia técnica en transmisiones en vivo y monitoreo de sistemas audiovisuales multidisciplinarios.

[ COMPETENCIAS TÉCNICAS ]
------------------------------------------------------------------------------
* Inteligencia Artificial & Datos:
  Machine Learning • Scikit-Learn • Data Science • NLP Básico • Modelos Predictivos • Python Científico

* Backend & Microservicios:
  Spring Boot 3 • FastAPI • Flask • Java Empresarial • Python 3.11+ • PHP • APIs RESTful • Arquitectura por Capas

* Cloud, DevOps & DevSecOps:
  Kubernetes (k8s) • Terraform (IaC) • Docker & Compose • GitHub Actions (CI/CD) • NGINX Canary • Prometheus & Grafana • OWASP ZAP

* Bases de Datos & Persistencia:
  SQL Relacional • PostgreSQL 15 (+ PostGIS) • MySQL • SQLite • SQLAlchemy (Async) • Modelado Entidad-Relación

* Frontend & Web UI:
  React 19 / Next.js 14 • Angular • TypeScript • JavaScript (ES6+) • PWA Serverless • Tailwind CSS • HTML5 • CSS3 Grid

* Sistemas Operativos & Seguridad:
  Linux Kernel (C Syscalls / Ring 0) • Vagrant • Hardening (IPTables / Fail2ban) • PowerShell / Bash • Git & GitHub

[ HABILIDADES BLANDAS ]
------------------------------------------------------------------------------
Pensamiento crítico y analítico • Resolución estructurada de problemas • Trabajo en equipo multidisciplinario • Comunicación técnica asertiva • Planificación ágil de tareas

[ IDIOMAS ]
------------------------------------------------------------------------------
* Español: Nativo — Lengua materna
* Inglés : C1 — Avanzado profesional (Fluido en lectura, escritura y conversación técnica)
  Acreditación: Oxford Placement Test (Score 93/120 — Nivel C1 CEFR)

==============================================================================
 Fin del documento — Formato Texto Plano ATS Optimizado
==============================================================================`;
