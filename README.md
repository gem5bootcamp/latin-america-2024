# gem5 bootcamp environment

This repository has been designed for use in gem5 tutorials.
It contains:

- The [slides](slides/) that are used in the bootcamp. The slides are rendered with [Marp](https://marp.app/).
- The [materials](materials/) directory contains templates code and completed code examples of how to use gem5.
- The [web](web/) directory enables the bootcamp to be hosted on GitHub pages.
- The [gem5](gem5/) directory is a submodule that contains the gem5 source code and [gem5-resources](gem5-resources/) is a submodule for gem5-resources.
  - These will usually point to the latest stable release of gem5.

To use this repository, you will need to have a GitHub account and a Codespaces subscription.
If you are using this repository as part of the official gem5 bootcamp, you will be provided with a codespace subscription.

To view the bootcamp slides, visit the [gem5 bootcamp website](https://gem5bootcamp.github.io/latin-america-2024/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to contribute to the gem5 bootcamp.

## Using this repository

> **Note:** 'gem5' and 'gem5-resources' are submodules though the [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) file specifies that a `git submodule update --init --recursive` command is executed when the Codespace Docker container is created.
>
> **Note:** The `.devcontainer/on_create.sh` script is executed the first time the codespace is created.
> This will pre-download much of the resources (disk images, etc.) that are used in the gem5 tutorials.
> It can take a while to do this.
> A pre-built devcontainer is set up for the bootcamp and should be used to avoid this delay.

The container used by Codespaces is built from [Dockerfile](gem5/util/dockerfiles/devcontainer/Dockerfile).
It contains:

- All gem5 dependencies (inc. optional dependencies).
- Prebuilt gem5 binaries:
  - `/usr/local/bin/gem5-chi` (`/usr/local/bin/gem5`) (gem5 ALL ISAs with CHI protocol)
  - `/usr/local/bin/gem5-mesi` (default gem5 ALL build with MESI_Two_Level)
  - `/usr/local/bin/gem5-vega` (x86-only with GPU protocol)
- A RISCV64 and an AARCH64 GNU cross-compiler:
  - RISCV64 GNU cross-compiler found in `/opt/cross-compiler/riscv64-linux/`.
  - AARCH64 GNU cross-compiler found in `/opt/cross-compiler/aarch64-linux/`.

### Beginners' example

The following can be used within the Codespace container to run a basic gem5 simulation straight away:

```sh
gem5 gem5/configs/example/gem5_library/arm-hello.py
```

This will execute a "Hello world!" program inside a simulated ARM system.

### Updating submodules

In this project we have two submodules: 'gem5' and 'gem5-resources'.
These are automatically obtained when the codespaces is initialized.
At the time of writing the 'gem5' directory is checked out to the stable branch at v24.0.0.0.
The 'gem5-resources' repository is checked out to revision '97532302', which should contain resources with known compatibility with gem5 v24.0.

To update the git submodules to be in-sync with their remote origins (that hosted on our [GitHub](https://github.com/gem5/gem5)), execute the following command:

```sh
git submodule sync   # Only needed if submodule remotes changed
git submodule update --remote
```

This repository may be updated to these in-sync submodules by running the following (this assumes you have correct permissions to do so):

```sh
git add gem5 gem5-resources
git commit -m "git submodules updated"
git push
```

## Launching a new version of the bootcamp

Steps to create a new instance of the bootcamp.

1. Create a new repo
2. Update your local repo with a new remote: `git remote add <name> git@github.com:gem5bootcamp/<repo>.git`
3. Create a new branch: `git checkout -b <name>`
4. Update repo to enable github actions. Use `https://github.com/gem5bootcamp/<repo>/actions`
5. Push new branch to new repo main: `git push <name> <name>:main`
6. Track the right upstream: `git branch --set-upstream-to=<name>/main`
7. Update [splash page](web/index.html)
8. Update [Introduction](slides/01-Introduction/00-introduction-to-bootcamp.md)
9. Enable github pages to "deploy from branch" `gh-pages`. Use `https://github.com/gem5bootcamp/<repo>/settings/pages`
