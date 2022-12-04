import yaml
from yaml.loader import SafeLoader

compose:str = ""
composeBackend:str = ""
with open("./compose/compose.yaml") as f:
    compose = yaml.load(f, Loader=SafeLoader)

with open("./compose.yaml") as f:
    composeBackend = yaml.load(f, Loader=SafeLoader)

compose["services"]["backend-reservations"] = composeBackend["services"]["backend-reservations"]
with open("./compose/compose.yaml", 'w') as f:
    data = yaml.dump(compose, f)
