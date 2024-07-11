import xml.etree.ElementTree as ET

def convert_receivers(root, receivers_layer):
    # Define the namespaces
    namespaces = {
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }
    
    # Register namespaces
    ET.register_namespace("xsi", namespaces["xsi"])
    
    # Remove existing receivers element if it exists
    receivers_element = root.find("receivers")
    if receivers_element is not None:
        root.remove(receivers_element)

    # Create a new receivers element
    receivers = ET.SubElement(root, "receivers")
    for sequence_number, feature in enumerate(receivers_layer.getFeatures(), start=1):
        receiver = ET.SubElement(receivers, "receiver")
        ET.SubElement(receiver, "name").text = feature["name"]
        ET.SubElement(receiver, "sequenceNumber").text = str(sequence_number)
        ET.SubElement(receiver, "heightAboveTerrain").text = str(feature["height"])
        ET.SubElement(receiver, "dwellingUnits").text = "1"
        ET.SubElement(receiver, "defaultAdjustment").text = "0"
        ET.SubElement(receiver, "noiseReductionGoal").text = "0"
        ET.SubElement(receiver, "existingLEQ").text = "0"
        ET.SubElement(receiver, "impactLEQ").text = "0"
        ET.SubElement(receiver, "impactIncrease").text = "0"
        ET.SubElement(receiver, "inactive").text = "false"
        ET.SubElement(receiver, "roadAdjustmentSet")
        
        points = ET.SubElement(receiver, "points")
        geom = feature.geometry()
        if geom:
            point = geom.asPoint()
            pt = ET.SubElement(points, "point")
            ET.SubElement(pt, "pointNumber").text = "0"
            ET.SubElement(pt, "OrderingNumber").text = "0"
            ET.SubElement(pt, "theX").text = str(point.x())
            ET.SubElement(pt, "theY").text = str(point.y())
            ET.SubElement(pt, "theZ").text = str(feature["elevation"])

        ET.SubElement(receiver, "ReceiverResults", attrib={f"{{{namespaces['xsi']}}}nil": "true"})
        ET.SubElement(receiver, "receiverResultsForEquipment", attrib={f"{{{namespaces['xsi']}}}nil": "true"})

    return root


# Example XML output:
#   <receivers>
#     <receiver>
#       <name>Receiver-1</name>
#       <sequenceNumber>1</sequenceNumber>
#       <heightAboveTerrain>5</heightAboveTerrain>
#       <dwellingUnits>1</dwellingUnits>
#       <defaultAdjustment>0</defaultAdjustment>
#       <noiseReductionGoal>8</noiseReductionGoal>
#       <existingLEQ>0</existingLEQ>
#       <impactLEQ>0</impactLEQ>
#       <impactIncrease>10</impactIncrease>
#       <inactive>false</inactive>
#       <roadAdjustmentSet />
#       <points>
#         <point>
#           <pointNumber>0</pointNumber>
#           <OrderingNumber>0</OrderingNumber>
#           <theX>3140318.5489245444</theX>
#           <theY>10085627.982748397</theY>
#           <theZ>550</theZ>
#         </point>
#       </points>
#       <ReceiverResults xsi:nil="true" />
#       <receiverResultsForEquipment xsi:nil="true" />
#     </receiver>
#   </receivers>