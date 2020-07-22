clear * 
insheet using "C:\Users\Drand\Documents\RESEARCH PROJECTS\gord pennycook\fake news\asking accuracy\S5_userday_data.csv"

// focus only on first 24 hours after DM is sent
quietly keep if posttreatment <2 

// transform average quality avg_quality into average relative quality avg_quality
gen avg_rel_quality=avg_quality-.34
replace avg_rel_quality=0 if avg_quality==.
gen avg_rel_quality_rt=avg_quality_rt-.34
replace avg_rel_quality_rt=0 if avg_quality_rt==.


// winsorize relevant variables at 95th percentile
gen Wsummed_rel_quality=summed_rel_quality
replace Wsummed_rel_quality=.59 if summed_rel_quality>.59 & summed_rel_quality~=.
replace Wsummed_rel_quality=-.57 if summed_rel_quality<-.57 & summed_rel_quality~=.
gen Wcount_misinfo=count_misinfo
replace Wcount_misinfo=4 if count_misinfo>4 & count_misinfo~=.
gen Wcount_mainstream=count_mainstream
replace Wcount_mainstream=4 if count_mainstream>4 & count_mainstream~=.
gen Wunrated=unrated
replace Wunrated=160 if unrated>160 & unrated~=.
gen Wsummed_rel_quality_rt=summed_rel_quality_rt
replace Wsummed_rel_quality_rt=.59 if summed_rel_quality_rt>.59 & summed_rel_quality_rt~=.
replace Wsummed_rel_quality_rt=-.55 if summed_rel_quality_rt<-.55 & summed_rel_quality_rt~=.
gen Wcount_misinfo_rt=count_misinfo_rt
replace Wcount_misinfo_rt=4 if count_misinfo_rt>4 & count_misinfo_rt~=.
gen Wcount_mainstream_rt=count_mainstream_rt
replace Wcount_mainstream_rt=4 if count_mainstream_rt>4 & count_mainstream_rt~=.
gen Wunrated_rt=unrated_rt
replace Wunrated_rt=118 if unrated_rt>118 & unrated_rt~=.
gen Wcount_rt=count_rt
replace Wcount_rt=125 if count_rt>125 & count_rt~=.






///////////////////////////
// Intent-to-treat for wave 2 day 3 (where randomization failure occurred)
{
preserve

// create centered wave dummies and interactions with treatment 
quietly tabulate wave, gen(wave_)
quietly egen wave2z=std(wave_2)
quietly egen wave3z=std(wave_3)
quietly gen wave2z_x_post=wave2z*posttreatment
quietly gen wave3z_x_post=wave3z*posttreatment

// create centered date dummies and interactions with treatment
quietly tabulate date, gen(date_)
quietly egen tmp=group(date)
quietly sum tmp, meanonly
forvalues y=2/`r(max)' {
quietly egen zdate_`y' =std(date_`y')
quietly gen post1Xdate`y' = posttreatment*zdate_`y'
}
quietly drop tmp



// AVERAGE RELATIVE QUALITY
//
//     all tweets
//          wave fixed effects
reg avg_rel_quality posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg avg_rel_quality posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg avg_rel_quality posttreatment z* , cluster(screen_name)
//			date post-stratified
reg avg_rel_quality posttreatment *X* z*  , cluster(screen_name)
//
//     only RTs without comment 
//          wave fixed effects
reg avg_rel_quality_rt posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg avg_rel_quality_rt posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg avg_rel_quality_rt posttreatment z* , cluster(screen_name)
//			date post-stratified
reg avg_rel_quality_rt posttreatment *X* z*  , cluster(screen_name)

// SUMMED RELATIVE QUALITY
//
//     all tweets
//          wave fixed effects
reg Wsummed_rel_quality posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wsummed_rel_quality posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wsummed_rel_quality posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wsummed_rel_quality posttreatment *X* z*  , cluster(screen_name)
//
//     only RTs without comment 
//          wave fixed effects
reg Wsummed_rel_quality_rt posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wsummed_rel_quality_rt posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wsummed_rel_quality_rt posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wsummed_rel_quality_rt posttreatment *X* z*  , cluster(screen_name)

