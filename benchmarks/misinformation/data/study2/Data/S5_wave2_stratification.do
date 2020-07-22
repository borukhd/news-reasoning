clear
insheet using "091018-data_for_stratifications.csv"

// exclude subjects who were not assigned a bot score or ideology score, or who tweeted no rated links in the previous 2 weeks
drop if bot_score==-2 | avg_outlet_score==. | ideo=="" | ideo=="inf"

destring ideo, replace

// median split on each blocking variable
xtile Mideo=ideo
xtile Mscore=avg_outlet_score
xtile Mcount=outlet_count

// set random seed so assignment is reproducible
set seed 98034

// generate two random numbers that will be used for randomization
generate rand = runiform()
generate rand2 = runiform()

// first, assign users to treatment vs control
//       sort on each blocking variable and the random number
sort bot Mideo Mcount Mscore rand 
//      then assign odd users to control, even to treatment
gen id=_n
gen condition=id==(round(id/2)*2)
//     confirm balance across conditions on the 3 blocking vars 
mean Mideo Mcount Mscore , over(condition)

// next, assign treatment day (adding condition as another thing to block on)
//       sort on each blocking variable and the random number
sort bot Mideo Mcount Mscore condition rand2
//		 assign treatment day by numbering users to 1-3      
gen id2=_n
gen day=mod(id2,3)
//     confirm balance across days on the 4 blocking vars 
mean Mideo Mcount Mscore condition, over(day)
