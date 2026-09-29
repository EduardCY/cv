/**
 * @fileoverview Definición tipada de la Hoja de Vida y Perfil Creativo de Eduard Criollo Yule
 * para las áreas de Ilustración, Dibujo Técnico, Animación 2D/3D y Creación Literaria.
 * 
 * @module CreativeResume
 * @author Eduard Criollo Yule
 * @version 2.0.0
 * @see {@link ../../data/profile_creative.json} Fuente de datos madre
 */

/**
 * Disciplina artística formal.
 */
export interface ArtisticDiscipline {
  name: string;
  description: string;
  tools: string[];
}

/**
 * Distinción o galardón obtenido en certámenes o convocatorias.
 */
export interface AwardRecognition {
  title: string;
  organization: string;
  year: string;
  description: string;
}

/**
 * Estructura completa del perfil artístico.
 */
export interface CreativeProfile {
  personal: {
    name: string;
    headline: string;
    subtitle: string;
    location: string;
    summary_hook: string;
  };
  artistic_disciplines: ArtisticDiscipline[];
  awards_recognitions: AwardRecognition[];
  tools_matrix: string[];
}

/**
 * Instancia tipada del perfil creativo.
 */
export const CREATIVE_PROFILE_DATA: CreativeProfile = {
  personal: {
    name: "Eduard Criollo Yule",
    headline: "Ilustrador, Animador 2D/3D & Escritor Creativo",
    subtitle: "Bachiller Técnico en Dibujo Industrial • Producción Audiovisual & Narrativa",
    location: "Cali, Valle del Cauca, Colombia",
    summary_hook: "Creador visual y narrador multidisciplinario con formación técnica sólida en Dibujo Técnico Industrial (Instituto San Juan Bosco) y estudios en Ingeniería de Sistemas. Fusiono el rigor geométrico, la perspectiva y el modelado espacial con la expresión artística en ilustración digital, animación 2D/3D y construcción de mundos narrativos. Galardonado en certámenes literarios y beneficiario de distinciones académicas por excelencia creativa y analítica. Experiencia en producción audiovisual, soporte técnico en transmisiones en vivo y gestión de eventos de escala internacional (Juegos Panamericanos Juveniles 2021)."
  },
  artistic_disciplines: [
    {
      name: "Dibujo Técnico & Ilustración Digital",
      description: "Dominio de dibujo técnico de precisión, geometría descriptiva, perspectiva axonométrica, diseño de personajes (character concept art), entintado digital y renderizado de iluminación.",
      tools: ["AutoCAD", "Clip Studio Paint", "Adobe Photoshop", "Adobe Illustrator"]
    },
    {
      name: "Animación 2D/3D & Motion Graphics",
      description: "Principios fundamentales de animación, modelado poligonal 3D en Blender, rigging básico, animación de keyframes y composición de motion design para piezas audiovisuales.",
      tools: ["Blender 3D", "Adobe After Effects", "Adobe Premiere Pro", "Audacity"]
    },
    {
      name: "Guionismo, Worldbuilding & Creación Literaria",
      description: "Estructuración dramática, arcos de personajes, diseño de universos fantásticos y de ciencia ficción, redacción de narrativa corta y guiones técnicos audiovisuales.",
      tools: ["Scrivener", "Notion", "Celtx", "LaTeX"]
    }
  ],
  awards_recognitions: [
    {
      title: "Ganador de Certámenes Literarios & Creación de Cuentos",
      organization: "Concursos de Expresión Literaria y Narrativa Juvenil",
      year: "2019 - 2021",
      description: "Primer lugar y menciones de honor en concursos de narrativa corta y ensayo."
    },
    {
      title: "Beca de Excelencia Académica y Creativa",
      organization: "Instituto Técnico Industrial San Juan Bosco",
      year: "2014 - 2021",
      description: "Reconocimiento continuo por alto rendimiento en dibujo técnico y redacción."
    }
  ],
  tools_matrix: [
    "Blender 3D", "Photoshop", "Illustrator", "After Effects", "Premiere Pro", "Clip Studio Paint", "AutoCAD", "Scrivener", "Audacity"
  ]
};

/**
 * Representación en texto plano para sistemas ATS enfocados en perfiles creativos/editoriales.
 */
