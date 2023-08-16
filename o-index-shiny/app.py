from shiny import *
import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
from re import *
import os
from o_functions import *

app_ui = ui.page_fluid(
    ui.h2("Quantifying Open Access"),
    ui.markdown('''
### What is an o-index?
An o-index, or openness-index, is a metric to quantify the "openness" of a particular author's body of work. This app accepts an author's name and looks up the PMIDs associated with a PubMed search. It then scrapes any open access texts for keywords associated with data and/or code sharing. 

### Get o-index:'''),
    ui.input_text("author", "Author: ", "Jennifer Jahncke"),
    ui.input_action_button("go","Calculate o-index"),
    ui.output_text_verbatim("o_index_float"),
    ui.output_table("o_index_df"),
    ui.markdown('''
### App Source Code
Source code is available [on our github](https://github.com/jnjahncke/o-index/tree/main).
    ''')
)


def server(input, output, session):
    
    @output
    @render.table
    @reactive.event(lambda: input.go(), ignore_none=False)
    def o_index_df():
        o_df = get_openness(input.author(), "apikey.txt")
        return o_df

    @output
    @render.text
    @reactive.event(lambda: input.go(), ignore_none=False)
    def o_index_float():
        o_float = "x"
        #o_float = oindex(o_index_df())
        return f"o-index: {o_float}"


app = App(app_ui, server)
