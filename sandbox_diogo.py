
# calculate volume of pinus pinaster with bark and stump of each tree
def calculate_tree_volume(dbh, height):
    return 0.7520 * (dbh / 100) ** 2.0706 * height ** 0.8031

# vu_st – volume total sem casca e sem cepo (m3);di – diâmetro (cm) medido à altura hi (m);
# vudi_st – volume sem casca e sem cepo até ao diâmetro de desponta di (m3);
# Pvudi_st – proporção de volume sem casca e sem cepo até ao diâmetro de desponta di.

# calculate mercantile volume of pinus pinaster with no bark and stump of each tree (vu_st)
def calculate_vu_st(dbh, height):
    return 0.0000247 * dbh ** 2.1119 * height ** 0.9261





# biomass calculations
def calculate_trunk_biomass(dbh, height):
    return 0.0146 * dbh ** 1.94687 * height ** 1.106577

