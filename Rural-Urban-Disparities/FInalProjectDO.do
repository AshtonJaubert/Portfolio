log using C:\Users\ashto\Documents\project\project.txt, text replace 
cd D:\project
dir
*load merged dataset*
use seda_geodist_long_cs.dta, clear
** only keep values that only contain values mth (math) in subject:
* Filter the dataset so it only contains data that we will use for our project
keep if subject == "mth"
keep sedalea subject cs_mn_all urban suburb town rural locale_city_large locale_city_midsize locale_city_small locale_suburb_large locale_suburb_midsize locale_suburb_small locale_town_fringe locale_town_distant locale_town_remote locale_rural_fringe locale_rural_distant locale_rural_remote year grade stateabb_x perecd unempall povertyall
** codebook and describe new filtered dataset: **
describe
codebook, compact
** A descriptive summary of the variables that we will use:
/*
Variable Descriptions:
year                 - Spring of school year
grade                - Grade level
stateabb             - State abbreviation
suburb               - Proportion of students in suburban locale schools
town                 - Proportion of students in town locale schools
rural                - Proportion of students in rural locale schools
locale_city_large    - Proportion of students in city, large locale schools
locale_city_midsize  - Proportion of students in city, midsize locale schools
locale_city_small    - Proportion of students in city, small locale schools
locale_suburb_large  - Proportion of students in suburb, large locale schools
locale_suburb_midsize- Proportion of students in suburb, midsize locale schools
locale_suburb_small  - Proportion of students in suburb, small locale schools
locale_town_fringe   - Proportion of students in town, fringe locale schools
locale_town_distant  - Proportion of students in town, distant locale schools
locale_town_remote   - Proportion of students in town, remote locale schools
locale_rural_fringe  - Proportion of students in rural, fringe locale schools
locale_rural_distant - Proportion of students in rural, distant locale schools
locale_rural_remote  - Proportion of students in rural, remote locale schools
*/
*rename cs_mn_all to test_scores to avoid confusion:

**run summary statistics of variables in the new dataset:
sum sedalea subject cs_mn_all urban suburb town rural locale_city_large locale_city_midsize
sum locale_city_small locale_suburb_large locale_suburb_midsize locale_suburb_small
sum locale_town_fringe locale_town_distant locale_town_remote locale_rural_fringe
sum locale_rural_distant locale_rural_remote
sum grade year stateabb_x
*** run correlation matrix of variables against test scores:
corr cs_mn_all urban suburb town rural ///
     locale_city_large locale_city_midsize locale_city_small ///
     locale_suburb_large locale_suburb_midsize locale_suburb_small ///
     locale_town_fringe locale_town_distant locale_town_remote ///
     locale_rural_fringe locale_rural_distant locale_rural_remote perecd povertyall unempall
matrix C = r(C)
** from this we discovered that variables that indicate rural districts are negatively related to cs_mn_all
** scatter plot of cs_mn_all and locale_rural_remote:
twoway scatter cs_mn_all locale_rural_remote
** simple linear regression for cs_mn_all and rural:
reg cs_mn_all rural
**** 9: multiple regression of cs_mn_all against several geographic variables
** multiple regression only using rural metrics towards cs_mn_all
reg cs_mn_all locale_rural_fringe
reg cs_mn_all locale_rural_fringe locale_rural_distant
reg cs_mn_all locale_rural_fringe locale_rural_distant locale_rural_remote
** multiple regression using rural metrics towards cs_mn_all and nonrural metrics
reg cs_mn_all locale_rural_fringe locale_rural_distant locale_rural_remote urban
reg cs_mn_all locale_rural_fringe locale_rural_distant locale_rural_remote urban town
** regression for all**
reg cs_mn_all locale_city_large locale_city_midsize locale_city_small ///
     locale_suburb_large locale_suburb_midsize locale_suburb_small ///
     locale_town_fringe locale_town_distant locale_town_remote ///
     locale_rural_fringe locale_rural_distant locale_rural_remote perecd povertyall unempall
********* Data Exploration and Visualization: ********
*** heatmap of variables being used for regressions:
matrix rownames C = cs_mn_all urban suburb town rural ///
                      locale_city_large locale_city_midsize locale_city_small ///
                      locale_suburb_large locale_suburb_midsize locale_suburb_small ///
                      locale_town_fringe locale_town_distant locale_town_remote ///
                      locale_rural_fringe locale_rural_distant locale_rural_remote

