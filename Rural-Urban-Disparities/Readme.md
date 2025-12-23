# Rural-Urban Disparities in Student Achievement

**Authors:** Ashton Jaubert, Ryan Orr, Sal Patlan

**Institution:** Texas State University

**Department:** Department of Finance and Economics

![Status](https://img.shields.io/badge/Status-Completed-success)
![Tools](https://img.shields.io/badge/Tools-Stata%20|%20Excel%20|%20SEDA%20Data-blue)

## 📌 Project Overview
This research investigates the educational equity gap in the United States by analyzing the relationship between geographic school locales (Urban, Suburban, Town, Rural) and student academic achievement in mathematics.

Using data from the **Educational Opportunity Project** and **Stanford Education Data Archive (SEDA)**, this project moves beyond a simple "rural vs. non-rural" binary. Instead, it utilizes granular locale proportions and socioeconomic variables to determine how location serves as a proxy for resource availability and student success.

## 🔍 Research Question
**Does the geographic location of a school district—specifically the distinction between rural, town, and suburban locales—have a statistically significant impact on student standardized test scores when controlling for socioeconomic factors?**

## 📊 Data & Methodology

### Data Source
* **Dataset**: Stanford Education Data Archive (SEDA) Version 5.0.
* **Scope**: Grades 3-8, Years 2009–2019.
* **Sample Size**: 600,028 observations across U.S. school districts.

### Variables Analyzed
* **Dependent Variable**: `cs_mn_all` (Math Test Scores relative to the National Average).
* **Independent Variables (Locales)**:
    * *Rural*: Fringe, Distant, Remote.
    * *Town*: Fringe, Distant, Remote.
    * *Suburb*: Large, Midsize, Small.
    * *City*: Large, Midsize, Small.
* **Control Variables (Socioeconomic)**:
    * `perecd`: Percent Economically Disadvantaged.
    * `unempall`: Unemployment Rate.
    * `povertyall`: Poverty Rate.

### Analytical Approach (Stata)
The analysis was performed using **Stata**. Key analytical steps included:
1.  **Data Wrangling**: Filtering for Math subjects and merging geographic identifiers.
2.  **Descriptive Statistics**: Summary statistics (`sum`, `codebook`) to understand distributions.
3.  **Correlation Analysis**: Generating heatmaps (`heatplot`) to visualize relationships between locale types and scores.
4.  **OLS Regression Modeling**:
    * Simple Linear Regression (Rural vs. Math Scores).
    * Multiple Regression (Controlling for specific locale subtypes and socioeconomic factors).
5.  **Interquartile Range (IQR) Analysis**: Creating dummy variables to compare the bottom 25% vs. top 25% of districts within specific locales. This allowed us to identify "ceilings" on achievement in specific areas.

## 📉 Key Findings

1.  **The "Rural Penalty"**: There is a statistically significant negative correlation between rural locale proportions and test scores (-0.0734). As the proportion of rural students increases, predicted test scores decrease relative to the national average.
2.  **Suburban Advantage**: Unlike rural and town locales, large suburban areas showed a positive correlation with test scores, suggesting these environments better support high achievement.
3.  **Socioeconomic Impact**: Unemployment (`unempall`) was the most significant negative predictor of test scores (Coefficient: -1.41), outweighing pure geographic factors.
4.  **High-Achiever Disparity**: In "Rural Remote" areas, even the upper 25% of districts (the best performing) often scored *below* the national average (-0.07), whereas the upper 25% of "Suburb Large" districts scored significantly *above* it (+0.18).

## ⚠️ Limitations & Future Research

### Limitations
* **Subject Scope**: The analysis focused exclusively on Math scores; Reading/ELA scores were not included.
* **Missing Variables**: The model did not control for specific school funding levels, teacher tenure/expertise, or parental involvement, which are known drivers of achievement.
* **Correlation vs. Causation**: The findings are correlational. While we established a strong link between locale and scores, we cannot claim that living in a rural area *causes* lower scores without further causal inference methods.

### Future Research
* **Resource Analysis**: Investigate specific resource gaps (e.g., broadband access, AP course offerings) in Rural Remote areas.
* **Longitudinal Study**: Analyze how these trends have shifted post-2019, specifically examining the impact of the COVID-19 pandemic on the rural-urban gap.

## 📂 Repository Structure

```text
├── Data/
│   ├── seda_geodist_long_cs.dta    # (Note: Large file, may not be included in repo)
├── Scripts/
│   ├── FinalProjectDO.do           # Stata script containing all cleaning and regression logic
├── Docs/
│   ├── Research_Paper.pdf          # Full academic paper
│   ├── Research_Poster.pdf         # Visual summary poster
│   ├── Presentation_Slides.pdf     # Project presentation deck
└── README.md
