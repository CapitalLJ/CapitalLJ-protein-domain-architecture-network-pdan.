import argparse
import ast

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file  -l pidan_list -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,物种的蛋白/tDA文件')
    parser.add_argument('-l', '--pidanlist', help='输入文件,pidan列表文件')
    parser.add_argument('-o', '--output', help='输出文件,pidan的有无鉴定')

    args = parser.parse_args()
    return args

def read_species_proteins(input_file):
    species_proteins = {}
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            DA=ast.literal_eval(parts[1])[0]
            if DA not in species_proteins:
                species_proteins[DA]=[]
                species_proteins[DA].append(parts[0])
            else:
                species_proteins[DA].append(parts[0])
    return species_proteins

def read_compositions(file):
    compositions = {}
    with open(file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            compositions[parts[0]] = ast.literal_eval(parts[1])
    return compositions

def replace(species_proteins,pidan_compositions):
    replaced_pidan = {}
    for pidan,da_list in pidan_compositions.items():
        replaced_list = []
        for da in da_list:
            if da in species_proteins:
                replaced_list.extend(species_proteins[da])
        replaced_pidan[pidan] = replaced_list
    return replaced_pidan

def write_output(output_file, replaced_pidan):
    with open(output_file, 'w') as file:
        for pidan, replaced_list in replaced_pidan.items():
            file.write(f"{pidan}\t{replaced_list}\n")
                

def main():
    args = normol_get()

    species_proteins = read_species_proteins(args.input)
    pidan_compositions = read_compositions(args.pidanlist)
    # replaced_pidan = replace(species_proteins,pidan_compositions)
    write_output(args.output,species_proteins)


if __name__ == "__main__":
    main()