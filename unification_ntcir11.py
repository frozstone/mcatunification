from lxml import etree
from os import path
from unification import Unification

#create query
query_address = "NTCIR11-Math2-queries-participants.xml"
query_doc = etree.parse(query_address)
query_formulae = query_doc.xpath(".//*[local-name() = 'formula']")

queries = {}
for f in query_formulae:
    qid = f.getparent().getparent()[0].text
    qid = qid[qid.rindex("-")+1:]
    
    if qid not in queries: queries[qid] = []
    for ann in f.xpath(".//*[local-name() = 'annotation']") + f.xpath(".//*[local-name() = 'annotation-xml']"):
        ann_p = ann.getparent()
        ann_p.remove(ann)
    for sem in f.xpath(".//*[local-name() = 'semantics']"):
        queries[qid].append(sem)

#play th judgment pool
pool_address = "NTCIR11_Math-qrels.dat"
for ln in open(pool_address).readlines():
    cells = ln.strip().split()
    qid = cells[0]
    qid = qid[qid.rindex("-")+1:]

    pid = cells[2]
    rel = int(cells[3])
   
    mathml_flname = "%s_%s" % (qid, pid)
    mathml_address= path.join("dataset_small", mathml_flname)

    for math_ln in open(mathml_address).readlines():
        mathcells = math_ln.strip().split("\t")
        mathstring= "\t".join(mathcells[3:])

        mt_xml_b = etree.fromstring(mathstring)
        
        for mt_xml_a in queries[qid]:
            u = Unification()
            isunify = u.align(mt_xml_a, mt_xml_b)
            print isunify
        break
    break

