# Contributing Guidelines

This document shows you how to get started with your contribution to this project. If you follow these, your PR will be merged quickly.

[**ADDING A NEW APP**](#adding-a-new-app "ADDING A NEW APP")

[**OTHER CONTRIBUTIONS**](#other-contributions "OTHER CONTRIBUTIONS")

## Adding a new app

- Fork the repo

  - <https://github.com/albertomosconi/foss-apps/fork>

- Check out a new branch based and name it the same as the app you want to add:

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

  - Both the **categories** and the **sublist of apps** in each category are **ordered alphabetically**, so pay attention to this when you're adding your app to the list.

  - Use this template so that the list remains uniform

    ```
    - [![GitHub Stars](https://img.shields.io/github/stars/[AUTHOR]/[REPO].svg?label=★&style=flat)
    **[APP_NAME]**](https://github.com/[AUTHOR]/[REPO] "[APP_NAME]"): [DESCRIPTION]
    ```

    Replace `AUTHOR` with the username of the author, `REPO` with the name of the repository containing the source code, `APP_NAME` with the name of the app, and `DESCRIPTION` with a short description describing the app's purpose and features.

    For **GitLab** repos please refer to **issue #1**.

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

## Other Contributions

There are no specific rules for any other type of contribution, feel free to send your PR!
