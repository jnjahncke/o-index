from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("o-index"),
    ui.input_text("author", "Author: ", "Jennifer Jahncke"),
    ui.input_action_button("button","Calculate o-index"),
    ui.output_text_verbatim("txt")
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"Author: {input.author()}"


app = App(app_ui, server)
