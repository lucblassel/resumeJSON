import json
from datetime import datetime

def makeSocials(networks):
    socials = []
    for element in networks:
        socials.append(
            f"\\{element['network'].replace(' ', '')}{{{element['username']}}}"
        )
        if element["network"] == "google scholar":
            socials[-1] += "{}"
    return "\n".join(socials)

def makeLink(link, annot="More: "):
    if link == "": return ""
    shortened = link.replace("https://", "").replace("http://", "").replace("www.", "")
    for char in "\\$_&":
        shortened = shortened.replace(char, f"\{char}")
    return (
        f"\\href{{{link}}}{{{annot}\\tiny{{{shortened}}}}}"
    )

def makeHeader(headerDict):
    firstName, lastName = headerDict["name"].split()

    return (
        f"\\name{{{firstName}}}{{{lastName}}}\n"
        f"\\position{{{headerDict['label']}}}\n"
        f"\\address{{{headerDict['location']['city']} \\quad {headerDict['location']['countryCode']}}}\n"
        f"\\mobile{{{headerDict['phone'].replace(' ', '~')}}}\n"
        f"\\email{{{headerDict['email']}}}\n"
        f"{makeSocials(headerDict['profiles'])}"
    )


def makeDates(item):
    start = datetime.strptime(item['startDate'], "%Y-%m-%d").strftime("%b %Y")
    end = "Now"
    if (endStr:= item.get("endDate")) is not None and endStr != "":
        end = datetime.strptime(endStr, "%Y-%m-%d").strftime("%b %Y")
    return f"{start} - {end}"


def makeWorkHighlights(item):
    s = "\\begin{cvitems}\n"
    s += f"\\item{{\\textbf{{{item['summary']}}}}}\n"
    for highlight in item["highlights"]:
        s += f"\\item{{{highlight}}}\n"
    if (url := item.get("url")) is not None and url != "":
        s += f"\\item{{\\emph{{ {makeLink(url)} }} }}\n"
    return s + "\\end{cvitems}"


def makeWorkItem(workItem):
    return (
        "\\cventry\n"
        f"{{{workItem['position']}}}\n"  # Position
        f"{{{workItem['name']}}}\n"  # Institution name
        f"{{{workItem['location']}}}\n"  # Location
        f"{{{makeDates(workItem)}}}\n"  # dates
        "{\n"
        f"{makeWorkHighlights(workItem)}\n"
        "}\n"
    )

def makeEducationSummary(item):
    url = item.pop('url')
    score = item.pop('score', "")
    scoreLine = f"score: {score}~-~" if score != "" else ""
    courses = "\n".join([
        f"\\item{{{course}}}" for course in item['courses']
    ])
    if url is None:
        return ""
    return (
        "\\begin{cvitems}\n"
        f"{courses}\n"
        f"\\item{{{scoreLine}{makeLink(url)}}}\n"
        "\\end{cvitems}"
    )

def makeEducationItem(educationItem):
    return (
        "\\cventry\n"
        f"{{{educationItem['studyType']}:~{educationItem['area']}}}\n"  # Position
        f"{{{educationItem['institution']}}}\n"  # Institution name
        f"{{{educationItem['location']}}}\n"  # Location
        f"{{{makeDates(educationItem)}}}\n"  # dates
        "{\n"
        f"{makeEducationSummary(educationItem)}\n"
        "}\n"
    )


def makeWorkSection(workSection):
    items = "\n\n".join([
        makeWorkItem(item) for item in workSection
    ])
    return (
        "\\cvsection{Experience}\n"
        "\\begin{cventries}\n"
        f"{items}"
        "\\end{cventries}"
    )


def makeEducationSection(educationSection):
    items = "\n\n".join([
        makeEducationItem(item) for item in educationSection
    ])
    return (
        "\\cvsection{Education}\n"
        "\\begin{cventries}\n"
        f"{items}"
        "\\end{cventries}"
    )


def makeLanguageItem(languageItem):
    return (
        "\\cvhonor\n"
        f"{{{languageItem['fluency']}}}\n"
        f"{{{languageItem.get('additional','')}}}\n"
        "{}\n"
        f"{{{languageItem['language']}}}\n"
    )

def makeLanguages(languages):
    items = '\n'.join([
        makeLanguageItem(item) for item in languages
    ])
    return (
        "\\cvsection{Languages}\n"
        "\\begin{cvhonors}\n"
        f"{items}"
        "\\end{cvhonors}\n"
    )

def makePreamble():
    return (
        "\\documentclass[11pt, a4paper]{awesome-cv}\n"
        "\\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}\n"
        "\\fontdir[fonts/]\n"
        "\\colorlet{awesome}{awesome-darknight}\n"
        "\\setbool{acvSectionColorHighlight}{true}\n"
        r"\renewcommand{\acvHeaderSocialSep}{\quad\textbar\quad}"+"\n"
    )

def makeAuthors(authors):
    if len(authors) == 1:
        return authors[0]
    return ", ".join(authors[:-1]) + " and " + authors[-1]


def makePublicationItem(item):
    title = item['title']
    authors = makeAuthors(item['authors'])
    journal = f"\\textit{{{item['journal']}}}"
    date = parseDate(item['date'])
    doi = makeLink(item['doi'], "")

    return (
        f"\\item {authors}, \"{title}\", {journal} ({date}), {doi}\n"
    )


def parseDate(dateString):
    patterns = ["%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"]
    for pattern in patterns:
        try:
            date = datetime.strptime(dateString, pattern)
            return str(date.year)
        except:
            pass
    return dateString


def makePublicationSection(publications):
    items = '\n'.join([
        makePublicationItem(item) for item in publications
    ])
    return (
        "\\cvsection{Publications}\n"
        "\\begin{itemize}\n"
        f"{items}"
        "\\end{itemize}\n"
    )

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=False, default="resume.json")
    parser.add_argument('--output', required=False, default="tex/resume.tex")

    args = parser.parse_args()

    print(args)

    resume = json.load(open(args.input, "r"))

    preamble = makePreamble()
    header = makeHeader(resume["basics"])
    education = makeEducationSection(resume['education'])
    work = makeWorkSection(resume['work'])
    languages = makeLanguages(resume['languages'])
    publications = makePublicationSection(resume['publications'])

    document = (
f"""{preamble}

{header}

\\begin{{document}}

\\makecvheader
\\makecvfooter{{}}{{Luc Blassel \\quad\\cdotp\\quad CV}}{{}}

{work}
{education}
{publications}
{languages}

\\end{{document}}
""")

    with open(args.output, 'w') as out:
        out.writelines(document)

