# Nicolas Martinez — personal site

Standalone static-site repository for Nicolas Martinez's personal website.

This is Nicolas Martinez's standalone website repository, kept intentionally simple:
- `index.html` — main landing page
- `styles.css` — site styles
- no build step
- no framework
- ready for GitHub + Cloudflare Pages later

## Local preview
Open `index.html` directly in a browser, or serve the folder with any simple static server.

Example:
```bash
python3 -m http.server 8000
```
Then open <http://localhost:8000>.

## Deploy to Cloudflare Pages
1. Push this folder to its own GitHub repository.
2. In Cloudflare Pages, create a new project and connect that repo.
3. Use these settings:
   - **Framework preset:** None
   - **Build command:** leave empty
   - **Build output directory:** `/`
4. Deploy.

Because this is a plain static site, Cloudflare Pages can serve it directly without a build process.

## Notes
- Source content was preserved from the isolated Nicolas Martinez site files.
- The preview-only artifact from the source folder was intentionally not copied.
