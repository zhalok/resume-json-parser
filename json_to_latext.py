import json

def json_to_latex(data):
    latex = []

    # Document preamble
    latex.append(r"""\documentclass[a4paper,10pt]{article}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\usepackage{xcolor}
\geometry{margin=0.8in}
\pagenumbering{gobble}
\titleformat{\section}{\large\bfseries\color{blue!70!black}}{}{0em}{}[\titlerule]
\setlist[itemize]{noitemsep, topsep=2pt, leftmargin=1.5em}
\begin{document}
""")

    # Basics
    basics = data.get("basics", {})
    name = basics.get("name", "")
    label = basics.get("label", "")
    email = basics.get("email", "example@email.com")
    phone = basics.get("phone", "+00000000000")

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
    latex.append(r"\small %s \\quad %s\\[2pt]" % (email, phone))
    if linkedin:
        latex.append(r"\small %s\\[4pt]" % linkedin)
    latex.append(r"\end{center}")

    # Work Experience
    work = data.get("work", [])
    if work:
        latex.append(r"\section*{Experience}")
        for job in work:
            if "show" in job and job["show"] == False:
                continue
            latex.append(r"\textbf{%s} \hfill \textit{%s}\\"
                         % (job.get("name", ""), job.get("position", "")))
            date_range = f"{job.get('startDate','')} -- {job.get('endDate','Present')}"
            latex.append(r"\textit{%s}" % date_range)
            latex.append(r"\begin{itemize}")
            for hl in job.get("highlights", []):
                latex.append(r"\item %s" % hl)
            latex.append(r"\end{itemize}")

    # Skills
    skills = data.get("skills", [])
    if skills:
        latex.append(r"\section*{Skills}")
        skill_list = [s.get("name", "") for s in skills]
        latex.append(", ".join(skill_list))

    # Education
    edu = data.get("education", [])
    if edu:
        latex.append(r"\section*{Education}")
        for e in edu:
            latex.append(r"\textbf{%s}\\"
                         % e.get("institution", ""))
            latex.append("%s in %s\\"
                         % (e.get("studyType", ""), e.get("area", "")))
            latex.append(r"\textit{%s -- %s}\\"
                         % (e.get("startDate", ""), e.get("endDate", "")))

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
