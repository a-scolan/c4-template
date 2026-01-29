# Tutorial: Your First CI/CD Pipeline

**Learning Goal**: Create and execute your first automated pipeline using Forgejo Actions.

**Time Required**: 20 minutes  
**Prerequisites**: 
- Completed [Tutorial 01: Onboarding](01-onboarding-developer.md)
- Have a repository on Dev-Forge (we'll use `hello-devforge` from Tutorial 01)

---

## What You'll Learn

By the end of this tutorial, you will have:
- Created a Forgejo Actions workflow file
- Triggered an automated pipeline
- Viewed pipeline execution logs
- Understood the basic structure of a CI/CD workflow

This tutorial introduces CI/CD concepts through hands-on practice. Every step will produce visible results you can verify.

---

## Step 1: Understand Forgejo Actions

Forgejo Actions is Dev-Forge's built-in CI/CD system. It automatically runs tasks when you push code, such as:
- Running tests
- Building applications
- Deploying to environments
- Checking code quality

Workflows are defined in YAML files stored in your repository under `.forgejo/workflows/`.

**You are** about to create your first workflow file.

---

## Step 2: Create the Workflow Directory

In your terminal, navigate to your `hello-devforge` repository:

```bash
cd ~/projects/hello-devforge
```

Create the workflow directory structure:

```bash
mkdir -p .forgejo/workflows
```

**You have** created the standard location where Forgejo looks for automation definitions.

---

## Step 3: Create Your First Workflow

Create a new workflow file:

```bash
nano .forgejo/workflows/hello.yml
```

Copy and paste this workflow definition:

```yaml
name: Hello Workflow

on:
  push:
    branches:
      - main

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Say hello
        run: echo "Hello from Forgejo Actions!"
      
      - name: Show files
        run: ls -la
      
      - name: Display hello.txt
        run: cat hello.txt
```

Save and exit (in nano: `Ctrl+X`, then `Y`, then `Enter`).

**Notice** the structure:
- **name**: Human-readable workflow name
- **on**: Trigger condition (runs on pushes to `main` branch)
- **jobs**: One or more jobs to execute
- **steps**: Individual commands within a job

---

## Step 4: Commit and Push the Workflow

Add the new workflow file to Git:

```bash
git add .forgejo/workflows/hello.yml
```

Commit the workflow:

```bash
git commit -m "Add first CI/CD workflow"
```

Push to Dev-Forge:

```bash
git push origin main
```

**You have** just triggered your first automated pipeline! The push to `main` branch activates the workflow.

---

## Step 5: View the Pipeline Execution

Open your repository in Forgejo:

```
https://forge.yourcompany.internal/yourname/hello-devforge
```

Click on the **"Actions"** tab in the repository navigation.

**You'll see** your workflow run listed with:
- Workflow name: "Hello Workflow"
- Commit message: "Add first CI/CD workflow"
- Status indicator (⏳ running, ✅ success, or ❌ failed)

Click on the workflow run to see details.

---

## Step 6: Explore the Logs

In the workflow run details page:

1. **You'll see** the `greet` job listed
2. Click on the `greet` job to expand it
3. **Notice** each step from your workflow file:
   - "Checkout code"
   - "Say hello"
   - "Show files"
   - "Display hello.txt"

Click on the **"Say hello"** step.

**You'll see** the output:
```
Hello from Forgejo Actions!
```

Click on **"Display hello.txt"** step.

**You'll see** the contents:
```
Hello from Dev-Forge!
```

**You have** successfully executed and monitored an automated workflow.

---

## Step 7: Trigger the Workflow Again

Make another small change to see the pipeline run again:

```bash
echo "Pipeline test" >> hello.txt
```

Commit and push:

```bash
git add hello.txt
git commit -m "Test pipeline trigger"
git push origin main
```

Return to the **Actions** tab in Forgejo.

**Notice** a second workflow run has started automatically. This demonstrates that workflows trigger on every push to `main`.

---

## Step 8: Understand What Happened

Let's review what the workflow does:

1. **Forgejo detected** your push to the `main` branch
2. **A runner** (containerized execution environment) was assigned
3. **Checkout step** cloned your repository into the runner
4. **Custom steps** executed your commands sequentially
5. **Logs** captured all output for debugging
6. **Status** reported success or failure back to Forgejo

The entire process happened automatically without manual intervention.

---

## What You've Achieved

✅ Created a Forgejo Actions workflow file  
✅ Triggered CI/CD automatically on code push  
✅ Viewed real-time execution logs  
✅ Understood the workflow → runner → execution model  
✅ Verified automated repetition on subsequent pushes

You now understand the foundation of CI/CD automation on Dev-Forge.

---

## Next Steps

Now that you understand basic pipelines, you can:
- **Expand your workflow**: Add testing, linting, or building steps specific to your technology
- **Learn advanced features**: See the [Configure Runners How-To](../how-to/configure-runners.md) for scaling strategies
- **Implement real CI/CD**: Check the [Forgejo Configuration Reference](../reference/forgejo-config.md) for available runner options

---

## Common Patterns to Explore

Once you're comfortable, you can expand your workflow to include:

**Testing** (example for Python):
```yaml
- name: Run tests
  run: |
    pip install pytest
    pytest tests/
```

**Building** (example for Node.js):
```yaml
- name: Build application
  run: |
    npm install
    npm run build
```

**Deploying** (example using SSH):
```yaml
- name: Deploy to staging
  run: |
    scp -r ./build user@staging:/var/www/app
```

These examples demonstrate the technology-agnostic nature of Dev-Forge—use any language or framework.

---

## Troubleshooting

**Problem**: Workflow doesn't appear in Actions tab  
**Solution**: Verify the file is in `.forgejo/workflows/` (note the dot prefix) and has `.yml` or `.yaml` extension

**Problem**: Pipeline fails immediately  
**Solution**: Check the logs for YAML syntax errors. Use a YAML validator online to verify your workflow file

**Problem**: "No runners available"  
**Solution**: Contact your administrator—runner pool may need scaling (see ADR-0002 for architecture details)

**Problem**: Steps run but don't produce expected output  
**Solution**: Check that commands work in your local terminal first, then replicate exactly in workflow steps
