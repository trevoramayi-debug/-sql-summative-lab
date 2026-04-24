#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# In part 1 of this assessment, you will complete several requested SQL queries in order to extract data, analyze, and provide insights from a single provided SQL database. You will also visualize the key results of 3 of these queries. There are also several 'Reflection' questions that ask you to write out a text based answer in the provided markdown cell. Following the guided question and answer section, in part 2 you will explore a second dataset on your own using SQL in order to conduct a preliminary analysis. You will be asked to produce a very short slide presentation highlighting the work you did for this second section.
# 
# ## Objectives
# You will be able to:
# - Interpret "word problems" and translate them into SQL queries
# - Decide and perform whichever type of JOIN is best for retrieving desired data
# - Use GROUP BY statements to apply aggregate functions like COUNT, MAX, MIN, and SUM
# - Use the HAVING clause to compare different aggregates
# - Write subqueries to decompose complex queries
# - Visualize data using matplotlib, seaborn, or pandas
# - Choose the correct chart type based on the given data
# 

# ## Part 1: Guided SQL Queries
# 
# ### Your Task: Querying a Customer Database
# 
# ![toy car picture](images/toycars.jpg)
# 

# ### Business Understanding
# Your employer sells wholesale miniature models of products such as classic cars, motorcycles, and planes. They want you to pull several reports on different segments of their past customers, in order to better understand past sales as well as determine which customers will receive promotional material. They are also interested in investigating which products have performed the best, as well as having several smaller asks.
# 
# In addition to providing the requested data from the SQL database you have also been asked to create some basic visuals to display some of the more insightful information. It is up to your discretion to choose the correct plot/chart type for the data in question. **Questions that want you to visualize the results will be explicitly marked**.
# 
# ### Data Understanding
# You may remember this database from a previous lab. As a refresher, here's the ERD diagram for this database:
# 
# ![ERD picture](images/ERD.png)
# 
# The queries you are asked to write will become more complex over the course of the lab.
# 
# 

# ### Getting Started
# For this assessment you are expected to make use of both sqlite3 and the Pandas libraries in order to write, execute, and return SQL queries as a Pandas DataFrame. Assign each returned answer as its own explicit variable.
# 
# For the visualization piece you are expected to utilize either Pandas, Seaborn, or Matplotlib to create your visuals. Make sure you are providing verbose labels and titles according to the data you are being asked to visualize. Do not worry too much about choosing a 'style' or 'context' instead focus on conveying the requested information correctly.
# 
# ### Step 1: Connect to Data
# 
# In the cell below
# - Import the necessary libraries
# - Establish a connection to the database data.sqlite

# In[1]:


# Replace None with your code
# Imports
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Create connection to database
conn = sqlite3.connect('data.sqlite')


# ### Step 2: Limited Edition California Product
# The California sales rep team is interested in running promotional material for a new limited edition model they are releasing based on the famous San Francisco Cable Cars. This product will only be available to customer stores based in California and given its high price value they want to first target promotional material to existing California customers with a high credit limit. Upon communicating with the accounting department, a credit limit of over 25,000 is considered to be high. 
# 
# Execute a SQl query that returns which customers the sales rep team wants to market to first.

# In[2]:


# Replace None with your code
california_customers_df = pd.read_sql_query("""
SELECT customerNumber,
       customerName,
       city,
       state,
       country,
       creditLimit
FROM customers
WHERE country = 'USA'
  AND state = 'CA'
  AND creditLimit > 25000
ORDER BY creditLimit DESC, customerName
""", conn)

california_customers_df


# ### Step 3: International Collectable Campaign
# 
# The international sales rep team has reached out to you to help them identify partners for a 'Collectable' marketing campaign that highlights the potential collectors value in purchasing these model kits. They want to try and promote a 'collect them all' mentality. The team had a great idea to partner with any of their international customers (non-US) who have "Collect" in their name as a tie in to the larger theme.
# 
# Execute a SQL that returns the customers in question.

# In[3]:


# Replace None with your code
collectable_customers_df = pd.read_sql_query("""
SELECT customerNumber,
       customerName,
       city,
       country
FROM customers
WHERE country <> 'USA'
  AND customerName LIKE '%Collect%'
ORDER BY country, customerName
""", conn)

collectable_customers_df


