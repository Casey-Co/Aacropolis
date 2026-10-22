# Aacropolis Homes — GitHub Pages

Responsive static recreation of the publicly accessible Aacropolis Homes website, including its hidden content pages, captured October 22, 2026.

The site runs directly from the repository root. It uses standard HTML, CSS and JavaScript, with no Node installation, framework, API key or build service required. GitHub Pages should serve the `main` branch, root directory.

## Editing

- Layout and styling: `assets/site.css`.
- Shared navigation, photo viewer and location selector: `assets/site.js`.
- Page content and captured source copy: `tools/content.json`.
- Shared HTML templates and page assembly: `tools/build.py`.
- After changing templates/content, run `python3 tools/build.py`, then `python3 tools/check.py` and commit the regenerated HTML.
- Photos and PDF brochures are stored under `assets/`.
- Each page also has an `index.html` so nested routes work on GitHub Pages. Previous `.html` links redirect to the corresponding page.

## Included

Main home page, show homes, about, full gallery, our homes, quick possession, all nine blog articles, nine-step process, referral promotions, video tours, digital welcome, Welcome Home, Meet the Team, Edmonton Communities and STEF TESTER HOMEPAGE. All hidden content pages are accessible from navigation or All Pages. Friendly aliases are also included.

## Existing service dependencies

GitHub Pages does not run a server or copy Wix databases. Booking, tour scheduling, referral registrations, member accounts and checkout links continue to the existing Aacropolis/Wix service. These pages use an explicit working-service link rather than a nonfunctional form or a false success message. Do not cancel the original service until those backend functions have been replaced. The community map uses Google Maps. See `MIGRATION-NOTES.md` for source issues and exclusions.

The original Next.js draft has been replaced by this buildless site. The prior version remains available in Git history.
