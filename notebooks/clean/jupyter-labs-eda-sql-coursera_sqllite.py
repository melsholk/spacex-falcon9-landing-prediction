
# <p style="text-align:center">
#     <a href="https://skills.network" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 
# <h1 align=center><font size = 5>Assignment: SQL Notebook for Peer Assignment</font></h1>
# 
# Estimated time needed: **60** minutes.
# 
# ## Introduction
# Using this Python notebook you will:
# 
# 1.  Understand the Spacex DataSet
# 2.  Load the dataset  into the corresponding table in a Db2 database
# 3.  Execute SQL queries to answer assignment questions


# ## Overview of the DataSet
# 
# SpaceX has gained worldwide attention for a series of historic milestones. 
# 
# It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.
# SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. 
# 
# 
# Therefore if we can determine if the first stage will land, we can determine the cost of a launch. 
# 
# This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.
# 
# This dataset includes a record for each payload carried during a SpaceX mission into outer space.


# ### Download the datasets
# 
# This assignment requires you to load the spacex dataset.
# 
# In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet. Click on the link below to download and save the dataset (.CSV file):
# 
#  <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv" target="_blank">Spacex DataSet</a>


!pip install sqlalchemy==1.3.9


# ### Connect to the database
# 
# Let us first load the SQL extension and establish a connection with the database


!pip install ipython-sql
!pip install ipython-sql prettytable


%load_ext sql


import csv, sqlite3
import prettytable
prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect("my_data1.db")
cur = con.cursor()


!pip install -q pandas


%sql sqlite:///my_data1.db


import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")


# **Note:This below code is added to remove blank rows from table**


#DROP THE TABLE IF EXISTS

%sql DROP TABLE IF EXISTS SPACEXTABLE;


%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null


# ## Tasks
# 
# Now write and execute SQL queries to solve the assignment tasks.
# 
# **Note: If the column names are in mixed case enclose it in double quotes
#    For Example "Landing_Outcome"**
# 
# ### Task 1
# 
# 
# 
# 
# ##### Display the names of the unique launch sites  in the space mission


# ### Task 2
# 
# 
# #####  Display 5 records where launch sites begin with the string 'CCA'


# ### Task 3
# 
# 
# 
# 
# ##### Display the total payload mass carried by boosters launched by NASA (CRS)


# ### Task 4
# 
# 
# 
# 
# ##### Display average payload mass carried by booster version F9 v1.1


# ### Task 5
# 
# ##### List the date when the first succesful landing outcome in ground pad was acheived.
# 
# 
# _Hint:Use min function_


# ### Task 6
# 
# ##### List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000


# ### Task 7
# 
# 
# 
# 
# ##### List the total number of successful and failure mission outcomes


# ### Task 8
# 
# 
# 
# ##### List all the booster_versions that have carried the maximum payload mass, using a subquery with a suitable aggregate function.


# ### Task 9
# 
# 
# ##### List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
# 
# **Note: SQLLite does not support monthnames. So you need to use  substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.**


# ### Task 10
# 
# 
# 
# 
# ##### Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.


# ### Reference Links
# 
# * <a href ="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20String%20Patterns%20-%20Sorting%20-%20Grouping/instructional-labs.md.html?origin=www.coursera.org">Hands-on Lab : String Patterns, Sorting and Grouping</a>  
# 
# *  <a  href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Built-in%20functions%20/Hands-on_Lab__Built-in_Functions.md.html?origin=www.coursera.org">Hands-on Lab: Built-in functions</a>
# 
# *  <a  href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Sub-queries%20and%20Nested%20SELECTs%20/instructional-labs.md.html?origin=www.coursera.org">Hands-on Lab : Sub-queries and Nested SELECT Statements</a>
# 
# *   <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-3-SQLmagic.ipynb">Hands-on Tutorial: Accessing Databases with SQL magic</a>
# 
# *  <a href= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Module%205/DB0201EN-Week3-1-4-Analyzing.ipynb">Hands-on Lab: Analyzing a real World Data Set</a>


# ## Author(s)
# 
# <h4> Lakshmi Holla </h4>


# ## Other Contributors
# 
# <h4> Rav Ahuja </h4>


# <!--
# ## Change log
# | Date | Version | Changed by | Change Description |
# |------|--------|--------|---------|
# | 2024-07-10 | 1.1 |Anita Verma | Changed Version|
# | 2021-07-09 | 0.2 |Lakshmi Holla | Changes made in magic sql|
# | 2021-05-20 | 0.1 |Lakshmi Holla | Created Initial Version |
# -->


# ## <h3 align="center"> © IBM Corporation 2021. All rights reserved. <h3/>
