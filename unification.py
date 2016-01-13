from lxml import etree, objectify
from collections import OrderedDict
from copy import deepcopy

#INPUT:  one math expression
#OUTPUT: n (depth of the input) unified math expressions

#TODO:
# 1. Get the mapping between depth and all related elements
# 2. Unify from the deepest level

m = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
    <msup>
        <mi>a</mi>
        <mn>2</mn>
    </msup>
    <mo>+</mo>
    <mfrac>
        <msqrt>
            <mi>b</mi>
        </msqrt>
        <mi>c</mi>
    </mfrac>
</math>"""

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

def unify(level_subexps, namespace):
    level_unif = OrderedDict()
    #Descendingly order the level_subexps
    level_subexps = OrderedDict(sorted(level_subexps.iteritems(), key = lambda dt: dt[0], reverse = True))

    for level, subexps in level_subexps.iteritems():
        for exp in subexps:
            #1. Remove the children, thus do postorder processing
            remove_children(exp)
            #2. Put placeholder in place of the children
            exp.text = "PLACE"
            #3. Rename the tag (mo -> mo, otherwise into mi)
            if exp.tag != "{%s}mo" % namespace:
                exp.tag = "mi"
        level_unif[level] = deepcopy(subexps[0].getroottree())
    return level_unif

mtdt = parse(m)
result = unify(level_to_subexps(mtdt), mtdt.nsmap[None])

for k, v in result.iteritems():
    print k
    print etree.tostring(v)

