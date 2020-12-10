import pandapower as pp
import pandapower.networks as pn
import pandas as pd
import numpy as np
import copy
import random


def emergency_data_generation_a(vars=None, if_random=True, n_var=3, net=pn.case9(), radio=5, n_sample=20, **kwargs) -> pd:
    """Data generation: method A 

    Args:
        vars ([dict], optional): [扰动源类型]. Defaults to None.
                                such as: {'gen':['p_mw', 'vm_pu'], 'load': ['p_mw', 'q_mvar']}
        if_random (bool, optional): [扰动方式(True: 随机; False: 逐步)]. Defaults to True.
        n_var (int, optional): [扰动源个数]. Defaults to 3.
        net ([pn], optional): [pandapower.network]. Defaults to pn.case9().
        radio (int, optional): [扰动范围]. Defaults to 5.
        n_sample (int, optional): [扰动次数]. Defaults to 20.

    Returns:
        res[pd]: [description]
    """
    if if_random:
        res = dg_a_random(vars, n_var, net, radio, n_sample)
    else:
        res = dg_a_stepwise(vars, net, radio, n_sample)

    return res


def run_powerflow(net, algorithm='nr', **kwargs):
    """run powerflow

    Args:
        net ([pn]): [description]
        algorithm (str, optional): [description]. Defaults to 'nr'.
    
    Returns:
        None (The input(net) has been changed)
    """
    pp.runpp(net, algorithm, **kwargs)


def dg_a_stepwise_simple(net=pn.case9(), node_type='gen', var='p_mw', radio=5, n_sample=20, **kwargs):
    """[summary]

    Args:
        net ([type], optional): [description]. Defaults to pn.case9().
        node_type (str, optional): [description]. Defaults to 'gen'.
        var (str, optional): [description]. Defaults to 'p_mw'.
        radio (int, optional): [description]. Defaults to 5.
        n_sample (int, optional): [description]. Defaults to 20.

    Returns:
        [type]: [description]
    """
    # todo: Consider the constraint variables (such as: in_service, controllable)
    res = pd.DataFrame(columns=['net', 'node_type', 'var', 'node', 'radio', 'success'])
    res['node_type'] = node_type
    res['var'] = var
    
    n_node = getattr(net, node_type).shape[0]
    n = 0
    for r in list(np.linspace(-radio, radio, int(n_sample/2))) + [0]:
        for i in range(n_node):
            net_new = copy.deepcopy(net)
            df = getattr(net_new, node_type)
            if df.loc[i, var]:
                df.loc[i, var] = pow(df.loc[i, var], r)
                try:
                    run_powerflow(net_new, **kwargs)
                    # pp.runpp(net_new)
                    res.loc[n] = [net_new, node_type, var, i, r, 1]
                except Exception as e:
                    if isinstance(e, pp.powerflow.LoadflowNotConverged):
                        res.loc[n] = [net_new, node_type, var, i, r, 0]
                    else:
                        print('error')
                        break
                finally:   
                    n += 1
    return res


def dg_a_stepwise(vars=None, net=pn.case9(), radio=5, n_sample=20, **kwargs):
    res = pd.DataFrame(columns=['net', 'node_type', 'var', 'node', 'radio', 'success'])
    
    if vars is None:
        vars = {'gen':['p_mw', 'vm_pu'], 'load': ['p_mw', 'q_mvar']}
    
    for node_type, v in vars.items():
        for var in v:
            r = dg_a_stepwise_simple(net, node_type, var, radio, n_sample)
            res = pd.concat([res, r], ignore_index=True)

    return res

    
def dg_a_random(vars=None, n_var=3, net=pn.case9(), radio=5, n_sample=20, **kwargs):
    res = pd.DataFrame(columns=['net', 'sample_name', 'sample_before', 'sample_after',  'success'])

    if vars is None:
        vars = {'gen':['p_mw', 'vm_pu'], 'load': ['p_mw', 'q_mvar']}
    
    var_list = []
    for node_type, v in vars.items():
        n_node = getattr(net, node_type).shape[0]
        for var in v:
            var_list += [[node_type, var, a] for a in range(n_node)]

    v_samples = random.sample(var_list, n_var)

    for i in range(n_sample):
        net_new = copy.deepcopy(net)
        value_before = []
        value_after = []
        for v in v_samples:
            # v[0]: node_type(gen, bus, load...); v[1]: var(p_mw, q_mvar, vm_pu...); v[2]：the number of device
            df = getattr(net_new, v[0])
            value_before.append(df.loc[v[2], v[1]]) 
            if df.loc[v[2], v[1]]:
                # the range of the node
                radio_list = list(np.linspace(0, radio, 10000))
                df.loc[v[2], v[1]] = df.loc[v[2], v[1]] * random.choice(radio_list)
            value_after.append(df.loc[v[2], v[1]])

        try:
            run_powerflow(net_new, **kwargs)
            # pp.runpp(net_new)
            res.loc[i] = [net_new, v_samples, value_before, value_after, 1]
        except Exception as e:
            if isinstance(e, pp.powerflow.LoadflowNotConverged):
                res.loc[i] = [net_new, v_samples, value_before, value_after, 0]
            else:
                print('error')
                break
    return res
    

if __name__ == "__main__":
    # res = emergency_data_generation_sigle_batch()
    # vars = {'gen':['p_mw', 'vm_pu'], 'load': ['p_mw', 'q_mvar']}
    res = emergency_data_generation_a(if_random=False)
    print(res)



