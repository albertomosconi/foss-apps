import functools, json, pathlib, re


def parse_categories():
    cats = list(filter(lambda f: f.suffix == ".json", pathlib.Path.iterdir(json_dir)))

    return cats


def replace_chunk(content, marker, chunk):
    # replaces the text between the comments with the specified marker with the content
    r = re.compile(f"<!-- {marker} starts -->.*<!-- {marker} ends -->", re.DOTALL)
    chunk = f"<!-- {marker} starts -->\n{chunk}\n<!-- {marker} ends -->"
    return r.sub(chunk, content)


def count_apps():
    count = 0
    for cat in categories:
        with cat.open("r") as f:
            cat_json = json.load(f)
            count += len(cat_json.get("apps"))

    return count


def build_category(cat):
    with cat.open("r") as f:
        cat_json = json.load(f)

    md_file = categories_dir / (cat.stem + ".md")
    with md_file.open("w") as f:
        lines = [
            f'# {cat_json.get("emoji")} {cat_json.get("title")}',
            "[`< go back home`](../README.md)",
        ]

        for app in cat_json.get("apps"):
            name = app.get("name")
            description = app.get("description")
            source = app.get("source")
            fdroid = app.get("fdroid")
            playstore = app.get("playstore")
            website = app.get("website")

            m = re.match(
                "https:\/\/(gitlab|github)\.com/([a-zA-Z0-9\-\_\.]+)/([a-zA-Z0-9\-\_\.]+)",
                source,
            )
            if m == None:
                stars_link = app.get("stars_link")
                last_commit_link = app.get("last_commit_link")
            else:
                stars_link = (
                    f"https://badgen.net/{m.group(1)}/stars/{'/'.join(m.group(2,3))}"
                )
                last_commit_link = f"https://img.shields.io/{m.group(1)}/last-commit/{'/'.join(m.group(2,3))}"

            badge_stars = f"![Stars]({stars_link})" if stars_link else ""
            badge_commit = (
                f"![last commit]({last_commit_link})" if last_commit_link else ""
            )
            link_source = f'[`[source]`]({source} "source")'
            link_fdroid = f'[`[f-droid]`]({fdroid} "f-droid")' if fdroid else ""
            link_playstore = (
                f'[`[playstore]`]({playstore} "playstore")' if playstore else ""
            )
            link_website = f'[`[website]`]({website} "website")' if website else ""

            lines.append(
                f"""
- **{name}**: {description}

    {badge_stars} {badge_commit}

    {link_source} {link_fdroid} {link_playstore} {link_website}"""
            )

        f.write("\n".join(lines))


def build_readme():
    readme_contents = (root / "README.md").open("r").read()

    app_count_md = f'<img src="https://img.shields.io/badge/{n_apps}-apps-red?style=for-the-badge" alt="App count"/>'
    readme_contents = replace_chunk(readme_contents, "apps-count", app_count_md)

    sorted_categories = list(categories)
    sorted_categories.sort()

    toc_lines = [""]
    for category in sorted_categories:
        with category.open("r") as f:
            json_cat = json.load(f)
            title = json_cat.get("title")
            emoji = json_cat.get("emoji")
        link = category.stem
        toc_lines.append(f"- [{emoji} {title}](categories/{link}.md)")
    readme_contents = replace_chunk(
        readme_contents, "table-of-contents", "\n".join(toc_lines)
    )

    (root / "README.md").open("w").write(readme_contents)


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    scripts_dir = root / "scripts"
    json_dir = root / "apps"
    categories_dir = root / "categories"

    if not categories_dir.exists():
        pathlib.Path.mkdir(categories_dir)

    categories = parse_categories()
    n_apps = count_apps()
    build_readme()
    for category in categories:
        build_category(category)
