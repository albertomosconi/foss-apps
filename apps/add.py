#!/usr/bin/env python3
import requests, sys, json, pathlib, bisect

def exit_with_error(message):
    print(f"\033[01m\033[31m{message}\033[0m")
    # sys.exit(1)

def test_link(link, empty=True):
    if link == "":
        if empty:
            return
        else:
            print("- link is required")
            sys.exit(1)
    
    testing_message = "- testing link..."
    print(testing_message, end="\r")
    try:
        r = requests.get(link)
        if r.status_code == 200:
            print(f"{testing_message} OK")
        else:
            raise Exception
    except Exception as e:
        exit_with_error(f"{testing_message} ERROR")


def new_category():
    while True:
        name = input("name: ").strip().lower()
        if name in apps:
            exit_with_error("ERROR: category already exists")
        else:
            break
    
    while True:
        print("https://unicode.org/emoji/charts/full-emoji-list.html")
        emoji = input("emoji: ")
        if emoji in emojis:
            exit_with_error("ERROR: emoji is already taken")
        else:
            break

    apps[name] = {"emoji": emoji, "apps": []}


def new_app():
    new_app = {}
    while True:
        category = input("category: ")
        if category not in apps:
            exit_with_error("ERROR: category doesn't exist")
        else:
            break

    while True:
        source = input("source: ")
        test_link(source, empty=False)
        if source in sources:
            exit_with_error("ERROR: source already exists")
        else:
            new_app["source"] = source
            break

    required_fields = ["name", "description"]
    optional_fields = ["fdroid", "playstore", "website"]
    for k in required_fields + optional_fields:
        while True:
            v = input(f"{k}: ").strip()
            if v in optional_fields:
                test_link(v)
            if v != "":
                new_app[k] = v
                break
            elif k in optional_fields:
                break
                
    # insert in app list for given category in alphabetical order
    bisect.insort(apps[category]["apps"], new_app, key=lambda x: x.get("name"))


root = pathlib.Path(__file__).parent.resolve()
apps = json.load(open(root / "apps.json", "r"))
emojis = [apps.get(c).get("emoji") for c in apps]
sources = [[a.get("source") for a in apps.get(c).get("apps")] for c in apps]

try:
    cmd = int(input("[0] new app\t[1] new category\n> "))
    if cmd:
        new_category()
    else:
        new_app()
    
    with (root/"apps.json").open("w", encoding='utf-8') as f:
        json.dump(apps, f, indent=4)

except KeyboardInterrupt:
    exit_with_error("\nTerminating")
