#!/usr/bin/env Rscript
# andrew borgman
# launch script for our Rserve instance


# if we load packages here, all connecting sessions should
# have them loaded
# library(BioradConfig)

Rserve::Rserve(args=c("--RS-conf", "det-rserve.conf"))
