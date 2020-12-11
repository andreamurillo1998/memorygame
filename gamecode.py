import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import random

# setup app with stylesheets
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

#dictionary of images
animal_image_dict = {'tiger': 'tiger.png', 'lion': 'lion.png', 'bear': 'bear.png', 'camel': 'camel.png',
                     'elephant': 'elephant.png', 'hawk': 'hawk.png', 'koala': 'koala.png', 'sheep': 'sheep.png',
                     'pig': 'pig.png', 'raccoon': 'raccoon.png', 'turkey': 'turkey.png', 'turtle': 'turtle.png',
                     'zebra': 'zebra.png', 'giraffe': 'giraffe.png', 'dolphin': 'dolphin.png'}

image_dict_dif = {'accordion': 'accordion.png', 'ballons': 'balloons.png', 'bananas': 'bananas.png', 'boots': 'boots.png',
                  'camera': 'camera.png', 'cash register': 'cashregister.png', 'chair': 'chair.png', 'taxi': 'taxi.png',
                  'hot cheetos': 'hotcheetos.png', 'lasagna': 'lasagna.png', 'Abraham Lincoln': 'lincoln.png', 'microwave': 'microwave.png',
                  'Barack Obama': 'obama.png', 'pancakes': 'pancakes.png', 'starbucks': 'starbucks.png', 'toothpaste': 'toothpaste.png',
                  'sunflower': 'sunflower.png', 'sweater': 'sweater.png', 'thread': 'thread.png'}


####This code is for easy tab
# button to load new images and start new game
refresh_button = html.Div(
    dbc.Button('Load Images', color='info', n_clicks=0, className="mb-3", block=True, id="refresh")
)

#button to bring up modal with the question and answer options
next_page_button = html.Div(
        dbc.Button("Play", id='next', color="success", block=True, className="mb-3")
)
 #callback to update screen with new images that are randomly selected from dictionary
@app.callback(
    [Output("new-images", "children"), Output("answer-input", "options")],
    Input("refresh", "n_clicks"),
    State("new-images", "children")
)
def update_images(n, image):
    if n:
        # generate random images so that the game is different everytime you press start button
        random_image_tuple_list = random.sample(list(animal_image_dict.items()), 4)
        global random_image_value_list
        global random_image_key_list
        random_image_value_list = [x[1] for x in random_image_tuple_list]
        random_image_key_list = [x[0] for x in random_image_tuple_list]
        answer_options_list = list(animal_image_dict.keys())
        random.shuffle(answer_options_list)
        updated_options = list({"label": x, "value": x} for x in answer_options_list)

        image1 = dbc.Card(
            [dbc.CardImg(src='/assets/easy/' + random_image_value_list[0], bottom=True)],
            style={"height": "15rem", 'width': '10rem', "border": "None"}
        )
        image2 = dbc.Card(
            [dbc.CardImg(src='/assets/easy/' + random_image_value_list[1], top=True)],
            style={"height": "15rem", 'width': '10rem', "border": "None"}
        )
        image3 = dbc.Card(
            [dbc.CardImg(src='/assets/easy/' + random_image_value_list[2], bottom=True)],
            style={"height": "15rem", 'width': '10rem', "border": "None"}
        )
        image4 = dbc.Card(
            [dbc.CardImg(src='/assets/easy/' + random_image_value_list[3], top=True)],
            style={"height": "15rem", 'width': '10rem', 'border': 'None'}
        )

        updated_images = dbc.Row(
            [
                dbc.Col([image1, image2], width=5),
                dbc.Col([image3, image4], width=5),
            ],
            justify="center",
        )

        return [updated_images, updated_options]
    else:
        answer_options = []
        return [None, answer_options]

#fade function makes images disappear when question modal pops up so that player cannot cheat in the game
fading_pics = html.Div(
    style={"display": "flex", "flex-direction": "column"},
    id='new-images')

fade = html.Div(
    [
        dbc.Fade(
            fading_pics,
            id="fade",
            is_in=True,
            appear=False
        ),
    ]
)

