import logging

import daiquiri

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger("rule_evaluation")

safe_eval_cmds={"float": float, "int": int, "str": str}


def replace_tags(rule,tags):
    # Run the substitue operation manually instead of using
    # the standard string function to enforce that the values
    # read from the tags are treated as strings by default
    logger.info(rule)

    while len(rule)>0:
        opening=rule.find("@")
        if opening<0:
            break
        closing=rule.find("@",opening+1)
        if closing<0:
            break
        tagstring=rule[opening+1:closing]
        if tagstring in tags:
            tagvalue=tags[tagstring]    
        else:
            tagvalue="MissingTag"
        rule=rule.replace("@"+tagstring+"@","'"+tagvalue+"'")
    return rule


def parse_rule(rule,tags):
    try:
        logger.info(f"Rule: {rule}")
        rule=replace_tags(rule,tags)
        logger.info(f"Evaluated: {rule}")
        result=eval(rule,{"__builtins__": {}},safe_eval_cmds)
        logger.info(f"Result: {result}")
        return result
    except Exception as e: 
        logger.error(f"ERROR: {e}")
        logger.warn(f"WARNING: Invalid rule expression {rule}",'"'+rule+'"')
        return False


def test_rule(rule,tags):
    try:
        logger.info(f"Rule: {rule}")
        rule=replace_tags(rule,tags)
        logger.info(f"Evaluated: {rule}")
        if ("MissingTag" in rule):
            return "Rule contains invalid tag"
        result=eval(rule,{"__builtins__": {}},safe_eval_cmds)
        logger.info(f"Result: {result}")
        if result:
            return "True"
        else:
            return "False"
    except Exception as e: 
        return str(e)    

#if __name__ == "__main__":
#    result=parse_rule(sys.argv[1],{ "ManufacturerModelName": "Trio" })
#    logger.info(result)
#    sys.exit(result)

# Example: "('Tr' in @ManufacturerModelName@) | (@ManufacturerModelName@ == 'Trio')"
