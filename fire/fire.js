// print(image);
// Map.addLayer(image)
var slope = ee.Terrain.slope(image)
// Map.addLayer(slope)
var slopesmrt = ee.Terrain.slope(image);

// Remap values.
var slopereclass = ee.Image(1)
          .where(slopesmrt.gt(0).and(slopesmrt.lte(7)), 9)
          .where(slopesmrt.gt(7).and(slopesmrt.lte(15)), 6)
          .where(slopesmrt.gt(15).and(slopesmrt.lte(22)), 4)
// Map.addLayer(slopereclass)

// aspect
var aspect = ee.Terrain.aspect(image)
// Map.addLayer(aspect)
// Remap values.
// print(aspect)
var aspectreclass = ee.Image(1)
          .where(aspect.gt(0).and(aspect.lte(7)), 9)
          .where(aspect.gt(7).and(aspect.lte(15)), 6)
          .where(aspect.gt(15).and(aspect.lte(22)), 4)
// Map.addLayer(aspectreclass)

// lulc
// self 
// Make a cloud-free Landsat 8 TOA composite (from raw imagery).
var l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1');

var image = ee.Algorithms.Landsat.simpleComposite({
  collection: l8.filterDate('2018-01-01', '2018-12-31'),
  asFloat: true
});

// Use these bands for prediction.
var bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11'];
var agriculture = table.geometry()
var barren_land = table2.geometry()
var buildings = table3.geometry()
var forest = table4.geometry()
var river = table5.geometry()
// var forest = ee.FeatureCollection('users/landsatpractise/forest');
// // Map.addLayer(forest,{},"Forest")

// var agriculture = ee.FeatureCollection('users/landsatpractise/agriculture');
// // Map.addLayer(agriculture,{},"agriculture")

// var barren_land = ee.FeatureCollection('users/landsatpractise/barren_land');
// // Map.addLayer(barren_land,{},"barren_land")

// var buildings = ee.FeatureCollection('users/landsatpractise/buildings');
// // Map.addLayer(buildings,{},"buildings")

// Make a FeatureCollection from the hand-made geometries.
var polygons = ee.FeatureCollection([
  ee.Feature(forest, {'class': 0}),
  ee.Feature(agriculture, {'class': 1}),
  ee.Feature(barren_land, {'class': 2}),
  ee.Feature(buildings, {'class': 3}),
]);

// Get the values for all pixels in each polygon in the training.
var training = image.sampleRegions({
  // Get the sample from the polygons FeatureCollection.
  collection: polygons,
  // Keep this list of properties from the polygons.
  properties: ['class'],
  // Set the scale to get Landsat pixels in the polygons.
  scale: 30
});

// Create an SVM classifier with custom parameters.
var classifier = ee.Classifier.libsvm({
  kernelType: 'RBF',
  gamma: 0.5,
  cost: 10
});
// Train the classifier.
var trained = classifier.train(training, 'class', bands);

// Classify the image.
var classified = image.classify(trained);
Map.addLayer(classified,
             {min: 0, max: 3, palette: ['#282828', '#FFBB22','#FFFF4C'
,'#F096FF']},
             'self classify');
// Display the inputs and the results.
Map.centerObject(forest, 11);

// Remap values.
var reclass = ee.Image(1)
          .where(classified.eq(0), 9)
          .where(classified.eq(1), 6)
          .where(classified.eq(2), 4)
Map.addLayer(reclass)





// pre
var lulc1 = ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")
.select('discrete_classification');
print(lulc1)
// var properties = lulc1.propertyNames();
// print('Metadata properties:', properties);
// print(lulc1.bandNames())

Map.addLayer(lulc1, {min: 0, max: 200, palette: ['#282828', '#FFBB22','#FFFF4C'
,'#F096FF','#FA0000','#B4B4B4','#F0F0F0','#0032C8','#0096A0','#FAE6A0',
'#58481F','#009900','#70663E','#00CC00','#4E751F','#007800','#666000','#8DB400'
,'#8D7400','#A0DC00','#929900	','#648C00','#000080']}, "Land Cover")

var lulcreclass = lulc1.map(function (img) {
  
  return ee.Image(img)
    .where(img.eq(0).and(img.eq(50)), 9)
    .where(img.gt(50).and(img.lte(100)), 6)
    .where(img.gt(100).and(img.lte(150)), 4);
  
});

print(lulcreclass);

Map.addLayer(lulcreclass, {min: 0, 
                     max: 200, 
                     palette: ['#282828', '#FFBB22','#FFFF4C','#F096FF','#FA0000',
                     '#B4B4B4','#F0F0F0','#0032C8','#0096A0','#FAE6A0','#58481F',
                     '#009900','#70663E','#00CC00','#4E751F','#007800','#666000',
                     '#8DB400','#8D7400','#A0DC00','#929900','#648C00','#000080']},
                     "LULC RECLASS");
// temperature

//select thermal band 10(with brightness tempereature), no calculation
