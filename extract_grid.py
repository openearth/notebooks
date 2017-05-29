# remove part of the grid
ds = netCDF4.Dataset(path.with_name('pillar_net.nc'))
variables = {}
node_vars = ['NetNode_x', 'NetNode_y', 'NetNode_z', 'NetNode_lat', 'NetNode_lon']
link_vars = ['NetLink', 'NetLinkType']
bndlink_vars = ['BndLink']
elem_vars = ['NetElemNode']

for var in node_vars:
    # copy data
    variables[var] = ds.variables[var][:]  
node_selection = np.logical_and(variables['NetNode_y'] >= 1000, variables['NetNode_y'] <= 2000)
for var in node_vars:
    variables[var] = variables[var][node_selection]


for var in link_vars:
    variables[var] = ds.variables[var][:]
# lookup  nodes that are still available
node_idx_1 = np.where(node_selection)[0] + 1
# look which links are still available
from_filter = np.in1d(variables['NetLink'][:, 0], node_idx_1)
to_filter = np.in1d(variables['NetLink'][:, 1], node_idx_1)
# assume three grids are not connected
assert (from_filter == to_filter).all()
# otherwise we would have to transform into boundary links on removal of link
link_selection = np.logical_and(from_filter, to_filter)
for var in link_vars:
    variables[var] = variables[var][link_selection]

for var in bndlink_vars:
    variables[var] = ds.variables[var][:]
variables['BndLink']
bndlink_selection = np.in1d(variables['BndLink'], node_idx_1)
for var in bndlink_vars:
    variables[var] = variables[var][bndlink_selection]


for var in elem_vars:
    variables[var] = ds.variables[var][:]
variables['NetElemNode']
net_elem_node = np.ma.masked_equal(variables['NetElemNode'], -2147483647)
elem_selection = np.apply_along_axis(np.ma.in1d, 0, net_elem_node, node_idx_1)
elem_selection = np.ma.masked_array(elem_selection, mask=net_elem_node.mask)
# assume all cells are all in, or all out
assert (elem_selection.all(axis=1) == elem_selection.any(axis=1)).all()
elem_selection = elem_selection.all(axis=1)
for var in elem_vars:
    variables[var] = variables[var][elem_selection]

dims = {
    'nNetNode': node_selection.sum(),
    'nNetLink': link_selection.sum(),
    'nNetLinkPts': 2,
    'nBndLink': bndlink_selection.sum(),
    'nNetElem': elem_selection.sum(),
    'nNetElemMaxNode': 4
}


ds_new = netCDF4.Dataset(path.with_name('pillar_new.nc'), mode='w')
# copy attributes
for attr in ds.ncattrs():
    ds_new.setncattr(attr, ds.getncattr(attr))
for dim, length in dims.items():
    ds_new.createDimension(dim, length)
for name, var in ds.variables.items():
    new_var = ds_new.createVariable(name, var.dtype, var.dimensions)
    for attr in var.ncattrs():
        new_var.setncattr(attr, var.getncattr(attr))

for name in ds.variables.keys():
    ds_new.variables[name][:] = variables.get(name, ds.variables[name][:])
ds_new.close()