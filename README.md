# Git Deployer

A utility for automated deployment of generated static websites (documentation, help guides, etc.) using Git.

## Advantages

- **Simplicity**: Deploy with a single command.
- **Reliability**: Uses proven Git mechanisms.
- **Versatility**: Suitable for any hosting service that supports Git repositories (GitHub Pages, GitLab Pages, your own server, etc.).
- **Incremental Deployment**: Only modified files are transferred.

## Installation

```bash
python -m pip install git+https://github.com/optinosft/git-deployer.git
```

## How Does It Work?

1. You generate a static site (for example, using Docusaurus, Sphinx, Jekyll, MkDocs).
2. Initialize a Git repository in the directory containing the generated site (e.g., `_build/html`).

Example:

```bash
cd _build/html
git init
```

3. Using Git, add a new remote repository and specify which remote branch your local branch should track.

Example:

```bash
git remote add origin https://github.com/owner/repository.git 
git branch --set-upstream-to origin/main main
```

4. Run `deploy`.

```bash
deploy .
```

5. The utility publishes the files to the remote repository.

To publish, Git Deployer executes the following commands:

```bash
git add .
git commit -m "Site updated: %Y-%m-%d %H:%M:%S"
git push
```

`%Y-%m-%d %H:%M:%S` will be replaced by the current date and time, ex.: `2025-09-29 10:44:15`

## Usage

```bash
deploy _build/html
```
