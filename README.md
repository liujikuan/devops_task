- # ✅ Overview #
  This guide walks you through:

  - Creating and configuring a GitHub Actions workflow

  - Setting up Azure infrastructure

  - Deploying a Python app in a Docker container via CI/CD

  # 🔐 Set up CI/CD pipelines
  ## 1. prepare workflow files
  The pipeline is structured in three jobs:

  - build: Builds and pushes the Docker image to GitHub Container Registry (GHCR)

  - test_CodeQL: Runs CodeQL static analysis

  - deploy: Deploys the image to Azure Web App

  ## 2.  set up a personal access token 

  1. Navigate to "Settings" -> "Developer settings" -> "Personal Access Tokens" -> "Fine-grained tokens".

  Ensure the PAT includes these permissions:

- **Actions**: Read & Write
- **Contents**: Read & Write
- **Workflows**: Read & Write

  2. In a local repo, run the following  command:
  - git branch -M main
  - git remote set-url origin https://<your_github_id>:<your_access_token>@github.com/<your_github_org>/<your_github_repo>.git
  - git push --set-upstream origin main

  ## 3. Set Up GitHub Environment Secrets
  In the GitHub repo:

  Navigate to Settings > Environments

  Create a new environment (e.g., prod)

  Add the following secrets to that environment:

  > AZURE_WEBAPP_PUBLISH_PROFILE: The content of publish-profile.xml
    (the file will be able to be downloaded later)

  ## 4. Set up branch protection rules
  ✅ Steps to Forbid Merging When Checks Fail
  Go to your repository on GitHub.

  Click on Settings → then Branches in the left sidebar.

  Under "Rules" -> "Rulesets", , click "New ruleset" -> "New branch ruleset".

  Set the branch naming pattern (i.e., main).

  Enable the following options:

  ✅ Require status checks to pass before merging

  ✅ Select the specific checks (e.g., build, test, lint) that must pass.

  Click Create or Save changes.
  # Setting up Azure infrastructure
  ## Step 1: Create App Service Plan (Linux, not zone-redundant)
  ```bash
  az appservice plan create \
      --name python_cicd_demo_plan \
      --resource-group devops_task \
      --is-linux \
      --sku B1 
  ```

  ## Step 2: Create the Web App for Containers
  ```bash
  az webapp create \
      --name python-cicd-demo \
      --plan python_cicd_demo_plan \
      --resource-group devops_task \
  	--runtime "PYTHON:3.10"
  ```

  ## Step 3: Set Docker container image
  ```bash
  az webapp config container set \
    --name python-cicd-demo \
    --resource-group devops_task \
    --docker-registry-server-url https://ghcr.io \
    --docker-custom-image-name ghcr.io/liujikuan/python-demo:latest
  ```

  ## Step 4: Set the WEBSITES_PORT environment variable


  If your container listens on port `5000`, you must **map that internal port to port 80 in Azure App Service** using the `WEBSITES_PORT` application setting.

  #### 🔧 Steps via Azure Portal:

  1. Go to your **App Service > Settings > Environment variables**.
  2. Under **App Settings**, click **Add**:
     - **Name**: `WEBSITES_PORT`
     - **Value**: `5000`
  3. Click **Apply** and restart the App Service.

  #### 🔧 Steps via Azure Cli:
  ```bash
  az webapp config appsettings set \
    --name python-cicd-demo \
    --resource-group devops_task \
    --settings WEBSITES_PORT=5000
  ```

  ## Step 5 : Download publish profile manually
   (the publish profile will be used to deploy a docker container to the web app.)

  ```bash
  az webapp deployment list-publishing-profiles \
      --name python-cicd-demo \
      --resource-group devops_task \
      --output tsv > publish-profile.xml
  ```
  Copy the contents of this file into GitHub secret AZURE_WEBAPP_PUBLISH_PROFILE.


  # push code to repo

## 📤 Push Code to GitHub Repository

Make sure to push the following components:

- Application code (`app.py`, `test_app.py`)
- `Dockerfile`
- GitHub Actions workflow file (`.github/workflows/main.yml`)

The workflow is triggered by:

- Pushes to `feature-*`, `develop`, or `staging` branches
- Pull requests to `main`
- Manual runs via GitHub UI `workflow_dispatch`

---

## ✅ Health Check Endpoints

The Flask app exposes:

- `/` – Main endpoint: `Hello, world!`
- `/healthz` – Health check: Returns `200 OK`
