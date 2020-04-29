from models.rule import RuleChangeField, RuleEvacuation
import json
import re
import importlib

def export_json(filename, parameters = None, rules = None, others = None ) :

    ''' @TODO eventually this should be part of the Rule class '''
    def serialise_rule(rule) :
        return { 'type' : str(type(rule)), 'vars' : vars(rule) }

    data = dict()
    data['parameters'] = parameters
    data['rules'] = [ serialise_rule(r) for r in rules ]
    data['others'] = others

    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
        json_file.close()


def import_json(filename) :

    with open(filename) as json_file:
        data = json.load(json_file)
        json_file.close()

    parameters = data['parameters']
    others = data['others']

    raw_rules = data['rules']

    ''' @TODO the following code should eventually be in class Rule '''
    rules = list()

    for r in raw_rules :
        ''' format is "<class 'models.rule.RuleChangeField'>" '''
        m = re.search(r"<class '(\w+\.)*(\w+)'>", r['type'])
        rule_module = m.group(1)
        rule_type = m.group(2)
        print(rule_type, r['vars'])
        print(rule_module)

        module = importlib.import_module("models.rule")
        class_type = getattr(module, rule_type)
        ''' @BUG there is no guarantee the order is preserved, arguments may be passed in the wrong order '''
        rule = class_type(*r['vars'].values())

        rules.append(rule)

    ''' end @TODO section '''

    return parameters, rules, others


def get_default_params() :
    r0 = 3.31
    r0_confinement = 0.4
    pc_ih = 0.02
    pc_si = 0.16
    pc_sm_si = 0.21

    day0 = 5  # start of simulation: 06/01/2020 => 5 days from 01/01/2020
    dm_r = 9
    # r0 = 2.799
    # r0_confinement = 1.205
    # pc_ih = 0.067
    # pc_si = 0.228
    # pc_sm_si = 0.256
    parameters = {'population': 1000000,
                  'patient0': 90,
                  'lim_time': 200,
                  'r': 1.0,
                  'beta': r0 / dm_r,
                  'kpe': 1.0,
                  'dm_incub': 4,
                  'dm_r': dm_r, 'dm_h': 6,
                  'dm_sm': 6, 'dm_si': 9, 'dm_ss': 14,
                  'pc_ir': 1 - pc_ih, 'pc_ih': pc_ih,
                  'pc_sm': 1 - pc_si, 'pc_si': pc_si,
                  'pc_sm_si': pc_sm_si, 'pc_sm_dc': (1-pc_sm_si) * 0.25, 'pc_sm_out': (1-pc_sm_si) * 0.75,
                  'pc_si_dc': 0.4, 'pc_si_out': 0.6,
                  'pc_h_ss': 0.2, 'pc_h_r': 0.8}

    # number of days since 01/01/2020 -> number of residents in SI
    data_chu_rea = {46: 1.5, 47: None, 48: None, 49: None,
                50: None, 51: None, 52: None, 53: 1.5, 54: 1.5,
                55: 1.5, 56: 1.5, 57: 1.5, 58: 1.5, 59: 3,
                60: 4.5, 61: 3, 62: 6, 63: 9, 64: 9,
                65: 12, 66: 10.5, 67: 12, 68: 12, 69: 13.5,
                70: 12, 71: 12, 72: 13.5, 73: 18, 74: 30,
                75: 33, 76: 42, 77: 51, 78: 63, 79: 76.5,
                80: 82.5, 81: 91.5, 82: 105, 83: 111, 84: 121.5,
                85: 144, 86: 142.5, 87: 153, 88: 148.5, 89: 156,
                90: 169.5, 91: 172.5, 92: 174, 93: 171, 94: 168,
                95: 168, 96: 162, 97: 156, 98: 153, 99: 145.5,
                100: 141, 101: 138, 102: 139.5, 103: 138, 104: 124.5,
                105: 109.5, 106: 105, 107: 100.5, 108: 99, 109: 99,
                110: 93, 111: 87}

    confinement = 75 - day0  # 16/03/2020 -> 01/01 + 75
    deconfinement = 131 - day0  # 11/05/2020 -> 01/01 + 131

    rules = [
        RuleChangeField(confinement,  'r',  1.0),
        RuleChangeField(confinement,  'beta', r0_confinement / dm_r),
    ]

    return { 'parameters' : dict(parameters),
             'rules' : [ r for r in rules ],
             'data' : dict({'data_chu_rea' : dict(data_chu_rea), 'day0' : day0 }),
             'other' : dict({ 'confinement' : confinement,
                              'deconfinement' : deconfinement,
                              'r0' : r0,
                              'r0_confinement' : r0_confinement}) }
