# Data Analyst Case Study: Data Analysis and Dashboard creation

**Task:** Use the shared dummy data to perform data analysis and create dashboards for better understanding.

**Note:** Attach the final code for the dashboards created, python / notebook files with the analysis. No need for PPT. Make sure your code is working properly, and specify the python version, package versions being used for the exercise.

## Data
The shared data represents the Profit and Loss for a cloud kitchen company across different kitchen stores, cities and the corresponding values of the fixed and operating costs, along with the expenses happening at the monthly level.

We want you to explore the data for analysis purposes, and make use of open-source tools, like Plotly or Streamlit, and create dashboards for it by applying different types of filters on the below shared list of columns.

---

## The Exercise Involves 2 Parts:

### Dashboard 1 (Kitchen Level PNL)
Create kitchen level Profit & Loss information by putting filters on the shared dataset.

**The list of the columns to be used for filtering the overall data:**
`STORE`, `GM%`, `GM`, `CM %`, `CM`, `EBITDA`, `NET_REVENUE`, `Month`, `REVENUE COHORT`, `CM COHORT`, `EBITDA CATEGORY`, `EBITDA COHORT`

*(Reference mockups are provided in the document detailing sliders for EBITDA Range and dropdowns for Zone, EBITDA Category, Month, Revenue Category, Store, etc. for the KITCHEN SNAPSHOT view).*

### Dashboard 2 (VARIANCE Level PNL)
Make use of the 'VARIANCE' column to create a second dashboard by creating buckets on the basis of the value segments shared in the image below.

This dashboard is to be split into 2 parts:
* **a. Sub-dashboard 1:** Create a summary of the average variance % of the kitchens under specific revenue (`NET_REVENUE` column) categories.
* **b. Sub-dashboard 2:** Create a summary of the total number of kitchen stores on the basis of the Variance filter used at the top, and then further bifurcate the revenue (`NET_REVENUE` column) field in the shared value ranges. Populate the table with the count of kitchen stores (`STORE` column) for each of the respective months.

---

## Notes:
* The revenue category filter is cohort-based (fixed). Additionally, it should include range-based filters for EBITDA, Contribution Margin (CM), and Revenue.
* **Variance:** Wastage of food material.

## Proposed Steps:
1. Create dataset in the desired format for both the dashboards.
2. Develop Streamlit / Plotly app with the dashboards.
3. Include code segments to optimize the performance of the dashboard, in case the data is getting refreshed on real time basis.
4. Bonus points for creating fancy features in the dashboard, like the interactive variance category filters shown in the document.

---

## Final Instructions
The final analysis of the data should be represented in a Streamlit or Plotly dashboard in the shared template. 

In addition to this, if there are any other level of insights you are able to gather from the shared data then please share those as well.

**Preferred language is Python.**