matrix colnames C = cs_mn_all urban suburb town rural ///
                      locale_city_large locale_city_midsize locale_city_small ///
                      locale_suburb_large locale_suburb_midsize locale_suburb_small ///
                      locale_town_fringe locale_town_distant locale_town_remote ///
                      locale_rural_fringe locale_rural_distant locale_rural_remote
heatplot C, xlabel(, angle(45)) ylabel(, angle(0)) ///
    legend(title("Correlation")) title("Correlation Heatmap")

* Graph cs_mn_all by year
graph bar (mean) cs_mn_all, over(year)
* Graph cs_mn_all by grade level **
graph bar (mean) cs_mn_all, over(grade)
*** creating dummy variables that include the interquartile range of locale variables:
** urban
gen urban_lower25 = (urban <= r(p25))   // Lower 25%
gen urban_middle25 = (urban > r(p25) & urban <= r(p50))   // Middle 25%
gen urban_upper25 = (urban > r(p50) & urban <= r(p75))   // Upper 25%
gen urban_upper100 = (urban > r(p75))   // Upper 25% (75-100%)
tabulate urban_lower25 urban_middle25
tabulate urban_upper25 urban_upper100
** suburb
summarize suburb, detail
gen suburb_lower25 = (suburb <= r(p25))
gen suburb_middle25 = (suburb > r(p25) & suburb <= r(p50))
gen suburb_upper25 = (suburb > r(p50) & suburb <= r(p75))
gen suburb_upper100 = (suburb > r(p75))
tabulate suburb_lower25 suburb_middle25
tab suburb_upper25 suburb_upper100
*town
summarize town, detail
gen town_lower25 = (town <= r(p25))
gen town_middle25 = (town > r(p25) & town <= r(p50))
gen town_upper25 = (town > r(p50) & town <= r(p75))
gen town_upper100 = (town > r(p75))
tabulate town_lower25 town_middle25
tab town_upper25 town_upper100
* rural
summarize rural, detail
gen rural_lower25 = (rural <= r(p25))
gen rural_middle25 = (rural > r(p25) & rural <= r(p50))
gen rural_upper25 = (rural > r(p50) & rural <= r(p75))
gen rural_upper100 = (rural > r(p75))
tabulate rural_lower25 rural_middle25
tab  rural_upper25 rural_upper100
* locale_city_large
summarize locale_city_large, detail
gen locale_city_large_lower25 = (locale_city_large <= r(p25))
gen locale_city_large_middle25 = (locale_city_large > r(p25) & locale_city_large <= r(p50))
gen locale_city_large_upper25 = (locale_city_large > r(p50) & locale_city_large <= r(p75))
gen locale_city_large_upper100 = (locale_city_large > r(p75))
tabulate locale_city_large_lower25 locale_city_large_middle25
tab locale_city_large_upper25 locale_city_large_upper100
* locale_city_midsize
summarize locale_city_midsize, detail
gen locale_city_midsize_lower25 = (locale_city_midsize <= r(p25))
gen locale_city_midsize_middle25 = (locale_city_midsize > r(p25) & locale_city_midsize <= r(p50))
gen locale_city_midsize_upper25 = (locale_city_midsize > r(p50) & locale_city_midsize <= r(p75))
gen locale_city_midsize_upper100 = (locale_city_midsize > r(p75))
tabulate locale_city_midsize_lower25 locale_city_midsize_middle25
tab locale_city_midsize_upper25 locale_city_midsize_upper100
*
summarize locale_city_small, detail
gen locale_city_small_lower25 = (locale_city_small <= r(p25))
gen locale_city_small_middle25 = (locale_city_small > r(p25) & locale_city_small <= r(p50))
gen locale_city_small_upper25 = (locale_city_small > r(p50) & locale_city_small <= r(p75))
gen locale_city_small_upper100 = (locale_city_small > r(p75))
tabulate locale_city_small_lower25 locale_city_small_middle25
tab locale_city_small_upper25 locale_city_small_upper100
*
summarize locale_suburb_large, detail
gen locale_suburb_large_lower25 = (locale_suburb_large <= r(p25))
gen locale_suburb_large_middle25 = (locale_suburb_large > r(p25) & locale_suburb_large <= r(p50))
gen locale_suburb_large_upper25 = (locale_suburb_large > r(p50) & locale_suburb_large <= r(p75))
gen locale_suburb_large_upper100 = (locale_suburb_large > r(p75))
tabulate locale_suburb_large_lower25 locale_suburb_large_middle25
 tab locale_suburb_large_upper25 locale_suburb_large_upper100
