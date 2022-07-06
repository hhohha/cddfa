#!/usr/bin/python

from cddfa import cddfa
from netbench.pattern_match import pcre_parser

FileName = "../../rules/Snort/http-bots.reg"


parser = pcre_parser.pcre_parser()
parser.load_file(FileName)

my_cddfa = cddfa()
my_cddfa.create_by_parser(parser)

my_cddfa.determinise()
my_cddfa.minimise()

my_cddfa.compute()
