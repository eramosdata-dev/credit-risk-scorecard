from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path

# ── Rutas ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
FIG_DIR = BASE_DIR / "reports" / "figures"
OUT_PDF = BASE_DIR / "reports" / "Credit_Risk_Scorecard_Report.pdf"

# ── Documento ─────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUT_PDF),
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm,
)

# ── Estilos ───────────────────────────────────────────────────
styles = getSampleStyleSheet()

estilo_titulo = ParagraphStyle(
    "titulo",
    fontSize=24,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1A237E"),
    alignment=TA_CENTER,
    spaceAfter=8,
)
estilo_subtitulo = ParagraphStyle(
    "subtitulo",
    fontSize=13,
    fontName="Helvetica",
    textColor=colors.HexColor("#424242"),
    alignment=TA_CENTER,
    spaceAfter=20,
)
estilo_seccion = ParagraphStyle(
    "seccion",
    fontSize=14,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1565C0"),
    spaceBefore=16,
    spaceAfter=8,
)
estilo_texto = ParagraphStyle(
    "texto",
    fontSize=10,
    fontName="Helvetica",
    textColor=colors.HexColor("#212121"),
    spaceAfter=6,
    leading=16,
)
estilo_caption = ParagraphStyle(
    "caption",
    fontSize=9,
    fontName="Helvetica-Oblique",
    textColor=colors.HexColor("#757575"),
    alignment=TA_CENTER,
    spaceAfter=12,
)

# ── Contenido ─────────────────────────────────────────────────
contenido = []

# Título
contenido.append(Spacer(1, 1 * cm))
contenido.append(Paragraph("Credit Risk Scorecard", estilo_titulo))
contenido.append(
    Paragraph("Análisis y Modelado de Riesgo Crediticio", estilo_subtitulo)
)
contenido.append(
    HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1565C0"))
)
contenido.append(Spacer(1, 0.5 * cm))

# Contexto de negocio
contenido.append(Paragraph("1. Contexto de Negocio", estilo_seccion))
contenido.append(
    Paragraph(
        "Este proyecto construye un sistema de scoring crediticio siguiendo los estándares "
        "de la industria bancaria (Basel II). El objetivo es predecir la probabilidad de que "
        "un cliente entre en mora grave (90+ días) en los próximos 2 años, asignando una "
        "puntuación entre 300 y 850 donde mayor puntuación indica menor riesgo.",
        estilo_texto,
    )
)

# Dataset
contenido.append(Paragraph("2. Dataset", estilo_seccion))
data_tabla = [
    ["Campo", "Valor"],
    ["Fuente", "Give Me Some Credit — Kaggle"],
    ["Registros", "150,000 clientes"],
    ["Variables", "11 (10 predictoras + 1 target)"],
    ["Target", "Mora grave en los próximos 2 años"],
    ["Tasa de incumplimiento", "6.68%"],
]
tabla = Table(data_tabla, colWidths=[7 * cm, 9 * cm])
tabla.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.HexColor("#F5F5F5"), colors.white],
            ),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
contenido.append(tabla)
contenido.append(Spacer(1, 0.3 * cm))

# Hallazgos EDA
contenido.append(Paragraph("3. Hallazgos del Análisis Exploratorio", estilo_seccion))
contenido.append(
    Paragraph(
        "El análisis exploratorio reveló patrones claros de riesgo crediticio. "
        "El dataset presenta un desbalanceo significativo con solo el 6.68% de defaults. "
        "Las variables más predictivas son el historial de moras previas y la "
        "utilización del crédito rotativo.",
        estilo_texto,
    )
)

# Imagen edad
img_edad = FIG_DIR / "04_default_por_edad.png"
if img_edad.exists():
    contenido.append(Image(str(img_edad), width=14 * cm, height=7 * cm))
    contenido.append(
        Paragraph("Figura 1 — Tasa de default por segmento de edad", estilo_caption)
    )

# Imagen utilización
img_util = FIG_DIR / "06_default_por_utilizacion.png"
if img_util.exists():
    contenido.append(Image(str(img_util), width=14 * cm, height=7 * cm))
    contenido.append(
        Paragraph(
            "Figura 2 — Tasa de default por utilización de crédito", estilo_caption
        )
    )

# Imagen mora
img_mora = FIG_DIR / "07_default_por_mora90.png"
if img_mora.exists():
    contenido.append(Image(str(img_mora), width=14 * cm, height=7 * cm))
    contenido.append(
        Paragraph(
            "Figura 3 — Tasa de default por historial de mora 90+ días", estilo_caption
        )
    )

# Metodología
contenido.append(Paragraph("4. Metodología del Modelo", estilo_seccion))
contenido.append(
    Paragraph(
        "Se utilizó la metodología estándar de scoring crediticio basada en "
        "Weight of Evidence (WoE) e Information Value (IV) para la transformación "
        "y selección de variables, seguida de una Regresión Logística como modelo base. "
        "Esta metodología es la más utilizada en la industria bancaria por su "
        "interpretabilidad y cumplimiento regulatorio (Basel II).",
        estilo_texto,
    )
)

