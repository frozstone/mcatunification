from lxml import etree
from mathml_to_string import MathML2String

s1 = '''<math xmlns="http://ntcir-math.nii.ac.jp/" xmlns:m="http://www.w3.org/1998/Math/MathML">
    <m:mrow xml:id="m22.1.10.pmml" xref="m22.1.10">
        <m:mo xml:id="m22.1.1.pmml" xref="m22.1.1">-</m:mo>
        <m:mrow xml:id="m22.1.10.1.pmml" xref="m22.1.10.1">
          <m:mi xml:id="m22.1.2.pmml" xref="m22.1.2">t</m:mi>
          <m:mo xml:id="m22.1.10.1.1.pmml" xref="m22.1.10.1.1">⁢</m:mo>
          <m:mi xml:id="m22.1.3.pmml" xref="m22.1.3">r</m:mi>
          <m:mo xml:id="m22.1.10.1.1a.pmml" xref="m22.1.10.1.1">⁢</m:mo>
          <m:mrow xml:id="m22.1.10.1.2.pmml" xref="m22.1.10.1.2">
            <m:mo xml:id="m22.1.10.1.2a.pmml" xref="m22.1.10.1.2">(</m:mo>
            <m:mrow xml:id="m22.1.10.1.2b.pmml" xref="m22.1.10.1.2">
              <mws:qvar xmlns:mws="http://search.mathweb.org/ns" name="x"/>
              <m:mo xml:id="m22.1.10.1.2.1.pmml" xref="m22.1.10.1.2.1">⁢</m:mo>
              <m:mi xml:id="m22.1.6.pmml" xref="m22.1.6">l</m:mi>
              <m:mo xml:id="m22.1.10.1.2.1a.pmml" xref="m22.1.10.1.2.1">⁢</m:mo>
              <m:mi xml:id="m22.1.7.pmml" xref="m22.1.7">n</m:mi>
              <m:mo xml:id="m22.1.10.1.2.1b.pmml" xref="m22.1.10.1.2.1">⁢</m:mo>
              <mws:qvar xmlns:mws="http://search.mathweb.org/ns" name="x"/>
            </m:mrow>
            <m:mo xml:id="m22.1.10.1.2c.pmml" xref="m22.1.10.1.2">)</m:mo>
          </m:mrow>
        </m:mrow>
      </m:mrow>
    </math>
'''

d1 = etree.fromstring(s1.encode("utf-8"))

