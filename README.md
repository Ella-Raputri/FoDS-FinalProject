# FoDS and Statistic Final Project

<br>

**Class:** L3AC

**Members:**
- Ella Raputri (2702298154)
- Ellis Raputri (2702298116)

<br>

## Project Description
This is the final project for our Fundamental of Data Science and Basic Statistic class. With this research, we aim to analyze the local trends of programming languages in Indonesia. For Fundamental of Data Science class, we utilized the unsupervised clustering algorithms to determine the clusters of programming languages in Indonesia and the classification algorithms to predict the popularity of the programming languages based on other time series factors. Meanwhile, for Basic Statistic class, we tested our hypothesis to determine the significance of the dependency between each factors and the significance of difference in average popularity between newer and older programming languages.

<br>

## Folders
<details>
<summary>&ensp;<b>data</b></summary>

- Contains the data for our research, which are the job scraping result, name of programming languages, monthly Google Trends, monthly Wikipedia views, yearly Stack Overflow user count, monthly TIOBE Index, and the result of the merge of all the dataset.

- Also contains the normalized data (in the normalised folder) for languages that are considered 'popular' based on the clustering result. These dataset will be used for classification algorithms.
</details>

<br>

<details>
<summary>&ensp;<b>demo</b></summary>

- Contains the demo to predict the popularity (TIOBE Index or Google Trends) of the language.

- The languages that are selected into the demo are languages that has high model accuracy for their data and is considered 'popular' based on the clustering result.

</details>

<br>
<details>
<summary>&ensp;<b>documentation</b></summary>

- Contains the reports for our final project, which are the Fundamental of Data Science and Basic Statistic final reports.
</details>


<br>
<details>
<summary>&ensp;<b>EDA</b></summary>

- Contains the plot (graph/data visualization) for our exploratory data analysis part of this project.
- The stat_count.ipynb and stat2.ipynb are used to make us easy to get the number of observations that will further be used in our statistical analysis.
</details>



<br>
<details>
<summary>&ensp;<b>ML</b></summary>

- Contains the machine learning methods that we enforced in our project, which is the classification, unsupervised clustering, and time series analysis.

</details>

<br>
<details>
<summary>&ensp;<b>raw_data</b></summary>

- Contains the raw data and cleaning process for our project.
- The cleaned data is in the 'data' folder.

</details>
<br>