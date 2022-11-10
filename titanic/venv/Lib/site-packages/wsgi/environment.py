from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("titanic"),
    autoescape=select_autoescape()
)