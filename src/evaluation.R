library(readr)
dat <-read_csv("parametersPerPersonNonAdapt.csv", 
      col_types = cols(id = col_character(), 
      parameter2 = col_character(), parameter3 = col_character(), 
      value2 = col_double(), value3 = col_double()))
library(tidyr)
dat <- dat[(dat$onlyTrainingOptimization == TRUE) & (dat$adaptModelInTesting == FALSE), ]
data_wide <- spread(dat, parameter1, value1)
data_wide <- spread(data_wide, parameter2, value2)
data_wide <- spread(data_wide, parameter3, value3)
dat <- data_wide

dat$species <- ifelse(dat$source %in% c("HumScrm", "Human", "Humans"), "Human", dat$species)
dat$species <- ifelse(dat$source %in% c("WaspsNew"), "Wasp", dat$species)
dat$species <- ifelse(dat$source %in% c("FHL", "RGMDL3", "RGMDL2", "RGMDL1"), "Monkey", dat$species)
dat$species <- ifelse(dat$source %in% c("Camarena"), "Pigeon", dat$species)

models <- unique(dat$model)
parameters <- c("a", "bMinus", "Db", "h", "b", "B", "bPlus", "e", "s", "t", "y")
param_results <- c()
for (parameter in parameters) {
  param_results <- c(param_results, paste(parameter, ".mean", sep=""), paste(parameter, ".mdn", sep=""), paste(parameter, ".sd", sep=""))
}

eval <- data.frame(matrix(ncol = 38, nrow = 0))
x <- c(c("model", "species"), param_results, c("meanPerformance", "mdnPerformance", "sdPerformance"))
colnames(eval) <- x

for (model in models){
  for (species in unique(dat$species)){
    eval[nrow(eval) + 1,] = c(model, species, rep.int(NA, 36))
  }
}

for (model in models){
  for (species in unique(dat$species)){
    for (parameter in parameters) {
      i <- 0
      funs <- c("mean", "mdn", "sd")
      for (fun in c(mean, median, sd)) {
        i <- i+1
        dat_slice <- dat[(dat$model==model) & (dat$species==species), ]
        col <- dat_slice[parameter]
        col <- as.numeric(unlist(col))
        #if (colSums(!is.na(col)) > 0) {
        try(fun(col))
        try({
          fun(col)
          eval[(eval$model==model) & (eval$species==species), ][paste(parameter, funs[i], sep=".")] <- fun(col)
        }
          , silent=TRUE)
        #}
        eval[(eval$model==model) & (eval$species==species), ]$meanPerformance <- mean(dat_slice$performance)
        eval[(eval$model==model) & (eval$species==species), ]$mdnPerformance <- median(dat_slice$performance)
        eval[(eval$model==model) & (eval$species==species), ]$sdPerformance <- sd(dat_slice$performance)
      }
    }
  }
}
png("rlelo_a")
boxplot(a~species, data=dat[dat$model=="RLELO",], ylab="Parameter value after optimization")
dev.off()
png("rlelo_b")
boxplot(b~species, data=dat[dat$model=="RLELO",], ylab="Parameter value after optimization")
dev.off()
png("rescorlaWynne_a")
boxplot(a~species, data=dat[dat$model=="RescorlaWagnerWynne95",], ylab="Parameter value after optimization")
dev.off()
png("rescorlaWynne_B")
boxplot(B~species, data=dat[dat$model=="RescorlaWagnerWynne95",], ylab="Parameter value after optimization")
dev.off()
png("sct_a")
boxplot(a~species, data=dat[dat$model=="SCT",], ylab="Parameter value after optimization")
dev.off()
png("Trabasso_h")
boxplot(h~species, data=dat[dat$model=="Trabasso",], ylab="Parameter value after optimization")
dev.off()
png("vtt_a")
boxplot(a~species, data=dat[dat$model=="VTTBS",], ylab="Parameter value after optimization")
dev.off()
png("vtt_b")
boxplot(b~species, data=dat[dat$model=="VTTBS",], ylab="Parameter value after optimization")
dev.off()
png("vtt_t")
boxplot(t~species, data=dat[dat$model=="VTTBS",], ylab="Parameter value after optimization")
dev.off()

eval$meanPerformance <- as.double(eval$meanPerformance)
eval$mdnPerformance <- as.double(eval$mdnPerformance)
eval$sdPerformance <- as.double(eval$sdPerformance)

wasps <- dat[dat$species =="Wasp", ]  # best models: Siemann Delius (0.7202081   0.7747855    0.13402594) ; configuralCuesWynne95
wilcox.test(wasps[wasps$model=="SiemannDelius",]$performance, wasps[wasps$model=="configuralCuesWynne95",]$performance)

pigeons <- dat[dat$species =="Pigeon",] # RLELO_F (0.7469570      0.7427043    0.03931642); Trabasso ( 0.7453732      0.7426449    0.04103056)
wilcox.test(pigeons[pigeons$model=="RLELO_F",]$performance, pigeons[pigeons$model=="Trabasso",]$performance)

humans <- dat[dat$species == "Human",] #configuralCuesWynne95 ; RLELO
wilcox.test(humans[humans$model=="configuralCuesWynne95",]$performance, humans[humans$model=="RLELO",]$performance)

monkeys <- dat[dat$species =="Monkey",] # Siemann Delius (0.7445730  0.7027276    0.11833391); Trabasso (0.6925297      0.7017958    0.11970595)
wilcox.test(monkeys[monkeys$model=="RLELO_F",]$performance, monkeys[monkeys$model=="Trabasso",]$performance)


# Performance of the species
correct <- dat[dat$model== "CorrectReply", ]
correct$species <- as.factor(correct$species)
boxplot(performance~species, data=correct)
