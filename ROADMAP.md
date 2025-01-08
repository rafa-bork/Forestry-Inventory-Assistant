Forest Inventory Management System
        Pinus Pinaster, total inventory

Priorities:
- calculate stand metrics (dominant height, dominant diameter, density, basal area, total valume, total biomass, mean quadratic diametre, wilson factor)
- correctly use COD_status
- export the tree's metrics and the stand's metrics into a dowloadable csv
- create diameter distribution graph
- create height distribution graph
- create custom errors
- update the code to work with multiple species (Eucalyptus globulus, Pinus pinea, Quercus Suber)
- calculate diameter from height and vice versa if we dont have both
- calculate wood *value* by assortments
- calculate site index
- spacing index, cover percentage, canopy competition factor, stand density index
- biomass wood, bark, trunk, branches, leaves, canopy, roots
- adapt to a sampled area, and not the total area (expansion factor)



Minimum Features
- create a blueprint .csv file (maybe also create a plot blueplrint csv? with area, age, f_exp, density, hdom, etc)
- **create welcome message**
- **importing the csv** 
- **importing the attributes to an object**
- **calculate tree metrics (volumes, biomass)**
- calculate stand metrics (dominant height, dominant diameter, density, basal area, total valume, total biomass, mean quadratic diametre, wilson factor)
- create plots and graphs with the data (using matplotlib probably)



Display the values per hectare !!!!! (maybe input area manually before/after uploading csv; or crate new plot csv)

Extras:
- multiple species
-       multiple years
-       multiple places
- auto-fill missing diameter/height data
- diameter distribution
-       auto-import the requirements library
- having just a sample of the tree data parcel
- border parcels?
- concentric parcels and other types
-       tree age 
-       bark width
-       base canopy height, caopy proportion, canopy depth
-       canopy diametre, canopy area
-       leaf area 
- site index 
-       quality class curves
- espaçamento index, cover percentage, canopy competition factor, stand density index
-       shape coefficient ?
- volume by assortments
- vulume without bark, without stump, without both
- volume without bicada
-       model trees (height or diameter)
-       cubing equations (for stands without diametre and height only hdom and g)
- biomass wood, bark, trunk, branches, leaves, canopy, roots
- create custom error messages


possible errors to catch:
- lines with char insted of INT/DECIMAL
- missing lines/missing values
- structure of csv not square (specify to user that the .csv needs to be square)
- improper file format (not uploading csv but instead .xslx , wtv)
- writing improper things when asked to upload file (e.g. writing random numbers or characters)


COD_Status
- ALIVE
- DEAD
- MISSING
- STUMPS


