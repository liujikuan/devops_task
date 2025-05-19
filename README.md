- # ✅ Overview #

    This guide walks you through:

    - Setting up Azure infrastructure

    - Creating and configuring a GitHub Actions workflow

    - Deploying and running a Python app on Azure App Service via CI/CD

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
  
     (the publish profile will be used to deploy a docker container to the Azure app service.)
  
  
  Go to “Overview” page of your App Service, look for and click the "Download publish profile" button near the top.
  It will download an .PublishSettings file (this is the publish profile).
  
  
  Copy the contents of this file into GitHub secret `AZURE_WEBAPP_PUBLISH_PROFILE` later.
  
  
  
  
  # 🔐 Set up CI/CD pipelines
  
  ## 1. Set Up GitHub Environment Secrets
  
    In the GitHub repo:
  
    Navigate to `Settings` -> `Environments`
  
    Create a new environment (e.g., prod)
  
    Add the following secrets to that environment:
  
    > AZURE_WEBAPP_PUBLISH_PROFILE: <The content of publish-profile.xml>
  
  ## 2. Prepare workflow files
  
    The pipeline is structured in three jobs:
  
    - build: Builds, test and pushes the Docker image to GitHub Container Registry (GHCR)
      - Build and run a Docker container in a GitHub runner 
      - Lint with flake8
      - Run functional tests with Pytest
      - Run Trivy vulnerability scanner
      - Log in to and push the Docker Image to GitHub Container Registry
    - test_CodeQL: Runs CodeQL static analysis
    - deploy: Deploys the image to Azure Web App
  
  ## 3.  Set up a personal access token 
  
      1. Navigate to "Settings" -> "Developer settings" -> "Personal Access Tokens" -> "Fine-grained tokens".
  
    Ensure the PAT includes these permissions:
  
  - **Actions**: Read & Write
  
  - **Contents**: Read & Write
  
  - **Workflows**: Read & Write
  
  ##  4. 📤Push code to repo
  
  In a local repo, run the following  command:
  
    - git branch -M main
    - git remote add origin https://<your_github_id>:<your_access_token>@github.com/<your_github_org>/<your_github_repo>.git
    - git checkout -b develop
    - git push --set-upstream origin develop
  
  ## 5. change the default branch(optional)
  
   In the GitHub repo:
  
  1. Navigate to `Settings` -> `General`
  2. Under "Default branch", click the `bidirectional arrow` button to the right of the default branch name . 
  3. Switch default branch to the `main` branch
  
  ## 6. Set up branch protection rules(optional)
  
    ✅ Steps to Forbid Merging When Checks Fail:
  
  - Go to your repository on GitHub.
    Click on `Settings` →  `Rules` -> `Rulesets`,  then  `New ruleset` -> `New branch ruleset`.
    Set the branch naming pattern (i.e., main).
  
  - Enable the following options:
    ✅ Require a pull request before merging
    ✅ Require status checks to pass before merging
    ✅ Select the specific checks (e.g., build, test, lint) that must pass.
  
    Click Create or Save changes.
  
  
  
  
  
  ## ✅ Tests
  
  CLI testing tools:
  
  - flake8(linter)
  - pytest(functional test)
  
  
  
  _Once the deployment completes, you can find the live app’s URL in two ways:_
  
  - in the **"Summary"**  section at a GitHub Actions workflow run page.
  - By visiting the **Deployments** tab at:
     `https://github.com/<your_github_id>/<your_github_repo>/deployments`,
     then selecting the relevant environment (e.g., `prod`) to view the latest deployment details and URL.
  
  