# ## Reflection Question:
# 
# Describe the WHERE clause you used in the above query to a non-technical manager who wants to be ensured that you are properly filtering and only selecting the requested data. How is the operator and conditional expression you are using acting to accomplish this?
# 
# The `WHERE` clause acts like a checklist. First, `country <> 'USA'` removes all domestic customers so we are only looking at international accounts. Then `customerName LIKE '%Collect%'` keeps only companies whose name contains the word fragment `Collect`, which matches the campaign theme. Using `AND` means both conditions must be true at the same time, so the final result only includes non-US customers whose names fit the collectables promotion idea.

# ### Step 4: USA Credit and Inventory Policy - Visual Required
# The USA based product team is planning to adjust its credit policies and inventory allocation strategy based on the average credit limit of its customers. They would like to target this strategy at a state level with several goals in mind. 
# 1. Optimize inventory distribution:
#     - States with higher average credit limits might be able to place larger orders, justifying priority in inventory allocation.
#     - This could help ensure that states with more purchasing power always have products in stock.
# 2. Tailor credit policies:
#     - Adjust credit limits for new customers based on the state average.
#     - Identify states where they might be too conservative or too liberal with credit limits.
# 3. Target marketing and sales efforts:
#     - Focus promotional campaigns on states with higher credit limits, potentially leading to larger orders.
#     - Develop strategies to increase sales in states with lower average credit limits.
# 
# Execute a SQl query that returns the information required to address this ask.

# In[4]:


# Replace None with your code
usa_credit_by_state_df = pd.read_sql_query("""
SELECT state,
       ROUND(AVG(creditLimit), 2) AS avg_credit_limit,
       COUNT(*) AS customer_count
FROM customers
WHERE country = 'USA'
  AND state IS NOT NULL
GROUP BY state
ORDER BY avg_credit_limit DESC
""", conn)

usa_credit_by_state_df


# Once you have the information returned in a dataframe, select an appropriate visualization to represent this data. You are welcome to utilize matplotlib, seaborn, or pandas plotting to produce your visual. Ensure that it has a verbose title and axis labels!

# In[5]:


# Replace None with your visual code
# Produce a visual to represent the average credit limit by state
credit_plot_df = usa_credit_by_state_df.sort_values('avg_credit_limit')