export const CREATIVE_ATS_PLAIN_TEXT: string = `==============================================================================
 EDUARD CRIOLLO YULE
 Ilustrador, Animador 2D/3D & Escritor Creativo • Bachiller Técnico en Dibujo
==============================================================================
 Teléfono : +57 314 ••• ••••
 Correo   : eduardcriolloyule2004@gmail.com
 Ubicación: Cali, Valle del Cauca, Colombia
 ArtStation: https://artstation.com/eduardyule
 Behance  : https://behance.net/eduardcriollo
 Idiomas  : Español (Nativo) | Inglés (C1 Avanzado - Oxford Placement Test 93/120)
------------------------------------------------------------------------------

[ PERFIL & DECLARACIÓN ARTÍSTICA ]
------------------------------------------------------------------------------
Creador visual y narrador multidisciplinario con formación técnica sólida en Dibujo
Técnico Industrial (Instituto San Juan Bosco) y estudios en Ingeniería de Sistemas.
Fusiono el rigor geométrico, la perspectiva y el modelado espacial con la expresión
artística en ilustración digital, animación 2D/3D y construcción de mundos narrativos.
Galardonado en certámenes literarios y beneficiario de distinciones académicas por
excelencia creativa y analítica. Experiencia en producción audiovisual, soporte
técnico en transmisiones en vivo y gestión de eventos de escala internacional (Juegos
Panamericanos Juveniles 2021).

[ DISTINCIONES & PREMIOS ]
------------------------------------------------------------------------------
* Ganador de Certámenes Literarios & Creación de Cuentos (2019 - 2021)
  Primer lugar y menciones de honor en concursos de narrativa corta y ficción especulativa.

* Beca de Excelencia Académica y Creativa — Instituto San Juan Bosco (2014 - 2021)
  Reconocimiento continuo por excelencia en dibujo técnico de precisión y redacción.

* Oxford Placement Test (OOPT) — Nivel C1 Avanzado (Score 93/120)
  Fluidez internacional para guionismo bilingüe y producción audiovisual en inglés.

[ DISCIPLINAS ARTÍSTICAS & COMPETENCIAS ]
------------------------------------------------------------------------------
* Dibujo Técnico & Ilustración Digital:
  Dibujo geométrico de precisión • Perspectiva axonométrica y cónica • Concept Art de personajes • Entintado digital • Iluminación volumétrica

* Animación 2D/3D & Motion Graphics:
  Modelado 3D poligonal (Blender) • Animación de keyframes • Timing & Spacing • Motion Graphics (After Effects) • Composición y corrección de color

* Creación Literaria & Guionismo:
  Worldbuilding • Desarrollo de arcos dramáticos • Guion técnico audiovisual • Ficción especulativa y Sci-Fi • Corrección de estilo

[ HERRAMIENTAS & SOFTWARE CREATIVO ]
------------------------------------------------------------------------------
Blender 3D • Adobe Photoshop • Adobe Illustrator • Adobe After Effects • Adobe Premiere Pro • Clip Studio Paint • AutoCAD • Scrivener • Audacity

[ FORMACIÓN ACADÉMICA & TÉCNICA ]
------------------------------------------------------------------------------
* Bachiller Técnico en Dibujo Técnico e Industrial (2014 - 2021)
  Institución: Instituto Técnico Industrial San Juan Bosco [Graduado con Mención de Honor]
  Enfoque    : 7 años de formación intensiva en diseño geométrico, proyecciones ortogonales y CAD

* Ingeniería de Sistemas (2022 - Presente)
  Institución: Universidad Autónoma de Occidente [En curso]
  Enfoque    : Gráficos computacionales, renderizado 3D e interfaces interactivas

[ EXPERIENCIA EN PRODUCCIÓN AUDIOVISUAL ]
------------------------------------------------------------------------------
* Asistente Técnico Audiovisual & Soporte Operativo — Juegos Panamericanos Juveniles 2021
  Periodo: Noviembre 2021 - Diciembre 2021
  Responsabilidades:
   - Apoyo operativo y técnico en transmisiones en vivo y monitoreo de cámaras.
   - Montaje de escenarios, cableado de señal multimedia y pantallas técnicas.

==============================================================================
 Fin del documento — Perfil Creativo en Formato Texto Plano ATS
==============================================================================`;
