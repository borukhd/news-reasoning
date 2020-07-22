clear
insheet using "C:\Users\drand\Documents\RESEARCH PROJECTS\gord pennycook\fake news\asking accuracy\011819-stratification.csv"

// filter on count of rated outlets
drop if outlets_last_2wks<5 | outlets_last_2wks>30 | outlets_last_2wks==. 
// drop users without ideology score
drop if ideo=="" | ideo=="inf" 
// rescale score to be [0,1] instead of [-2,2]
replace avg_outlet_score_2wks =(avg_outlet_score_2wks +2)/4
// set number of days
gen numDays=13

destring ideo, replace

// create quantiles for each blocking var
xtile Mideo=ideo, nquantiles(4)
xtile Mscore=avg_outlet_score_2wks, nquantiles(4)
xtile Mcount=outlets_last_2wks, nquantiles(4)


// set random seed so assignment is reproducible
set seed 98034

// generate random number that will be used for randomization
generate rand = runiform()



// assign treatment day
//      sort on each blocking variable and the random number
sort bot Mideo Mcount Mscore rand
//		 assign treatment day by numbering users to 1-numDays      
gen id2=_n
gen day=mod(id2,numDays)+1
//     confirm balance across days on the blocking vars 
mean Mideo Mcount Mscore , over(day)
