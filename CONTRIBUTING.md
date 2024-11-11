---
title: Guidelines for creating content
author: Jason Lowe-Power
---

This file describes how to create content for the bootcamp and contribute to this repository.

## Creating slides

Slides go in the `slides/` directory. Each slide deck is a markdown file.
They are written using [Marp](https://marp.app/), a Markdown-based slide design tool.
We chose to use Markdown for slides to make it easier for us to update the code in the slides as gem5 changes and for the participants to copy-paste code.

To use Marp, we encourage you to install the [VS Code extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode), which should be automatically installed if you're using the codespaces devcontainer.
With the VS Code extension installed, when you open one of the slide decks (e.g., [Getting started](slides/02-Using gem5/00-getting-started.md)), you can click on the preview button in the upper right to view the slides.
Also, you can use the Marp extension to save the slides as HTML or PDF.

For using the Marp command line, you can use the following command (pass in the file to convert).
You should run this command from the root of the repository.
Note: The local paths for the css file and the markdown don't work great. YMMV.

```sh
docker run --rm -v $PWD:/home/marp/app/ -e MARP_USER=$UID:$GID -e LANG=$LANG marpteam/marp-cli <markdown file>
```

### Testing changes locally

Below is a one-liner that builds the website the same way as via GitHub Actions.
Once you run this, you can run a local webserver in `web/` to view the slides.

```sh
docker run --rm -v $PWD:/home/marp/app/ -e MARP_USER=$UID:$GID -e LANG=$LANG marpteam/marp-cli --html -o web/slides/ -I slides -c .vscode/settings.json && find slides \( -name "*.png" -or -name "*.svg" -or -name "*.css" -or -name "*.jpg" \) -exec sh -c 'mkdir -p web/"$(dirname "{}")"' \; -exec cp {} web/{} \;
```

To view the slides:

```sh
python -m http.server 8000
```

### Writing content

The first slide should be the title slide and should have the title and author in the yaml frontmatter.
The title slide should be a "title" slide `<!-- _class: title -->`.

It is encouraged to have a outline slide at the beginning of the slide deck.

Each slide should be separated by `---`, and each slide's title should be `h2` (`##`).

### Naming conventions

Each slide deck is numbered so that it appears in order in the file system.
The slide deck should be named with the format `XX-<name>.md`, where `XX` is the number of the slide deck.
The name should be short and easy to remember.

### Adding diagrams

To add diagrams, you can use the [draw.io VS Code extension](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio).
**You are strongly encouraged to use svg images for diagrams.**

After installing the extension, create a file with the name "\<name\>.drawio.png" and open it in VS Code.
Make sure you create a directory for each slide deck with its images.
You can then embed the image in the slide with the following markdown.

```md
![<description of the image>](<current slide name>-imgs/<name>.drawio.svg)
```

If you need to have images on the left or right use `[bg left]` and `[bg right]` respectively.

Make sure to add a description of the image in the alt text.

### Slide Layouts

To use a different layout, you specify a class in the markdown file.

```md
<!-- _class: <layout> -->
```

Here are some of the available layouts:

- `title`: Title slide
- `two-col`: Two columns. To split the slide into two columns, use `###` (heading 3) to create a new column.
- `center-image`: Centers images horizontally
- `code-XX-percent`: Reduces font-size in code blocks. Valid values for `XX` are any of `[50, 60, 70, 80]`.
- `no-logo`: Removes the bottom logo.
- `logo-left`: Positions the bottom logo further to the left. Useful when using `bg right` images that cover the logo.

### Style rules

- INSTALL THE [MARKDOWN LINT EXTENSION IN VS CODE](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) TO HELP WITH FORMATTING.
- Use `---` to separate slides.
- The first slide should be a "title" slide `<!-- _class: title -->`.
- The titles of all slides should be heading 2 `##`
- Code should be at most 65 characters wide.
- Always put links to the resources when referencing.

#### Linking to materials and slides

When linking to materials, use the following format:

```md
[path relative to the root of the repo](path relative to the current file)
```

Use the relative path from the current file.

> **Note**: The above is currently broken. We need to revisit this.

## Creating materials

Materials go in the `materials/` directory.
Materials are code examples, code templates, etc. which support the learning of students in the bootcamp.

Each slide deck should have its own directory in the materials directory which follows the same naming convention as the slide deck.
For example, the materials for the slide deck `02-Using gem5` should be in the directory `materials/02-Using gem5`.

Each slide deck directory should contain the following:

- `completed/`: A directory containing the completed code examples.

Ensure that the completed codes always has a docstring at the top of the file explaining what the code does, how to run it, and what the expected output is.
In this docstring, there should be a gem5 command which can be used to run the code.
The gem5 command should always begin with a `$` and on the next line you can write the expected result.
You can include `...` in the result.
This should be tested before committing the code.
You can test each script with `materials/test-materials.py <path>`.

For example:

```python
"""
One of the most basic gem5 scripts you can write.

This boots linux (just the kernel) and exits. However, we will only run it for
20 ms to save time.

This takes just a minute or so to run.

$ gem5 basic.py
gem5 Simulator System.  https://www.gem5.org
...
info: Entering event queue @ 0.  Starting simulation
"""
```

Note that when running examples, you should assume the students are in the directory with the example.
Otherwise, their paths will be littered with `m5out` directories.

## Committing changes to the repository

When you are ready to commit your changes, you should create a pull request.
This will allow others to review your changes and provide feedback.
It also ensures that the changes are synchronized.

To create a pull request, you should:

- Make sure you have a branch with your committed changes
- Push your branch to the repository
- Go to the repository on GitHub
- Click on the "Pull requests" tab
- Click on the "New pull request" button

## Improvement to make

- [ ] Can we possibly make it so that there's a button to copy the code examples?
- [ ] Fix the linking to materials and slides.

## To print the slides

```bash
find . -name "*.md" -exec pandoc {} -o {}.html --self-contained -c ../themes/print-style.css \;
```

## Suggestions for creating content

- Keep code snippets short
  - Each snippet should fit on a slide
  - A good rule of thumb is about 10 lines at most
  - You can have an example that spans multiple snippets
  - Talk about each code snippet on its own
- Keep the theory part short
- Think about ways to keep things interactive

Inspiration:

- [Learning gem5](https://www.gem5.org/documentation/learning_gem5/introduction/) and the [old version](http://learning.gem5.org/).
- [Standard library docs](https://www.gem5.org/documentation/gem5-stdlib/overview)

## How to provide/use code

- We are planning on using github codespaces.
- Put boilerplate in the template repo under `materials/`.

## Things that were effective at teaching

- Lots of template code and just leave empty the main point that you were trying to learn.
- Copying code from a book into the terminal and make minor modifications to see what happens.
- Small short code snippets to write.
- It's helpful to have a site map for the directory structure.
- Youtube videos writing the code live line-by-line and explaining things.
- Having a big project with a specific goal in mind which touches the things you want to learn.
- Listening to someone else's thought process while they are working on the problem
- Take working code and then break it to see what errors happen.
- Someone provides a library with APIs and you have to implement the APIs and it's tested heavily outside.
- Extend someone else's (simple) code with some specific goal in mind.
- Code under very specific constraints so that you don't get lost in the forest.
- Pair programming
- Taking the code and then pulling out the state machine / structure.
  - Build your own callgraphs
  - Use gdb in a working example
- The socratic method. Have them try something and then help them move toward the "best" solution.
- Make sure to point out how gem5 differs from real hardware. Gap between theory and model.
- Keywords: repeat many times and have a glossary.
- Focus on one module. Ignore the others except for the interfaces. **Write detailed comments/notes**
- Practice and do "it" yourself.
