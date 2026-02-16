library(OneR)
library(readxl)
setwd("~/Klausur")
qq <- read_excel("quallen.XLS")
qq$giftig <- as.factor(qq$giftig)
model <- OneR(giftig ~ ., data = qq)
summary(model)

tstdat <- data.frame(Farbe = "gelb", Größe = "mittel", transparent = "nein", 
                     Geschmack = "süß")
colnames(tstdat) <- c("Farbe","Größe","transparent","Geschmack")
predict(model, tstdat)