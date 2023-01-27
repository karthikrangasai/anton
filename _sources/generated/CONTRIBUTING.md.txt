# Contributing Guide

## Pre-Requisites

- A working installation of Git
- A GitHub Account
- Python 3.8
- Poetry 1.3.1

## Contributing to the project

### 1. Setting up the repository

#### 1.1 Forking the project
Fork the [anton](https://github.com/karthikrangasai/anton) repository to your local github account.

#### 1.2 Forking the project

After forking the project, clone the project locally using the one of the following commands:

```bash
$ git clone git@github.com:<your_github_username>/anton.git      # If using SSH

$ git clone https://github.com/<your_github_username>/anton.git  # If using HTTPS
```

Enter the project directory once the project has been cloned locally.

```bash
$ cd anton  # enter the directory
```

#### 1.3 Set up appropriate remotes

Cloning a repository auto creates the `origin` remote for the project which enables to push/pull to the forked repository.

To enable receiving the latest project updates, it is necessary to setup another remote generally named as `upstream`. This also helps in submitting Pull Requests.

Use one of the following commands:

```bash
$ git remote add upstream git@github.com:karthikrangasai/anton.git      # If using SSH

$ git remote add upstream https://github.com/karthikrangasai/anton.git  # If using HTTPS
```


To verify that the remote has been added, run the following command and verify the outputs: (HTTPS version accordingly)

```bash
$ git remote -v
origin  git@github.com:<your_github_username>/anton.git(fetch)
origin  git@github.com:<your_github_username>/anton.git (push)
upstream    git@github.com:karthikrangasai/anton.git (fetch)
upstream    git@github.com:karthikrangasai/anton.git (push)
```

#### 1.4 Keep the local branches up-to-date

It is necessary to `fetch` the latest changes from the `upstream` remote to work the latest version of the project.

```bash
$ git fetch upstream
```

The `git fetch` command fetches the latest code from all the branches on the `upstream` remote and saves it locally.

To apply these changes to the local copy, it is required to `rebase` the local branch with the `upstream` branch.

```bash
$ git checkout master          # To ensure that the destination branch is correctly set
$ git rebase upstream/master   # Apply the latest changes to the local `master` branch
```

**NOTE:** `rebase` assumes the destination branch as the current local branch and applies the changes from the branch provided in the command.

#### 1.5 Making new changes

Before you make changes, you should always create a new branch to implement your changes.

Running the following command creates a new branch from the current branch and its current state:

```bash
$ git checkout -b feature/<small_description_of_the_feature>
```

**NOTE:** <b style="color:red"> Please do not make changes on the master branch! </b>


To ensure that changes are being made on the right branch, run the following command:

```bash
$ git branch
```

The active branch will have a asterisk <b style="color:red"> \* </b> in front of it.

### 2. Creating a development environment

#### 2.1 Setting the virtual environment

This project uses the [`poetry`](https://python-poetry.org) dependency management tool. Ensure that a working installation of poetry 1.3.1 or above is installed.

Creating a virtual environment with `poetry` is as easy as running the following command:

```bash
$ poetry install --all-extras
```

This aforementioned command creates a virtual environment, installs all the dependencies, and also editable installs the project to reflect the changes during development.

#### 2.2 Setting up `pre-commit`

Once `section 2.1` is complete, run the following command to setup [`pre-commit`](https://pre-commit.com)

```bash
$ poetry run pre-commit install
```

This aforementioned command installs the hooks (functions / tools) that before a git commit is made. These tools could be code formatting or type checking etc. that help maintain a consistent codebase.

### 3. Making your changes

Make the necessary changes to the required files on the custom branch that was created earlier.

**NOTE:** Don't use the same branch again after it has been merged using a Pull Request. Create a new branch for working on a new issue.

### 4. Check that your code works

To ensure that the changes to the codebase do not break any other functionality and also the new tests do work, run the following command

```bash
$ poetry run pytest -vv tests
```

**NOTE:**
1. Run this commands from the top level of the `anton` repo (i.e. the same directory that contains the `pyproject.toml` file).
2. Ensure there are no failing tests. `pre-commit` does not allow to create a commit if the checks fail.


### 5. Format your code (**Run these commands in your custom branch**)

Add the files that have been changed/added to the index and call the pre-commit runner to format the files.

Add the files back to the index incase the tools like `black` or `isort` make any changes.

Some errors pointed by `mypy` and `pytest` will need manual resolving.

```bash
$ pre-commit run --verbose  # Runs multiple checks and formats the code.
```

### 6. Commit your changes (**Run these commands in your custom branch**)

When `pre-commit` runs successfully, the files can be committed.

```bash
$ git commit -m "A message describing your commit"
```

**NOTE:** It is recommended to fetch and rebase the local repository with the latest changes from the `upstream` remote at this point. Refer to section `1.4` for that.

Push these changes to **your fork** with the following command:

```bash
$ git push origin feature/<small_description_of_the_feature>
```

### 7. Make a pull request

Make a Pull Request to implement your changes on the main repository [here](https://github.com/karthikrangasai/anton/pulls).

To do so, click "New Pull Request". Then, choose your branch from your fork to push into "base:master".

When opening a PR, please link the [issue](https://github.com/karthikrangasai/anton/issues) corresponding to your feature using [closing keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) in the PR's description, e.g. `Resolves #23`.
