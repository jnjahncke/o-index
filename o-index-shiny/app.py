#!/usr/bin/env python

from shiny import *
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from re import *
from o_functions import *
import seaborn as sns

app_ui = ui.page_fluid(
    ui.h2("Quantifying Open Access"),

    ui.div(ui.column(8, ui.markdown('''
### What is an o-index?
An o-index, or openness index, is a metric to quantify the "openness" of a particular author's body of work. This app accepts an author's name and looks up the PMIDs associated with a PubMed search. It then scrapes any open access texts for keywords associated with data and/or code sharing. An "o-score" is assigned to each individual paper and the average of all o-scores is an author's o-index. 
'''))),

    ui.row(
        ui.column(2, 
            ui.row(
                ui.markdown("### Get o-index"),
                ui.input_text("author", "Author: ", "Jennifer Jahncke"),
                ui.input_action_button("go", "Calculate o-index")),

            ui.row(ui.p(".")),
            ui.row(ui.output_text("o_index_float")),
            ui.row(ui.p("."))),
        ui.column(6, ui.output_plot("plot_years"))
        ),


    ui.div(
        ui.column(8, ui.output_table("o_index_df"))),

    ui.div(ui.markdown('''
### App Source Code
Source code is available [on our github](https://github.com/jnjahncke/o-index/tree/main).
    '''))
)


def server(input, output, session):
   
    @reactive.Calc
    @reactive.event(lambda: input.go(), ignore_none=False)
    def get_df():
        o_df = get_openness(input.author(), "apikey.txt")
        return o_df
    

    @output
    @render.table
    def o_index_df():
        return get_df()

    @output
    @render.plot
    def plot_years():
        ax = sns.pointplot(data = get_df().sort_values(by ='year'), 
                x= 'year', y= 'o-score', color='hotpink', errwidth=0.5)
        ax.set(xlabel='', ylabel='O-Score', title='Yearly O-Score')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        return ax

    @output
    @render.text
    def o_index_float():
        #o_float = "x"
        o_float = oindex(get_df())
        return f"o-index: {o_float:.3f}"


app = App(app_ui, server)