*
summarize locale_suburb_midsize, detail
gen locale_suburb_midsize_lower25 = (locale_suburb_midsize <= r(p25))
gen locale_suburb_midsize_middle25 = (locale_suburb_midsize > r(p25) & locale_suburb_midsize <= r(p50))
gen locale_suburb_midsize_upper25 = (locale_suburb_midsize > r(p50) & locale_suburb_midsize <= r(p75))
gen locale_suburb_midsize_upper100 = (locale_suburb_midsize > r(p75))
tabulate locale_suburb_midsize_lower25 locale_suburb_midsize_middle25
tab locale_suburb_midsize_upper25 locale_suburb_midsize_upper100
*
summarize locale_suburb_small, detail
gen locale_suburb_small_lower25 = (locale_suburb_small <= r(p25))
gen locale_suburb_small_middle25 = (locale_suburb_small > r(p25) & locale_suburb_small <= r(p50))
gen locale_suburb_small_upper25 = (locale_suburb_small > r(p50) & locale_suburb_small <= r(p75))
gen locale_suburb_small_upper100 = (locale_suburb_small > r(p75))
tabulate locale_suburb_small_lower25 locale_suburb_small_middle25
tab locale_suburb_small_upper25 locale_suburb_small_upper100
*
summarize locale_town_fringe, detail
gen locale_town_fringe_lower25 = (locale_town_fringe <= r(p25))
gen locale_town_fringe_middle25 = (locale_town_fringe > r(p25) & locale_town_fringe <= r(p50))
gen locale_town_fringe_upper25 = (locale_town_fringe > r(p50) & locale_town_fringe <= r(p75))
gen locale_town_fringe_upper100 = (locale_town_fringe > r(p75))
tabulate locale_town_fringe_lower25 locale_town_fringe_middle25
tab locale_town_fringe_upper25 locale_town_fringe_upper100
*
summarize locale_town_distant, detail
gen locale_town_distant_lower25 = (locale_town_distant <= r(p25))
gen locale_town_distant_middle25 = (locale_town_distant > r(p25) & locale_town_distant <= r(p50))
gen locale_town_distant_upper25 = (locale_town_distant > r(p50) & locale_town_distant <= r(p75))
gen locale_town_distant_upper100 = (locale_town_distant > r(p75))
tabulate locale_town_distant_lower25 locale_town_distant_middle25
tab locale_town_distant_upper25 locale_town_distant_upper100
*
summarize locale_town_remote, detail
gen locale_town_remote_lower25 = (locale_town_remote <= r(p25))
gen locale_town_remote_middle25 = (locale_town_remote > r(p25) & locale_town_remote <= r(p50))
gen locale_town_remote_upper25 = (locale_town_remote > r(p50) & locale_town_remote <= r(p75))
gen locale_town_remote_upper100 = (locale_town_remote > r(p75))
tabulate locale_town_remote_lower25 locale_town_remote_middle25
tab locale_town_remote_upper25 locale_town_remote_upper100
*
summarize locale_rural_fringe, detail
gen locale_rural_fringe_lower25 = (locale_rural_fringe <= r(p25))
gen locale_rural_fringe_middle25 = (locale_rural_fringe > r(p25) & locale_rural_fringe <= r(p50))
gen locale_rural_fringe_upper25 = (locale_rural_fringe > r(p50) & locale_rural_fringe <= r(p75))
gen locale_rural_fringe_upper100 = (locale_rural_fringe > r(p75))
tabulate locale_rural_fringe_lower25 locale_rural_fringe_middle25
tab locale_rural_fringe_upper25 locale_rural_fringe_upper100
*
summarize locale_rural_distant, detail
gen locale_rural_distant_lower25 = (locale_rural_distant <= r(p25))
gen locale_rural_distant_middle25 = (locale_rural_distant > r(p25) & locale_rural_distant <= r(p50))
gen locale_rural_distant_upper25 = (locale_rural_distant > r(p50) & locale_rural_distant <= r(p75))
gen locale_rural_distant_upper100 = (locale_rural_distant > r(p75))
tabulate locale_rural_distant_lower25 locale_rural_distant_middle25
tab locale_rural_distant_upper25 locale_rural_distant_upper100
*
summarize locale_rural_remote, detail
gen locale_rural_remote_lower25 = (locale_rural_remote <= r(p25))
gen locale_rural_remote_middle25 = (locale_rural_remote > r(p25) & locale_rural_remote <= r(p50))
gen locale_rural_remote_upper25 = (locale_rural_remote > r(p50) & locale_rural_remote <= r(p75))
gen locale_rural_remote_upper100 = (locale_rural_remote > r(p75))
tabulate locale_rural_remote_lower25 locale_rural_remote_middle25
tab locale_rural_remote_upper25 locale_rural_remote_upper100

