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
    sequence_number = 1
    for feature in receivers_layer.getFeatures():
        name_base = feature["name"]
        base_height = feature["height"]
        levels = feature["levels"]
        height_per_level = feature["height per level"]

        for level in range(1, levels + 1):
            receiver = ET.SubElement(receivers, "receiver")
            ET.SubElement(receiver, "name").text = f"{name_base}_level_{level}"
            ET.SubElement(receiver, "sequenceNumber").text = str(sequence_number)
            ET.SubElement(receiver, "heightAboveTerrain").text = str(base_height + (level - 1) * height_per_level)
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

            sequence_number += 1

    return root

# Example XML output:
#   <receivers>
#     <receiver>
#       <name>Receiver-1_level_1</name>
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
#     <receiver>
#       <name>Receiver-1_level_2</name>
#       <sequenceNumber>2</sequenceNumber>
#       <heightAboveTerrain>10</heightAboveTerrain>
#       <!-- similar structure as above -->
#     </receiver>
#   </receivers>
