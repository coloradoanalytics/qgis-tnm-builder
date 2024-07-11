import xml.etree.ElementTree as ET

def convert_roadways(root, road_layer):
    # Remove existing roadways element if it exists
    roadways_element = root.find("roadways")
    if roadways_element is not None:
        root.remove(roadways_element)

    # Create a new roadways element
    roadways = ET.SubElement(root, "roadways")
    for feature in road_layer.getFeatures():
        roadway = ET.SubElement(roadways, "roadway")
        ET.SubElement(roadway, "name").text = feature["Name"]
        ET.SubElement(roadway, "comments").text = feature["Notes"]

        points = ET.SubElement(roadway, "points")
        geom = feature.geometry()
        if geom:
            for i, point in enumerate(geom.vertices()):
                pt = ET.SubElement(points, "point")
                ET.SubElement(pt, "name").text = f"Point-{i}"
                ET.SubElement(pt, "pointNumber").text = str(i)
                ET.SubElement(pt, "theX").text = str(point.x())
                ET.SubElement(pt, "theY").text = str(point.y())
                ET.SubElement(pt, "theZ").text = str(point.z())
                ET.SubElement(pt, "roadwayWidth").text = str(feature["Width"])
                ET.SubElement(pt, "onStructure").text = str(feature["On Structure"]).lower()
                ET.SubElement(pt, "roadType").text = feature["Pavement Type"]
                ET.SubElement(pt, "roadCategory").text = feature["Category"]
                ET.SubElement(pt, "speedConstraint").text = "0"
                ET.SubElement(pt, "controlDevice").text = feature["Flow Control"]
                ET.SubElement(pt, "percentAffected").text = "100"

                # Extract and convert attribute values
                adt = feature["ADT"]
                auto_night_percent = feature["Auto Night Percent"]
                auto_speed = feature["Auto Speed"]
                medium_truck_percent = feature["Medium Truck Percent"]
                medium_truck_night_percent = feature["Medium Truck Night Percent"]
                medium_truck_speed = feature["Medium Truck Speed"]
                heavy_truck_percent = feature["Heavy Truck Percent"]
                heavy_truck_night_percent = feature["Heavy Truck Night Percent"]
                heavy_truck_speed = feature["Heavy Truck Speed"]

                medium_truck_adt = adt * (medium_truck_percent / 100)
                heavy_truck_adt = adt * (heavy_truck_percent / 100)
                auto_adt = adt - medium_truck_adt - heavy_truck_adt

                auto_night_adt = auto_adt * (auto_night_percent / 100)
                auto_day_adt = auto_adt - auto_night_adt
                medium_truck_night_adt = medium_truck_adt * (medium_truck_night_percent / 100)
                medium_truck_day_adt = medium_truck_adt - medium_truck_night_adt
                heavy_truck_night_adt = heavy_truck_adt * (heavy_truck_night_percent / 100)
                heavy_truck_day_adt = heavy_truck_adt - heavy_truck_night_adt

                total_day_adt = auto_day_adt + medium_truck_day_adt + heavy_truck_day_adt
                total_night_adt = auto_night_adt + medium_truck_night_adt + heavy_truck_night_adt

                medium_truck_percent_day = (medium_truck_day_adt / total_day_adt) * 100
                medium_truck_percent_night = (medium_truck_night_adt / total_night_adt) * 100
                heavy_truck_percent_day = (heavy_truck_day_adt / total_day_adt) * 100
                heavy_truck_percent_night = (heavy_truck_night_adt / total_night_adt) * 100
                auto_percent_day = 100 - (medium_truck_percent_day + heavy_truck_percent_day)
                auto_percent_night = 100 - (medium_truck_percent_night + heavy_truck_percent_night)

                day_percent_volume = total_day_adt / adt * 100
                night_percent_volume = 100 - day_percent_volume

                myTraffic = ET.SubElement(pt, "myTraffic")
                ET.SubElement(myTraffic, "LDN_ADT").text = str(adt)
                ET.SubElement(myTraffic, "DayPercentVolume").text = str(day_percent_volume)
                ET.SubElement(myTraffic, "NightPercentVolume").text = str(night_percent_volume)

                vehicleFlowSet = ET.SubElement(myTraffic, "vehicleFlowSet")

                for vehicle_type, percent_day, percent_night, speed in [
                    ("Automobiles", auto_percent_day, auto_percent_night, auto_speed),
                    ("MediumTrucks", medium_truck_percent_day, medium_truck_percent_night, medium_truck_speed),
                    ("HeavyTrucks", heavy_truck_percent_day, heavy_truck_percent_night, heavy_truck_speed),
                ]:
                    vehicleFlow = ET.SubElement(vehicleFlowSet, "vehicleFlow")
                    ET.SubElement(vehicleFlow, "vehicleType").text = vehicle_type
                    ET.SubElement(vehicleFlow, "ldnPercentDay").text = str(percent_day)
                    ET.SubElement(vehicleFlow, "ldnPercentNight").text = str(percent_night)
                    ET.SubElement(vehicleFlow, "ldnAverageSpeed").text = str(speed)
    return root
