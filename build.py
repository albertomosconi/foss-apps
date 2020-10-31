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


if __name__ == "__main__":
    readme = root / "README.md"

    apps = parse_apps()

    md = "\n".join([
        "- [{text}](#{link} \"{text}\")".format(text=" ".join(x.title() if x != "and" else "and" for x in category.split(" ")),
                                                link=category.replace(" ", "-"))
        for category in apps.keys()
    ])

    readme_contents = readme.open().read()
    new = replace_chunk(readme_contents, "table-of-contents", md)

    readme.open("w").write(new)
