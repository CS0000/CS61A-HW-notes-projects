def tree(label, branches= []):
    return [label] + branches

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    # if len(tree) is 0 (empty), then branches(tree) would be a False value (empty list),
    # so not False would be True, which is "is leaf"
    return not branches(tree)

def count_leaves(t):
    if is_leaf(t):
        return 1
    else:
        return sum([count_leaves(b) for b in branches(t)])

def leaves(tree):
    if is_leaf(tree):
        return [label(tree)]
    else:
        return sum([leaves(b) for b in branches(tree)],[])

def print_tree(t,indent=0):
    print('  '* indent + str(label(t)))
    for b in branches(t):
        print_tree(b,indent+1)

def sprout_leaves(t,leaves):
    if is_leaf(t):
        return tree(label(t),branches=[tree(i) for i in leaves])
    else:
        return tree(label=label(t),branches=[sprout_leaves(b,leaves) for b in branches(t)])

def add_tree(t1,t2):
    b1 = branches(t1)
    b2 = branches(t2)
    if is_leaf(t1) + is_leaf(t2) >=1:
        return tree(label=label(t1)+label(t2),
                    branches=branches(t1)+branches(t2))

    else:
        branches_overlap = [add_tree(i[0],i[1]) for i in zip(b1,b2)]
        if len(b1) < len(b2):
            branches_unique = b2[len(b1):]
        elif len(b2) < len(b1):
            branches_unique = b1[len(b2):]
        return tree(label=label(t1)+label(t2),
                    branches= branches_overlap+branches_unique)