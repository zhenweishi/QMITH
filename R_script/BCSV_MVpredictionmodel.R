# Zhenwei Shi, this script is for the analysis of paper
# Breast Cancer ITED-NAC prediction

library(forestplot)
library(pROC)
library(binom)
library(ggplot2)
library(glmnet)
library(MASS)
library(caret)
library(car)
library(ResourceSelection)
library(SDMTools)
library(cutpointr)
library(corrplot)

#load data
data_train = read.csv('./data/SYHN_Clinical_R_ITED_335.csv')
data_duke = read.csv(('./data/Duke_Clinical_R_ITED_280.csv'))
data_ispy2 = read.csv(('./data/ISPY2_Clinical_R_ITED_384.csv'))
data_zs2 = read.csv(('./data/ZS2_Clinical_R_ITED_590.csv'))
#设置哑变量

#Menstrual_status
data_train$Menstrual_status = as.factor(data_train$Menstrual_status)
levels(data_train$Menstrual_status) = c('0','1')

#pre_cT stage (cT1-2 vs cT3-4)
data_train$pre_cT_stage_2category = data_train$pre_cT_stage
data_train$pre_cT_stage_2category[data_train$pre_cT_stage_2category==1] = 1
data_train$pre_cT_stage_2category[data_train$pre_cT_stage_2category==2] = 1
data_train$pre_cT_stage_2category[data_train$pre_cT_stage_2category==3] = 0
data_train$pre_cT_stage_2category[data_train$pre_cT_stage_2category==4] = 0
data_train$pre_cT_stage_2category =  as.factor(data_train$pre_cT_stage_2category)
levels(data_train$pre_cT_stage_2category) = c('0','1')

#pre_cN stage (cN1 vs cN2-3)
data_train$pre_cN_stage_2category = data_train$pre_cN_stage
data_train$pre_cN_stage_2category[data_train$pre_cN_stage_2category==2] = 0
data_train$pre_cN_stage_2category[data_train$pre_cN_stage_2category==3] = 0
data_train$pre_cN_stage_2category = as.factor(data_train$pre_cN_stage_2category)
levels(data_train$pre_cN_stage_2category) = c('0','1')

# ER status
data_train$ER_status_category = data_train$ER_status
data_train$ER_status_category[data_train$ER_status_category==0] = 2
data_train$ER_status_category[data_train$ER_status_category==1] = 0
data_train$ER_status_category[data_train$ER_status_category==2] = 1
data_train$ER_status_category = as.factor(data_train$ER_status_category)
# data_train$ER_status = as.factor(data_train$ER_status)
levels(data_train$ER_status_category) = c('0','1')

# PR status
data_train$PR_status_category = data_train$PR_status
data_train$PR_status_category[data_train$PR_status_category==0] = 2
data_train$PR_status_category[data_train$PR_status_category==1] = 0
data_train$PR_status_category[data_train$PR_status_category==2] = 1
data_train$PR_status_category = as.factor(data_train$PR_status_category)
# data_train$PR_status = as.factor(data_train$PR_status)
levels(data_train$PR_status_category) = c('0','1')

#HER2_status
data_train$HER2_status = as.factor(data_train$HER2_status)
levels(data_train$HER2_status) = c('0','1')

#Ki67_status
data_train$Ki67_status = as.factor(data_train$Ki67_status)
levels(data_train$Ki67_status) = c('0','1')

# HR status
data_train$HR_status_category = data_train$Molecular_subtypes
data_train$HR_status_category[data_train$HR_status_category==3] = 0
data_train$HR_status_category[data_train$HR_status_category==4] = 0
data_train$HR_status_category[data_train$HR_status_category==2] = 1 
data_train$HR_status_category = as.factor(data_train$HR_status_category)
# data_train$PR_status = as.factor(data_train$PR_status)
levels(data_train$PR_status_category) = c('0','1')

#Molecular_subtypes
data_train$Molecular_subtypes = as.factor(data_train$Molecular_subtypes)
levels(data_train$Molecular_subtypes) = c('1','2','3','4')

#pre_cN_stage
data_train$pre_cN_stage = as.factor(data_train$pre_cN_stage)
levels(data_train$pre_cN_stage) = c('1','2','3')

#age
data_train$age = data_train$age_Y
# -----------------------------
# iTED index and radiomics score
data_train$iTED_prob_C_binary <- ifelse(data_train$proba_ITED_new>median(data_train$proba_ITED_new),1,0)
data_train$Radiomics_prob_C_binary <- ifelse(data_train$proba_radiomics_new>median(data_train$proba_radiomics_new),1,0)

# data_train = data_train[data_train$Group==2,]
outcome_train = data_train$Overall_pCR_gt
#单变量分析
univariate_df = data.frame()
feature_names = names(data_train)[9:length(data_train)]
p_threshold = 0.05 # set p-value threshold 
for (i in 1:length(feature_names)){
  print(i)
  tmp_data = data_train[,feature_names[i]]
  print(feature_names[i])
  model = glm(outcome_train~tmp_data,family = binomial('logit'))
  if(summary(model)$coefficients[2,4] < p_threshold){
    tmp_df = data.frame(row.names = i,feature=feature_names[i],OR = exp(coef(model))[2],lower=exp(confint(model))[2,1],upper=exp(confint(model))[2,2],p_value=summary(model)$coefficients[2,4])
    univariate_df = rbind(univariate_df,tmp_df)
  }
}
univariate_df

