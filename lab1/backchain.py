from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def backchain_to_goal_tree(rules, hypothesis):
  tree = OR() # OR() is basically a list, thanks to production.py, given to me by the teacher.
  # Find all the consequences in rules that match my hypothesis.
  matchingRules = filter  (
                            lambda rule: match( rule.consequent()[0],hypothesis ), rules
                          )
  tree.append( hypothesis ) # Add the hypothesis now so we do not add the hypothesis twice if there are two or more
                            # rules that match my hypothesis. 
  for rule in matchingRules:
    binding = match( rule.consequent()[0],hypothesis ) # Save the noun of the hypothesis ( rules have variables in them ).
    boundAntecedents = populate( rule.antecedent(), binding ) # Add that noun to all the antecedents of the matching rule.
    # backchain on each antecedent in the antecedent list, and wrap them in an AND node
    # NOTE: I can not find a way to make this work for both OR and AND nodes without an explicit check for it.
    if isinstance( boundAntecedents, AND ):  
      nestedAntecedents = AND([backchain_to_goal_tree( rules, antecedent ) for antecedent in boundAntecedents])
    else:
      nestedAntecedents = OR([backchain_to_goal_tree( rules, antecedent ) for antecedent in boundAntecedents])
    tree.append( simplify( nestedAntecedents ) )
  return tree

# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
