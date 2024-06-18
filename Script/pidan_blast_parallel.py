import os
import subprocess
from Bio import SeqIO
from Bio.Blast.Applications import NcbimakeblastdbCommandline, NcbiblastpCommandline

def create_blast_db(fasta_file, db_name):
    """创建BLAST数据库"""
    if not os.path.exists(db_name + ".pin"):  # 检查数据库是否已经存在
        print(f"Creating BLAST database at {db_name}...")
        makeblastdb_cline = NcbimakeblastdbCommandline(dbtype="prot", input_file=fasta_file, out=db_name)
        stdout, stderr = makeblastdb_cline()
        print(stdout)
        print(stderr)
    else:
        print(f"BLAST database {db_name} already exists. Skipping creation.")


def run_blast_query(query_file, db_name, output_file, num_threads=23):
    """运行BLAST比对"""
    blastp_cline = NcbiblastpCommandline(query=query_file, db=db_name, evalue=0.001, outfmt=6, out=output_file, num_threads=num_threads)
    stdout, stderr = blastp_cline()
    print(stdout)
    print(stderr)

def parse_blast_output(output_file):
    """解析BLAST输出结果并统计每对序列的最高分数"""
    scores = {}
    with open(output_file) as f:
        for line in f:
            fields = line.strip().split("\t")
            query_id = fields[0]
            subject_id = fields[1]
            score = float(fields[2])  # 比对分数位于第12列

            # 使用 (query_id, subject_id) 作为键
            key = (query_id, subject_id)
            
            # 更新分数，如果当前分数比之前存储的高
            if key not in scores or score > scores[key]:
                scores[key] = score

    # 计算总分数
    total_score = sum(scores.values())
    return total_score

def count_sequences(fasta_file):
    """统计输入文件中序列的数量"""
    with open(fasta_file) as f:
        return sum(1 for _ in SeqIO.parse(f, "fasta"))

def process_file(fasta_file, output_dir, num_threads):
    # 提取输入文件名并去掉后缀
    base_name = os.path.splitext(os.path.basename(fasta_file))[0]
    db_name = os.path.join(output_dir, f"{base_name}_db")
    blast_output_file = os.path.join(output_dir, f"{base_name}_blast.tsv")

    # 创建BLAST数据库（如果尚未存在）
    create_blast_db(fasta_file, db_name)

    # 运行BLAST比对
    run_blast_query(fasta_file, db_name, blast_output_file, num_threads)

    # 解析BLAST输出结果并统计总分数
    total_score = parse_blast_output(blast_output_file)

    # 统计输入文件中序列的数量
    num_sequences = count_sequences(fasta_file)

    # 计算平均得分
    if num_sequences > 0:
        average_score = (total_score - (num_sequences*100)) / (num_sequences * (num_sequences -1 ))
        return base_name, average_score
    else:
        print(f"No sequences found in the input file: {fasta_file}")
        return base_name, None

def main(input_dir, output_dir, summary_file, num_threads):
    results = []

    # 遍历输入目录中的所有文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".faa") or file_name.endswith(".fasta"):
            fasta_file = os.path.join(input_dir, file_name)
            base_name, average_score = process_file(fasta_file, output_dir, num_threads)
            if average_score is not None:
                results.append((base_name, average_score))

    # 将结果输出到TSV文件
    with open(summary_file, 'w') as out_file:
        out_file.write("base_name\taverage_score\n")
        for base_name, average_score in results:
            out_file.write(f"{base_name}\t{average_score}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create BLAST database and run BLASTP query on multiple files.")
    parser.add_argument('-i', '--input', required=True, help='输入文件夹，包含多个FAA文件')
    parser.add_argument('-o', '--output', required=True, help='输出文件夹')
    parser.add_argument('-s', '--summary', required=True, help='输出汇总结果的TSV文件')
    parser.add_argument('-t', '--threads', type=int, default=4, help='BLAST比对使用的线程数')

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    main(args.input, args.output, args.summary, args.threads)