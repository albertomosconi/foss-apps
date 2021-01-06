# Contributing Guidelines

This document shows you how to get started with your contribution to this project. If you follow these, your PR will be merged quickly.

[**ADDING A NEW APP**](#adding-a-new-app "ADDING A NEW APP")

[**OTHER CONTRIBUTIONS**](#other-contributions "OTHER CONTRIBUTIONS")

## Adding a new app

- Fork the repo

  - <https://github.com/albertomosconi/foss-apps/fork>

- Check out a new branch from `master` and name it the same as the app you want to add:

  - Run this command in a terminal (replacing `APP_NAME` with the name of your app)
    ```
    $ git checkout -b APP_NAME
    ```
    If you get an error, you may need to run this command first
    ```
    $ git remote update && git fetch
    ```
  - Use one branch per app

- Add your app to the list, respecting the general structure

  - ### The only file that should be edited is `apps.json`

  - If you're not familiar with the `json` format please look it up before editing to avoid errors. For example read [this article](https://www.w3schools.com/whatis/whatis_json.asp "this article").

  - Both the **categories** and the **sublist of apps** in each category are **ordered alphabetically**, so pay attention to this when you're adding your app to the list.

  - Each app entry has the same structure, fill as many fields as possible so that the information is the most complete. If the field remains empty please delete it from the object.

    ```
      {
            "host": "",
            "name": "",
            "description": "",
            "stars_link": "",
            "source": "",
            "fdroid": "",
            "playstore": "",
            "website": ""
      }
    ```

    `host` should either be "GitHub" or "GitLab", if your app isn't provided through one of these platforms please delete this field, along with the `stars_link` field. The latter should contain the link for the stars badge using the following templates:

    - GitHub: `https://img.shields.io/github/stars/<USERNAME>/<REPO>.svg?label=★&style=flat`
    - GitLab: please refer to [**issue #1**](https://github.com/albertomosconi/foss-apps/issues/1 "issue #1").

    `description` should contain a text from 15 to 60 words, describing the key functionality and selling points of your application.

- Commit your changes

  - Make sure your commit message follows the following pattern, where `APP_NAME` is the name of your app, and `CATEGORY_NAME` is the category in which your app resides
    ```
    $ git commit -am "Added APP_NAME in CATEGORY_NAME"
    ```

- Push to the branch

  - Check that you're pushing to the branch named after your app
    ```
    $ git push origin APP_NAME
    ```

- Make a pull request

  - Make sure you send the PR to the `master` branch

- Don't forget to star the repo ;)

## Other Contributions

There are no specific rules for any other type of contribution, feel free to send your PR!
