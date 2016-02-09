from lxml import etree, objectify
from unification import Unification

s1 = """
    <semantics>
        <cerror>
        <qvar name='a'></qvar>
        <leq/>
        <qvar name='b'></qvar>
        </cerror>
    </semantics>
"""

s2 = """
          <semantics>
            <cerror>
              <csymbol>fragments</csymbol>
              <csymbol>P</csymbol>
              <cerror>
                <csymbol>fragments</csymbol>
                <ci>normal-[</ci>
                <csymbol>X</csymbol>
                <geq/>
                <csymbol>t</csymbol>
                <ci>normal-]</ci>
              </cerror>
              <leq />
              <apply>
                <divide/>
                <apply >
                  <times/>
                  <ci>E</ci>
                  <qvar name="X"/>
                </apply>
                <qvar name="t"/>
              </apply>
            </cerror>
        </semantics>
"""

u = Unification()

#test alignments
mt_xml_a = etree.fromstring(s1)
mt_xml_b = etree.fromstring(s2)
alignments = u.align(mt_xml_a, mt_xml_b)
print alignments
#for k, v in alignments.iteritems():
#    print etree.tostring(k)
#    print [etree.tostring(val) for val in v]
