import xml.etree.ElementTree as ET

def convert_terrain_lines(root, elevation_contours_layer, terrain_lines_layer):
    # Remove existing terrainLines element if it exists
    terrain_lines_element = root.find("terrainLines")
    if terrain_lines_element is not None:
        root.remove(terrain_lines_element)

    # Create a new terrainLines element
    terrain_lines = ET.SubElement(root, "terrainLines")

    elevation_contours_count = 0

    # Process Elevation Contours (uniform elevation)
    if elevation_contours_layer is not None:
        for feature_id, feature in enumerate(elevation_contours_layer.getFeatures()):
            terrain_line = ET.SubElement(terrain_lines, "terrainLine")
            ET.SubElement(terrain_line, "name").text = f"Elevation Contour-{feature_id}"
            
            points = ET.SubElement(terrain_line, "points")
            geom = feature.geometry()
            elevation = feature["elevation"] if feature["elevation"] else 0
            if geom:
                for i, point in enumerate(geom.vertices()):
                    pt = ET.SubElement(points, "point")
                    ET.SubElement(pt, "name").text = f"Point-{i}"
                    ET.SubElement(pt, "pointNumber").text = str(i)
                    ET.SubElement(pt, "OrderingNumber").text = str(i)
                    ET.SubElement(pt, "theX").text = str(point.x())
                    ET.SubElement(pt, "theY").text = str(point.y())
                    ET.SubElement(pt, "theZ").text = str(elevation)

            elevation_contours_count += 1

    # Process Terrain Lines (differing elevations) if the layer exists
    if terrain_lines_layer is not None:
        for feature_id, feature in enumerate(terrain_lines_layer.getFeatures(), start=elevation_contours_count):
            terrain_line = ET.SubElement(terrain_lines, "terrainLine")
            ET.SubElement(terrain_line, "name").text = f"Terrain Line-{feature_id}"
            
            points = ET.SubElement(terrain_line, "points")
            geom = feature.geometry()
            if geom:
                for i, point in enumerate(geom.vertices()):
                    pt = ET.SubElement(points, "point")
                    ET.SubElement(pt, "name").text = f"Point-{i}"
                    ET.SubElement(pt, "pointNumber").text = str(i)
                    ET.SubElement(pt, "OrderingNumber").text = str(i)
                    ET.SubElement(pt, "theX").text = str(point.x())
                    ET.SubElement(pt, "theY").text = str(point.y())
                    ET.SubElement(pt, "theZ").text = str(point.z())

    return root
