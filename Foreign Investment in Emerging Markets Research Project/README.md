# Structural Transformation and Socio-Economic Advancement

## A Multi-Dimensional Analysis of Foreign Investment in Emerging Markets

**Author:** Ashton Jaubert
**Institution:** Texas State University 
**Course:** Emerging Markets Economics ECO 3320.251 (Spring 2026) 
**Contact:** ashtonkjaubert@gmail.com | sat196@txstate.edu

---

## Project Overview
This repository contains the research and econometric modeling for an empirical examination into the structural transformation of emerging markets. The central objective is to model the interactive relationships between foreign direct investment (FDI), gross domestic savings, demographic transitions, and regional inequality.

While facilitating the structural transition from agrarian subsistence to high-productivity industrial environments is a global economic priority, this growth is historically non-uniform. This project evaluates why urbanized enclaves modernize rapidly while rural agrarian geographies remain locked in generational stagnation, a phenomenon deeply tied to the "Poverty Trap".

## Data & Scope
* **Scope:** 20 major emerging market economies.
* **Timeframe:** 2010 - 2024.
* **Primary Data Source:** World Bank's World Development Indicators (WDI) panel data.

## Methodology & Econometric Models
The empirical analysis is conducted using Python to process panel datasets and estimate several econometric models:
1. **Baseline Ordinary Least Squares (OLS):** An initial regression to isolate correlates of national inequality (Gini Index) .
2. **Two-Stage Least Squares (2SLS) Instrumental Variable Approach:** Corrects for simultaneity bias caused by elite wealth concentration. The **Age Dependency Ratio** is utilized as an exogenous instrument to isolate the true causal impact of capital accumulation on inequality, satisfying the exclusion restriction under the Life-Cycle Hypothesis .
3. **Dynamic System Generalized Method of Moments (GMM):** Implemented to capture the highly path-dependent nature of inequality and savings, controlling for unobserved individual fixed effects.

## Key Findings
* **The Power of Domestic Savings:** The empirical findings reject the presence of a 'Spatial Paradox of Thrift' . Standard OLS models severely underestimate the inequality-reducing power of domestic savings. The 2SLS IV model mathematically proves that true, democratized capital accumulation actively reduces national inequality.
* **Demographic Frictions (Pre-Turning Point):** In heavily agrarian nations, as structural transformation takes hold, the wage gap between modern industrial workers and subsistence farmers widens. This validates the upward-sloping phase of the classic Kuznets Curve .
* **The FDI Spatial Paradox & Spatial Masking:** Multinational corporations concentrate high-tier FDI inside highly localized, urbanized export enclaves, leaving the rural periphery largely untouched . These profound local transformations are "spatially masked" and diluted within aggregate national macroeconomic statistics.

##  Policy Recommendations
Based on the empirical evidence, attracting aggregate FDI is insufficient for holistic economic development. Host governments must adopt active, state-led frameworks:
* **Mandate Backward Linkages:** Model policies on Costa Rica's PROCOMER by implementing tiered corporate tax incentives for MNCs that source from rural-adjacent SMEs.
* **Implement Green FDI Thresholds:** Incorporate strict environmental compliance standards into Special Economic Zone (SEZ) charters to safeguard agricultural resources .
* **Scale Psychometric Credit Scoring:** Adopt models like Ethiopia's WEDP to bypass traditional collateral requirements and democratize credit for rural SMEs.
* **Enhance Domestic Saving Incentives:** Democratize access to the financial system via zero-fee postal banking and mobile money platforms to capture unbanked rural capital [cite: 1].

## 📖 Theoretical Frameworks Referenced
* **Harrod-Domar & Solow-Swan Neo-Classical Growth Models** [cite: 1]
* **Lewis Dual-Sector Model & Harris-Todaro Model of Migration** [cite: 1]
* **Michael Kremer's O-Ring Theory of Economic Development** [cite: 1]
* **Amartya Sen's Capability Approach** [cite: 1]
