library(xlsx)
data = read.xlsx2("NB_Forschung_Datensatz_FINAL_SPSS.xlsx",sheetIndex = 1)

table(data$BesuchEltern) # 0 , 1-2 , 3-5, 6-11,12 + 
table(data$NichtBesucher1)
table(data$X.Aktivität)
table(data$X.Bildung1)

library(plyr)
library(tidyverse)
library(magrittr)

library(ggplot2)

data %<>% filter(BesuchEltern != 99 & NichtBesucher1 != 99 & Grad != "99")

ggplot(data = data) + 
  geom_jitter(aes(x = BesuchEltern,
                  y = NichtBesucher1))

data$Grad %>% unique()

mod1 <- glm(NichtBesucher1 ~  relevel(factor(Grad),ref = "5") , data = data,family = "binomial")
summary(mod1)

ggplot(data = data) + 
  geom_bar(aes(x = BesuchEltern,
               fill = NichtBesucher1))
