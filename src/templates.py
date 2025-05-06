from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")


def render_template(template: str, kwargs: dict) -> str:
    content = templates.TemplateResponse(template, kwargs).body.decode("utf-8")
    return content
