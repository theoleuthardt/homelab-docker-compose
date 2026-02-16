library(readxl)
library(ggplot2)
library(GGally)
library(corrplot)
library(caret)
library(rpart)
library(rpart.plot)
library(cluster)
library(factoextra)

data <- read_excel("EU2024.xlsx")
colnames(data)


# Korrelogramm
cor_matrix <- cor(data[, sapply(data, is.numeric)], use = "pairwise.complete.obs")
corrplot(cor_matrix, method = "color", addCoef.col = "black", tl.cex = 0.7)

# Korrelierte Variablen
#high_cor_vars <- which(abs(cor_matrix) > 0.8 & abs(cor_matrix) < 1, arr.ind = TRUE)
#for (i in 1:nrow(high_cor_vars)) {
  #pair <- rownames(cor_matrix)[high_cor_vars[i, ]]
  
  #print(pair)
  
  #scatter_plot <- ggplot(data, aes_string(x = pair[1], y = pair[2], label = "Land")) +
    #geom_point() + 
    #geom_text(vjust = -1) + 
    #theme_minimal()
  
 #print(scatter_plot)
#}

# Lineare Regression
#pair <- rownames(cor_matrix)[high_cor_vars[1, ]]
#scatter_plot <- ggplot(data, aes_string(x = pair[1], y = pair[2], label = "Land")) +
  #geom_point() + 
  #geom_text(vjust = -1) + 
  #theme_minimal()

#print(scatter_plot)


# Entscheidungsbaum
set.seed(123)
decision_tree <- rpart(`BIP` ~ ., data = data, method = "anova")
rpart.plot(decision_tree)

# Hierarchisches Clustering
dist_matrix <- dist(scale(data[, sapply(data, is.numeric)]))
hclust_model <- hclust(dist_matrix)
plot(hclust_model, labels = data$Land, main = "Dendrogramm")

# K-Means Clustering
set.seed(123)
kmeans_model <- kmeans(scale(data[, sapply(data, is.numeric)]), centers = 3)
fviz_cluster(kmeans_model, data = scale(data[, sapply(data, is.numeric)]), labelsize = 8)

# PCA
pca_model <- prcomp(data[, sapply(data, is.numeric)], scale = TRUE)
fviz_pca_biplot(pca_model, label = "var", habillage = as.factor(data$Land))

# PCA-Koordinatensystem
fviz_pca_ind(pca_model, label = "none", habillage = as.factor(data$Land))

# Chernoff-Faces
#data_matrix <- as.data.frame(data[, sapply(data, is.numeric)])
#fviz_pca_ind(scale(data_matrix))
