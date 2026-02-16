library(corrgram)

xx <- data.frame(a=c(1,2,3,4,5), b=c(2,1,4,3,5))
mean(xx$b)
corelation <- cor(xx, use = "complete.obs")
print(corelation)

plot(xx)
li <- lm(b~a, data=xx)
abline(li)

corrgram(xx, main="Korrelogramm", lower.panel=panel.pts,
         upper.panel=panel.cor)