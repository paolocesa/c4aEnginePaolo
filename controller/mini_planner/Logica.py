import json
import xml.etree.ElementTree as ET

def readXML(xmlFile):
    if xmlFile is None:
        return None
    else:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        prefix = root.tag
        # save all the variables in a dictionary
        variables = root.attrib
        # used to make the keys of the variables all different between each others
        attributes = {}
        for v in variables:
            key = prefix + "_" + v
            attributes[key] = variables[v]
            if variables[v].count("[")>0:
                #print "ho trovato una lista corrispondente a :", variables[v], "devo trasformarla"
                variables[v] = variables[v].replace("[","").replace("]","")
                #print variables[v]
                splitted = variables[v].split(",")
                for element in splitted:
                    #remove the old instance
                    splitted.remove(element)
                    #convert it without spaces
                    elem = element.strip()
                    #add the new element
                    splitted.append(elem)
                attributes[key] = splitted
                #print type(attributes[key]), attributes[key]
        return attributes


def myLogic(tests, data=None):
  # You've recursed to a primitive, stop!
  if tests is None or type(tests) != dict:
    return tests
  #print type(tests), tests
  data = data or {}
  #print type(data), data
  op = tests.keys()[0]
  #print type(op), op
  values = tests[op]
  #print type(values), values
  operations = {
    "=="  : (lambda a, b: a == b),
    "!="  : (lambda a, b: a != b),
    ">"   : (lambda a, b: a > b),
    ">="  : (lambda a, b: a >= b),
    "<"   : (lambda a, b, c=None: a < b if (c is None) else (a < b) and (b < c)),
    "<="  : (lambda a, b, c=None: a <= b if (c is None) else (a <= b) and (b <= c)),
    "!"   : (lambda a: not a),
    "and" : (lambda *args: reduce(lambda total, arg: total and arg, args, True)),
    "or"  : (lambda *args: reduce(lambda total, arg: total or arg, args, False)),
    #funziona se passo due elementi ( and e or invece riescono a fare controllo su una serie di n elementi nello stesso gruppo)
    "xor" : (lambda a, b: (a and (not b)) or ((not a) and b )),
    #funziona se passo due elementi
    "->" : (lambda a, b: (not a) or b),
    #funziona se passo due elementi
    "<->": (lambda a, b: ((a and b) or ((not a) and (not b)))),
    #todo: da sistemare come funziona
    "in"  : (lambda a, b: a in b if "__contains__" in dir(b) else False),
    #todo: tentativo per 'in'
    "+++" : (lambda x: sorted(x,key=(lambda a, b: a + b))),



    "var" : (lambda a, not_found=None:
        reduce(lambda data, key: (data.get(key, not_found)
                                  if type(data) == dict
                                  else data[int(key)]
                                       if (type(data) in [list, tuple] and
                                           str(key).lstrip("-").isdigit())
                                       else not_found),
               str(a).split("."),
               data)
      ),
    #stessa funzione di "var", usato solo per distinguere tra variabili e regole semplic
    #da usare come punto di partenza per tentativo ricorsione
    "rule": (lambda a, not_found=None:
        reduce(lambda data, key: (data.get(key, not_found)
                                 if type(data) == dict
                                 else data[int(key)]
                                      if (type(data) in [list, tuple] and str(key).lstrip("-").isdigit())
                                      else not_found),
                str(a).split("."),
               data)
      ),
    "min" : (lambda *args: min(args)),
    "max" : (lambda *args: max(args)),
    "count": (lambda *args: sum(1 if a else 0 for a in args)),
  }

  #print type(operations), operations

  if op not in operations:
    raise RuntimeError("Unrecognized operation %s" % op)

  # Easy syntax for unary operators, like {"var": "x"} instead of strict
  # {"var": ["x"]}
  if type(values) not in [list, tuple]:
    values = [values]

  # Recursion!
  values = map(lambda val: myLogic(val, data), values)

  return operations[op](*values)


def evaluateRules(rule_data_file, data_for_rules):
    with open(rule_data_file) as json_rules:
        json_closes = json.load(json_rules)
        json_rules.close()

    # first compute the simple rules (aka the one not composed by other rules)
    rules_results = {}
    for c in json_closes:
        # print c, type(c)
        if (c == "basic_rules"):
            for rule in json_closes[c]:
                rules_results[rule] = myLogic(json_closes[c][rule], data_for_rules)
    #print "valori regole semplici: ", rules_results

    # put together for simplicity the results of the rules and the data needed
    mixed_data_dictionary = data_for_rules
    mixed_data_dictionary.update(rules_results)

    for c in json_closes:
        if (c == "complex_rules"):
            for rule in json_closes[c]:
                rules_results[rule] = myLogic(json_closes[c][rule], mixed_data_dictionary)
                #print "valore regola complessa :", rules_results[rule]
    #print "insieme di tutti i risultati delle regole \n", rules_results
    return rules_results

