# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

def input2(inp, default=None):
    inp = input(inp).strip()
    if not inp:
        return default
    return inp
