# Reporting and credentials

Never commit API keys or route data containing private addresses. Use `GOOGLE_MAPS_API_KEY` in the process environment. An API key was present in the original repository history; the owner should revoke or rotate it in Google Cloud and restrict the replacement to the required API. Removing it from the current files does not remove it from old commits.

Live routing is an explicit operation and can incur provider charges. Offline examples and tests must not make paid API requests. Report security problems privately to the repository owner.
