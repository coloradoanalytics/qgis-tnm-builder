import xml.etree.ElementTree as ET

def convert_barriers(root, buildings_layer, existing_barriers_layer):
    # Remove existing barriers element if it exists
    barriers_element = root.find("barriers")
    if barriers_element is not None:
        root.remove(barriers_element)

    # Create a new barriers element
    barriers = ET.SubElement(root, "barriers")

    # Convert buildings to barriers
    for feature_id, feature in enumerate(buildings_layer.getFeatures()):
        barrier = ET.SubElement(barriers, "barrier")
        ET.SubElement(barrier, "FeatureId").text = str(feature_id)
        ET.SubElement(barrier, "FeatureType").text = "SKEWLINE"
        ET.SubElement(barrier, "name").text = feature["name"]
        ET.SubElement(barrier, "barrierType").text = "Wall"
        ET.SubElement(barrier, "segPertResolution").text = "0"
        ET.SubElement(barrier, "segUpIncrements").text = "0"
        ET.SubElement(barrier, "segDownIncrements").text = "0"
        ET.SubElement(barrier, "segTopWidth").text = "0"
        ET.SubElement(barrier, "segSideSlopeRun").text = "2"
        ET.SubElement(barrier, "segSideSlopeRise").text = "1"
        ET.SubElement(barrier, "segNRCLSide").text = "0"
        ET.SubElement(barrier, "segNRCRSide").text = "0"
        ET.SubElement(barrier, "segNRCPBA").text = "0"
        ET.SubElement(barrier, "costPerUnitArea").text = "0"
        ET.SubElement(barrier, "costPerUnitVolume").text = "0"
        ET.SubElement(barrier, "addedCostPerUnitLength").text = "0"
        
        # Check and set height and elevation values
        height = feature["height"] if feature["height"] else 0
        elevation = feature["elevation"] if feature["elevation"] else 0

        ET.SubElement(barrier, "maxHeight").text = "300"
        ET.SubElement(barrier, "minHeight").text = "0"
        ET.SubElement(barrier, "baseHeight").text = "10"
        
        points = ET.SubElement(barrier, "points")
        geom = feature.geometry()
        if geom:
            for i, point in enumerate(geom.vertices()):
                pt = ET.SubElement(points, "point")
                ET.SubElement(pt, "name").text = f"Point-{i}"
                ET.SubElement(pt, "pointNumber").text = str(i)
                ET.SubElement(pt, "theX").text = str(point.x())
                ET.SubElement(pt, "theY").text = str(point.y())
                ET.SubElement(pt, "theZ").text = str(elevation)
                ET.SubElement(pt, "pertResolution").text = "0"
                ET.SubElement(pt, "upIncrements").text = "0"
                ET.SubElement(pt, "downIncrements").text = "0"
                ET.SubElement(pt, "height").text = str(height)
                ET.SubElement(pt, "nrcLSide").text = "0"
                ET.SubElement(pt, "nrcRSide").text = "0"
                ET.SubElement(pt, "nrcPBA").text = "0"
                ET.SubElement(pt, "shieldedRoadSegmentSet")
                ET.SubElement(pt, "reflectedRoadSegmentSet")
                ET.SubElement(pt, "ForNoiseMitigation").text = "true"

    # Count the features in the buildings layer
    buildings_count = sum(1 for _ in buildings_layer.getFeatures())

    # Convert existing barriers to barriers
    for feature_id, feature in enumerate(existing_barriers_layer.getFeatures(), start=buildings_count):
        barrier = ET.SubElement(barriers, "barrier")
        ET.SubElement(barrier, "FeatureId").text = str(feature_id)
        ET.SubElement(barrier, "FeatureType").text = "SKEWLINE"
        ET.SubElement(barrier, "name").text = feature["name"]
        ET.SubElement(barrier, "barrierType").text = "Wall"
        ET.SubElement(barrier, "segPertResolution").text = "0"
        ET.SubElement(barrier, "segUpIncrements").text = "0"
        ET.SubElement(barrier, "segDownIncrements").text = "0"
        ET.SubElement(barrier, "segTopWidth").text = "0"
        ET.SubElement(barrier, "segSideSlopeRun").text = "2"
        ET.SubElement(barrier, "segSideSlopeRise").text = "1"
        ET.SubElement(barrier, "segNRCLSide").text = "0"
        ET.SubElement(barrier, "segNRCRSide").text = "0"
        ET.SubElement(barrier, "segNRCPBA").text = "0"
        ET.SubElement(barrier, "costPerUnitArea").text = "0"
        ET.SubElement(barrier, "costPerUnitVolume").text = "0"
        ET.SubElement(barrier, "addedCostPerUnitLength").text = "0"
        
        # Check and set height value, elevation is in the z coordinate
        height = feature["height"] if feature["height"] else 0
        # elevation = feature["elevation"] if feature["elevation"] else 0

        ET.SubElement(barrier, "maxHeight").text = "300"
        ET.SubElement(barrier, "minHeight").text = "0"
        ET.SubElement(barrier, "baseHeight").text = "10"
        
        points = ET.SubElement(barrier, "points")
        geom = feature.geometry()
        if geom:
            for i, point in enumerate(geom.vertices()):
                pt = ET.SubElement(points, "point")
                ET.SubElement(pt, "name").text = f"Point-{i}"
                ET.SubElement(pt, "pointNumber").text = str(i)
                ET.SubElement(pt, "theX").text = str(point.x())
                ET.SubElement(pt, "theY").text = str(point.y())
                ET.SubElement(pt, "theZ").text = str(point.z())
                ET.SubElement(pt, "pertResolution").text = "0"
                ET.SubElement(pt, "upIncrements").text = "0"
                ET.SubElement(pt, "downIncrements").text = "0"
                ET.SubElement(pt, "height").text = str(height)
                ET.SubElement(pt, "nrcLSide").text = "0"
                ET.SubElement(pt, "nrcRSide").text = "0"
                ET.SubElement(pt, "nrcPBA").text = "0"
                ET.SubElement(pt, "shieldedRoadSegmentSet")
                ET.SubElement(pt, "reflectedRoadSegmentSet")
                ET.SubElement(pt, "ForNoiseMitigation").text = "true"

    return root
