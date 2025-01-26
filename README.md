# Land Use and Land Cover Classification Map Generation usind Deep Learning

##Overview

Harnessing remote sensing for earth observation has allowed researchers to study and determine the various ways in which the land cover is being utilised in area over a period of time.  Using satellite images spanning over decades , land use maps are prepared for a region of interest that can further be used to quanitfy and analyse changes in vegetation, built-up areas, water-bodies etc. Therefore, land use maps are integral for land management, ecosystem monitering and urban planning. Classical methods of preparing land use maps include manual interpretation of the ROI with field surveys and the use of Geographic Information Systems (GIS) software. With the advancement in field of ML/AI, deep learniing can be used to automate the process of  LULC map generation. 

This project therefore, demonstrates the workflow of training and finetuning a Convolutional Neural Network (CNN) on Sentinel-2 satellite images for land use classification. The trained model will then predict the usecover class of an area for the specified ROI. 


##Methodology

#Data Used
1. Model development was carried out using the EuroSAT dataset which comprises of  27,000 labeled geographic images spanning over 10 classees. These include AnnualCrop, Forest, HerbaceousVegetation, Highway, Industrial, Pasture, PermanentCrop, Residential, River and SeaLake. 

![eurosat_overview_small](https://github.com/user-attachments/assets/297e6822-0b7f-4c0e-ab49-17c80e38e940)

2. Adminstrative boundaries of the country of interest (used to create the land use maps) was obtained from geoBoundaries by the William and Mary GeoLab. The geoboundaries can be downloaded for any country and varying adminstrative hierarchy via API call. For the project, India was chosen as the country of interest.

3. Google Earth Engine was used to download Sentinel-2 satellite images of regions of interest in the desired timeframe. For the purpose of the project demonstration, images of Delhi Cantonment and Yukson districts between the years 2021-2023. Illustrated below, Delhi Cantonment

![satimg](https://github.com/user-attachments/assets/4868411b-1011-4e1f-9785-369f471c5827)

#Model
The standard ResNet50 architecture pretrained on Sentinel-2 data was used by retaining the weights via the Torchgeo library. The model was chose due to its proven performance on land use classification on EuroSAT.

#Geospatial Tools Used
1. GeoPandas : Python library similar to Pandas extended for the handling geospatial work
2. Rasterio: reads and writes geospatial raster data that is stored in GeoTIFF format to organize and store gridded datasets.
3. Folium: Visualisation tool used to overlay the landuse map and geographic boundaries on interactive leaflet maps

# Maps


