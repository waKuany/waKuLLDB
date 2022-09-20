import logs.log

def breakpoint_callback(frame, bp_loc, internal_dict):
    """
    断点回调函数
    """
    this_thread = frame.GetThread()
    this_process = this_thread.GetProcess()
    logs.log.log_bpinfo(frame)
    bp_loc.SetEnabled(False)
    this_target = this_process.GetTarget()
    this_target.GetDebugger().HandleCommand('c')
    this_process.Continue()