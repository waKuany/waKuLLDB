#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# waKuLLDB的主程序
# codeBy： waKuany
# wakuLLDB的所有导出命令都将在这里列出
"""

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




def breakmore(debugger, command, result, internal_dict):
    pth = shlex.split(command)[0]
    files = open(pth, 'r')
    lines = files.readlines()
    for line in lines:
        debugger.HandleCommand('ba %s' % line)
    num = len(lines)

    for i in range(0, num):
        debugger.HandleCommand('breakpoint  command add -F waKuLLDB.breakpoint_callback  {}'.format(i+1))
        
    #print >> result, "%s" %(files)

def breakpoint_callback(frame, bp_loc, internal_dict):
    print(bp_loc)
    this_thread = frame.GetThread()
    this_process = this_thread.GetProcess()
    bp_loc.SetEnabled(False)
    this_process.Continue()


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f waKuLLDB.breakpoint_address ba')
    debugger.HandleCommand('command script add -f waKuLLDB.frame_address sa')
    debugger.HandleCommand('command script add -f waKuLLDB.breakmore bm')
