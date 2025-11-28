import json


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

    # Work Experience
    work = data.get("work", [])
    if work:
        latex.append(r"\section*{Experience}")
        for job in work:
            if "show" in job and job["show"] == False:
                continue
            latex.append(
                r"\textbf{%s} \hfill \textit{%s}\\"
                % (job.get("name", ""), job.get("position", ""))
            )
            date_range = f"{job.get('startDate','')} -- {job.get('endDate','Present')}"
            latex.append(r"\textit{%s}" % date_range)
            latex.append(r"\begin{itemize}")
            for hl in job.get("highlights", []):
                latex.append(r"\item %s" % hl)
            latex.append(r"\end{itemize}")
        latex.append(r"\vspace{2pt}")

    # Skills
    skills = data.get("skills", [])
    if skills:
        latex.append(r"\section*{Skills}")
        skill_list = [s.get("name", "") for s in skills]
        latex.append(", ".join(skill_list))
        latex.append(r"\vspace{2pt}")

    # Projects
    projects = data.get("projects", [])
    if projects:
        latex.append(r"\section*{Projects}")
        for idx, proj in enumerate(projects):
            proj_name = proj.get("name", "")
            proj_url = proj.get("url", "")
            project_demo = proj.get("demo","")
            proj_desc = proj.get("description", "")
            proj_stack = proj.get("stack","")
            proj_contributions = proj.get("contributions","")

            # Project name
            latex.append(r"\textbf{%s}\\" % proj_name)

            # if proj_desc:
            #     latex.append(r"\textit{%s}\\" % proj_desc)

            # Project URL if available
            if proj_url:
                latex.append(r"\textit{%s}" % proj_url)

            if proj_contributions:
                    latex.append(r"\begin{itemize}")
                    for contribution in proj_contributions:
                        latex.append(r"\item %s" % contribution)
                    latex.append(r"\end{itemize}")

 

            # Project stack if available
            if proj_stack:
                stack_text = ", ".join([r"\small{%s}" % tech for tech in proj_stack])
                latex.append(r"\small Tech: %s\\" % stack_text)
            

            # if idx != len(projects)-1:
            #     latex.append(r"\\")


        latex.append(r"\vspace{2pt}")


    #     latex.append(r"\section*{Awards}")
    #     for award in awards:
    #         title = award.get("title", "")
    #         awarder = award.get("awarder", "")
    #         summary = award.get("summary", "")
    #         position = award.get("position", "")

    #         # Award title
    #         latex.append(r"\textbf{%s}\\" % title)

    #         # Awarder if available
    #         if awarder:
    #             latex.append(r"\small %s\\" % awarder)

    #         if position:
    #             latex.append(r"\small %s\\" % position)

    #         if summary:
    #             latex.append(r"\textit{%s}\\" % summary)

    #         # Add spacing after each award
    #         latex.append(r"\vspace{3pt}")

    #         # Add spacing between awards section
    #     latex.append(r"\vspace{2pt}")

    # publications = data.get("publications", [])
    # if publications:
    #     latex.append(r"\section*{Publications}")
    #     for publication in publications:
    #         name = publication.get("name", "")
    #         url = publication.get("url", "")
    #         summary = publication.get("summary", "")
    #         publisher = publication.get("publisher", "")
    #         demo = publication.get("demo", "")

    #         # Publication name
    #         latex.append(r"\textit{%s}\\" % name)
    #         if publisher:
    #             latex.append(r"\small %s\\" % publisher)
    #         if url:
    #             latex.append(r"\small %s\\" % url)

    #         if demo:
    #             latex.append(r"\small Demo: %s\\" % demo)
    #         # latex.append(r"\small %s\\" % summary)

    #         # Add spacing after each publication
    #         # latex.append(r"\vspace{3pt}")

    #     latex.append(r"\vspace{2pt}")

    # Certifications
    certifications = data.get("certificates", [])
    if certifications:
        latex.append(r"\section*{Certifications}")
        for cert in certifications:
            name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            summary = cert.get("summary", "")
            url = cert.get("url", "")
            show = cert.get("show","")

            if show == False:
                continue

            latex.append(r"\textbf{%s}\\" % name)
            if issuer:
                latex.append(r"\small %s\\" % issuer)
            if url:
                latex.append(r"\small %s\\" % url)
            if summary:
                latex.append(r"\textit{%s}\\" % summary)

            # Add spacing after each certification
            # latex.append(r"\vspace{3pt}")

        latex.append(r"\vspace{2pt}")

    # Education
    edu = data.get("education", [])
    if edu:
        latex.append(r"\section*{Education}")
        for e in edu:
            latex.append(r"\textbf{%s}\\" % e.get("institution", ""))
            latex.append(r"%s in %s\\" % (e.get("studyType", ""), e.get("area", "")))
            latex.append(
                r"\textit{%s -- %s}\\" % (e.get("startDate", ""), e.get("endDate", ""))
            )
        latex.append(r"\vspace{2pt}")

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
