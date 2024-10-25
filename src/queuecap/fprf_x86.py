import os
import csv
import math

class ROB:
    def generate_header(block_num,payload_num):
        header_file = open("test.h", "w")
        header_file.write(" #define REPEAT 100000LL \n")
        header_file.write(" #define FIVE ONE ONE ONE ONE ONE \n")
        header_file.write(" #define TEN FIVE FIVE \n")
        header_file.write(" #define FIFTY TEN TEN TEN TEN TEN \n")
        header_file.write(" #define HUNDRED FIFTY FIFTY \n")
        header_file.write(" #define ONE \\\n")
        for i in range(0,block_num):
            header_file.write("\"mov %2, %%rax\\n\\t\" \\\n")
            header_file.write("\"div %1\\n\\t\" \\\n")
        for i in range(0,payload_num):
            if(i % 6 == 0):
                header_file.write("\"vandpd %%xmm0, %%xmm0, %%xmm1\\n\\t\" \\\n")
            elif(i % 6 == 1):
                header_file.write("\"vandpd %%xmm0, %%xmm0, %%xmm2\\n\\t\" \\\n")
            elif(i % 6 == 2):
                header_file.write("\"vandpd %%xmm0, %%xmm0, %%xmm3\\n\\t\" \\\n")
            elif(i % 6 == 3):
                header_file.write("\"vandpd %%xmm0, %%xmm0, %%xmm4\\n\\t\" \\\n")
            elif(i % 6 == 4):
                header_file.write("\"vandpd %%xmm0, %%xmm0, %%xmm5\\n\\t\" \\\n")
            else:
                header_file.write("\"vandpd %%xmm0, %%xmm0, %%xmm6\\n\\t\" \\\n")
        header_file.write(" \n")
        header_file.write(" #define TEST_LOOP \\\n")
        header_file.write("asm( \\\n")
        header_file.write("\"mov %2, %%rax\\n\\t\" \\\n")
        header_file.write("\"mov $0, %%rdx\\n\\t\" \\\n")
        header_file.write("\"2: \" \\\n")
        header_file.write("ONE \\\n")
        header_file.write("\"dec %0 \\n\\t\" \\\n")
        header_file.write("\"jne 2b \\n\\t\" \\\n")
        header_file.write(" : \\\n : \"r\"(repeat),\"r\"(a),\"r\"(b)\\\n :\"rax\",\"rdx\",\"xmm1\",\"xmm2\",\"xmm3\",\"xmm4\",\"xmm5\",\"xmm6\");\n ")

    def payload_num_inc(cur_num):
        return cur_num + 1

## test code
# run test
min_num = 0
max_num = 256*2

# for interval in intervals :
payload_num = min_num
while payload_num < max_num:
    # print("------------ generate code ------------")
    ROB.generate_header(6,payload_num)
    # ROB.generate_header(8,0)

    # print("------------ compile code ------------")
    command = "gcc ftest.c -o test"
    os.system(command)

    # print("------------ run test ------------")
    command = "./test >> res.txt"
    ret = os.system(command)

    # command = "objdump -D test > test.S"
    # ret = os.system(command)

    # print("------------ control ------------")
    payload_num  = ROB.payload_num_inc(payload_num)
    # print("payload_num: ",payload_num,"interval: ",interval)

# collect data
res_file = open("res.txt","r")
res_time = []
lines = res_file.readlines()
pos = 0
payload_num = min_num
while payload_num < max_num:
    res_time.append(float(lines[pos]))
    payload_num  = ROB.payload_num_inc(payload_num)
    pos = pos + 1

output_file = open("output.csv","w")
csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
legend = ['']

loop_size = pos
payload_num = min_num
for i in range(0,loop_size):
    row_content = []
    row_content.append(payload_num)
    row_content.append(res_time[i])
    csv_writer.writerow(row_content)
    payload_num = ROB.payload_num_inc(payload_num)