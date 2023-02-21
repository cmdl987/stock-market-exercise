#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_scrapping.py
This module contains the class IBEXCompanyScrapper whose methods are involved in the data collection for
every stock included on the IBEX35 stockmarket (SPAIN).

It is involved in the development of the running program.
__author__: Cristobal Moreno (@cmdl987)
__modified__: 07/08/2022
"""

import pprint
import os

import requests
import pandas as pd
from pathlib import Path


class IBEXCompanyScrapper:
    def __init__(self):
        self._make_folders()
        self.file_path = "data/companies.txt"
        self.all_companies_url = "https://www.infobolsa.es/acciones/ibex35"
        self.company_url = "https://www.infobolsa.es/cotizacion/historico-{company}"
        self.my_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        self.stock_market_list = self._check_file()
        self.all_companies_dict = {}
        self.selected_company = ""

    def _make_folders(self):
        """
        Create the folders '/data' and '/output' where the files are saved.
        """
        try:
            os.makedirs("data")
            os.makedirs("output")
        except FileExistsError:
            pass

    def _get_stocks_list(self):
        """
        Makes a request to get all the IBEX35 stock-market companies and save it on a .txt file

        Returns:
            str : Text with all the companies included on the IBEX35 stock-market.
        """
        my_request = requests.get(self.all_companies_url, headers=self.my_headers)
        # Parse the table inside the request response as a dataframe
        table_list = pd.read_html(my_request.text)
        df = table_list[0]

        # Get the attribute in which the company names are allocated inside the dataframe.
        companies_list = df["Nombre"].to_list()

        # Save all the names into a .txt file
        with open(self.file_path, "w") as file:
            file_content = file.write(str(companies_list))

        return companies_list

    def _check_file(self):
        """
        It checks if the file with the list of companies of the IBEX35 stock market exists.
        In case not, it calls to the self._get_companies_file function to create it.

        Returns:
            list : with the IBEX35 stock market companies.
        """
        # Set the path where the .txt file with all the companies should be allocated.
        path = Path(self.file_path)
        # Checks if the file exist on that path. In case not, create it.
        if not path.is_file():
            print("File doesn't exist. Searching for content")
            content = str(self._get_stocks_list())
        else:
            with open(self.file_path, "r") as file:
                content = file.read()

        # Clean the content of the .txt file
        for character in ["[", "]", "'"]:
            content = content.replace(character, "")

        return content

    def select_company(self):
        """
        It gets a list of companies and ask the user to select one of them.
        After choosing the company, it creates the personalized URL to get access to the market history.
        """
        companies_list = self.stock_market_list.split(",")
        self.all_companies_dict = {key: value for key, value in enumerate(companies_list, start=1)}
        print("--" * 50)
        print("COMPANIES OF THE IBEX35 STOCK MARKET")
        print("--" * 50)
        pprint.pprint(self.all_companies_dict, indent=4)
        while True:
            try:
                user_selection = int(input("Insert the number of the company: "))
                if user_selection < 36:
                    self.selected_company = self.all_companies_dict[user_selection]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Wrong selection, please enter it again a number between 1 and 35.")
        print(self.selected_company, "has been chosen.")
        self.company_url = self.company_url.format(company=self.selected_company.lower().strip()).replace(" ", "_")

    def get_company_URL(self):
        """
        Get the URL where the data content is allocated.

        Returns:
            str : URL with the company selected by the user.
        """
        return self.selected_company

    def get_company_historic_data(self):
        """
        Get a html parsed data content from the requested url.
        Extract the info from the table published on the URL WITH pandas.

        Returns:
           pandas.Dataframe : dataframe with the company historic data.
        """
        my_request = requests.get(self.company_url, headers=self.my_headers)
        df = pd.read_html(my_request.text)
        table_columns = (df[0].columns.values.tolist())
        daily_results = df[1]
        daily_results.columns = table_columns
        daily_results["Fecha"] = pd.to_datetime(daily_results["Fecha"], dayfirst=True).dt.tz_localize(None)
        daily_results.sort_values(by="Fecha", ignore_index=True, inplace=True)
        return daily_results

    def get_company_name(self):
        """
        Get the company name selected by the user.

        Returns:
            str : Name of the company selected by the user.
        """
        return self.selected_company
