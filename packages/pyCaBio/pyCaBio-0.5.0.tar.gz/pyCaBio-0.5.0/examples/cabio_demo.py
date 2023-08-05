#!/usr/bin/env python
#
# Basic example which retrieves some genes and prints information about them.
#

from cabig.cabio.service import *

c = CaBioApplicationService()

gene = Gene()
gene.symbol = 'brca*'

r = c.queryObject(Gene.className, gene)

for g in r:
    print "%s (%s) - %s" % (g.symbol,g.taxon.commonName,g.fullName)
    for x in g.databaseCrossReferenceCollection:
        print "    %s: %s" % (x.dataSourceName, x.crossReferenceId)