// TWEETS WITHOUT LINKS TO RATED NEWS SITES
//
//     all tweets
//          wave fixed effects
reg Wunrated posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wunrated posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wunrated posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wunrated posttreatment *X* z*  , cluster(screen_name)
//
//     only RTs without comment 
//          wave fixed effects
reg Wunrated_rt posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wunrated_rt posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wunrated_rt posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wunrated_rt posttreatment *X* z*  , cluster(screen_name)

// DISCERNMENT
//
// reshape data into long format (separate rows for mainstream versus misinformation link counts)
gen tmp=_n
rename Wcount_misinfo Wnum0
rename Wcount_mainstream Wnum1
rename Wcount_misinfo_rt Wnum_rt0
rename Wcount_mainstream_rt Wnum_rt1
reshape long Wnum Wnum_rt, i(tmp) j(mainstream)
quietly drop tmp
//
// create interactions between the mainstream dummy and all the date dummies and date dummy interactions
quietly egen tmp=group(date)
quietly sum tmp, meanonly
forvalues y=2/`r(max)' {
quietly gen mainstreamXzdate_`y' =mainstream*zdate_`y'
quietly gen gooodXpost1Xdate`y' = mainstream*posttreatment*zdate_`y'
}
//
// now do the regressions
//
//     all tweets
//          wave fixed effects
xi: reg Wnum i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z , cluster(screen_name)  
//			wave post-stratified
xi: reg Wnum i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z i.mainstream*wave2z_x_post i.mainstream*wave3z_x_post , cluster(screen_name) 
//				no difference in treatment effect size across waves
test _ImaiXwave2a1 _ImaiXwave3a1
//			date fixed effects 
xi: reg Wnum i.mainstream*posttreatment z* mainstreamXz*, cluster(screen_name)  
//			date post-stratified
xi: reg Wnum i.mainstream*posttreatment *X* z*  , cluster(screen_name) 
//
//     only RTs without comment 
//          wave fixed effects	
xi: reg Wnum_rt i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z , cluster(screen_name)  
//			wave post-stratified
xi: reg Wnum_rt i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z i.mainstream*wave2z_x_post i.mainstream*wave3z_x_post , cluster(screen_name)  
//				no difference in treatment effect size across waves
test _ImaiXwave2a1 _ImaiXwave3a1
//			date fixed effects
xi: reg Wnum_rt i.mainstream*posttreatment z* mainstreamXz*, cluster(screen_name)  
//			date post-stratified
xi: reg Wnum_rt i.mainstream*posttreatment *X* z*  , cluster(screen_name) 

restore
//////////////////
}




///////////////////////////
// Exclusion of data from wave 2 day 3 
{
preserve

// drop data from the day where randomization failure occurred
quietly drop if wave==2 & (date==43357 )

// create centered wave dummies and interactions with treatment 
quietly tabulate wave, gen(wave_)
quietly egen wave2z=std(wave_2)
quietly egen wave3z=std(wave_3)
quietly gen wave2z_x_post=wave2z*posttreatment
quietly gen wave3z_x_post=wave3z*posttreatment

// create centered date dummies and interactions with treatment
quietly tabulate date, gen(date_)
quietly egen tmp=group(date)
quietly sum tmp, meanonly
forvalues y=2/`r(max)' {
quietly egen zdate_`y' =std(date_`y')
quietly gen post1Xdate`y' = posttreatment*zdate_`y'
}
quietly drop tmp



