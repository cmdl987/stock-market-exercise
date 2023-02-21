# Stock-market exercise
![ibex35](https://user-images.githubusercontent.com/59370680/220184258-dca440e3-3f13-4c28-a351-39065d111518.jpeg)


---------------------------

**Objectives**

Drawing a chart (box plot) within the opening/close values of one selected company for the last month.

---------------

**Steps**

***1) Data extraction.***

First time executed, it creates a .txt file with all the companies within the IBEX35 stock-market via 
simple webscraping with requests module.
Show all the listed companies on to the terminal and ask the user to pick the company to draw. It needs to input an integer between
1 and 35. After choosing the company, a second URL requests is made in order to get all the data information.
Afterwards, the data obtained is parsed into a table with Pandas method 'read_html()'.

***2) Data visualization.***

In order to represent the chart, we need to draw a box and their whisker plots.
Matplotlib.pyplot has the ['bxp' method](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bxp.html). It makes a box and whisker plot for each day values.
![boxplot](https://user-images.githubusercontent.com/59370680/220443592-1144c162-a53b-4bb3-8575-0ee99fc3d9f4.png)

Instead of using the 3rd and 1st quartile, we will use the stock opening and close value for each day.
It requires a list of dicts with the following keys-values: 

- "q1" : lower part of the box: opening/close
- "q3" : upper part of the box: opening/close
- "label" : date
- "whislo" : lower whisker position, being the minimum price of the day
- "whishi" : higher whisker position, being the maximum price of the day
- "med" : median (not necessary)
- "fliers" : data beyond the whiskers (not applicable)

The color of the box plot will change as the closing value is greater than the open one (green color). 
Otherwise, the box plot color will be red.

***3) Data saving.***
Not only the chart is showed but an image is saved into the /output folder.
There it is an example.

![2023-02-21  REPSOL](https://user-images.githubusercontent.com/59370680/220445716-2b7ca625-7caa-4397-8cec-5bb6e0aa0032.png)
