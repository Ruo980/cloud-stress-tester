import csv
import heapq
import os
from tqdm import tqdm

def external_sort(input_file, output_file, intermediate_folder='../dataset/intermediate_files', chunk_size=10000):
    # 确保中间文件夹存在
    os.makedirs(intermediate_folder, exist_ok=True)

    header = None

    # 定义一个生成器，用于分块读取数据
    def chunk_generator(reader, chunk_size):
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    # 定义一个生成器，用于逐块排序并写入中间文件
    def sorted_chunks(input_file, chunk_size):
        nonlocal header
        with open(input_file, 'r') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            for i, chunk in enumerate(chunk_generator(reader, chunk_size)):
                chunk.sort(key=lambda x: int(x[0]))
                chunk_file_path = f'{intermediate_folder}/chunk_{i}.csv'
                with open(chunk_file_path, 'w', newline='') as chunk_file:
                    writer = csv.writer(chunk_file)
                    writer.writerow(header)
                    writer.writerows(chunk)
                yield chunk_file_path

    # 使用堆进行合并排序
    def merge_sorted_files(sorted_files):
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            heap = []

            # 打开每个排序后的文件，读取第一行到堆中
            for file_path in sorted_files:
                with open(file_path, 'r') as chunk_file:
                    reader = csv.reader(chunk_file)
                    next(reader)  # 跳过标题行
                    first_row = next(reader, None)
                    if first_row:
                        timestamp = int(first_row[0])
                        heapq.heappush(heap, (timestamp, first_row, file_path))

            # 从堆中弹出最小的元素，写入输出文件，并将下一行加入堆中
            while heap:
                timestamp, row, file_path = heapq.heappop(heap)
                writer.writerow(row)
                next_row = next(csv.reader(open(file_path, 'r')), None)
                if next_row and next_row[0].isdigit():  # 检查下一行是否为数字（时间戳）
                    next_timestamp = int(next_row[0])
                    heapq.heappush(heap, (next_timestamp, next_row, file_path))
                else:
                    os.remove(file_path)

    # 执行外部排序
    sorted_files = list(sorted_chunks(input_file, chunk_size))
    merge_sorted_files(sorted_files)

    print(f"\n排序完成。已保存排序后的文件至 {output_file}")

if __name__ == "__main__":
    input_file_path = '../dataset/azurefunctions-accesses-2020.csv'
    output_file_path = '../dataset/sorted_azurefunctions-accesses-2020-svc.csv'

    external_sort(input_file_path, output_file_path)