plt.figure(figsize=(10, 6))
plt.barh(credit_plot_df['state'], credit_plot_df['avg_credit_limit'], color='steelblue')
plt.title('Average Customer Credit Limit by US State')
plt.xlabel('Average Credit Limit (USD)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ### Step 5: Top Customers - Visual Required
# The company is approaching its 10 year anniversary and wants to acknowledge and thank its top customers with personalized communication. They have asked you to determine the top 10 customers based on the total amount of payments made, making sure to return the customer name for clarity. 
# 
# Execute a SQl query that returns the information required to address this ask.
# 

# In[6]:


# Replace None with your code
top_customers_df = pd.read_sql_query("""
SELECT c.customerName,
       ROUND(SUM(p.amount), 2) AS total_payments
FROM customers c
JOIN payments p
  ON c.customerNumber = p.customerNumber
GROUP BY c.customerNumber, c.customerName
ORDER BY total_payments DESC
LIMIT 10
""", conn)

top_customers_df


# Once you have the information returned in a dataframe, select an appropriate visualization to represent this data. You are welcome to utilize matplotlib, seaborn, or pandas plotting to produce your visual. Ensure that it has a verbose title and axis labels!

# In[7]:


# Replace None with your visual code
# Produce a visual to represent the top ten customers in terms of total payments
top_customers_plot_df = top_customers_df.sort_values('total_payments')

plt.figure(figsize=(11, 7))
plt.barh(top_customers_plot_df['customerName'], top_customers_plot_df['total_payments'], color='darkorange')
plt.title('Top 10 Customers by Total Payments Made')
plt.xlabel('Total Payments (USD)')
plt.ylabel('Customer Name')
plt.tight_layout()
plt.show()


# ### Step 6: Top Customer + Product Quantities
# The product team is running an analysis on popular and common products sold to each customer in order to try and determine what new products they should be looking at to include in their catalog. This data will also be used by individual sales reps to recommend similar products to each customer next time they place an order. 
# 
# They have asked you to query information, for each customer, about any product they have purchased 10 or more units of. In addition they would like the full set of data to be sorted in ascending order by the total amount purchased.
# 
# Execute a SQl query that returns the information required to address this ask.
# 
# Hint: For this one, you'll need to make use of HAVING, GROUP BY, and ORDER BY — make sure you get the order of them correct!

# In[8]:


# Replace None with you code
customer_product_quantity_df = pd.read_sql_query("""
SELECT c.customerName,
       p.productName,
       SUM(od.quantityOrdered) AS total_quantity_purchased
FROM customers c
JOIN orders o
  ON c.customerNumber = o.customerNumber
JOIN orderdetails od
  ON o.orderNumber = od.orderNumber
JOIN products p
  ON od.productCode = p.productCode
GROUP BY c.customerNumber, c.customerName, p.productCode, p.productName
HAVING SUM(od.quantityOrdered) >= 10
ORDER BY total_quantity_purchased ASC, c.customerName, p.productName
""", conn)

customer_product_quantity_df


# ### Step 7: Product Analysis - Visual Required
# 
# The product team is looking into the demand across its different product lines. They are conducting a comprehensive review of its product portfolio and inventory management strategies. You have been asked to query data pertaining to each different product line, that contains the total quantity ordered and the total number of products for each respective product line. By examining the number of products and total quantity ordered for each product line, the company aims to:
# 1. Optimize product mix:
#     - Identify which product lines have the most diverse offerings (high number of products)
#     - Determine which lines are most popular (high total quantity ordered)
#     - Compare if lines with more products necessarily lead to more orders
# 2. Improve inventory management:
#     - Adjust stock levels based on the popularity of each product line
#     - Identify potential overstocking in lines with low order quantities
#     - Ensure adequate variety in high-performing product lines
# 3. Adjust marketing strategy:
#     - Focus promotional efforts on product lines with high potential (many products but lower order quantities)
#     - Capitalize on the popularity of high-performing lines in marketing campaigns
# 4. Advise Product development:
#     - Invest in expanding product ranges for lines with high order quantities
#     - Consider phasing out or revamping product lines with low numbers of products and low order quantities
# 
# Hint: Think about how you can and might have to utilize SQL DISTINCT statement
# 
# Execute a SQl query that returns the information required to address this ask.

# In[9]:


# Replace None with your code
product_line_analysis_df = pd.read_sql_query("""
SELECT p.productLine,
       SUM(od.quantityOrdered) AS total_quantity_ordered,
       COUNT(DISTINCT p.productCode) AS number_of_products
FROM products p
LEFT JOIN orderdetails od
  ON p.productCode = od.productCode
GROUP BY p.productLine
ORDER BY total_quantity_ordered DESC
""", conn)

product_line_analysis_df


# Once you have the information returned in a dataframe, select an appropriate visualization to represent the relationship between total quantity ordered and the number of products in order to perform a preliminary investigation into the question of if more products lead to more orders. You are welcome to utilize matplotlib, seaborn, or pandas plotting to produce your visual. Ensure that it has a verbose title and axis labels!

# In[10]:


# Replace None with your visual code
# Produce a visual to represent the the relation between number of products and the total amount ordered
plt.figure(figsize=(9, 6))
plt.scatter(product_line_analysis_df['number_of_products'], product_line_analysis_df['total_quantity_ordered'], s=140, color='seagreen')

for _, row in product_line_analysis_df.iterrows():
    plt.annotate(row['productLine'], (row['number_of_products'], row['total_quantity_ordered']), xytext=(5, 5), textcoords='offset points')

plt.title('Relationship Between Product Variety and Quantity Ordered by Product Line')
plt.xlabel('Number of Products in Product Line')
plt.ylabel('Total Quantity Ordered')
plt.tight_layout()
plt.show()


# ## Reflection Question:
# 
# Please explain your choice in the type of visual you used in order to highlight and represent the data from the above query. In a non-technical manner explain why that chart type makes sense for the information being conveyed. What does this visual convey in the context of the question it was asked for?
# 
# I used a scatter plot because the business question is about the relationship between two numeric measures: how many products a line offers and how many total units were ordered. A scatter plot makes it easy to see whether product lines with more variety also tend to receive more demand, and it also makes outliers easy to spot. In this case, the visual helps show that having more products often lines up with stronger ordering volume, while also revealing that some lines perform better or worse than that general pattern.

# ### Step 8: Remote Offices
# Upper management is considering a shift to hybrid and remote work for certain locations and roles. They have tasked you with providing them data about employees who work in any office that has fewer than 5 total employees so they can better understand how to support those employees remotely when offices are shut down. 
# 
# Be sure to include information about the employees job and supervisor so management can adjust everyone to remote work properly.
# 
# Hint: Utilize a subquery to find the relevant offices
# 
# Execute a SQl query that returns the information required to address this ask.

# In[11]:


# Replace None with your code
remote_office_employees_df = pd.read_sql_query("""
SELECT e.employeeNumber,
       e.firstName,
       e.lastName,
       e.jobTitle,
       o.city AS officeCity,
       o.country AS officeCountry,
       m.firstName || ' ' || m.lastName AS supervisor
FROM employees e
JOIN offices o
  ON e.officeCode = o.officeCode
LEFT JOIN employees m
  ON e.reportsTo = m.employeeNumber
WHERE e.officeCode IN (
    SELECT officeCode
    FROM employees
    GROUP BY officeCode
    HAVING COUNT(*) < 5
)
ORDER BY o.country, o.city, e.lastName, e.firstName
""", conn)

remote_office_employees_df


# ## Reflection Question:
# 
# Describe how you decided on the subquery that you used in the query above? This answer can be technically in nature, describing your thought process in how the main query is utilizing the subquery to return the correct data.
# 
# I started by noticing that the rule for inclusion depends on the office as a group, not on any one employee row by itself. Because of that, the first step was to build a subquery that groups employees by `officeCode` and counts how many employees work in each office. The `HAVING COUNT(*) < 5` filter isolates only the office codes that meet management's remote-support condition. The main query then uses those office codes in the `WHERE e.officeCode IN (...)` clause, which lets me return the detailed employee-level columns such as name, job title, office location, and supervisor only for the offices identified by the subquery.

# ### Step 9: Close the Connection
# 
# Now that you are finished executing your queries and retrieving the required information you always want to make sure to close the connection to your database.

# In[12]:


# Replace None with your code
conn.close()


# ### End of Guided Section
# In this initial portion of the assessment, you produced several data queries and visualizations for a model company, mainly focused around its customer and product data. You wrote and engineered specific SQL queries to address pertinent questions and asks from the company. Along the way, you utilized many of the major concepts and keywords associated with SQL SELECT queries: FROM, WHERE, GROUP BY, HAVING, ORDER BY, JOIN, SUM, COUNT, and AVG.
# 
# ## Part 2: Exploratory Analysis with SQL
# In this open-ended exploratory section, you will analyze real-world data from the movie industry. As a data analyst, you have the freedom to investigate questions and topics that intrigue you within this dataset. The database schema and Entity-Relationship Diagram (ERD) are provided below for your reference. A general overview and instructions are also provided below.

# In[13]:


# Run this cell without changes
import zipfile

zip_file_path = 'im.db.zip'
extract_to_path = './'

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_path)

