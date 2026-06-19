# Anaunim Interaction Manager

Anaunim is a local-first prototype for managing social interactions across Instagram, Facebook, TikTok, LinkedIn, and X.

The app now has two layers:

- A browser dashboard in `index.html`, `styles.css`, and `app.js`.
- A zero-dependency Python backend in `backend/server.py` with SQLite persistence, provider adapters, mock sync, queued removals, and audit logs.

## Run It

From the project folder:

```powershell
python backend/server.py --port 5173
```

Then open:

```text
http://localhost:5173/
```

If the backend is unavailable, the frontend falls back to static demo mode. When the backend is online, the top status pill says `Backend online - mock adapters`.

## What Works Now

- Filter interactions by network, type, status, and search query.
- Multi-select and deselect visible interactions.
- Remove selected interactions through a backend removal job.
- Bulk remove visible interactions per interaction type.
- Undo the last backend removal job.
- Persist networks, interactions, jobs, and audit logs in SQLite.
- Show provider capability/readiness data per social network.
- Expose OAuth placeholder routes that report the missing provider credentials/review requirements.
- Start Meta OAuth, exchange the authorization code for a token, and discover Facebook Pages plus linked Instagram Business accounts.

## Backend API

- `GET /api/bootstrap` returns networks, interactions, jobs, audit entries, and capabilities.
- `GET /api/capabilities` returns the provider capability matrix.
- `GET /api/jobs` returns recent removal jobs.
- `GET /api/audit` returns recent audit activity.
- `GET /api/oauth/start?provider=instagram` starts Meta OAuth for Instagram/Facebook Page access.
- `GET /api/oauth/callback?provider=instagram` completes Meta OAuth, stores the token locally, and discovers Meta accounts.
- `GET /api/meta/status` returns local Meta configuration/connection status without exposing tokens.
- `GET /api/meta/accounts` returns discovered Facebook Pages and linked Instagram accounts without exposing tokens.
- `POST /api/sync` runs mock provider sync for connected/review accounts.
- `POST /api/removals` creates and processes a mock removal job.
- `POST /api/removals/undo` restores the latest or specified removal job.
- `POST /api/accounts/toggle` toggles a mock account connection state.
- `POST /api/meta/discover` refreshes discovered Meta accounts using the stored token.

The SQLite file is created at `data/anaunim.sqlite` and is ignored by Git.

## Provider Reality Check

The UI can model comments, likes/reactions, reposts/shares, saves/favorites/bookmarks, and replies, but production support depends on each network's official API and review process.

See [docs/provider-capability-matrix.md](docs/provider-capability-matrix.md) for the current conservative matrix.

## Inputs Needed From You Later

## Meta Setup

Add these values to `.env`:

```env
APP_BASE_URL=http://localhost:5173
SESSION_SECRET=replace-with-a-long-random-string
META_APP_ID=your-meta-app-id
META_APP_SECRET=your-meta-app-secret
META_GRAPH_VERSION=v23.0
META_LOGIN_CONFIG_ID=your-facebook-login-for-business-configuration-id
META_REDIRECT_URI=http://localhost:5173/api/oauth/callback?provider=instagram
```

In Meta's app dashboard, save this OAuth redirect URI under Facebook Login for Business:

```text
http://localhost:5173/api/oauth/callback?provider=instagram
```

Then run the backend and click `Connect Meta` in Anaunim.

If Meta reports `Invalid Scopes`, open `Facebook Login for Business` in the Meta app dashboard and create or edit a Login Configuration. Add the needed permissions there, save the configuration, then copy its Configuration ID into `META_LOGIN_CONFIG_ID`. When this value is present, Anaunim uses Meta's `config_id` OAuth flow instead of sending raw scopes directly.

## Deploy On Render

On Render, choose **Web Services**, not Static Sites.

Use these settings:

- Runtime: `Python`
- Build command: `pip install -r requirements.txt`
- Start command: `python backend/server.py --host 0.0.0.0`

Set these environment variables in Render:

```env
APP_BASE_URL=https://your-render-or-custom-domain
SESSION_SECRET=replace-with-a-long-random-string
META_APP_ID=your-meta-app-id
META_APP_SECRET=your-meta-app-secret
META_GRAPH_VERSION=v23.0
META_LOGIN_CONFIG_ID=your-facebook-login-for-business-configuration-id
META_REDIRECT_URI=https://your-render-or-custom-domain/api/oauth/callback?provider=instagram
DATABASE_PATH=/opt/render/project/src/data/anaunim.sqlite
```

After Render deploys, set the same callback in Meta:

```text
https://your-render-or-custom-domain/api/oauth/callback?provider=instagram
```

Useful public URLs for Meta setup:

- Privacy policy: `/privacy`
- Data deletion: `/data-deletion`
- Terms: `/terms`
- Health check: `/healthz`

Real provider integration beyond OAuth will require:

- Meta developer app, app ID/secret, redirect URI, and approved permissions for Instagram/Facebook.
- TikTok developer app, client key/secret, redirect URI, and approved product scopes.
- LinkedIn developer app and the required product access for member or organization social actions.
- X developer app, OAuth 2.0 credentials, redirect URI, and an API tier that includes the needed endpoints.
- Confirmation of which accounts/pages/organizations you own and want this app to manage.

Until those are available, the mock adapters are the correct place to keep building product behavior safely.
