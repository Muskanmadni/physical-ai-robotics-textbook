---
id: "003"
title: "Remove-Logo-And-Blog-From-Header"
stage: "refactor"
date: "2025-12-06"
model: "Qwen Code"
feature: "001-textbook-project-structure"
branch: "main"
user: "user"
command: "edit docusaurus.config.js"
labels: ["docusaurus", "ui", "navigation", "refactor"]
spec: null
ticket: null
adr: null
pr: null
files:
  - "textbook/docusaurus.config.js"
tests: []
---

# Remove Logo And Blog From Header

## PROMPT_TEXT

```
in docusarus header logo remove logo image and blog
```

User requested to remove the logo image and blog link from the Docusaurus header.

## RESPONSE_TEXT

I have successfully removed both the logo image and blog link from the Docusaurus header by making the following changes to the docusaurus.config.js file:

1. Removed the `logo` property from the navbar configuration, which was displaying the logo image
2. Removed the blog entry `{to: '/blog', label: 'Blog', position: 'left'}` from the navbar items array
3. Disabled the blog functionality in the presets by setting `blog: false`
4. Removed the blog link from the footer section as well

The header now only contains:
- Title: 'Physical AI & Humanoid Robotics'
- Textbook navigation link
- Chat Assistant link
- Admin link
- GitHub link

These changes simplify the header navigation as requested by the user.

## OUTCOME

Successfully removed the logo image and blog link from the Docusaurus header. The site now has a cleaner navigation without the logo and blog link.