// AVERAGE RELATIVE QUALITY
//
//     all tweets
//          wave fixed effects
reg avg_rel_quality posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg avg_rel_quality posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg avg_rel_quality posttreatment z* , cluster(screen_name)
//			date post-stratified
reg avg_rel_quality posttreatment *X* z*  , cluster(screen_name)
//
//     only RTs without comment 
//          wave fixed effects
reg avg_rel_quality_rt posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg avg_rel_quality_rt posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg avg_rel_quality_rt posttreatment z* , cluster(screen_name)
//			date post-stratified
reg avg_rel_quality_rt posttreatment *X* z*  , cluster(screen_name)

// SUMMED RELATIVE QUALITY
//
//     all tweets
//          wave fixed effects
reg Wsummed_rel_quality posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wsummed_rel_quality posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wsummed_rel_quality posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wsummed_rel_quality posttreatment *X* z*  , cluster(screen_name)
//
//     only RTs without comment 
//          wave fixed effects
reg Wsummed_rel_quality_rt posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wsummed_rel_quality_rt posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wsummed_rel_quality_rt posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wsummed_rel_quality_rt posttreatment *X* z*  , cluster(screen_name)

// TWEETS WITHOUT LINKS TO RATED NEWS SITES
//
//     all tweets
//          wave fixed effects
reg Wunrated posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wunrated posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wunrated posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wunrated posttreatment *X* z*  , cluster(screen_name)
//
//     only RTs without comment 
//          wave fixed effects
reg Wunrated_rt posttreatment wave2z wave3z , cluster(screen_name)
//			wave post-stratified
reg Wunrated_rt posttreatment wave2z wave3z wave2z_x_post wave3z_x_post , cluster(screen_name)
//				no difference in treatment effect size across waves
test wave2z_x_post wave3z_x_post 
//			date fixed effects
reg Wunrated_rt posttreatment z* , cluster(screen_name)
//			date post-stratified
reg Wunrated_rt posttreatment *X* z*  , cluster(screen_name)

// DISCERNMENT
//
// reshape data into long format (separate rows for mainstream versus misinformation link counts)
gen tmp=_n
rename Wcount_misinfo Wnum0
rename Wcount_mainstream Wnum1
rename Wcount_misinfo_rt Wnum_rt0
rename Wcount_mainstream_rt Wnum_rt1
reshape long Wnum Wnum_rt, i(tmp) j(mainstream)
quietly drop tmp
//
// create interactions between the mainstream dummy and all the date dummies and date dummy interactions
quietly egen tmp=group(date)
quietly sum tmp, meanonly
forvalues y=2/`r(max)' {
quietly gen mainstreamXzdate_`y' =mainstream*zdate_`y'
quietly gen gooodXpost1Xdate`y' = mainstream*posttreatment*zdate_`y'
}
//
// now do the regressions
//
//     all tweets
//          wave fixed effects
xi: reg Wnum i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z , cluster(screen_name)  
//			wave post-stratified
xi: reg Wnum i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z i.mainstream*wave2z_x_post i.mainstream*wave3z_x_post , cluster(screen_name) 
//				no difference in treatment effect size across waves
test _ImaiXwave2a1 _ImaiXwave3a1
//			date fixed effects 
xi: reg Wnum i.mainstream*posttreatment z* mainstreamXz*, cluster(screen_name)  
//			date post-stratified
xi: reg Wnum i.mainstream*posttreatment *X* z*  , cluster(screen_name) 
//
//     only RTs without comment 
//          wave fixed effects	
xi: reg Wnum_rt i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z , cluster(screen_name)  
//			wave post-stratified
xi: reg Wnum_rt i.mainstream*posttreatment i.mainstream*wave2z i.mainstream*wave3z i.mainstream*wave2z_x_post i.mainstream*wave3z_x_post , cluster(screen_name)  
//				no difference in treatment effect size across waves
test _ImaiXwave2a1 _ImaiXwave3a1
//			date fixed effects
xi: reg Wnum_rt i.mainstream*posttreatment z* mainstreamXz*, cluster(screen_name)  
//			date post-stratified
xi: reg Wnum_rt i.mainstream*posttreatment *X* z*  , cluster(screen_name) 

restore
//////////////////
}

