import re
import pathlib
import json

root = pathlib.Path(__file__).parent.resolve()


def parse_apps():
    with open(root / "apps.json", "r") as file:
        return json.load(file)


def replace_chunk(content, marker, chunk, inline=False):
    # replaces the text between the comments with the specified marker with the content
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(
        marker, chunk, marker)
    return r.sub(chunk, content)


def build_readme():
    readme_contents = readme.open().read()

    # count apps
    count = 0
    for category in apps.keys():
        count += len(apps[category])

    app_count_md = '<img src="https://img.shields.io/badge/{}-apps-red?style=for-the-badge" alt="App Count"/>'.format(
        count)

    rewritten = replace_chunk(
        readme_contents, "counter", app_count_md)

    # write the table of contents
    md = "\n".join([
        "- [{text}](#{link} \"{text}\")".format(text=" ".join(x.title() if x != "and" else "and" for x in category.split(" ")),
                                                link=category.replace(" ", "-"))
        for category in apps.keys()
    ])

    rewritten = replace_chunk(rewritten, "table-of-contents", md)

    # write app list
    list_md = ""
    for category in apps.keys():

        list_md += "## {}\n\n**[`^ back to top ^`](#table-of-contents)**\n\n".format(
            " ".join(x.title() if x != "and" else "and" for x in category.split(" ")))

        for app in apps[category]:

            list_md += "- "

            if "host" in app:
                list_md += "![{} Stars]({})\n".format(
                    app["host"], app["stars_link"])

            list_md += "**{}**: {}\n".format(app["name"], app["description"])

            list_md += "[`[source]`]({} \"source\")".format(app["source"])

            if "fdroid" in app:
                list_md += "[`[f-droid]`]({} \"f-droid\")".format(app["fdroid"])

            if "playstore" in app:
                list_md += "[`[playstore]`]({} \"playstore\")".format(
                    app["playstore"])

            if "website" in app:
                list_md += "[`[website]`]({} \"website\")".format(
                    app["website"])

            list_md += "\n\n"

    rewritten = replace_chunk(rewritten, "list", list_md)

    return rewritten


if __name__ == "__main__":
    readme = root / "README.md"

    apps = parse_apps()

    rewritten = build_readme()

    readme.open("w").write(rewritten)
