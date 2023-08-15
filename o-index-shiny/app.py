from shiny import *
import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
from re import *
import os
from o_functions import *

app_ui = ui.page_fluid(
    ui.h2("o-index"),
    ui.input_text("author", "Author: ", "Jennifer Jahncke"),
    ui.input_action_button("go","Calculate o-index"),
    ui.output_table("o_index_df")
)


def server(input, output, session):
    
    @output
    @render.table
    @reactive.event(lambda: input.go(), ignore_none=False)
    def o_index_df():
        o_df = get_openness(input.author(), "apikey.txt")
        return o_df


app = App(app_ui, server)