# Connection
conn4 = sqlite3.connect('im.db')

# Schema
schema_df = pd.read_sql("""
SElECT * FROM sqlite_master                        
""", conn4)
schema_df


# ## The Data
# 
# ![movie ERD](images/movie_data_erd.jpeg)
# ### Database Content:
# 
# - Source: IMDB
# - Time Range: Movies released between 2010 and 2019
# - Note: Exclude any movies with a start_year after 2019 as this data is not current or accurate
# 
# Available Data Categories:
# - Genre
# - Runtime
# - Personnel (writers, directors, actors)
# - Movie ratings
# 
# ### Objectives:
# 
# Initial Exploration:
# - Use SQL in combination with Pandas to explore the database
# - Identify interesting trends, patterns, or relationships in the data
# 
# Business Question Formulation:
# - Develop at least one substantial business question for deeper analysis
# - Ensure the question is relevant, specific, and can be addressed with the available data
# 
# Data Cleaning Assessment:
# - Identify potential data cleaning tasks necessary for your deeper analysis
# - Note: You are not required to perform the cleaning, only to recognize and list the necessary tasks
# 
# Null Value Handling:
# - Be aware that the dataset contains null values in certain fields
# - Exclude these null values from your exploration
# - Do not attempt to input or fill in missing information
# 
# ### Deliverables:
# 
# You need to produce a short slide presentation (3-5 slides) that highlights the three key deliverables below. Utilize a data visualization to support the second deliverable.
# 
# 1. A summary of your initial data exploration findings
#     - Can be bulleted or sentence form
# 2. At least one well-formulated business question for further analysis
#     - Should stem from a relevant trend or pattern your initial exploration identified
# 3. A list of potential data cleaning tasks identified during your exploration
#     - This can and should include things like data normalization/standardization and null handling
# 
# Tips for Success:
# 
# Begin with broad exploratory queries to understand the data's scope and content. Then focus on honing in on interesting relationships between different data categories. Consider industry trends, audience preferences, or financial aspects when formulating your business question. Pay attention to data quality issues, inconsistencies, or limitations that might affect your analysis. Remember, the goal is to demonstrate your analytical thinking and ability to derive meaningful insights from complex datasets. Good luck with your exploration!
# 
# NOTE: You do not need to explore every aspect of this database. Find something that you think is interesting or relevant about the data and focus your exploration there.

