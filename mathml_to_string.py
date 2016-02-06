from lxml import etree

class MathML2String:
    def __is_leaf(self, mt_ele):
        return len(mt_ele) == 0

    def __join_math_eles(self, mt_eles):
        mt_str = mt_eles[0]["text"]
        for i in range(1, len(mt_eles)):
            if mt_eles[i]["tag"] != "mo" and mt_eles[i-1]["tag"] != "mo":
                mt_str = "%s*%s" % (mt_str, mt_eles[i]["text"])
            else:
                mt_str = "%s%s" % (mt_str, mt_eles[i]["text"])
        return "(%s)" % mt_str
            
    def __create_prefix_notation(self, mt_eles, function_name):
        return "%s(%s)" % (function_name, ",".join([item["text"] for item in mt_eles]))

    def __walk_mathml(self, mt_xml):
        temp_flat = []
        
        if self.__is_leaf(mt_xml): return mt_xml.xpath("local-name()"), mt_xml.text
        
        contain_operator = False
        for ele in mt_xml:
            ele_tag, ele_text = self.__walk_mathml(ele)
            if ele_tag == "mo": contain_operator = True
            temp_flat.append({"tag": ele_tag, "text": ele_text})

        if contain_operator: return "mi", self.__join_math_eles(temp_flat)
        return "mi", self.__create_prefix_notation(temp_flat, mt_xml.xpath("local-name()"))
        

    def convert(self, mt_xml):
       tag, mt_flat = self.__walk_mathml(mt_xml if mt_xml is etree.Element else mt_xml.getroot())
       return mt_flat

#m = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
#    <msup>
#        <mi>a</mi>
#        <mn>2</mn>
#    </msup>
#    <mo>+</mo>
#    <mfrac>
#        <msqrt>
#            <mi>b</mi>
#        </msqrt>
#        <mi>c</mi>
#    </mfrac>
#</math>"""
#
#m2 = """<math xmlns='http://www.w3.org/1998/Math/MathML'>
#    <msup>
#        <mi>a</mi>
#        <mn>2</mn>
#    </msup>
#    <mo>+</mo>
#    <mi>b</mi>
#</math>"""
#
#print(convert(etree.fromstring(m)))
#print 
#print(convert(etree.fromstring(m2)))
