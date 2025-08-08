import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins

# Load data
df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguins dashboard", fillable=True)

with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass (g)", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

with ui.layout_column_wrap(fill=False):
    # Use a valid icon name (e.g., "kiwi-bird")
    with ui.value_box(showcase=icon_svg("kiwi-bird")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            fig, ax = plt.subplots()
            sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
                ax=ax,
            )
            ax.set_xlabel("Bill length (mm)")
            ax.set_ylabel("Bill depth (mm)")
            ax.set_title("Bill length vs depth")
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# ui.include_css(app_dir / "styles.css")

@reactive.calc()
def filtered_df():
    # Start with selected species
    filt_df = df[df["species"].isin(input.species())].copy()

    # Ensure numeric and drop rows without required fields
    for col in ["body_mass_g", "bill_length_mm", "bill_depth_mm"]:
        filt_df[col] = pd.to_numeric(filt_df[col], errors="coerce")
    filt_df = filt_df.dropna(subset=["body_mass_g", "bill_length_mm", "bill_depth_mm"])

    # Include records up to and including the slider value
    return filt_df.loc[filt_df["body_mass_g"] <= input.mass()]
