# Legacy Django UI

This package preserves the original server-rendered Django interface for learning and comparison.

- `views.py` and `forms.py` handle ordinary HTML form submissions and Django session authentication.
- `templates/legacy_ui/` contains the original Django pages.
- `static/legacy_ui/` contains their CSS and JavaScript.
- `reference_screenshots/` preserves the original design screenshots; they are not served as runtime assets.
- `urls.py` keeps the original route names and paths working.

The Next.js application does not use these views or templates. It communicates with the separate Django REST/JWT modules in the parent `todo` package: `api_urls.py`, `api_views.py`, `serializers.py`, and the `auth_*` modules.
