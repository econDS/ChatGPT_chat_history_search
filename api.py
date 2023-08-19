import pandas as pd
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional

# Constants
CONTENT_DISPLAY_LENGTH = 80
EXCEL_PATH = 'chat.xlsx'

# Load Data
df = pd.read_excel(EXCEL_PATH)
print("Data loaded")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def render_dataframe(data_frame: pd.DataFrame) -> str:
    return data_frame.to_html(
        escape=False,
        classes=[
            "table table-bordered table-striped table-hover text-start w-auto mx-auto table-responsive"
        ],
        justify="center"
    ).replace("<thead>", "<thead class='thead-light'>", 1)

def format_data_frame(text: str) -> pd.DataFrame:
    filter_df = df[df['contents'].str.lower().str.contains(text.lower())]
    filter_df.reset_index(drop=True, inplace=True)
    filter_df.index += 1
    filter_df['create_times'] = pd.to_datetime(filter_df['create_times'], unit='s').dt.strftime('%d %b %Y')
    filter_df['contents'] = filter_df['contents'].apply(lambda x: x[:CONTENT_DISPLAY_LENGTH] + '...' if len(x) > CONTENT_DISPLAY_LENGTH else x)
    return filter_df

def create_clickable_links(row) -> str:
    link = row['link']
    display_text = link.split("/")[-1][:30]
    return f'<a href="{link}" target="_blank">{display_text}</a>'

@app.get("/search/")
@app.get("/search/{text}")
def get_search(request: Request, text: Optional[str] = ""):
    if text is None or text.strip() == '':
        return render_template(request, "", pd.DataFrame(columns=df.columns))

    filter_df = format_data_frame(text)
    
    try:
        filter_df['link'] = filter_df.apply(create_clickable_links, axis=1)
    except ValueError:
        filter_df = pd.DataFrame(columns=filter_df.columns)

    return render_template(request, text, filter_df)

def render_template(request: Request, text: str, data_frame: pd.DataFrame):
    return templates.TemplateResponse(
        'df_representation.html',
        {
            'request': request,
            'data': render_dataframe(data_frame),
            'text': text
        }
    )

if "__main__" == __name__:
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
