import plotly.express as px
from dash import dash_table
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


colors = {'light_blue': '#0d76bd',
          'dark_blue': '#0660a9',
          'red': '#ed1c23',
          'white': '#ffffff',
          'grey': '#888888',
          'light_grey': '#d3d3d3'
          }


def create_stacked_chart_race(df):
    party_colors = {
        'Republican': colors['red'],
        'Democrat': colors['dark_blue'],
        'DK/REF': colors['white'],
        'Independent': colors['light_blue']
    }

    fig = px.bar(df, x='race', y='percentage', color='political_party',
                 title='Political Party by Race',
                 labels={'percentage': '', 'race': 'Race'},
                 category_orders={'race': sorted(df['race'].unique())},
                 hover_data={'percentage': ':.1%'},
                 barmode='relative',
                 color_discrete_map=party_colors)

    fig.update_yaxes(title='', tickformat='0.0%')
    fig.update_layout(
        title_text='Political Party by Race',
        title_font_size=20,
        xaxis_title='',
        yaxis_title_font=dict(size=15),
        legend_title_font_size=10,
        legend_font_size=10,
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        height=380,
        width=350,
        paper_bgcolor=colors['light_grey'],
        plot_bgcolor=colors['light_grey'],
        legend_title='Political Party',
        showlegend=False
    )

    return fig


def create_stacked_chart_education(df):
    party_colors = {
        'Republican': colors['red'],
        'Democrat': colors['dark_blue'],
        'DK/REF': colors['white'],
        'Independent': colors['light_blue']
    }

    fig = px.bar(df, x='higher_education', y='percentage', color='political_party',
                 title='Political Party by Education Level',
                 labels={'percentage': 'Percentage',
                         'higher_education': 'Education Level'},
                 category_orders={'higher_education': sorted(
                     df['higher_education'].unique())},
                 hover_data={'percentage': ':.2%'},
                 barmode='relative',
                 color_discrete_map=party_colors)

    fig.update_yaxes(visible=True, tickformat=',.0%')
    fig.update_traces(selector=dict(type='bar'),
                      showlegend=True,
                      legendgroup='political_party',
                      hovertemplate=None)

    fig.update_layout(
        title_text='Political Party by Education Level',
        title_font_size=20,
        yaxis_title='',
        xaxis_title='',
        legend_title_font_size=10,
        legend_font_size=10,
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        height=380,
        width=350,
        paper_bgcolor=colors['light_grey'],
        plot_bgcolor=colors['light_grey'],
        legend_title='Political Party'
    )

    fig.update_layout(legend_itemclick=False, legend_itemdoubleclick=False)

    return fig


def create_donut_chart(df):
    counts = df['trump_2020'].value_counts().reset_index()
    counts.columns = ['trump_2020', 'counts']
    custom_colors = {
        'Very Likely': colors['red'],
        'Somewhat Likely': colors['light_blue'],
        'Not at all likely': colors['dark_blue'],
        'DK/REF': colors['white']
    }
    category_colors = [custom_colors.get(
        x, colors['grey']) for x in counts['trump_2020']]

    fig_donut = px.pie(counts, values='counts', names='trump_2020', hole=0.4)
    fig_donut.update_traces(textinfo='percent+label', pull=[0 for _ in range(len(counts))],
                            marker=dict(colors=category_colors))
    fig_donut.update_layout(
        title='Likelihood of Donald Trump Reelection in 2020',
        showlegend=False,
        annotations=[dict(text='Trump', x=0.5, y=0.5,
                          font_size=20, showarrow=False)],
        title_font_size=20,
        xaxis_title_font=dict(size=15),
        yaxis_title_font=dict(size=15),
        legend_title_font_size=10,
        legend_font_size=10,
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        height=340,
        width=750,
        paper_bgcolor=colors['light_grey'],
        plot_bgcolor=colors['light_grey']
    )

    return fig_donut


def create_war_likelihood_chart(df):
    # Ensure data is in the correct format
    if df['likelihood_of_war'].dtype != object:
        likelihood_mapping = {
            2: 'Very Likely',
            1: 'Somewhat Likely',
            0: 'Not at all likely'
        }
        df['likelihood_of_war'] = df['likelihood_of_war'].map(
            likelihood_mapping)

    # Aggregate the data to get the count of responses for each category
    likelihood_counts = df['likelihood_of_war'].value_counts().reset_index()
    likelihood_counts.columns = ['Opinion', 'Count']

    # Define colors for the opinions
    opinion_colors = {
        'Very Likely': colors['red'],
        'Somewhat Likely': colors['white'],
        'Not at all likely': colors['dark_blue']
    }

    # Create the horizontal bar chart using Plotly Express
    fig = px.bar(likelihood_counts, x='Count', y='Opinion', orientation='h',
                 title='Perceived Likelihood of War',
                 labels={'Count': 'Number of Responses', 'Opinion': ''},
                 text='Count',
                 color='Opinion',
                 color_discrete_map=opinion_colors)

    fig.update_layout(
        title_text='Perceived Likelihood of War<br><sub>Likelihood of War in the next 50 years</sub>',
        title_font_size=20,
        xaxis_title_font=dict(size=15),
        yaxis_title_font=dict(size=15),
        legend_title_font_size=10,
        legend_font_size=10,
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        height=340,
        width=700,
        paper_bgcolor=colors['light_grey'],
        plot_bgcolor=colors['light_grey'],
        showlegend=False
    )
    return fig


def create_heatmap(df):
    pivot_df = df.pivot_table(
        index='fairness_voting', columns='fairness_voting', aggfunc='size', fill_value=0)
    fig = px.imshow(pivot_df,
                    labels=dict(x="Trump Approval", y="Voting Fairness"),
                    color_continuous_scale='RdBu_r',
                    text_auto=True)

    fig.update_layout(
        title='Heatmap of Voting Fairness vs. Trump Approval',
        title_font_size=20,
        xaxis_title_font=dict(size=15),
        yaxis_title_font=dict(size=15),
        legend_title_font_size=10,
        legend_font_size=10,
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        height=380,
        width=750,
        paper_bgcolor=colors['light_grey'],
        plot_bgcolor=colors['light_grey']
    )
    return fig


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="/page-1",
                    style={'color': colors['light_blue']})),
        dbc.NavItem(dbc.NavLink("Page 2", href="/page-2",
                    style={'color': colors['light_blue']})),
    ],
    color='0660a9',
    dark=True
)

navbar_brand_style = {
    'color': colors['light_blue'],
    'fontSize': '24px'
}