# only clinical variables
candidates =c("HER2_status","Molecular_subtypes","HR_status_category")
# only radiomics score
candidates =c("proba_radiomics_new")
# only iTED index
candidates =c("proba_ITED_new")
candidates =c("iTED_prob_C_binary")
# radiomics score + ITED
candidates =c("proba_radiomics_new","proba_ITED_new")
# iTED + clinical variables
candidates =c("proba_ITED_new","HER2_status","Molecular_subtypes","HR_status_category")
# radiomics score + clinical variables
candidates =c("proba_radiomics_new","HER2_status","Molecular_subtypes","HR_status_category")
# combined model
candidates =c("proba_ITED_new","HER2_status","Molecular_subtypes","proba_radiomics_new","HR_status_category")
# # all variables
candidates =c("HER2_status","Molecular_subtypes","proba_radiomics_new","HR_status_category","Ki67_status",
              "pre_cT_stage_2category","pre_cN_stage_2category","Menstrual_status")

# AIC backward feature selection
tmp_data = data_train[c('Overall_pCR_gt',candidates)]
full <- glm(Overall_pCR_gt~., data=tmp_data, family = binomial(link = "logit"))
step_model <- stepAIC(full, direction = 'backward', trace = 1)
step_model <- glm(step_model$formula, data=tmp_data, family = binomial(link = "logit"))
summary(step_model)
summary(full)

#prediction
pred_train <- predict(step_model, data_train, type='response')

#ROC
ROC_train <- pROC::roc(predictor=pred_train, response=data_train$Overall_pCR_gt, ci=T)
CI_train <- round(as.numeric(ROC_train$ci), 3)
print(ROC_train)
print(paste(CI_train[2],',',CI_train[1],',',CI_train[3]))

# plot.roc(ROC_train,asp=NA,legacy.axes = TRUE,col="blue")


# ------------------ZS2 (n = 590)--------------------
data_zs2$Molecular_subtypes = as.factor(data_zs2$Molecular_subtypes)
levels(data_zs2$Molecular_subtypes) = c('1','2','3','4')

pred_zs2 <- predict(step_model, data_zs2, type='response')

ROC_zs2 <- pROC::roc(predictor=pred_zs2, response=data_zs2$Overall_pCR_gt, ci=T)
CI_zs2 <- round(as.numeric(ROC_zs2$ci), 3)
print(ROC_zs2)
print(paste(CI_zs2[2],',',CI_zs2[1],',',CI_zs2[3]))
# lines(ROC_zs2,asp=NA,legacy.axes = TRUE,col="red")

# ------------------Duke (n = 280)--------------------
data_duke$Molecular_subtypes = as.factor(data_duke$Molecular_subtypes)
levels(data_duke$Molecular_subtypes) = c('1','2','3','4')

pred_duke <- predict(step_model, data_duke, type='response')

ROC_duke <- pROC::roc(predictor=pred_duke, response=data_duke$Overall_pCR_gt, ci=T)
CI_duke <- round(as.numeric(ROC_duke$ci), 3)
print(ROC_duke)
print(paste(CI_duke[2],',',CI_duke[1],',',CI_duke[3]))
# lines(ROC_duke,asp=NA,legacy.axes = TRUE,col="orange")

# ------------------ISPY2 (n = 384)--------------------
data_ispy2$Molecular_subtypes = as.factor(data_ispy2$Molecular_subtypes)
levels(data_ispy2$Molecular_subtypes) = c('1','2','3','4')

pred_ispy2 <- predict(step_model, data_ispy2, type='response')

ROC_ispy2 <- pROC::roc(predictor=pred_ispy2, response=data_ispy2$Overall_pCR_gt, ci=T)
CI_ispy2 <- round(as.numeric(ROC_ispy2$ci), 3)
print(ROC_ispy2)
print(paste(CI_ispy2[2],',',CI_ispy2[1],',',CI_ispy2[3]))
# lines(ROC_ispy2,asp=NA,legacy.axes = TRUE,col="purple")

# save results (probabilty)
df_pred_train = data.frame(ID = data_train$ID, group = rep(1,length(pred_train)), prob_C = c(pred_train),label = data_train$Overall_pCR_gt)
df_pred_test_zs2 = data.frame(ID = data_zs2$ID, group = rep(1*2,length(pred_zs2)),prob_C = c(pred_zs2),label = data_zs2$Overall_pCR_gt)
df_pred_test_duke = data.frame(ID = data_duke$ID, group = rep(1*3,length(pred_duke)),prob_C = c(pred_duke),label = data_duke$Overall_pCR_gt)
df_pred_test_ispy2 = data.frame(ID = data_ispy2$ID,group = rep(1*4,length(pred_ispy2)), prob_C = c(pred_ispy2),label = data_ispy2$Overall_pCR_gt)

df_all = rbind(df_pred_train,df_pred_test_zs2,df_pred_test_duke,df_pred_test_ispy2)

# write.csv(df_all,'./R_script/results/BSV_Clinical_proba.csv',row.names = FALSE)
# write.csv(df_all,'./R_script/results/BSV_Radiomics_proba.csv',row.names = FALSE)
# write.csv(df_all,'./R_script/results/BSV_iTED_proba.csv',row.names = FALSE)
# write.csv(df_all,'./R_script/results/BSV_iTED_Radiomics_proba.csv',row.names = FALSE)
# write.csv(df_all,'./R_script/results/BSV_Clinical_iTED_proba.csv',row.names = FALSE)
# write.csv(df_all,'./R_script/results/BSV_Clinical_Radiomics_proba.csv',row.names = FALSE)
# write.csv(df_all,'./R_script/results/BSV_Combined_proba.csv',row.names = FALSE)
