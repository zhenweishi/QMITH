library(pheatmap)
library(rmda)
# -----------------------  组学-通路热图 ----------------------#
# dev.off(); dev.off(); dev.off(); dev.off()
# cat("\014"); rm(list = ls()); options(stringsAsFactors = F); options(warn = -1)


data_train = read.csv('./data/SYHN_Clinical_R_ITED_335.csv')
data_duke = read.csv('./data/Duke_Clinical_R_ITED_280.csv')
data_ispy2 = read.csv('./data/ISPY2_Clinical_R_ITED_384.csv')
data_zs2 = read.csv('./data/ZS2_Clinical_R_ITED_590.csv')
data_duke$age_Y = -round(data_duke$age_Day/365)

data_train$proba_ITED_new = 1- data_train$proba_ITED_new
data_duke$proba_ITED_new = 1- data_duke$proba_ITED_new
data_ispy2$proba_ITED_new = 1- data_ispy2$proba_ITED_new
data_zs2$proba_ITED_new = 1- data_zs2$proba_ITED_new

ID = outcome = c(data_train$ID,data_zs2$ID,
                 data_duke$ID,data_ispy2$ID)
outcome = c(data_train$Overall_pCR_gt,data_zs2$Overall_pCR_gt,
            data_duke$Overall_pCR_gt,data_ispy2$Overall_pCR_gt)
# Age = c(data_train$age_Y,data_zs2$age_Y,
#         data_duke$age_Y,data_ispy2$age_Y)
molecular_type = c(data_train$Molecular_subtypes,data_zs2$Molecular_subtypes,
                   data_duke$Molecular_subtypes,data_ispy2$Molecular_subtypes)
HER2 = c(data_train$HER2_status,data_zs2$HER2_status,
         data_duke$HER2_status,data_ispy2$HER2_status)
ITH_index = c(data_train$proba_ITED_new,data_zs2$proba_ITED_new,
               data_duke$proba_ITED_new,data_ispy2$proba_ITED_new)
C_Radiomics_score = c(data_train$proba_radiomics_new,data_zs2$proba_radiomics_new,
                      data_duke$proba_radiomics_new,data_ispy2$proba_radiomics_new)
Binary_ITH_index = ifelse(ITH_index>median(median(ITH_index)),1,0)
# Binary_ITH_index = ifelse(ITH_index>=0.5930141287284145,1,0)

# 
# data_original = data.frame(ID = ID,
#                             Molecular_type = molecular_type,HER2_status = HER2,Age = Age,Binary_ITH_index = Binary_ITH_index,pCR = outcome,
#                            ITH_index = ITH_index,C_Radiomics_score = C_Radiomics_score)
# data_original = data.frame(ID = ID,pCR = outcome,Binary_ITH_index = Binary_ITH_index,
#                            Molecular_type = molecular_type,HER2_status = HER2,Age = Age,
#                            ITH_index = ITH_index,C_Radiomics_score = C_Radiomics_score)
data_original = data.frame(ID = ID,pCR = outcome,Binary_ITH_index = Binary_ITH_index,
                           Molecular_type = molecular_type,HER2_status = HER2,
                           ITH_index = ITH_index,C_Radiomics_score = C_Radiomics_score)


names(data_original)[names(data_original) == "Binary_ITH_index"] <- "Binary ITH index"
names(data_original)[names(data_original) == "Molecular_type"] <- "Molecular subtype"
names(data_original)[names(data_original) == "HER2_status"] <- "HER2 status"
names(data_original)[names(data_original) == "ITH_index"] <- "Continuous ITH index"
names(data_original)[names(data_original) == "C_Radiomics_score"] <- "C-radiomics score"
names(data_original)[names(data_original) == "pCR"] <- "Treatment response"

# write.csv(data_original,'./R_script/results/BSV_AllData_CRiTED.csv',row.names = FALSE)

# mean(ITH_index)
data = data_original[order(data_original$`Treatment response`),]
row.names(data) = data[,1]

cc = 5
# 2.改头改尾2.5%
# for (j in (cc+1):length(data)) {index05 = which(data[,j] < quantile(data[,j],0.025));  index95 = which(data[,j] > quantile(data[,j],0.975)); data[index05,j] = quantile(data[,j],0.025);  data[index95,j] = quantile(data[,j],0.975)}
# ## 3.标准化
for (v in (cc+1):ncol(data)) {
  data[, v] = (data[,v] - mean(data[,v])) / sd(data[,v])}
# 
Data = t(data[,-c(1:cc)])
# -----------------构建列注释信息------------------------
if (cc>2)  {annotation_col = data[,2:(cc)]}
if (cc==2) {annotation_col = data.frame(label=data[,cc])}
# row.names(annotation_col) = row.names(data)
rownames(annotation_col) = paste(row.names(data),sep = "")

# paste("Gene", 1:20, sep = "")
head(annotation_col)

annotation_col$`Treatment response` = ifelse(annotation_col$`Treatment response`==1,'pCR','non-pCR')
annotation_col$`Molecular subtype`[annotation_col$`Molecular subtype`==1] = 'HR+/HER2-'
annotation_col$`Molecular subtype`[annotation_col$`Molecular subtype`==2] = 'HR+/HER2+'
annotation_col$`Molecular subtype`[annotation_col$`Molecular subtype`==3] = 'HR-/HER2+'
annotation_col$`Molecular subtype`[annotation_col$`Molecular subtype`==4] = 'HR-/HER2-'

annotation_col$`Binary ITH index` = ifelse(annotation_col$`Binary ITH index`==1,'High','Low')
annotation_col$`HER2 status` = ifelse(annotation_col$`HER2 status`==1,'Positive','Negative')

# colnames(annotation_col) <- sub("_", " ", colnames(annotation_col))
# colnames(annotation_col) <- sub("_", " ", colnames(annotation_col))
# names(annotation_col)

# ------------------------热力图全参数------------------------------------
bk=c(seq(0,1,by=0.01))
p2 = pheatmap(Data, #scale="row",
              cluster_rows = F,             # 是否对指标进行聚类
              cluster_cols = F,             # 是否对指标进行聚类
              show_rownames=T, show_colnames=F,   # 是否显示行,列名称
              annotation_col=annotation_col,
              annotation_legend=TRUE, 
              legend_breaks = c(seq(0,1,by=1)), breaks = bk,
              color=c(colorRampPalette (colors = c("#0160BE", "#ffffff")) (length(bk)/2), 
                      colorRampPalette (colors = c("#ffffff", "#ff0000")) (length(bk)/2)), 
              fontsize=11, border=TRUE, border_color="white",
              filename = './R_script/results/Figure/BCSV_Heatmap_20230515_noAge.pdf' # filename = paste0(file_name, '热图.pdf')
              , width = 10, height = 5.5
)

p2

