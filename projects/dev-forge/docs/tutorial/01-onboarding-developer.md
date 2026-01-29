# Tutorial: Onboarding as a Developer

**Learning Goal**: Create your first Git repository on the Dev-Forge platform and make your initial commit.

**Time Required**: 15 minutes  
**Prerequisites**: Dev-Forge account provisioned by your administrator

---

## What You'll Learn

By the end of this tutorial, you will have:
- Accessed the Forgejo web interface
- Created a new Git repository
- Configured your local Git client
- Made your first commit and pushed to Dev-Forge

This tutorial guides you through the complete workflow step by step. Follow each instruction carefully—everything here is designed to work reliably.

---

## Step 1: Access Forgejo

Open your web browser and navigate to your Dev-Forge instance:

```
https://forge.yourcompany.internal
```

**You'll see** the Forgejo login page.

Log in with the credentials provided by your administrator:
- **Username**: Your company username (usually your email prefix)
- **Password**: Your initial password (you'll be prompted to change it on first login)

**Notice** the dashboard that appears after login, showing recent activity and your repositories.

---

## Step 2: Create Your First Repository

From the dashboard, click the **"+"** button in the top-right corner, then select **"New Repository"**.

Fill in the repository details:

- **Owner**: Select yourself (your username should be pre-selected)
- **Repository Name**: `hello-devforge`
- **Description**: "My first Dev-Forge repository"
- **Visibility**: 
  - ✅ **Private** (recommended for this tutorial)
- **Initialize Repository**:
  - ✅ Check "Add a README file"
  - ✅ Check "Add .gitignore" and select **"None"** from the dropdown
  - ⬜ Leave "Add a licence" unchecked for now

Click **"Create Repository"**.

**You'll see** your new repository page with a single README.md file listed.

---

## Step 3: Configure Your Local Git Client

Open your terminal or command prompt.

First, tell Git who you are (if you haven't already done this):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

**You have** now configured your Git identity. Every commit you make will include this information.

---

## Step 4: Clone the Repository

On the Forgejo repository page, find the **"Clone"** button. Click it and copy the **HTTPS** URL. It will look like:

```
https://forge.yourcompany.internal/yourname/hello-devforge.git
```

In your terminal, navigate to where you want to store your projects:

```bash
cd ~/projects
```

Clone your repository:

```bash
git clone https://forge.yourcompany.internal/yourname/hello-devforge.git
```

When prompted for credentials:
- **Username**: Your Forgejo username
- **Password**: Your Forgejo password (or personal access token if configured)

Enter the repository directory:

```bash
cd hello-devforge
```

**You'll see** the repository contents (just README.md at this point) when you run:

```bash
ls
```

---

## Step 5: Make Your First Change

Create a new file to demonstrate a basic workflow:

```bash
echo "Hello from Dev-Forge!" > hello.txt
```

Check the status of your repository:

```bash
git status
```

**Notice** that Git shows `hello.txt` as an untracked file.

Add the file to the staging area:

```bash
git add hello.txt
```

Check status again:

```bash
git status
```

**You'll see** that `hello.txt` is now ready to be committed (shown in green).

---

## Step 6: Commit and Push

Create your first commit:

```bash
git commit -m "Add hello.txt with greeting message"
```

**You have** now recorded your change in local Git history.

Push your commit to Dev-Forge:

```bash
git push origin main
```

**You'll see** output showing the upload progress and confirmation that the branch was updated.

---

## Step 7: Verify in Forgejo

Return to your web browser and refresh the repository page:

```
https://forge.yourcompany.internal/yourname/hello-devforge
```

**Notice** that:
- Your `hello.txt` file now appears in the file list
- The commit message "Add hello.txt with greeting message" is shown
- The commit count has increased to 2

Click on the **"Commits"** tab to see the full commit history.

---

## What You've Achieved

✅ Accessed Forgejo and created a repository  
✅ Configured your local Git environment  
✅ Cloned a repository from Dev-Forge  
✅ Made a local change and committed it  
✅ Pushed your work to the platform  
✅ Verified your changes in the web interface

You now have a complete development workflow from local machine to Dev-Forge.

---

## Next Steps

Now that you've mastered the basics, you're ready to:
- **Continue learning**: Follow the [First Pipeline tutorial](02-first-pipeline.md) to set up CI/CD
- **Work with real code**: Create a new repository for your actual project
- **Collaborate**: Invite team members and learn about merge requests (see How-To guides)

---

## Troubleshooting

**Problem**: Git asks for username/password on every push  
**Solution**: Configure Git credential storage:
```bash
git config --global credential.helper store
```

**Problem**: Cannot connect to forge.yourcompany.internal  
**Solution**: Verify you're on the company network or VPN

**Problem**: "Permission denied" when pushing  
**Solution**: Verify your account has write access to the repository (contact your administrator)