data_metodo = [
    ["Etapa", "Técnica", "Herramienta"],
    ["Selección de variables", "Information Value (IV)", "Scorecardpy"],
    ["Transformación", "Weight of Evidence (WoE)", "Scorecardpy"],
    ["Modelo", "Regresión Logística", "Scikit-learn"],
    ["Validación", "AUC-ROC, Gini, KS", "Scikit-learn"],
    ["Escala final", "PDO 20 puntos", "Scorecardpy"],
]
tabla_metodo = Table(data_metodo, colWidths=[5 * cm, 6 * cm, 5 * cm])
tabla_metodo.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.HexColor("#F5F5F5"), colors.white],
            ),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
contenido.append(tabla_metodo)
contenido.append(Spacer(1, 0.3 * cm))

# Resultados del modelo
contenido.append(Paragraph("5. Resultados del Modelo", estilo_seccion))

data_metricas = [
    ["Métrica", "Valor obtenido", "Benchmark industria", "Estado"],
    ["AUC-ROC", "0.8495", "> 0.70", "✓ Supera"],
    ["Gini", "0.6989", "> 0.35", "✓ Supera"],
    ["KS Statistic", "0.5474", "> 0.30", "✓ Supera"],
]
tabla_metricas = Table(data_metricas, colWidths=[4 * cm, 4 * cm, 4.5 * cm, 3.5 * cm])
tabla_metricas.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.HexColor("#F5F5F5"), colors.white],
            ),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#1565C0")),
            ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ]
    )
)
contenido.append(tabla_metricas)
contenido.append(Spacer(1, 0.3 * cm))

# Imagen ROC
img_roc = FIG_DIR / "10_curva_roc.png"
if img_roc.exists():
    contenido.append(Image(str(img_roc), width=12 * cm, height=9 * cm))
    contenido.append(
        Paragraph("Figura 4 — Curva ROC del modelo (AUC = 0.8495)", estilo_caption)
    )

# Scorecard
contenido.append(Paragraph("6. Scorecard y Segmentación de Cartera", estilo_seccion))
contenido.append(
    Paragraph(
        "El modelo fue convertido a un scorecard con escala 300-850 siguiendo "
        "la metodología PDO (Points to Double Odds = 20). La segmentación de "
        "cartera permite definir políticas crediticias claras por rango de riesgo.",
        estilo_texto,
    )
)

data_scorecard = [
    ["Rango", "% Cartera", "Tasa Default", "Política"],
    ["Muy bajo (750+)", "6.9%", "0.4%", "Aprobar automáticamente"],
    ["Bajo (700-750)", "58.3%", "1.7%", "Aprobar condiciones estándar"],
    ["Moderado (650-700)", "26.7%", "9.5%", "Revisar manualmente"],
    ["Alto (600-650)", "6.1%", "35.0%", "Pedir garantías"],
    ["Crítico (<600)", "1.9%", "51.2%", "Rechazar"],
]
tabla_sc = Table(data_scorecard, colWidths=[4 * cm, 3 * cm, 3.5 * cm, 5.5 * cm])
tabla_sc.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.HexColor("#F5F5F5"), colors.white],
            ),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("TEXTCOLOR", (2, 1), (2, 2), colors.HexColor("#43A047")),
            ("TEXTCOLOR", (2, 4), (2, 5), colors.HexColor("#E53935")),
            ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
        ]
    )
)
contenido.append(tabla_sc)
contenido.append(Spacer(1, 0.3 * cm))

# Imagen scores
img_scores = FIG_DIR / "11_distribucion_scores.png"
if img_scores.exists():
    contenido.append(Image(str(img_scores), width=14 * cm, height=7 * cm))
    contenido.append(
        Paragraph(
            "Figura 5 — Distribución de credit scores por grupo de riesgo",
            estilo_caption,
        )
    )

# Conclusiones
contenido.append(Paragraph("7. Conclusiones", estilo_seccion))
contenido.append(
    Paragraph(
        "El modelo desarrollado supera todos los benchmarks de la industria bancaria. "
        "Las tres variables más predictivas son el historial de mora 90+ días, "
        "la utilización del crédito rotativo y las moras de 30-59 días. "
        "El scorecard permite clasificar el 65% de la cartera como bajo riesgo "
        "con tasas de default inferiores al 2%, mientras identifica el 8% de "
        "clientes de alto riesgo con tasas superiores al 35%.",
        estilo_texto,
    )
)

# Stack tecnológico
contenido.append(Paragraph("8. Stack Tecnológico", estilo_seccion))
data_stack = [
    ["Herramienta", "Uso"],
    ["Python 3.10", "Lenguaje principal"],
    ["Pandas / NumPy", "Manipulación de datos"],
    ["Matplotlib / Seaborn", "Visualización"],
    ["DuckDB", "SQL analítico en local"],
    ["Scikit-learn", "Regresión logística"],
    ["Scorecardpy", "WoE, IV y scorecard"],
    ["Power BI", "Dashboard ejecutivo"],
]
tabla_stack = Table(data_stack, colWidths=[6 * cm, 10 * cm])
tabla_stack.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.HexColor("#F5F5F5"), colors.white],
            ),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
contenido.append(tabla_stack)

# Generar PDF
doc.build(contenido)
print(f"PDF generado → {OUT_PDF.resolve()}")