#callback so that pictures fade out when next button is clicked and question modal pops up
@app.callback(
    Output("fade", "is_in"),
    [Input("next", "n_clicks"),
     Input("close", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_fade(n, n2, is_in):
    if not n:
        return True
    return not is_in

#keeps track of player score
score_tracker = html.Div(
        html.P(id="answer-output")
)

#question and answer options checklist
answer_options = dbc.FormGroup(
    [
        dbc.Label("Which images appeared?"),
        dbc.Checklist(options=[],
            id="answer-input"
        ),
    ]
)

#modal that contains question and answer options checklist
question_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Which of these images were present?"),
                dbc.ModalBody([answer_options, score_tracker]),
                dbc.ModalFooter(
                    [dbc.Button("Submit answer", id="submit", n_clicks=0, className="ml-auto"),
                    dbc.Button("Close", id="close", className="ml-auto")]
                ),
            ],
            id="modal",
            size="xl",
            backdrop="static",
            keyboard=False
        ),
    ]
)

#modal callback so that modal pops up when next button is clicked
@app.callback(
    Output("modal", "is_open"),
    [Input("next", "n_clicks"),
     Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#callback that updates amount of points if question is answered correctly
@app.callback(
    Output("answer-output", "children"),
    Input('submit', 'n_clicks'),
    [State("answer-input", "value"),
    State("answer-output", "children")]
)
def add_point(n, answer_value, answer_output):
    if n>0:
        points=0
        template = "You scored {} points."
        for x in answer_value:
            if x in random_image_key_list:
                points=points+1
            elif x not in random_image_key_list:
                points=points-1
        output_string = template.format(
            points
        )
        return output_string

### End of easy tab code



### Next is the code for difficult tab

#button to load new images and start new game
refresh_button_dif=html.Div(
    dbc.Button('Start Game', color='info', n_clicks=0, className="mb-3", block=True, id="refresh-dif")
)

#button that refreshes page so that the difficult version of game can be played again
page_refresh_button = html.A(html.Button('Play Again', className="btn btn-success btn-block"), href='/')

#callback that generates new images selected randomly from dictionary
@app.callback(
    [Output("new-images-dif", "children"), Output("answer-input-dif", "options")],
    Input("refresh-dif", "n_clicks"),
    State("new-images-dif", "children")
)
def update_images_dif(n, image):
    if n:
        # generate random images to show so that the game is different everytime you press start button
        random_image_tuple_list_dif = random.sample(list(image_dict_dif.items()), 9)
        global random_image_value_list_dif
        global random_image_key_list_dif
        random_image_value_list_dif = [x[1] for x in random_image_tuple_list_dif]
        random_image_key_list_dif = [x[0] for x in random_image_tuple_list_dif]
        answer_options_list_dif = list(image_dict_dif.keys())
        # answer_options_list = random_image_key_list + ['zebra', 'dog', 'platypus', 'giraffe']
        random.shuffle(answer_options_list_dif)
        updated_options_dif= list({"label": x, "value": x} for x in answer_options_list_dif)

        image1_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[0])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )
        image2_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[1])],
            style={"height": "10rem", 'width': '10rem', "border": "None"}
        )
        image3_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[2])],
            style={"height": "10rem", 'width': '10rem', "border": "None"}
        )
        image4_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[3])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )
        image5_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[4])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )
        image6_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[5])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )
        image7_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[6])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )
        image8_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[7])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )
        image9_dif = dbc.Card(
            [dbc.CardImg(src='/assets/hard/' + random_image_value_list_dif[8])],
            style={"height": "10rem", 'width': '10rem', 'border': 'None'}
        )

        updated_images_dif=dbc.Row(
            [
                dbc.Col([image1_dif, image2_dif, image3_dif], width=4),
                dbc.Col([image4_dif, image5_dif, image6_dif], width=4),
                dbc.Col([image7_dif, image8_dif, image9_dif], width=4),
            ],
            justify="center",
        )

        return [updated_images_dif, updated_options_dif]
    else:
        answer_options_dif=[]
        return [None,answer_options_dif]

#fade function makes images disappear when question pops up so that player cannot cheat in the game
fading_pics_dif= html.Div(
    style={"display": "flex", "flex-direction": "column"},
    id='new-images-dif'
)

fade_dif = html.Div(
    [
        dbc.Fade(
            fading_pics_dif,
            id="fade-dif",
            is_in=True,
            appear=False
        ),
    ]
)

#tracks player score
score_tracker_dif = html.Div(
        html.P(id="answer-output-dif")
)

#set up answer options checklist
answer_options_dif = dbc.FormGroup(
    [
        dbc.Label("Which images appeared?"),
        dbc.Checklist(options=[],
            id="answer-input-dif"
        ),
    ]
)

