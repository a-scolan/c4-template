Run the pull only for the template-managed generic areas:

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

Use `--squash` because it keeps your project history cleaner and more compact. Instead of importing the full upstream commit graph for each subtree update, it records the pulled template changes as a smaller, easier-to-review change in your repository.

This is the right scope because `.github` and `projects/shared` are generic template content; project-specific files should not be pulled this way.
