# Provider Capability Matrix

Last reviewed: 2026-06-19.

This matrix is conservative on purpose. The mock adapter can simulate every action, but production adapters must only enable actions after the provider account type, OAuth scopes, app review, and API tier are confirmed.

## Summary

| Provider | Production status | Best first production target | Main blocker |
| --- | --- | --- | --- |
| Instagram | Requires Meta app review | Comments on authorized Business/Creator assets | Meta app, permissions, linked Facebook Page |
| Facebook | Requires Page permissions and app review | Page comments/reactions | Page ownership and approved permissions |
| TikTok | Requires TikTok app/product review | Read-only account/content sync first | Product access for engagement history/actions |
| LinkedIn | Requires LinkedIn product access | Organization/member comments and reactions | Marketing/API product access approval |
| X | Requires API access tier | Likes/reposts/bookmarks/replies where scopes allow | Paid/elevated tier and OAuth scopes |

## Instagram

Likely surfaces:

- Comments can be synced and removed only for authorized assets where the token and permissions allow it.
- Likes and saves should remain disabled until the exact read/remove permissions are verified for the account type.
- Reposts are not a normal Instagram Graph API cleanup surface.

User input needed:

- Meta developer app.
- Instagram Business or Creator account.
- Facebook Page linked to the Instagram account.
- Approved scopes for the interaction surfaces.

Official docs:

- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/
- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-comment/
- https://developers.facebook.com/docs/permissions/

## Facebook

Likely surfaces:

- Page comments and reactions are the safest initial target.
- Shares should be treated as limited until the exact object ownership and API behavior are verified.
- Bulk destructive actions must be rate-limited and audited.

User input needed:

- Meta developer app.
- Facebook Page ownership or admin access.
- Approved Page permissions.

Official docs:

- https://developers.facebook.com/docs/graph-api/
- https://developers.facebook.com/docs/graph-api/reference/comment/
- https://developers.facebook.com/docs/pages-api/

## TikTok

Likely surfaces:

- Start with OAuth and read-only account/content sync.
- Comments, likes, favorites, and repost removals are not safe to promise until TikTok product access confirms those user-history actions.
- Do not build scraping fallbacks for private account history.

User input needed:

- TikTok developer app.
- Login Kit setup.
- Product access approval for the exact interaction data/actions.

Official docs:

- https://developers.tiktok.com/doc/overview/
- https://developers.tiktok.com/doc/login-kit-web/
- https://developers.tiktok.com/doc/content-posting-api-get-started/

## LinkedIn

Likely surfaces:

- Comments and reactions are the most plausible initial surfaces for authorized member or organization contexts.
- Reposts should remain limited until product access and endpoint behavior are confirmed.
- Organization actions may require different authorization than member actions.

User input needed:

- LinkedIn developer app.
- Marketing Developer Platform or relevant product access.
- Organization/member authorization matching the desired actions.

Official docs:

- https://learn.microsoft.com/linkedin/
- https://learn.microsoft.com/linkedin/marketing/
- https://learn.microsoft.com/linkedin/shared/authentication/authorization-code-flow

## X

Likely surfaces:

- Delete own replies/posts where the token and tier allow it.
- Unlike, unrepost, and remove bookmarks may be production-feasible with the correct OAuth scopes and API tier.
- Rate limits and paid access tiers are product constraints, not just engineering details.

User input needed:

- X developer project and app.
- OAuth 2.0 client credentials.
- API tier that includes post, like, repost, and bookmark endpoints.

Official docs:

- https://docs.x.com/x-api/
- https://docs.x.com/x-api/posts/manage-tweets/delete-post
- https://docs.x.com/x-api/posts/likes/manage-likes
- https://docs.x.com/x-api/posts/reposts/manage-reposts
- https://docs.x.com/x-api/bookmarks/manage-bookmarks

## Implementation Rule

Every real adapter should report action-level capability before the UI enables a destructive operation. If a provider does not explicitly support removing a specific interaction type for the authorized account, the UI should keep that action disabled and explain the missing scope or access level.
