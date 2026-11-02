"""Build the filled template and the LaTeX reading companion from course JSON."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / 'course.json').read_text())
P = json.loads((ROOT / 'course_papers.json').read_text())
R = json.loads((ROOT / 'projects.json').read_text())
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
def tag(x): return '{'+W+'}'+x
def el(x, **attrs):
    e = E.Element(tag(x))
    for k,v in attrs.items(): e.set(tag(k), str(v))
    return e
def plain(s): return str(s).replace('–','-').replace('—','-').replace('’',"'").replace('“','"').replace('”','"')
def paragraph(text='', size=18, bold=False, keep=False):
    p=el('p'); pr=el('pPr'); pr.append(el('spacing',after=60,line=240,lineRule='auto'))
    if keep: pr.append(el('keepNext'))
    p.append(pr); r=el('r'); rp=el('rPr'); rp.append(el('rFonts',ascii='Calibri',hAnsi='Calibri'));rp.append(el('sz',val=size));rp.append(el('color',val='000000'))
    if bold: rp.append(el('b'))
    r.append(rp);t=el('t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=plain(text);r.append(t);p.append(r);return p
def setcell(cell, text):
    for n in list(cell):
        if n.tag != tag('tcPr'): cell.remove(n)
    for s in (text if isinstance(text,list) else text.split('\n')): cell.append(paragraph(s))
def rows(t):return t.findall('w:tr',NS)
def cells(t,r):return rows(t)[r].findall('w:tc',NS)
def patchpara(p,text):
    rpr=p.find('.//w:rPr',NS)
    for n in list(p):
        if n.tag!=tag('pPr'): p.remove(n)
    r=el('r')
    if rpr is not None:r.append(copy.deepcopy(rpr))
    t=el('t');t.text=plain(text);r.append(t);p.append(r)
def newpage(body,before=None):
    p=paragraph();r=el('r');r.append(el('br',type='page'));p.append(r)
    body.insert(body.index(before) if before is not None else len(body)-1,p)
def heading(body,text,size=24,page_break=False):
    p=paragraph(text,size,True,True)
    if page_break:p.find('w:pPr',NS).append(el('pageBreakBefore'))
    body.insert(len(body)-1,p)
def addp(body,text,keep=False):body.insert(len(body)-1,paragraph(text,20,keep=keep))

def build_docx(template):
    with ZipFile(template) as z: parts={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(parts['word/document.xml']);body=root.find('w:body',NS);ts=body.findall('w:tbl',NS);ps=body.findall('w:p',NS)
    patchpara(ps[2],'CS4308 Graph Machine Learning');patchpara(ps[3],'Semester and year to be announced')
    patchpara(ps[4],'Proposed research and practice course plan. Administrative details and assessment weights require confirmation.')
    # All original package parts are retained; only document content and field settings change.
    for ri in range(7):setcell(cells(ts[0],ri)[1],'To be announced')
    setcell(cells(ts[0],7)[1],'https://amessbee.github.io/s27/')
    setcell(cells(ts[1],1)[1],'3 (proposed; subject to approval)')
    for ri,n,d in [(2,'2 (proposed)','75 minutes (proposed)'),(3,'Integrated practical studios','Within scheduled meetings'),(4,'Optional TA clinic','To be announced')]:
        cs=cells(ts[1],ri);setcell(cs[2],n);setcell(cs[4],d)
    for ri,v in [(1,'No - proposed elective'),(2,'Yes - proposed CS elective'),(3,'Senior undergraduates; graduate students with permission (proposed)'),(4,'Students without prerequisite preparation, unless instructor permission is granted')]:setcell(cells(ts[2],ri)[1],v)
    setcell(cells(ts[3],1)[0],C['description'])
    setcell(cells(ts[4],1)[0],'Required background');setcell(cells(ts[4],1)[1],C['prerequisites'])
    setcell(cells(ts[5],1)[0],'Course aims');setcell(cells(ts[5],1)[1],C['objectives'])
    setcell(cells(ts[6],1)[0],'Students will be able to');setcell(cells(ts[6],1)[1],[f'{i+1}. {v}' for i,v in enumerate(C['outcomes'])])
    grades=['Proposed assessment totals 100%.']+[f"{a['name']}: {a['weight']}%. {a['detail']}" for a in C['assessment']]+[C['policies'][1],C['policies'][0]]
    setcell(cells(ts[6],3)[0],grades)
    setcell(cells(ts[7],1)[1],['Yes: individual examination. Separate course paper; no combined examination proposed.','Duration: 90 minutes (proposed). Preferred timing: week 8; exact date to be announced.','Coverage: weeks 1-7. Graph reasoning, derivations, model comparisons and experiment interpretation. Permitted aids to be announced.'])
    setcell(cells(ts[7],2)[1],['Yes: individual cumulative examination. Separate course paper.','Duration: 120 minutes (proposed). Timing: official final examination period.','Coverage: cumulative, with emphasis on advanced methods and research reasoning. Permitted aids to be announced.'])
    # Clone the template schedule row to accommodate the full semester.
    row=copy.deepcopy(rows(ts[9])[2])
    for r in rows(ts[9])[2:]:ts[9].remove(r)
    for w in C['weeks']:
        nr=copy.deepcopy(row);ts[9].append(nr)
        vals=[str(w['week']),w['topic']+'\n'+w['detail'],', '.join(w['papers']) or w['reading'],w['activity']]
        for cc,v in zip(nr.findall('w:tc',NS),vals):setcell(cc,v)
    for r in rows(ts[9])[:2]:
        trpr=r.find('w:trPr',NS)
        if trpr is None:trpr=el('trPr');r.insert(0,trpr)
        for old in trpr.findall('w:tblHeader',NS):trpr.remove(old)
        trpr.append(el('tblHeader',val='true'))
    for r in rows(ts[9]):
        for cc in r.findall('w:tc',NS):
            cp=cc.find('w:tcPr',NS)
            mar=cp.find('w:tcMar',NS)
            if mar is None:mar=el('tcMar');cp.append(mar)
            for side in ['top','bottom']:
                old=mar.find('w:'+side,NS)
                if old is not None:mar.remove(old)
                mar.append(el(side,w=70,type='dxa'))
    setcell(cells(ts[10],1)[0],['The primary reading set is CS4308_Papers.pdf (50 papers, P01-P50), with editable LaTeX in CS4308_Papers.tex. The weekly table uses these stable paper identifiers.',C['reading_selection']['summary']]+[f"{r['author']}. {r['title']}. {r['url']} {r['use']}" for r in C['resources']])
    # Remove template minimum blank heights, and keep schedule rows together.
    for ti,t in enumerate(ts):
        if ti==8:continue
        for h in t.findall('.//w:trHeight',NS):h.getparent().remove(h)
        for r in rows(t):
            trpr=r.find('w:trPr',NS)
            if trpr is None:trpr=el('trPr');r.insert(0,trpr)
            if ti not in [6,10]:trpr.append(el('cantSplit'))
    # Make the original oversized letterhead first-page-only to prevent source overlap on later pages.
    sect=body.find('w:sectPr',NS);sect.find('w:headerReference',NS).set(tag('type'),'first');sect.append(el('titlePg'))
    # Remove pre-existing manual breaks in spacer paragraphs, then use meaningful section boundaries.
    for p in ps[5:]:
        for n in p.findall('.//w:br',NS):n.getparent().remove(n)
        for n in p.findall('.//w:pageBreakBefore',NS):n.getparent().remove(n)
        pp=p.find('w:pPr',NS)
        if pp is not None:
            for n in pp.findall('w:spacing',NS):pp.remove(n)
            pp.append(el('spacing',before=0,after=0,line=80,lineRule='exact'))
    for t in [ts[6],ts[8],ts[9]]:newpage(body,t)
    heading(body,'Research and practice requirements',28,page_break=True)
    heading(body,'Five paper portfolio')
    for x in C['paper_protocol']:addp(body,x)
    heading(body,'Phased research project')
    for ph in C['phases']:addp(body,f"Week {ph['week']} - {ph['name']} ({ph['weight']}% of course). {ph['deliverable']}")
    addp(body,C['research_standard']);addp(body,'Paper structure: '+C['paper_structure']);addp(body,C['project_rubric'])
    heading(body,'Workload and research practice')
    addp(body,C['workload'])
    for x in C['policies'][2:]:addp(body,x)
    heading(body,'Illustrative research projects',28,page_break=True)
    addp(body,'Choose a focused question and a feasible experiment. These 20 ideas are starting points, not required projects. Compute estimates are illustrative; agree on a manageable scope with the instructor. Dataset links and expanded descriptions are also available on the course page.')
    for i,r in enumerate(R):
        if i and i%5==0:heading(body,'Illustrative research projects continued',28,page_break=True)
        heading(body,r['id']+' '+r['title'])
        addp(body,r['question'],keep=True)
        addp(body,'Data: '+r['data']+'. Baselines: '+r['baselines']+'.',keep=True)
        addp(body,'Evaluation: '+r['evaluation'],keep=True)
        addp(body,'Extension: '+r['extension']+' Compute: '+r['compute']+'.',keep=True)
        addp(body,'Dataset source: '+r['source'])
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    settings=E.fromstring(parts['word/settings.xml'])
    up=settings.find('w:updateFields',NS)
    if up is None:up=el('updateFields');settings.append(up)
    up.set(tag('val'),'true');parts['word/settings.xml']=E.tostring(settings,xml_declaration=True,encoding='UTF-8',standalone=True)
    out=ROOT/'CS4308_Course_Outline.docx'
    with ZipFile(out,'w',ZIP_DEFLATED) as z:
        for n,v in parts.items():z.writestr(n,v)
    with ZipFile(template) as a,ZipFile(out) as b:
        assert set(a.namelist())==set(b.namelist())
        assert all(a.read(n)==b.read(n) for n in a.namelist() if n not in ['word/document.xml','word/settings.xml'])
    print('Created',out)

def tex(s):
    s=plain(s).replace('é',"\\'e").replace('á',"\\'a").replace('ö','\\"o').replace('ü','\\"u').replace('í',"\\'i").replace('ć',"\\'c").replace('č','\\v{c}').replace('Š','\\v{S}')
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','~':r'\textasciitilde{}'}.get(c,c) for c in s)
def build_tex():
    out=[r'''\documentclass[11pt,letterpaper]{article}
\usepackage[margin=0.8in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype,xcolor,enumitem,hyperref,fancyhdr,needspace}
\definecolor{ink}{HTML}{183CB5}
\hypersetup{colorlinks=true,urlcolor=ink,linkcolor=ink,pdftitle={CS4308 Graph Machine Learning Reading List},pdfauthor={CS4308 Course Materials}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small CS4308 / Graph Machine Learning}\fancyhead[R]{\small Reading companion}\fancyfoot[R]{\thepage}
\setlength{\headheight}{14pt}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\setlist[itemize]{leftmargin=*,nosep}\urlstyle{same}
\begin{document}
{\Large\bfseries CS4308 Graph Machine Learning}\par
{\huge\bfseries Fifty papers to read and build}\par
\vspace{5pt}
A curated path from graph structure and random walks to neural message passing, transformers, generation, and reliable evaluation. The selection combines the instructor's graph-learning research with influential methods and evaluation frameworks from the wider field. Bibliographic sources were checked in November 2026. The year shown is the cited publication year; an arXiv preprint may be earlier. Workshop papers are identified explicitly.
\section*{How to use this list}
The class collectively discusses all 50 papers. Each group, normally a pair, must understand, implement, evaluate, and present at least five distinct papers. Register a balanced selection: one random-walk or spectral method, one message-passing or attention method, one advanced method, one evaluation or reliability paper, and one project-aligned paper. For theory and benchmark papers, implement a central diagnostic or evaluation protocol.

Submit a critical brief, reproducible code, a central result, one ablation or stress test, and a presentation for each study. Small-scale reproductions are acceptable when explicitly scoped. Both partners must contribute and defend the work. Suggested checkpoints are weeks 4, 6, 9, 11, and 13. This reading companion uses the same P01--P50 identifiers as the course outline and website.

GAN means generative adversarial network; GAT means graph attention network. The original GAN paper supplies the general prerequisite, followed by GraphGAN and MolGAN for graph-based adversarial learning.
\section*{Weekly reading map}
''']
    for w in C['weeks']:
        if w['papers']:out.append(r'\textbf{Week '+str(w['week'])+r': '+tex(w['topic'])+r'.} '+', '.join(w['papers'])+r'\par')
    out.append(r'\clearpage\section*{Selection and coverage}')
    out.append(tex(C['reading_selection']['summary'])+r'\par')
    for note in C['reading_selection']['policy']:out.append(tex(note)+r'\par')
    out.append(r'Coverage sources: \href{https://orcid.org/0000-0002-6961-0961}{author ORCID}; \href{https://anwar-said.github.io/anwarsaid/CV.pdf}{coauthor publication list}; \href{https://amessbee.github.io/s27/reading_selection.json}{coverage and version audit}. Each entry links its primary publication or manuscript.\par')
    categories=list(dict.fromkeys(p['category'] for p in P))
    out.append(r'\clearpage')
    for cat in categories:
        out.append(r'\Needspace{16\baselineskip}\section*{'+tex(cat)+'}')
        for p in [x for x in P if x['category']==cat]:
            out.append(r'\begin{minipage}{\linewidth}')
            out.append(r'{\large\bfseries '+p['id']+' '+tex(p['title'])+r'}\par')
            out.append(tex(p['authors'].rstrip('.'))+'. '+tex(p['venue'])+', '+str(p['year'])+r'.\par')
            out.append(r'\textcolor{ink}{\small '+('MUDASSIR SHABBIR / RESEARCH' if p.get('instructor_paper') else 'FIELD LANDMARK')+r'}\par')
            if p.get('display_note'):out.append(r'{\small '+tex(p['display_note'])+r'}\par')
            out.append(r'\textbf{Why read it.} '+tex(p['why'])+r'\par')
            out.append(r'\textbf{Build or investigate.} '+tex(p['exercise'])+r'\par')
            out.append(r'\textbf{Level.} '+tex(p['difficulty'])+r'\quad\href{'+p['url']+r'}{Primary source $\nearrow$}\par')
            out.append(r'\end{minipage}\par\vspace{10pt}')
    out.append(r'\clearpage\section*{Twenty illustrative research projects}')
    out.append(tex(C['research_standard'])+r'\par')
    out.append(r'These are scoped research suggestions. Agree on a dataset, question, and compute budget before beginning. Each project should report competitive and simple baselines, valid splits, ablations, error analysis, and reproducible artifacts.\par')
    for r in R:
        out.append(r'\begin{minipage}{\linewidth}\subsection*{'+r['id']+' '+tex(r['title'])+'}')
        out.append(tex(r['question'])+r'\par\textbf{Data.} '+tex(r['data'])+r'. \href{'+r['source']+r'}{Dataset documentation}\par')
        for k,label in [('baselines','Baselines'),('evaluation','Evaluation'),('extension','Extension'),('compute','Compute')]:out.append(r'\textbf{'+label+r'.} '+tex(r[k])+r'\par')
        out.append(r'\end{minipage}\par\vspace{8pt}')
    out.append(r'\end{document}')
    (ROOT/'CS4308_Papers.tex').write_text('\n'.join(out))
    print('Created CS4308_Papers.tex')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--template',type=Path);args=a.parse_args()
    if args.template:build_docx(args.template)
    build_tex()
