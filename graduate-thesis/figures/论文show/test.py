import re
import jieba
import os
import sys
import warnings
def pre_code(lines):
    # 删除在同一行内的//注释和/*...*/注释和#注释
    lines = [re.sub(r'//.*', '', line) for line in lines]
    lines = [re.sub(r'/\*.*?\*/', '', line) for line in lines]
    lines = [re.sub(r'#d.*', '', line) for line in lines]

    # 删除多行块注释/*...*/
    STATE_NORMAL = 0
    STATE_BEGIN = 1
    STATE_BLOCK_COMMENT = 2
    STATE_END = 3

    state = STATE_NORMAL
    idx_line = 0
    # 对于文件中的每一行代码line
    for line in lines:
        temp = []
        idx = 0
        # 判断当前的下标是否越界
        while idx < len(line):
            # 获取当前下标对应的字符
            # 通过判断字符的类型（'/' '*'）赋予不同状态位
            cmt_char = line[idx]
            if cmt_char == '':
                break
            if state == STATE_NORMAL:
                if cmt_char == '/':
                    state = STATE_BEGIN
                else:
                    temp.append(cmt_char)
            elif state == STATE_BEGIN:
                if cmt_char == '*':
                    state = STATE_BLOCK_COMMENT
                else:
                    temp.append('/' + cmt_char)
                    state = STATE_NORMAL
            elif state == STATE_BLOCK_COMMENT:
                if cmt_char == '*':
                    state = STATE_END
            elif state == STATE_END:
                if cmt_char == '/':
                    state = STATE_NORMAL
                    idx = idx + 1
                    if idx >= len(line):
                        break
                    cmt_char = line[idx]
                    while cmt_char == '\r' or cmt_char == '\n':
                        break
                elif cmt_char == '*':
                    state = STATE_END
                else:
                    state = STATE_BLOCK_COMMENT
            idx = idx + 1
        # 将处理后的该行字符拼接为字符串
        tempstr = "".join(temp)
        # 重新储存到lines中
        # 原来没有进行这一步，lines中的数据没有改变
        lines[idx_line] = tempstr
        idx_line = idx_line + 1
    return lines

file = "./show2.c"
f = open(file,'r')
code = ""
lines = f.readlines()
for line in lines:
     code = code + line
print("----------------Code---------------------")
print(code)

print("----------------Pre_code---------------------")
code = ""
lines = [line.strip() for line in lines if line.strip()]#删除多余空行
lines = pre_code(lines)
for line in lines:
     code = code + line
print(code)

print("----------------Token---------------------")
temp = jieba.lcut(code)  # 结巴分词 精确模式
words = []
for i in temp:
    # 过滤掉所有的标点符号
    i = re.sub("[\s+\.\!\/_,$^*(+\"\'””《》]+|[+——！，。？、~@#￥……*（）\[ \] { } ) ：; ；‘]+", "", i)
    if len(i) > 0:
        words.append(i)
if len(words) > 0:
    print(str(words))


print("----------------AST---------------------")
# parser_file 用于处理c语言文件
from pycparser import parse_file
from pycparser import CParser
ast = CParser().parse(code)
print(type(ast))
print(ast)


print("----------------PDG---------------------")

