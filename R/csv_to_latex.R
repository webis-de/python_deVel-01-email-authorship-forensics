library(plyr)
library(tidyverse)
library(magrittr)

library(xtable)

table <- read.csv2("features/style_markers.csv",stringsAsFactors = FALSE)

table$Status [table$Status %in% c("+")] <- "\\ding{51}"
table$Status [table$Status %in% c("0")] <- "$\\sim$"
table$Status [table$Status %in% c("-")] <- "\\ding{55}"

print(xtable(table, type = "latex",
             align = c("p{1cm}|p{6cm}|p{1cm}|p{3cm}|p{6cm}")),
      file = "results/tables/style_markers.tex")


