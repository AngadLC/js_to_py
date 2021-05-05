import ee 
from ee_plugin import Map 

# print(image)
# Map.addLayer(image)
slope = ee.Terrain.slope(image)
# Map.addLayer(slope)
slopesmrt = ee.Terrain.slope(image)

# Remap values.
slopereclass = ee.Image(1) \
          .where(slopesmrt.gt(0).And(slopesmrt.lte(7)), 9) \
          .where(slopesmrt.gt(7).And(slopesmrt.lte(15)), 6) \
          .where(slopesmrt.gt(15).And(slopesmrt.lte(22)), 4)
# Map.addLayer(slopereclass)

# aspect
aspect = ee.Terrain.aspect(image)
# Map.addLayer(aspect)
# Remap values.
# print(aspect)
aspectreclass = ee.Image(1) \
          .where(aspect.gt(0).And(aspect.lte(7)), 9) \
          .where(aspect.gt(7).And(aspect.lte(15)), 6) \
          .where(aspect.gt(15).And(aspect.lte(22)), 4)
# Map.addLayer(aspectreclass)

# lulc
# self
# Make a cloud-free Landsat 8 TOA composite (from raw imagery).
l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1')

image = ee.Algorithms.Landsat.simpleComposite({
  'collection': l8.filterDate('2018-01-01', '2018-12-31'),
  'asFloat': True
})

# Use these bands for prediction.
bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11']
agriculture = table.geometry()
barren_land = table2.geometry()
buildings = table3.geometry()
forest = table4.geometry()
river = table5.geometry()
# forest = ee.FeatureCollection('users/landsatpractise/forest')
# # Map.addLayer(forest,{},"Forest")

# agriculture = ee.FeatureCollection('users/landsatpractise/agriculture')
# # Map.addLayer(agriculture,{},"agriculture")

# barren_land = ee.FeatureCollection('users/landsatpractise/barren_land')
# # Map.addLayer(barren_land,{},"barren_land")

# buildings = ee.FeatureCollection('users/landsatpractise/buildings')
# # Map.addLayer(buildings,{},"buildings")

# Make a FeatureCollection from the hand-made geometries.
polygons = ee.FeatureCollection([
  ee.Feature(forest, {'class': 0}),
  ee.Feature(agriculture, {'class': 1}),
  ee.Feature(barren_land, {'class': 2}),
  ee.Feature(buildings, {'class': 3}),
])

# Get the values for all pixels in each polygon in the training.
training = image.sampleRegions({
  # Get the sample from the polygons FeatureCollection.
  'collection': polygons,
  # Keep this list of properties from the polygons.
  'properties': ['class'],
  # Set the scale to get Landsat pixels in the polygons.
  'scale': 30
})

# Create an SVM classifier with custom parameters.
classifier = ee.Classifier.libsvm({
  'kernelType': 'RBF',
  'gamma': 0.5,
  'cost': 10
})
# Train the classifier.
trained = classifier.train(training, 'class', bands)

# Classify the image.
classified = image.classify(trained)
Map.addLayer(classified,
             {'min': 0, 'max': 3, 'palette': ['#282828', '#FFBB22','#FFFF4C'
,'#F096FF']},
             'self classify')
# Display the inputs and the results.
Map.centerObject(forest, 11)

# Remap values.
reclass = ee.Image(1) \
          .where(classified.eq(0), 9) \
          .where(classified.eq(1), 6) \
          .where(classified.eq(2), 4)
Map.addLayer(reclass)





# pre
lulc1 = ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global") \
.select('discrete_classification')
print(lulc1)
# properties = lulc1.propertyNames()
# print('Metadata properties:', properties)
# print(lulc1.bandNames())

Map.addLayer(lulc1, {'min': 0, 'max': 200, 'palette': ['#282828', '#FFBB22','#FFFF4C'
,'#F096FF','#FA0000','#B4B4B4','#F0F0F0','#0032C8','#0096A0','#FAE6A0',
'#58481F','#009900','#70663E','#00CC00','#4E751F','#007800','#666000','#8DB400'
,'#8D7400','#A0DC00','#929900	','#648C00','#000080']}, "Land Cover")


def func_cbg (img):

  return ee.Image(img) \
    .where(img.eq(0).And(img.eq(50)), 9) \
    .where(img.gt(50).And(img.lte(100)), 6) \
    .where(img.gt(100).And(img.lte(150)), 4)


lulcreclass = lulc1.map(func_cbg)









print(lulcreclass)

Map.addLayer(lulcreclass, {'min': 0,
                     'max': 200,
                     'palette': ['#282828', '#FFBB22','#FFFF4C','#F096FF','#FA0000',
                     '#B4B4B4','#F0F0F0','#0032C8','#0096A0','#FAE6A0','#58481F',
                     '#009900','#70663E','#00CC00','#4E751F','#007800','#666000',
                     '#8DB400','#8D7400','#A0DC00','#929900','#648C00','#000080']},
                     "LULC RECLASS")
# temperature

#select thermal band 10(with brightness tempereature), no calculation
