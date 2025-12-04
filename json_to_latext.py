import json
from util import get_section_renderers


def json_to_latex(data):
    latex = []

    # Document preamble
    latex.append(
        r"""\documentclass[a4paper,10pt]{article}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\usepackage{xcolor}
\geometry{margin=0.8in}
\pagenumbering{gobble}
\titleformat{\section}{\large\bfseries\color{blue!70!black}}{}{0em}{}[\titlerule]
\titlespacing*{\section}{0pt}{2pt}{2pt}
\setlist[itemize]{noitemsep, topsep=2pt, leftmargin=1.5em}
\begin{document}
"""
    )

    # Basics
    basics = data.get("basics", {})
    name = basics.get("name", "")
    label = basics.get("label", "")
    email = basics.get("email", "example@email.com")
    phone = basics.get("phone", "+00000000000")
    video_introduction = basics.get("video_introduction", "")

    # Try to find LinkedIn from profiles
    linkedin = None
    for p in basics.get("profiles", []):
        if "linkedin" in p.get("network", "").lower():
            linkedin = p.get("url", "")
            break

    # Header section (name + contact info)
    latex.append(r"\begin{center}")
    latex.append(r"\Large \textbf{%s}\\[3pt]" % name)
    latex.append(r"\normalsize %s\\[2pt]" % label)
    latex.append(r"\small %s \\phone %s\\[2pt]" % (email, phone))
    if linkedin:
        latex.append(r"\small LinkedIn: %s\\[2pt]" % linkedin)

    latex.append(r"\small Video Introduction: %s\\[2pt]" % video_introduction)

    latex.append(r"\end{center}")

    # Get the fields to show and their order
    fields_to_show = data.get("fields_to_show", ["work", "skills", "projects", "certificates", "education"])

    # Get section renderers from utils
    section_renderers = get_section_renderers(data, latex)

    # Render sections in the order specified by fields_to_show
    for field in fields_to_show:
        if field in section_renderers:
            section_renderers[field]()

    # End
    latex.append(r"\end{document}")
    return "\n".join(latex)


if __name__ == "__main__":
    with open("resume.json") as f:
        data = json.load(f)
    tex = json_to_latex(data)
    with open("resume.tex", "w") as f:
        f.write(tex)
    print("✅ LaTeX resume saved as resume.tex (email, phone, and LinkedIn added)")