* --- Generate Lower and Upper 25% Dummies for Socioeconomic Variables ---

* perecd (Percent Economically Disadvantaged)
summarize perecd, detail
gen perecd_lower25 = (perecd <= r(p25)) if !missing(perecd)
gen perecd_upper25 = (perecd > r(p75)) if !missing(perecd)
label var perecd_lower25 "Perecd: Lowest 25%"
label var perecd_upper25 "Perecd: Highest 25% (Above 75th pct)"

* unempall (Unemployment Rate)
summarize unempall, detail
gen unempall_lower25 = (unempall <= r(p25)) if !missing(unempall)
gen unempall_upper25 = (unempall > r(p75)) if !missing(unempall)
label var unempall_lower25 "Unempall: Lowest 25%"
label var unempall_upper25 "Unempall: Highest 25% (Above 75th pct)"

* povertyall (Poverty Rate)
summarize povertyall, detail
gen povertyall_lower25 = (povertyall <= r(p25)) if !missing(povertyall)
gen povertyall_upper25 = (povertyall > r(p75)) if !missing(povertyall)
label var povertyall_lower25 "Povertyall: Lowest 25%"
label var povertyall_upper25 "Povertyall: Highest 25% (Above 75th pct)"

* --- Create Socioeconomic Group Variable ---

gen socioeconomic_group = ""
label var socioeconomic_group "Socioeconomic Category (Lower/Upper 25%)"

* Assign labels
replace socioeconomic_group = "Perecd: Lower 25%" if perecd_lower25 == 1 & !missing(perecd_lower25)
replace socioeconomic_group = "Perecd: Upper 25%" if perecd_upper25 == 1 & !missing(perecd_upper25)

replace socioeconomic_group = "Unempall: Lower 25%" if unempall_lower25 == 1 & !missing(unempall_lower25)
replace socioeconomic_group = "Unempall: Upper 25%" if unempall_upper25 == 1 & !missing(unempall_upper25)

replace socioeconomic_group = "Povertyall: Lower 25%" if povertyall_lower25 == 1 & !missing(povertyall_lower25)
replace socioeconomic_group = "Povertyall: Upper 25%" if povertyall_upper25 == 1 & !missing(povertyall_upper25)

* --- Summarize Scores by Socioeconomic Group ---

* Display counts for each generated category
tabulate socioeconomic_group

* Display mean scores 
* This shows how cs_mn_all varies across the lower/upper ends of each SES indicator
tabstat cs_mn_all, by(socioeconomic_group) stats(mean count sd) columns(statistics) longstub
* we have made all the interquartile dummy variables now we can see how they compare towards each other in cs_mn_all:
* Locale: Rural Remote
mean cs_mn_all if locale_rural_remote_lower25 == 1
mean cs_mn_all if locale_rural_remote_upper100 == 1

* Locale: Rural Distant
mean cs_mn_all if locale_rural_distant_lower25 == 1
mean cs_mn_all if locale_rural_distant_upper100 == 1

* Locale: Rural Fringe
mean cs_mn_all if locale_rural_fringe_lower25 == 1
mean cs_mn_all if locale_rural_fringe_upper100 == 1

