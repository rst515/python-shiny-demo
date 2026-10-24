from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

app_ui = ui.page_fluid(
    ui.panel_title("My First App with Data, Graph, and Controls"),
    ui.input_radio_buttons(
        "radio",
        "Radio buttons",
        ["pop", "lifeExp", "gdpPercap"],
        inline=True,
    ),
    ui.layout_columns(
        ui.output_data_frame("life_exp"),
        output_widget("plot"),
    ),
)


def server(input, output, session):
    @render.ui
    def value():
        return input.radio()

    @render.data_frame
    def life_exp():
        return render.DataGrid(df, filters=True)

    @reactive.calc
    def filter_life_exp():
        selected = input.radio()
        return df[df[selected]]

    @render_widget
    def plot():
        return px.histogram(
            data_frame=df,
            x="continent",
            y=input.radio(),
            histfunc="avg",
        )


app = App(app_ui, server)
