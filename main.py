#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
This is the main part of the project.
It is involved in the development of the running program.

__author__: Cristobal Moreno (@cmdl987)
__modified__: 07/08/2022
"""

from src.web_scrapping import IBEXCompanyScrapper
from src.chart_maker import ChartDrawer

if __name__ == "__main__":
    user_company = IBEXCompanyScrapper()
    user_company.select_company()
    company_data = user_company.get_company_historic_data()
    company_name = user_company.get_company_name()
    stock_market_chart = ChartDrawer(company_data, company_name)
    stock_market_chart.draw_chart()