* Locale: Town Remote
mean cs_mn_all if locale_town_remote_lower25 == 1
mean cs_mn_all if locale_town_remote_upper100 == 1

* Locale: Town Distant
mean cs_mn_all if locale_town_distant_lower25 == 1
mean cs_mn_all if locale_town_distant_upper100 == 1

* Locale: Town Fringe
mean cs_mn_all if locale_town_fringe_lower25 == 1
mean cs_mn_all if locale_town_fringe_upper100 == 1

* Locale: Suburb Small
mean cs_mn_all if locale_suburb_small_lower25 == 1
mean cs_mn_all if locale_suburb_small_upper100 == 1

* Locale: Suburb Midsize
mean cs_mn_all if locale_suburb_midsize_lower25 == 1
mean cs_mn_all if locale_suburb_midsize_upper100 == 1

* Locale: Suburb Large
mean cs_mn_all if locale_suburb_large_lower25 == 1
mean cs_mn_all if locale_suburb_large_upper100 == 1

* Locale: City Small
mean cs_mn_all if locale_city_small_lower25 == 1
mean cs_mn_all if locale_city_small_upper100 == 1

* Locale: City Midsize
mean cs_mn_all if locale_city_midsize_lower25 == 1
mean cs_mn_all if locale_city_midsize_upper100 == 1

* Locale: City Large
mean cs_mn_all if locale_city_large_lower25 == 1
mean cs_mn_all if locale_city_large_upper100 == 1
* Now show the means by this group
gen rural_group = ""
replace rural_group = "Rural Remote: Lower 25%" if locale_rural_remote_lower25 == 1
replace rural_group = "Rural Remote: Upper 100%" if locale_rural_remote_upper100 == 1
replace rural_group = "Rural Distant: Lower 25%" if locale_rural_distant_lower25 == 1
replace rural_group = "Rural Distant: Upper 100%" if locale_rural_distant_upper100 == 1
replace rural_group = "Rural Fringe: Lower 25%" if locale_rural_fringe_lower25 == 1
replace rural_group = "Rural Fringe: Upper 100%" if locale_rural_fringe_upper100 == 1
tabstat cs_mn_all, by(rural_group) stats(mean count sd) columns(statistics)
gen Town_group = ""
replace Town_group = "Town Remote: Lower 25%" if locale_town_remote_lower25 == 1
replace Town_group = "Town Remote: Upper 100%" if locale_town_remote_upper100 == 1
replace Town_group = "Town Distant: Lower 25%" if locale_town_distant_lower25 == 1
replace Town_group = "Town Distant: Upper 100%" if locale_town_distant_upper100 == 1
replace Town_group = "Town Fringe: Lower 25%" if locale_town_fringe_lower25 == 1

tabstat cs_mn_all, by(Town_group) stats(mean count sd) columns(statistics)
gen Suburb_group = ""
replace Suburb_group = "Suburb Small: Lower 25%" if locale_suburb_small_lower25 == 1
replace Suburb_group = "Suburb Small: Upper 100%" if locale_suburb_small_upper100 == 1
replace Suburb_group = "Suburb Midsize: Lower 25%" if locale_suburb_midsize_lower25 == 1
replace Suburb_group = "Suburb Midsize: Upper 100%" if locale_suburb_midsize_upper100 == 1
replace Suburb_group = "Suburb Large: Lower 25%" if locale_suburb_large_lower25 == 1
replace Suburb_group = "Suburb Large: Upper 100%" if locale_suburb_large_upper100 == 1
tabstat cs_mn_all, by(Suburb_group) stats(mean count sd) columns(statistics)
gen City_group = ""
replace City_group = "City Small: Lower 25%" if locale_city_small_lower25 == 1
replace City_group = "City Small: Upper 100%" if locale_city_small_upper100 == 1
replace City_group = "City Midsize: Lower 25%" if locale_city_midsize_lower25 == 1
replace City_group = "City Midsize: Upper 100%" if locale_city_midsize_upper100 == 1
replace City_group = "City Large: Lower 25%" if locale_city_large_lower25 == 1
replace City_group = "City Large: Upper 100%" if locale_city_large_upper100 == 1
tabstat cs_mn_all, statistics(mean sd n) by(City_group) columns(statistics)
save seda_geodist_long_cs.dta, replace
log close
