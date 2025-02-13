# About 📚
NxtGen's hub for weekly knowledge sharing, AI innovation, and collaboration, featuring LangChain, LLMs, and a range of other AI tools and techniques, combined with human insight and expertise to foster learning, growth, and innovation.

# Contents 📝
1. [Introduction 📚](#introduction)
2. [Overview 🤖](#overview)
   * [Query Answering System 💬](#query-answering-system)
3. [TODO for Contributors 📝](#todo-for-contributors)
4. [Adding a Submodule to the Repository 📁](#adding-a-submodule-to-the-repository)
5. [Modifying Submodule's Tracked Branch](#modifying-submodules-tracked-branch)
6. [Updating Submodule to Track Latest Commit](#updating-submodule-to-track-latest-commit)

# Introduction 📚
NxtGen's hub for weekly knowledge sharing, AI innovation, and collaboration is designed to bring together experts and enthusiasts in the field of artificial intelligence. By featuring LangChain, LLMs, and a range of other AI tools and techniques, combined with human insight and expertise to foster learning, growth, and innovation.

# Overview 🤖
Our repository contains several submodules, each focused on a specific aspect of AI research and development.

## Query Answering System 💬
A conversational AI system that takes documents and user queries, refines them, retrieves relevant documents, and generates answers using NLP techniques and LangChain framework. For more information, visit the [Query Answering System repository](https://github.com/NxtGen-AI-Public/query-answering-system).

# TODO for Contributors 📝
- [ ] Request creation of a new submodule repository
- [ ] Clone the new submodule repository and push initial files to it, ensuring that:
  - [ ] The code has no warnings
  - [ ] The code has no linter errors (follows PEP 8 or other relevant guidelines)
  - [ ] The code is thoroughly tested before being pushed
  - [ ] The code follows good coding practice principles, such as:
    - Single Responsibility Principle (SRP)
    - Separation of Concerns (SoC)
    - Don't Repeat Yourself (DRY)
    - KISS (Keep it Simple, Stupid)
- [ ] Modify the contents of the [Overview 🤖](#overview) section in this README.md file to include information about the new submodule
- [ ] Ensure that each submodule (a.k.a subrepo) has a clear and concise `README.md` file with the following sections:
  - Introduction: A brief overview of the submodule's purpose and functionality
    - **Include a link to the parent module/repo (https://github.com/NxtGen-AI-Public/NxtGen-OnTopic) to provide context and facilitate navigation**
  - Installation: Step-by-step instructions for installing and setting up the submodule
  - Usage: Examples and guidelines for using the submodule
  - System Overview: A high-level description of the submodule's architecture and components
  - Other relevant headings: Such as troubleshooting, contributing, or licensing information, as applicable to the submodule

# Adding a Submodule to the Repository 📁
For more information on adding submodules to GitHub repositories, visit: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-add-submodules-to-GitHub-repos

## Prerequisites 📝
* The submodule repository must be up and running under NxtGen-AI-Public's account
* Ownership of the submodule repository is necessary for linking submodules and parent modules

## Instructions 📚
To add a submodule to the NxtGen-OnTopic repository, follow these steps:
1. **Create a GitHub repository**: Create a new GitHub repository under the `NxtGen-AI-Public` account. This is necessary because submodules must belong to the same owner as the parent repository.
2. **Clone the submodule repository**: Run `git submodule add https://github.com/NxtGen-AI-Public/your-submodule-repo` (replace with your submodule repository URL)
3. **Check the status**: Run `git status`
4. **Stage changes**: Run `git add .`
5. **Commit changes**: Run `git commit -m "Add GitHub submodule"`
6. **Push changes**: Run `git push origin`

# Modifying Submodule Tracked Branch 📁
Git submodule objects are special kinds of Git objects, and **they hold the SHA information for a specific commit**, **they do not track the branch and update as and when any commit is pushed into the branch**, they have the latest changes of the latest commit at the time of adding the submodule. For more information on updating submodules to track different branches in GitHub repositories, visit: https://stackoverflow.com/a/18797720.

## Prerequisites 📝
* The submodule repository must be up and running under NxtGen-AI-Public's account
* Ownership of the submodule repository is necessary for linking submodules and parent modules
* A submodule must already exist in the repository

## Instructions 📚
To update a submodule to track a different branch, follow these steps:
1. **Update the submodule's configuration to track the new branch**: 
   - Manually edit the `.gitmodules` file in the superproject directory: add or modify the line `branch = main` (replace with your desired branch) under the `[submodule "path/to/your/submodule"]` section.
   - Alternatively, run `git config -f .gitmodules submodule.path/to/your/submodule.branch main` from the superproject root
2. **Commit the changes in the `.gitmodules` file**: Run `git add .gitmodules` and then `git commit -m "Updated submodule to track main branch"`
3. **Push changes**: Run `git push origin`

# Updating Submodule to Track Latest Commit 📁
Git submodule objects are special kinds of Git objects, and **they hold the SHA information for a specific commit**, **they do not track the branch and update as and when any commit is pushed into the branch**, they have the latest changes of the latest commit at the time of adding the submodule. For more information on updating submodules to track different branches in GitHub repositories, visit: https://stackoverflow.com/a/18797720.

## Prerequisites 📝
* The submodule repository must be up and running under NxtGen-AI-Public's account
* Ownership of the submodule repository is necessary for linking submodules and parent modules
* A submodule must already exist in the repository

## Instructions 📚
To update a submodule follow these steps:
1. **Update the submodule's configuration to track the newest commit**: Run `git submodule update --remote`
2. **Commit the changes in the `.gitmodules` file**: Run `git add .gitmodules` and then `git commit -m "Updated submodules to track latest commits"`
3. **Push changes**: Run `git push origin`
