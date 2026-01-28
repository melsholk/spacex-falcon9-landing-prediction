"""Plotly Dash dashboard for SpaceX launch outcomes.

Run:
    python -m spacex_landing.dashboard.app --data data/raw/spacex_launch_dash.csv
"""

from __future__ import annotations

import argparse
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

def build_app(df: pd.DataFrame) -> Dash:
    app = Dash(__name__)

    launch_sites = sorted(df["Launch Site"].dropna().unique().tolist())
    options = [{"label": "All Sites", "value": "ALL"}] + [{"label": s, "value": s} for s in launch_sites]

    min_payload = float(df["Payload Mass (kg)"].min())
    max_payload = float(df["Payload Mass (kg)"].max())

    app.layout = html.Div(
        children=[
            html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center"}),
            dcc.Dropdown(
                id="site-dropdown",
                options=options,
                value="ALL",
                placeholder="Select a Launch Site here",
                searchable=True,
            ),
            html.Br(),
            dcc.Graph(id="success-pie-chart"),
            html.Br(),
            html.P("Payload range (Kg):"),
            dcc.RangeSlider(
                id="payload-slider",
                min=0,
                max=10000,
                step=1000,
                marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
                value=[min_payload, max_payload],
            ),
            html.Br(),
            dcc.Graph(id="success-payload-scatter-chart"),
        ]
    )

    @app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
    def update_pie(site: str):
        if site == "ALL":
            # total successful launches per site
            tmp = df.groupby("Launch Site", as_index=False)["class"].sum()
            return px.pie(tmp, values="class", names="Launch Site", title="Total Successful Launches by Site")
        else:
            filtered = df[df["Launch Site"] == site]
            tmp = filtered["class"].value_counts().rename_axis("class").reset_index(name="count")
            tmp["class"] = tmp["class"].map({1: "Success", 0: "Failure"})
            return px.pie(tmp, values="count", names="class", title=f"Launch Outcomes for {site}")

    @app.callback(
        Output("success-payload-scatter-chart", "figure"),
        Input("site-dropdown", "value"),
        Input("payload-slider", "value"),
    )
    def update_scatter(site: str, payload_range):
        low, high = payload_range
        filtered = df[(df["Payload Mass (kg)"] >= low) & (df["Payload Mass (kg)"] <= high)]
        if site != "ALL":
            filtered = filtered[filtered["Launch Site"] == site]
        return px.scatter(
            filtered,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Payload vs. Launch Outcome",
        )

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="Path to spacex_launch_dash.csv")
    parser.add_argument("--port", type=int, default=8050)
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    app = build_app(df)
    app.run_server(host="0.0.0.0", port=args.port, debug=True)

if __name__ == "__main__":
    main()
