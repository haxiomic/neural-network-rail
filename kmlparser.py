import simplekml
kml = simplekml.Kml()

for point in points:
    kml.newpoint(coords=[(point[1], point[0])])

kml.save("pointcloud.kml")

