
def verify_rule(rule, endpoint):
    func = endpoint.split('+')[-1]
    # rule = globals()[rule]()
    if func in rule:
        return True
    else:
        return False

