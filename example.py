#!/usr/bin/python3

from cddfa import cddfa
from netbench.pattern_match import pcre_parser

FileName = "../../rules/Snort/sql.rules.pcre"


parser = pcre_parser.pcre_parser()
parser.load_file(FileName)

my_cddfa = cddfa()
my_cddfa.create_by_parser(parser)

print ('determinizing')
my_cddfa.determinise()
print ('minimizing')
my_cddfa.minimise()

print ('computing')
my_cddfa.compute()

