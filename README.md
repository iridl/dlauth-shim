# dlauth-shim

This is a wsgi service that implements the dlauth side of the ingrid<-->dlauth authorization protocol. Whereas dlauth includes its own authentication and authorization mechanisms, as well as user management and administration workflows, dlauth-shim delegates those responsibilities to external services such as PAM, Ory Kratos, or Keycloak.

## Creating a conda environment containing this project's dependencies

```
conda create -n dlauth-shim --file conda-linux-64.lock
```
(substituting osx or win for linux as appropriate)

You don't need to install conda-lock for this.

Note that the command is `conda create`, not `conda env create`. Both exist, and they're different :-(


## Adding or removing dependencies

Edit `environment.yml` and/or `environment-dev.yml`, then regenerate the lock files as follows:
```
conda-lock lock -f environment.yml -f environment-dev.yml
conda-lock render
```


