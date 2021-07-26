
def FlatToNested(flats,parent_id='parent_id',id='id',sub='children'):
    trees = {}
    for flat in flats:
        flat=dict(flat)
        if flat[parent_id] == None:
            flat[parent_id]='0'
        flat.setdefault(parent_id)
        trees.setdefault(flat[id], {sub: []})
        trees.setdefault(flat[parent_id], {sub: []})
        trees[flat[id]].update(flat)
        trees[flat[parent_id]][sub].append(trees[flat[id]])
    return trees['0']
