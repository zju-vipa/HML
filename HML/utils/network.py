import pandapower.networks as pn
import pandas as pd

def read_examples(name: str) -> pn:
    """get the example data

    Args:
        name (str): the name of examples. 样例名称
                    Options: {'case5',  'case9', 'case14', 'case30', 'case_ieee30', 'case39', 'case57','case118','case300'}
                    description: <https://pandapower.readthedocs.io/en/v2.4.0/networks/power_system_test_cases.html>

    Returns:
        net(pandapower.networks): include the DataFrame of {bus, load, gen, ext_grid, line, bus_geodata....}
                                description: <https://pandapower.readthedocs.io/en/v2.4.0/elements.html>
    """
    net = getattr(pn, name)()
    return net


def net_description(net: pn) -> dict:
    """get the component of the network

    Args:
        net ([pn]): [pandapower.network]

    Returns:
        description([dict]): the number of the component
    
    Usage: 母线个数：description['bus']
           负荷个数：description['load']
           电机个数：description['gen']
           线路个数：description['line']
    """
    description = {}
    for tb in list(net.keys()):
            if not tb.startswith("_") and isinstance(net[tb], pd.DataFrame):
                if 'res_' not in tb:
                    description[tb] = net[tb].shape[0]
    return description


def get_networks(net: pn, comp: str) -> pd:
    """get the dataframe of the components
    Args:
        net (pn): [network]
        comp (str): [the name of the component]
                    Options: {母线：'bus', 负荷：'load', 电机：'gen', 线路：'line', 
                                'shunt', 'switch','impedance', 'trafo', ......}
    Returns:
        pd: [description]
    """
    df = net[comp]

    return df

if __name__ == "__main__":
     n = pn.case30()
     read_examples()