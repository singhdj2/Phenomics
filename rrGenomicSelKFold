################################################################
##### Basic Ridge Regression BLUP based Genomic Selection ######
##### Daljit Singh (singhdj2@ksu.edu)                     ######
##### Updated: 09-16-2018                                 ######
################################################################

## This script takes:
#  - phenotypic data with multiple trait columns
#  - genotype/marker data (can take missing data)
## It performs:
#  - k-fold cross-validation with n-repeats
## It outputs:
#  - average genomic prediction accuracy by trait
## Note: Before running this script, make sure:
#   - The genotypes are correctly ordered in geno and pheno data frames
#   - Markers are formatted in {-1,0,1} format
## Also, this script was created as a basic GS tutorial, so as such,...
## ...the results should be indpendently varified in other programs before publication.

# load pcakages
install.packages("pacman")
library(pacman)
p_load(tidyverse,rrBLUP)

#### rBLUP GS model ####
## CV scheme 1. k-1 fold training set predicting the remaining 1 fold 
# read geno file
geno <- read.table("genotypic_GS.txt",header=T)
dim(geno)
geno[1:4,1:4]
# remove markers with too much missing data (>20%); impute the rest
geno <- A.mat(geno,min.MAF = 0.05,max.missing = 0.20,impute.method = "mean",return.imputed = TRUE)$imputed
#** we have 7456 markers now to work with compared to 16000 earlier..

# read pheno file
pheno <- read.table("meerut_traitsGS.txt",header = T)
pheno$GID <- row.names(pheno)   #create a new gid column of line names
row.names(pheno) <- NULL      #remove rownames
head(pheno)  # phenotype file
pheno <- select(pheno,GID,everything())  #rearrange columns
#pheno <- select(pheno,GID,1:2)  #rearrange columns


rrGenomicSel <- function(pheno, geno, nFold=5, nRepeat=5){
  ## create empty dataframe to hold prediction accuracy values 
  trait.col <-  ncol(pheno)-1   #number of phenotype columns 
  t <- nFold * nRepeat   #number of trials or folds (80% training and 20% testing set)
  out.pred <- matrix(nrow=t, ncol=trait.col) %>% data.frame() #create an empty df to hold validation accuracy
  names(out.pred) <- names(pheno)[-1]  #assign column/trait names
  ## loop over each trait times number of traits
  for (j in 2:ncol(pheno)) {                                        #trait loop
    for (k in 1:nRepeat){                                        #random repeat loop
      ## create a new df with additional column num_trial for k-fold
      #set.seed(8240)
      pt17 <- pheno %>% 
        mutate(num_trial=sample(c(rep(1:nFold,times=(nrow(pheno) %/% nFold)), 1:(nrow(pheno) %% nFold)),nrow(pheno))) %>%  #randomly assign 10 folds to genotypes
        select(GID,num_trial)
      for(l in 1:nFold){                                                #fold-loop
        gid.test <- as.character(pt17$GID[pt17$num_trial==l])       #select gid/line names of trial i
        p_train=pheno[!(pheno$GID %in% gid.test),]       #selects pheno gids for training set (all trials minus i)
        p_valid=pheno[pheno$GID %in% gid.test,]         #selects pheno gids for test set i.e. i
        m_train=geno[!(rownames(geno) %in% gid.test),]     # marker training set
        m_valid=geno[rownames(geno) %in% gid.test,]        # marker validation set
        ## run mixed model
        y_train = p_train[,j]            # this is your pheno trait (y) for the mixed model equations
        y_train_mixed <- try(mixed.solve(y_train, Z=m_train, K=NULL, SE=FALSE, return.Hinv = FALSE))
        if (!class(y_train_mixed)=="try=-error") {
          y.effect = y_train_mixed$u
          e = as.matrix(y.effect)
          pred_y_valid = try(m_valid %*% e)
          if(!class(pred_y_valid)=="try=-error"){
            pred_y = (pred_y_valid[,1]) + y_train_mixed$beta
            #pred_y
            y_valid = p_valid[,j]           # i.e. BLUPs from raw Phenotype data
            cat("Running fold ", l, ", repeat ", k,"of trait ", names(pheno)[j], "\n")
            cort <- cor.test(pred_y_valid, y_valid, use="complete")
            cat(cort$estimate, cort$p.val,"\n")
            out.pred[(l+(5*k-5)),j-1] <- cort$estimate
          } else {
            out.pred[(l+(5*k-5)),j-1] <- NA
          }
        } else {
          out.pred[(l+(5*k-5)),j-1] <- NA    #set to missing where model had issues
        }
      }
    }
  }
  return(out.pred)
}

out.pred.accuracy <- rrGenomicSel(pheno=pheno,geno = geno,nFold = 5,nRepeat = 5)
head(out.pred.accuracy)
# get average pred accuracy per trait
out.summary.mean <- out.pred.accuracy %>%
  summarise_all(.,funs(mean(.,na.rm=T)))
# get standard error on pred accuracy
out.summary.se <- out.pred.accuracy %>%
  summarise_all(.,funs(sd(.,na.rm=T)/sqrt(n())))

## end ##