#create modal that contains the questions, answer options, and player score
question_modal_dif = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Which of these images appeared?"),
                dbc.ModalBody([answer_options_dif, score_tracker_dif]),
                dbc.ModalFooter(
                    [dbc.Button("Submit answer", id="submit-dif", n_clicks=0, className="ml-auto"),
                    dbc.Button("Close", id="close-dif", className="ml-auto")]
                ),
            ],
            id="modal-dif",
            size="xl",
            backdrop="static",
            keyboard = False
        ),
    ]
)

#callback that updates amount of points if question is answered correctly
@app.callback(
    Output("answer-output-dif", "children"),
    Input('submit-dif', 'n_clicks'),
    [State("answer-input-dif", "value"),
    State("answer-output-dif", "children")]
)
def add_point_dif(n, answer_value_dif, answer_output):
    if n>0:
        points=0
        template = "You scored {} points."
        for x in answer_value_dif:
            if x in random_image_key_list_dif:
                points=points+1
            elif x not in random_image_key_list_dif:
                points=points-1
        output_string_dif = template.format(
            points
        )
        return output_string_dif

#this is the timer that keeps track of how much time is left since difficult level is timed
timer = dbc.Container(
    html.Div(
    [dcc.Interval(id="progress-interval", n_intervals=0, max_intervals=30, interval=1000, disabled=True),
    dbc.Progress(id="progress", value=0, max=30, style={'height': "2rem"}, color="danger")],
    style={'height': '3rem'}
    ),
    fluid=True)

#this is the main callback for the difficult level tab
#this updates the progress bar to show the user how much time they have left to look at images
#the timer only starts once the player clicks the start button
#once the timer hits 0, the images fade out and question modal pops up
@app.callback(
    [Output("modal-dif", "is_open"),
     Output("progress-interval", "disabled"),
     Output("progress", "value"),
     Output("progress", "children"),
     Output("refresh-dif", "disabled"),
     Output("fade-dif", "is_in")],
    [Input("refresh-dif", "n_clicks"),
     Input("progress-interval", "n_intervals"),
     Input("close-dif", "n_clicks")],
    [State("modal-dif", "is_open"),
     State("fade-dif", "is_in")]
)
def update_progress(n1, n2, n4, is_open, is_in):
    if n1:
        remaining_time = n2
        progress_text = f"{30-remaining_time} seconds left"
        disabled = False
        if remaining_time == 30:
            return [not is_open, disabled, remaining_time, progress_text, False, not is_in]
        else:
            return [is_open, disabled, remaining_time, progress_text, True, is_in]
    else:
        raise PreventUpdate

### code for difficult tab end

#create intro/instructions tab
#I included a sound to autoplay when page loads as a fun way to welcome player to the game
tab1_content = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("Memory Game", className="display-4"),
                html.Hr(className="my-2"),
                html.P(
                    """There will be several images displayed. Memorize
                    as many images as you can and select the images that appeared.""",
                    className="lead"),
                html.P(
                    """The easy level is not timed and has four images.""",
                    className="lead"),
                html.P(
                    """The hard level is timed. You will have 30 seconds to look at nine images
                    before the question pops up.""",
                    className="lead"),
                html.P("""You gain a point for every correct answer. You lose a point
                    for every incorrect answer.""",
                    className="lead text-danger"),
                html.Audio(id="player", src="/assets/thegame.m4a", autoPlay=True),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)


#wireframe for tab 2 (easy version of game)
tab2_content = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(question_modal, md=12),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(md=2),
                dbc.Col(fade, md='8', style={'offset':3})
            ],
            align="center",
        ),
        dbc.Row(
            dbc.Col(refresh_button, md=12)
        ),
        dbc.Row(
                dbc.Col(next_page_button, md=12),
            align="center",
        )
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)

#wireframe for difficult versiom of game
tab3_content =  dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(question_modal_dif, md=12),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(md=2),
                dbc.Col(fade_dif, md='8', style={'offset':3}, align='center')
            ],
            align="center",
        ),
        dbc.Row(
            dbc.Col(timer, md=12)
        ),
        dbc.Row(
            dbc.Col(refresh_button_dif, md=12)
        ),
        dbc.Row(
            dbc.Col(page_refresh_button, md=12)
        )
    ],
    id="main-container-difficult",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)

#main wireframe
app.layout = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Instructions", tab_style={"color": "#00AEF9"}),
        dbc.Tab(tab2_content, label="Difficulty: Easy", tab_style={"color": "#00AEF9"}),
        dbc.Tab(tab3_content, label="Difficulty: Hard", tab_style={"color": "#00AEF9"})],
)

# Main
if __name__ == "__main__":
    app.run_server(debug=True)