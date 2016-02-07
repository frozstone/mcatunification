from lxml import etree, objectify
from collections import OrderedDict
from copy import deepcopy
from mathmlcontent_to_string import MathML2String
from unify_prolog import UnifiableProlog

#INPUT:  one math expression
#OUTPUT: n (depth of the input) unified math expressions

#TODO:
# 1. Get the mapping between depth and all related elements
# 2. Unify from the deepest level

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



def parse(mt_str):
    return etree.fromstring(mt_str)

def remove_children(mt_xml):
    for child in mt_xml.getchildren():
        mt_xml.remove(child)
    return True

def level_to_subexps(mt_xml):
    level_subexps = OrderedDict()
    level = 1
    while True:
        subexps = mt_xml.xpath("//*[count(ancestor::*) = %d]" % level)

        if len(subexps) == 0: break
        level_subexps[level] = subexps
        level += 1
    return level_subexps

def unify(mt_xml, signature):
    level_subexps = level_to_subexps(mt_xml)

    level_unif = OrderedDict()
    #Descendingly order the level_subexps
    level_subexps = OrderedDict(sorted(level_subexps.iteritems(), key = lambda dt: dt[0], reverse = True))

    for level, subexps in level_subexps.iteritems():
        for exp in subexps:
            #1. Remove the children, thus do postorder processing
            remove_children(exp)
            #2. Put placeholder in place of the children
            #3. Rename the tag (mo -> mo, otherwise into mi)
            if (exp.tag == "csymbol" or exp.tag == "ci") and exp.text.isalnum() and not exp.text.isdigit():
                exp.text = "%s_%s" % (exp.text, signature)
                exp.tag = "ci"
        level_unif[level] = deepcopy(subexps[0].getroottree())
        print etree.tostring(subexps[0].getroottree())
    return level_unif

def align(mt_xml_a, mt_xml_b):
    '''
        Assuming mt_xml_a and mt_xml_b are from the same template
        mt_xml_a : query
        mt_xml_b : retrieved
    '''
    mt_xml_tounify_a = deepcopy(mt_xml_a)
    mt_xml_tounify_b = deepcopy(mt_xml_b)

    level_unif_a = unify(mt_xml_tounify_a, 1)
    level_unif_b = unify(mt_xml_tounify_b, 2)

    #descendingly order
    level_unif_a = sorted(level_unif_a.iteritems(), key = lambda dt: dt[0], reverse = True)
    level_unif_b = sorted(level_unif_b.iteritems(), key = lambda dt: dt[0], reverse = True)
    
#    print "A", mt_xml_a, [(k, etree.tostring(v)) for k, v in level_unif_a]
#    print "B", mt_xml_b, [(k, etree.tostring(v)) for k, v in level_unif_b]
#    print 
    str_flattener = MathML2String()
    unif = UnifiableProlog("./unify.pl")

    for level_a, exp_a in level_unif_a:
        for level_b, exp_b in level_unif_b:
            #if etree.tostring(exp_a) == etree.tostring(exp_b):
            mt_str_a = str_flattener.convert(exp_a)
            mt_str_b = str_flattener.convert(exp_b)
            print mt_str_a, mt_str_b
            is_aligned = unif.is_unified(mt_str_a, mt_str_b)
            if is_aligned: 
                return True
    return False

#test unification
mtdt = parse(s2)
result = unify(mtdt, 1)

#test alignments
mt_xml_a = parse(s1)
mt_xml_b = parse(s2)
alignments = align(mt_xml_a, mt_xml_b)
print alignments
#for k, v in alignments.iteritems():
#    print etree.tostring(k)
#    print [etree.tostring(val) for val in v]
