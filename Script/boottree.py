import argparse
from Bio import Phylo
from io import StringIO
import re

def read_trees(tree_file):
    with open(tree_file, 'r') as f:
        tree_str = f.read()
    trees = [tree for tree in re.split(r';\s*\n', tree_str) if tree]
    return [Phylo.read(StringIO(tree + ';'), 'newick') for tree in trees]

def get_clade_terminals(clade):
    return set(term.name for term in clade.get_terminals())

def calculate_bootstrap_values(base_tree, trees):
    clades = list(base_tree.find_clades())
    for clade in clades:
        clade.bootstrap = 0

    base_clades_dict = {frozenset(get_clade_terminals(clade)): clade for clade in clades if not clade.is_terminal()}

    for tree in trees:
        for clade in tree.find_clades():
            if clade.is_terminal():
                continue
            clade_set = frozenset(get_clade_terminals(clade))
            if clade_set in base_clades_dict:
                base_clades_dict[clade_set].bootstrap += 1

    for clade in clades:
        if not clade.is_terminal():
            clade.bootstrap = clade.bootstrap / len(trees) * 100
            print(f"Clade {clade}: Bootstrap {clade.bootstrap}")

    return base_tree

def format_clade_with_bootstrap(clade):
    if clade.is_terminal():
        return f"{clade.name}:{clade.branch_length}"
    else:
        children = ','.join(format_clade_with_bootstrap(child) for child in clade.clades)
        if clade.bootstrap:
            return f"({children}){int(clade.bootstrap)}:{clade.branch_length}"
        else:
            return f"({children}):{clade.branch_length}"

def tree_to_newick_with_bootstrap(tree):
    newick_str = format_clade_with_bootstrap(tree.root) + ";"
    return newick_str

def main(base_tree_file, bootstrap_trees_file, output_file):
    base_tree = Phylo.read(base_tree_file, 'newick')
    bootstrap_trees = read_trees(bootstrap_trees_file)
    base_tree = calculate_bootstrap_values(base_tree, bootstrap_trees)
    newick_str = tree_to_newick_with_bootstrap(base_tree)
    with open(output_file, 'w') as f:
        f.write(newick_str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate bootstrap values for a phylogenetic tree.")
    parser.add_argument('-q', '--base_tree_file', type=str, required=True, help="The file containing the base tree.")
    parser.add_argument('-i', '--bootstrap_trees_file', type=str, required=True, help="The file containing the bootstrap trees.")
    parser.add_argument('-o', '--output_file', type=str, required=True, help="The file to output the base tree with bootstrap values.")
    
    args = parser.parse_args()
    main(args.base_tree_file, args.bootstrap_trees_file, args.output_file)