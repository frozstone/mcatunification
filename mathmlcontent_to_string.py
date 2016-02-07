from lxml import etree

class MathML2String:
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
    
    def __join_into_prefix(self, operator, operands):
        #first child is the operator to apply
        op_name = operator["text"] if operator["text"] != "" else operator["tag"]
        if len(operands) <= 2: return "%s(%s)" % (op_name, ",".join(op["text"] for op in operands))
        return "%s(%s,%s)" % (op_name, operands[0]["text"], self.__join_into_prefix(operator, operands[1:]))

    def __join_into_infix(self, elements):
        output = ""
        for i, ele in enumerate(elements):
            if not any(ele["tag"] == ele_tag for ele_tag in ["ci", "cn", "csymbol", "qvar"]):
                if self.__is_open_fence(elements[0]["text"]) and self.__is_close_fence(elements[-1]["text"]):
                   return "(%s(%s,%s))" % (ele["text"], self.__join_into_infix(elements[1:i]), self.__join_into_infix(elements[i+1:-1]))
                return "%s(%s,%s)" % (ele["text"], self.__join_into_infix(elements[:i]), self.__join_into_infix(elements[i+1:]))

        return "".join([ele["text"] for ele in elements])

    def __walk_mathml(self, mt_xml):
        """
            mt_xml starts with <semantics>
        """
        temp_flat = []
        current_tag = mt_xml.xpath("local-name()")

        if self.__is_leaf(mt_xml): 
            if current_tag == "qvar": return current_tag, mt_xml.attrib["name"].upper()
            elif any(current_tag == ele_tag for ele_tag in ["ci", "cn", "csymbol"]): return current_tag, self.__normalize_symbol_name(mt_xml.text).lower()
            else: return current_tag, current_tag.lower() #usually an operator
        
        for ele in mt_xml:
            ele_tag, ele_text = self.__walk_mathml(ele)
            if ele_tag == "csymbol" and ele_text == "fragments": continue
            temp_flat.append({"tag": ele_tag, "text": ele_text})

        if current_tag == "apply":
            #join prefix
            return "ci", self.__join_into_prefix(temp_flat[0], temp_flat[1:])
        else:
            #join infix
            return "ci", self.__join_into_infix(temp_flat)

    def convert(self, mt_xml):
       tag, mt_flat = self.__walk_mathml(mt_xml.getroot())
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
