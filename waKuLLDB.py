# waKuLLDB的主程序
# codeBy： waKuany
# wakuLLDB的所有导出命令都将在这里列出
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
脚本基础：
    debugger:当前调试器对象
    command:命令参数
    result:执行命令后返回的参数
    internal_dict:当前脚本所有变量和函数
"""

import lldb
import re
import os
import shlex


def get_aslr():
    interpreter = lldb.debugger.GetCommandInterpreter() 
    return_object = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('image list -o -f', return_object)
    output = return_object.GetOutput()
    match = re.match(r'.+(0x[0-9a-fA-F]+)', output)
    if match:
        return match.group(1)
    else:
        return None


# 通过偏移下断点
def breakpoint_address(debugger, command, result, internal_dict):
    fileoff = shlex.split(command)[0]
    if not fileoff:
        print >> result, 'Please input the address!'
        return
    aslr = get_aslr()
    if aslr:
        debugger.HandleCommand('br set -a "%s+%s"' % (aslr, fileoff))
    else:
        print >> result, "ASLR not found!"


# 计算栈中真实地址的偏移地址
def frame_address(debugger, command, result, internal_dict):
    fileoff = shlex.split(command)[0]
    if not fileoff:
        print >> result, 'Please input the address!'
        return
    aslr = get_aslr()
    if aslr:
        debugger.HandleCommand('p/x %s-%s +0x0000000100000000' % (fileoff, aslr))
    else:
        print >> result, "ASLR not found!"



# 打印出该地址在LLDB中的位置
def jump_address(debugger, command, result, internal_dict):
    print >> result, "哎呀呀，前方施工，请绕行"

# 查看断点是否路过
def go_or_notgo(debugger, command, result, internal_dict):
    print >> result, "哎呀呀，前方施工，请绕行"


def breakmore(debugger, command, result, internal_dict):
    pth = shlex.split(command)[0]
    files = open(pth, 'r')
    lines = files.readlines()
    for line in lines:
        debugger.HandleCommand('ba %s' % line)
    #print >> result, "%s" %(files)


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f LLDBscript.breakpoint_address ba')
    debugger.HandleCommand('command script add -f LLDBscript.jump_address ja')
    debugger.HandleCommand('command script add -f LLDBscript.go_or_notgo isgo')
    debugger.HandleCommand('command script add -f LLDBscript.frame_address sa')
    debugger.HandleCommand('command script add -f LLDBscript.breakmore bm')