# In[14]:


# Begin your code here
from IPython.display import Markdown, display

movie_overview_df = pd.read_sql_query("""
SELECT COUNT(*) AS movie_count,
       ROUND(AVG(runtime_minutes), 2) AS avg_runtime_minutes
FROM movie_basics
WHERE start_year BETWEEN 2010 AND 2019
  AND runtime_minutes IS NOT NULL
""", conn4)

ratings_overview_df = pd.read_sql_query("""
SELECT COUNT(*) AS rated_movie_count,
       ROUND(AVG(averagerating), 2) AS avg_rating,
       ROUND(AVG(numvotes), 2) AS avg_votes
FROM movie_ratings
WHERE averagerating IS NOT NULL
  AND numvotes IS NOT NULL
""", conn4)

movie_genre_df = pd.read_sql_query("""
SELECT b.movie_id,
       b.primary_title,
       b.start_year,
       b.runtime_minutes,
       b.genres,
       r.averagerating,
       r.numvotes
FROM movie_basics b
JOIN movie_ratings r
  ON b.movie_id = r.movie_id
WHERE b.start_year BETWEEN 2010 AND 2019
  AND b.genres IS NOT NULL
  AND b.runtime_minutes IS NOT NULL
  AND r.averagerating IS NOT NULL
  AND r.numvotes IS NOT NULL
""", conn4)

genre_summary_df = (
    movie_genre_df.assign(genre=movie_genre_df['genres'].str.split(','))
    .explode('genre')
    .groupby('genre', as_index=False)
    .agg(
        movie_count=('movie_id', 'nunique'),
        avg_rating=('averagerating', 'mean'),
        avg_votes=('numvotes', 'mean'),
        avg_runtime=('runtime_minutes', 'mean')
    )
)

top_genres_df = genre_summary_df[genre_summary_df['movie_count'] >= 1000].sort_values(['avg_rating', 'movie_count'], ascending=[False, False])

display(movie_overview_df)
display(ratings_overview_df)
display(top_genres_df.head(10).round(2))

display(Markdown(f"""
### Initial Exploration Summary
- The cleaned exploration set covers **{int(movie_overview_df.loc[0, 'movie_count']):,}** movies released from 2010 to 2019 with non-null runtime information.
- Across rated titles, the average IMDb rating is **{ratings_overview_df.loc[0, 'avg_rating']:.2f}** and the average vote count is **{ratings_overview_df.loc[0, 'avg_votes']:.0f}**.
- When genres are split into individual labels, **Documentary** stands out as the highest-rated genre among genres with at least 1,000 films, followed by Biography and Music.

### Business Question
Do higher-rated genres also generate stronger audience engagement, measured by vote counts, or are there genres that earn strong ratings from smaller niche audiences?

### Potential Data Cleaning Tasks
- Split the comma-separated `genres` field into a normalized genre bridge table so each genre can be analyzed consistently.
- Remove or exclude rows with null values in `runtime_minutes`, `genres`, `averagerating`, or `numvotes` depending on the analysis.
- Restrict all exploratory work to titles released from **2010 through 2019** so the analysis matches the project scope.
- Check for duplicate movie records after joining tables and confirm each `movie_id` is counted once in aggregated analysis.
- Standardize any text-based categorical fields before deeper analysis across regions, genres, or personnel roles.
"""))

plot_df = top_genres_df.head(10).sort_values('avg_rating')
plt.figure(figsize=(10, 6))
plt.barh(plot_df['genre'], plot_df['avg_rating'], color='slateblue')
plt.title('Top Genres by Average IMDb Rating (Minimum 1,000 Films, 2010-2019)')
plt.xlabel('Average IMDb Rating')
plt.ylabel('Genre')
plt.tight_layout()
plt.show()

