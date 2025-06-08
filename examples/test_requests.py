import requests

with open("simple_bracket.step", "rb") as f:
    files = {"file": ("simple_bracket.step", f)}
    res = requests.post("http://localhost:8000/convert", files=files)
    print(res.json())
