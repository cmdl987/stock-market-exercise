#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chart_maker.py
This module contains the class ChartDrawer whose methods clean and prepare the data collected in order to draw the chart
that will be shown as a box plot. It also saves a .png image on the 'output/' folder.

It is involved in the development of the running program.
__author__: Cristobal Moreno (@cmdl987)
__modified__: 07/08/2022
"""

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class ChartDrawer:
    def __init__(self, company_data, company_name):
        self.colors = []
        self.output_path = "output/"
        self.company_data = company_data
        self.company_name = company_name

    def _set_data(self):
        """
        Given a dataframe, analyze the necessary parameters to build a box plot. Also checks the
        data in order to color the boxes depending on the price.
        Box plots components are defined as the following keys of a dictionary:
        - "q1" : lower part of the box: opening/close
        - "q3" : upper part of the box: opening/close
        - "label" : date
        - "whislo" : lower whisker position, being the lower price of the day
        - "whishi" : higher whisker position, being the higher price of the day
        - "med" : median (not applicable)
        - "fliers" : data beyond the whiskers (not applicable)
        Returns:
            list : list of dictionaries containing every key-values for every date, needed to draw the box plot.
        """
        # For every row of the dataframe, checks if the price of the stocks at the opening is greater than the price
        # at the close and assign a colored key that will be used to draw the graph.
        data_content = []
        for index in range(len(self.company_data)):
            # When opening price is lower than close, color will be green and the lower-line of the box will start
            # at the opening price value.
            if self.company_data["Apertura"][index] < self.company_data["Último"][index]:
                lower_box_line = self.company_data["Apertura"][index]
                upper_box_line = self.company_data["Último"][index]
                self.colors.append("green")

            # When opening price is bigger than close, color will be red and the lower-line of the box will start
            # at the close price value.
            else:
                upper_box_line = self.company_data["Apertura"][index]
                lower_box_line = self.company_data["Último"][index]
                self.colors.append("red")

            # Construct the dictionary that will be used to draw the box plot.
            dictionary = {"q1": lower_box_line,
                          "q3": upper_box_line,
                          "label": self.company_data["Fecha"][index].strftime("%d-%m-%Y"),
                          "whislo": self.company_data["Mínimo"][index],
                          "whishi": self.company_data["Máximo"][index],
                          "med": None,          # Empty but required key
                          "fliers": [],         # Empty but required key
                          }

            data_content.append(dictionary)

        return data_content

    def draw_chart(self):
        """
        Get the data dictionary from self._set_data method to draw the box plot.
        It saves an image with a timestamp to the output/ folder before showing the chart.
        """
        fig, ax = plt.subplots()
        data_for_graph = self._set_data()
        graph = ax.bxp(data_for_graph, patch_artist=True)

        # Set the color for every box
        for element, color in zip(graph["boxes"], self.colors):
            element.set_facecolor(color)

        # Set a correct format and info for the chart.
        ax.set_title(f"{self.company_name} - VALUES FOR THE LAST MONTH")
        plt.grid("--")
        plt.xticks(rotation=90)
        plt.xlabel("Date")
        plt.ylabel("Price value (EUR)")
        plt.subplots_adjust(bottom=0.3)

        # Set the filename to save every chart.
        file_name = str(datetime.now().date()) + " " + self.company_name
        plt.savefig(self.output_path + f"{file_name}.png")
        plt.show()
