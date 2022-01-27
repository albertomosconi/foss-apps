import functools, json, pathlib, re


def parse_apps():
    with open(root / "apps.json", "r") as file:
        return json.load(file)


def replace_chunk(content, marker, chunk):
    # replaces the text between the comments with the specified marker with the content
    r = re.compile(f'<!-- {marker} starts -->.*<!-- {marker} ends -->', re.DOTALL)
    chunk = f'<!-- {marker} starts -->{chunk}<!-- {marker} ends -->'
    return r.sub(chunk, content)


def build_readme(apps_dict):
    readme_contents = readme.open().read()

    count = functools.reduce(lambda a, b: a+b, [len(cat) for cat in list(apps_dict.values())])

    app_count_md = f'\n<img src="https://img.shields.io/badge/{count}-apps-red?style=for-the-badge" alt="App count"/>\n'
    readme_contents = replace_chunk(readme_contents, "apps-count", app_count_md)

    sorted_categories = list(apps_dict.keys())
    sorted_categories.sort()

    toc_lines = []
    list_lines = []
    for category in sorted_categories:
        title = " ".join(w.title() if w != "and" else "and" for w in category.split(" "))
        link = category.replace(" ", "-")

        toc_lines.append(f"- [{title}](#{link} \"{title}\")")
        list_lines.append(f"## {title}\n**[`^ back to top ^`](#table-of-contents)**\n")

        for app in apps_dict[category]:
            new_line = "- "
            new_line += f"![{app['host']} Stars]({app['stars_link']})\n" if "host" in app else ""
            new_line += f"**{app['name']}**: {app['description']}\n"
            new_line += f"[`[source]`]({app['source']} \"source\")"
            new_line += "[`[f-droid]`]({} \"f-droid\")".format(app["fdroid"]) if "fdroid" in app else ""
            new_line += f"[`[playstore]`]({app['playstore']} \"playstore\")" if "playstore" in app else ""
            new_line += f"[`[website]`]({app['website']} \"website\")" if "website" in app else ""
            new_line += "\n"

            list_lines.append(new_line)
    
    readme_contents = replace_chunk(readme_contents, "table-of-contents", "\n".join(toc_lines))
    readme_contents = replace_chunk(readme_contents, "list", "\n".join(list_lines))
    
    return readme_contents


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.resolve()
    readme = root / "README.md"

    apps = parse_apps()
    rewritten = build_readme(apps)
    readme.open("w").write(rewritten)
