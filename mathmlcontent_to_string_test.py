from lxml import etree
from mathmlcontent_to_string import MathML2String

s1 = """<semantics xml:id="m52.1a" xref="m52.1.pmml">
            <apply xml:id="m52.1.7" xref="m52.1.7.pmml">
              <eq xml:id="m52.1.2" xref="m52.1.2.pmml"/>
              <qvar xmlns:mws="http://search.mathweb.org/ns" name="A"/>
              <apply xml:id="m52.1.7.1" xref="m52.1.7.1.pmml">
                <times xml:id="m52.1.7.1.1" xref="m52.1.7.1.1.pmml"/>
                <qvar xmlns:mws="http://search.mathweb.org/ns" name="U"/>
                <qvar xmlns:mws="http://search.mathweb.org/ns" name="S"/>
                <apply xml:id="m52.1.7.1.2" xref="m52.1.7.1.2.pmml">
                  <csymbol cd="ambiguous" xml:id="m52.1.7.1.2.1">superscript</csymbol>
                  <qvar xmlns:mws="http://search.mathweb.org/ns" name="V"/>
                  <ci xml:id="m52.1.6.1" xref="m52.1.6.1.pmml">T</ci>
                </apply>
              </apply>
            </apply>
        </semantics>
"""

s2 = """
          <semantics xml:id="m54.1a" xref="m54.1.pmml">
            <cerror xml:id="m54.1b" xref="m54.1.pmml">
              <csymbol cd="ambiguous" xml:id="m54.1c" xref="m54.1.pmml">fragments</csymbol>
              <csymbol cd="unknown" xml:id="m54.1d" xref="m54.1.pmml">P</csymbol>
              <cerror xml:id="m54.1e" xref="m54.1.pmml">
                <csymbol cd="ambiguous" xml:id="m54.1f" xref="m54.1.pmml">fragments</csymbol>
                <ci xml:id="m54.1.2" xref="m54.1.2.pmml">normal-[</ci>
                <csymbol cd="unknown" xml:id="m54.1g" xref="m54.1.pmml">X</csymbol>
                <geq xml:id="m54.1.4" xref="m54.1.4.pmml"/>
                <csymbol cd="unknown" xml:id="m54.1h" xref="m54.1.pmml">t</csymbol>
                <ci xml:id="m54.1.6" xref="m54.1.6.pmml">normal-]</ci>
              </cerror>
              <leq xml:id="m54.1.7" xref="m54.1.7.pmml"/>
              <apply xml:id="m54.1.8" xref="m54.1.8.pmml">
                <divide xml:id="m54.1.8.1" xref="m5.1.8.1.pmml"/>
                <apply xml:id="m54.1.8.2" xref="m54.1.8.2.pmml">
                  <times xml:id="m54.1.8.2.5" xref="m54.1.8.2.5.pmml"/>
                  <ci xml:id="m54.1.8.2.1" xref="m54.1.8.2.1.pmml">E</ci>
                  <qvar xmlns:mws="http://search.mathweb.org/ns" name="X"/>
                </apply>
                <qvar xmlns:mws="http://search.mathweb.org/ns" name="t"/>
              </apply>
            </cerror>
        </semantics>
"""

s3 = """
    <semantics>
        <cerror>
        <qvar name='a'></qvar>
        <leq/>
        <qvar name='b'></qvar>
        </cerror>
    </semantics>
"""


address = "/home/narya/Dropbox/NTCIR11-Math2-queries-participants.xml" 
doc = etree.parse(address)
formulae = doc.xpath(".//*[local-name() = 'formula']")
for f in formulae:
    idx = f.getparent().getparent()[0].text
    print idx
    #if "10" not in idx: continue
    for ann in f.xpath(".//*[local-name() = 'annotation']") + f.xpath(".//*[local-name() = 'annotation-xml']"):
        ann_p = ann.getparent()
        ann_p.remove(ann)
    for sem in f.xpath(".//*[local-name() = 'semantics']"):
        m = MathML2String()
        print m.convert(etree.ElementTree(sem))
    print

#d1 = etree.fromstring(s3.encode("utf-8"))
#print m.convert(etree.ElementTree(d1))
