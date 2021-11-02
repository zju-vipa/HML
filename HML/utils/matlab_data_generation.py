from flask import current_app


def matlab_data_generation_b(file_path=None, load_list=[0.8, 1.2], fault_line_list=[1, 2],
                             line_percentage_list=[0.1, 0.2], fault_time_list=[1, 2], **kwargs):
    """Data generation: method B

    Args:
        file_path (string): [结果文件名]. Defaults to None.
        load_list ([float]): [负荷范围列表]. Defaults to [0.8, 1.2].
        fault_line_list ([int]): [故障线路列表]. Defaults to [1, 2].
        line_percentage_list ([float]): [线路故障位置列表]. Defaults to [0.1, 0.2].
        fault_time_list ([int]): [故障持续时间列表]. Defaults to [1, 2].
    Returns:
        res
    """
    # 判断None
    current_app.logger.info("p1 matlab_generation_b")
    if file_path is None:
        return 0
    # 故障持续时间转换：周期数 => 秒
    time_list = []
    for t in fault_time_list:
        time_list.append(t / 60.0)
    current_app.logger.info("p2 matlab_generation_b")
    # 调用 MATLAB 函数
    # eng = matlab.engine.start_matlab()
    # # generate_datas_function(data_path, list_load,list_line,list_linef,list_time)
    # res = eng.generate_datas_function(file_path, matlab.double(load_list), matlab.double(fault_line_list),
    #                                   matlab.double(line_percentage_list), matlab.double(time_list))
    current_app.logger.info("p3 matlab_generation_b")
    return 0
    # return res
# import matlab
# import matlab.engine
# from flask import current_app
#
#
# def matlab_data_generation_b(file_path=None, load_list=[0.8, 1.2], fault_line_list=[1, 2],
#                              line_percentage_list=[0.1, 0.2], fault_time_list=[1, 2], **kwargs):
#     """Data generation: method B
#
#     Args:
#         file_path (string): [结果文件名]. Defaults to None.
#         load_list ([float]): [负荷范围列表]. Defaults to [0.8, 1.2].
#         fault_line_list ([int]): [故障线路列表]. Defaults to [1, 2].
#         line_percentage_list ([float]): [线路故障位置列表]. Defaults to [0.1, 0.2].
#         fault_time_list ([int]): [故障持续时间列表]. Defaults to [1, 2].
#     Returns:
#         res
#     """
#     # 判断None
#     current_app.logger.info("p1 matlab_generation_b")
#     if file_path is None:
#         return 0
#     # 故障持续时间转换：周期数 => 秒
#     time_list = []
#     for t in fault_time_list:
#         time_list.append(t / 60.0)
#     current_app.logger.info("p2 matlab_generation_b")
#     # 调用 MATLAB 函数
#     eng = matlab.engine.start_matlab()
#     # generate_datas_function(data_path, list_load,list_line,list_linef,list_time)
#     res = eng.generate_datas_function(file_path, matlab.double(load_list), matlab.double(fault_line_list),
#                                       matlab.double(line_percentage_list), matlab.double(time_list))
#     current_app.logger.info("p3 matlab_generation_b")
#     return res
