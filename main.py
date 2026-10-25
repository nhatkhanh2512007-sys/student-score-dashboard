from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from charts import classification_chart_html, distribution_png
from data_service import (clean_scores, enrich_scores, filter_scores,
                          load_scores, summarize)

app = FastAPI(title="Student Score Dashboard")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_data():
    return enrich_scores(clean_scores(load_scores()))


@app.get("/api/summary")
def api_summary(class_name: Optional[str] = None):
    data = filter_scores(get_data(), class_name)
    return summarize(data)


@app.get("/api/students")
def api_students(class_name: Optional[str] = None):
    data = filter_scores(get_data(), class_name)
    return data.to_dict(orient="records")


@app.get("/charts/distribution.png")
def chart_distribution(class_name: Optional[str] = None):
    data = filter_scores(get_data(), class_name)
    image = distribution_png(data)
    return StreamingResponse(
        image,
        media_type="image/png",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, class_name: Optional[str] = None):
    all_data = get_data()
    data = filter_scores(all_data, class_name)
    classes = sorted(all_data["class_name"].unique().tolist())
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "summary": summarize(data),
            "students": data.to_dict(orient="records"),
            "classes": classes,
            "selected_class": class_name or "",
            "plotly_chart": classification_chart_html(data),
        },
    )