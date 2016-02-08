from lxml import etree
import re

class MathML2String:
    __invalid_exp = r"[^\w\+\-\*\/\<\>\=\:\.\&\~\(\)]+"
    __open_fences = set(["(", "[", "{"])
    __close_fences = set([")", "]", "}"])

    def __is_leaf(self, mt_ele):
        return len(mt_ele) == 0

    def __is_open_fence(self, s):
        return any(s == fence for fence in self.__open_fences)

    def __is_close_fence(self, s):
        return any(s == fence for fence in self.__close_fences)

    def __normalize_symbol_name(self, s):
        return s.replace("normal-", "")
    
    def __join_into_prefix(self, enclosing_tag, operator, operands):
        #first child is the operator to apply
        op_name = operator["text"] if operator["text"] != "" else operator["tag"]
        if len(operands) <= 2: return "apply(%s,%s)" % (op_name, ",".join(op["text"] for op in operands))
        return "%s(%s,%s,%s)" % (enclosing_tag, op_name, operands[0]["text"], self.__join_into_prefix(enclosing_tag, operator, operands[1:]))

    def __join_into_infix(self, enclosing_tag, elements):
        output = ""
        for i, ele in enumerate(elements):
            if not any(ele["tag"] == ele_tag for ele_tag in ["ci", "cn", "csymbol", "qvar", "apply", "cerror"]):
                if self.__is_open_fence(elements[0]["text"]) and self.__is_close_fence(elements[-1]["text"]):
                   return "%s(%s,%s,%s)" % (enclosing_tag, ele["text"], self.__join_into_infix("left", elements[1:i]), self.__join_into_infix("right", elements[i+1:-1]))
                return "%s(%s,%s,%s)" % (enclosing_tag, ele["text"], self.__join_into_infix("left", elements[:i]), self.__join_into_infix("right", elements[i+1:]))

        return elements[0]["text"] if len(elements) == 1 else "%s(%s)" % (enclosing_tag, ",".join([ele["text"] for ele in elements]))

    def __validify_expression(self, ele_text, mapping_invalid, index_invalid):
        if re.match(self.__invalid_exp, ele_text):
            if ele_text not in mapping_invalid: 
                replacer = "SYMBOL_%s" % index_invalid
                mapping_invalid[ele_text] = replacer
                index_invalid += 1

            return mapping_invalid[ele_text], mapping_invalid, index_invalid
        return ele_text, mapping_invalid, index_invalid 

    def __walk_mathml(self, mt_xml, mapping_invalid = {}, index_invalid = 0):
        """
            mt_xml starts with <semantics>
        """
        temp_flat = []
        current_tag = mt_xml.xpath("local-name()")

        if self.__is_leaf(mt_xml): 
            current_text = ""
            if current_tag == "qvar": 
                current_text = mt_xml.attrib["name"].upper()
            elif any(current_tag == ele_tag for ele_tag in ["ci", "cn", "csymbol"]): 
                current_text = self.__normalize_symbol_name(mt_xml.text).lower()
            else: 
                current_text = current_tag.lower() #usually an operator

            current_text, mapping_invalid, index_invalid = self.__validify_expression(current_text, mapping_invalid, index_invalid)
            return current_tag, current_text, mapping_invalid, index_invalid
        
        for ele in mt_xml:
            ele_tag, ele_text, mapping_invalid, index_invalid = self.__walk_mathml(ele, mapping_invalid, index_invalid)
            if ele_tag == "csymbol" and ele_text == "fragments": continue
            temp_flat.append({"tag": ele_tag, "text": ele_text})

        if current_tag == "apply":
            #join prefix
            return current_tag, self.__join_into_prefix(current_tag, temp_flat[0], temp_flat[1:]), mapping_invalid, index_invalid
        else:
            #join infix
            return current_tag, self.__join_into_infix(current_tag, temp_flat), mapping_invalid, index_invalid

    def convert(self, mt_xml):
       tag, mt_flat, mapping_invalid, index_invalid = self.__walk_mathml(mt_xml.getroot(), {}, 0)
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
