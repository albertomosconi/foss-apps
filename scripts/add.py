#!/usr/bin/env python3
import requests, sys, json, pathlib, bisect, math

root = pathlib.Path(__file__).parent.parent.resolve()
category_sources = list(filter(lambda f: f.suffix == ".json", pathlib.Path.iterdir(root/"apps")))
category_names = [c.stem for c in category_sources]
emojis = []
sources = []
for c in category_sources:
    json_c = json.load(c.open("r"))
    emojis.append(json_c.get("emoji"))
    for a in json_c.get("apps"):
        sources.append(a.get("source"))

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
        raise e


def display_categories():
    n = math.ceil(len(category_names)/3)
    
    col1, col2, col3 = category_names[:n], category_names[n:2*n], category_names[2*n:]
    if len(col3) < len(col1):
        col3.append("")
    maxlen1 = len(max(col1, key=len))
    maxlen2 = len(max(col2, key=len))

    for i,j,k in zip(col1, col2, col3):
        print(f"{i.ljust(maxlen1, ' ')}\t{j.ljust(maxlen2, ' ')}\t{k}")
    print()


def new_category():
    display_categories()
    while True:
        name = input("name: ").strip().lower()
        if name in category_names:
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

    # create new category json file
    title = " ".join(x.title() if x != "and" else "and" for x in name.split("-"))
    with open(root/"apps"/f"{name}.json", "w") as f:
        json.dump({"title": title, "emoji": emoji, "apps": []}, f, indent=4)


def new_app():
    new_app = {}
    display_categories()
    while True:
        category = input("category: ").strip().lower()
        if category not in category_names:
            exit_with_error("ERROR: category doesn't exist")
        else:
            break

    while True:
        source = input("source: ").strip().lower()
        try:
            test_link(source, empty=False)
        except:
            continue
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
            if v != "":
                try:
                    if k in optional_fields:
                        test_link(v)
                    new_app[k] = v
                    break
                except:
                    continue
            elif k in optional_fields:
                break
            else:
                exit_with_error("this field is required.")
                
    # insert in app list for given category in alphabetical order
    with open(root/"apps"/(category+".json"), "r") as f:
        json_c = json.load(f)
    bisect.insort(json_c["apps"], new_app, key=lambda x: x.get("name").lower())
    with open(root/"apps"/(category+".json"), "w") as f:
        json.dump(json_c, f, indent=4)

try:
    cmd = int(input("[0] new app\t[1] new category\n> "))
    if cmd:
        new_category()
    else:
        new_app()

except KeyboardInterrupt:
    exit_with_error("\nTerminating")
