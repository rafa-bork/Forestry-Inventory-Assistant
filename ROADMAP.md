Forest Inventory Management System
        Pinus Pinaster, total inventory


Minimum Features
- create a blueprint .csv file  
- importing the csv
- importing the attributes to an object
- calculate tree metrics (volumes, biomass)
- calculate stand metrics (dominant height, dominant diameter, density, basal area, total valume, total biomass, mean quadratic diametre, wilson factor)
- create plots and graphs with the data (using mathplotlib probably)

Display the values per hectare !!!!! (maybe input area manually before/after uploading csv; not sure how to do it inside .csv)


Extras:
- multiple species
- multiple years
- multiple places
- auto-fill missing diameter/height data
- diameter distribution
- auto-import the requirements library
- having just a sample of the tree data parcel
- border parcels?
- concentric parcels and other types
- tree age 
- bark width
- base canopy height, caopy proportion, canopy depth
- canopy diametre, canopy area
- leaf area 
- site index 
- quality class curves
- espaçamento index, cover percentage, canopy competition factor, stand density index
- shape coefficient ?
- volume by assortments
- vulume without bark, without stump, without both
- volume without bicada
- model trees (height or diameter)
- cubing equations (for stands without diametre and height only hdom and g)
- biomass wood, bark, trunk, branches, leaves, canopy, roots


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