"""Provider capability matrix for production planning.

This file is intentionally conservative. The mock adapter can simulate every
action, but production adapters must only enable actions after the app has the
provider account type, OAuth scopes, and review status required by that provider.
"""

CAPABILITY_MATRIX = {
    "instagram": {
        "label": "Instagram",
        "auth_model": "Meta OAuth through Instagram Graph API",
        "production_status": "requires_meta_app_review",
        "actions": {
            "comment": {
                "sync": "supported_for_authorized_business_or_creator_assets",
                "remove": "provider_scoped_delete_only",
            },
            "like": {
                "sync": "limited",
                "remove": "not_enabled_until_scope_verified",
            },
            "save": {
                "sync": "not_confirmed",
                "remove": "not_confirmed",
            },
            "repost": {
                "sync": "not_applicable",
                "remove": "not_applicable",
            },
        },
        "required_user_input": [
            "Meta developer app",
            "Instagram Business or Creator account linked to a Facebook Page",
            "Approved permissions for the exact interaction surfaces",
        ],
        "sources": [
            "https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/",
            "https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-comment/",
            "https://developers.facebook.com/docs/permissions/",
        ],
    },
    "facebook": {
        "label": "Facebook",
        "auth_model": "Meta OAuth through Graph API",
        "production_status": "requires_page_permissions_and_app_review",
        "actions": {
            "comment": {
                "sync": "supported_for_authorized_page_assets",
                "remove": "provider_scoped_delete_only",
            },
            "reaction": {
                "sync": "supported_for_authorized_page_assets",
                "remove": "provider_scoped_delete_only",
            },
            "share": {
                "sync": "limited",
                "remove": "not_confirmed_for_bulk_automation",
            },
        },
        "required_user_input": [
            "Meta developer app",
            "Facebook Page or asset ownership",
            "Approved Page permissions",
        ],
        "sources": [
            "https://developers.facebook.com/docs/graph-api/",
            "https://developers.facebook.com/docs/graph-api/reference/comment/",
            "https://developers.facebook.com/docs/pages-api/",
        ],
    },
    "tiktok": {
        "label": "TikTok",
        "auth_model": "TikTok OAuth and product-specific APIs",
        "production_status": "requires_tiktok_app_review",
        "actions": {
            "comment": {
                "sync": "limited_by_product_access",
                "remove": "not_confirmed_for_user_history_cleanup",
            },
            "like": {
                "sync": "limited_by_display_api_access",
                "remove": "not_confirmed",
            },
            "favorite": {
                "sync": "not_confirmed",
                "remove": "not_confirmed",
            },
            "repost": {
                "sync": "not_confirmed",
                "remove": "not_confirmed",
            },
        },
        "required_user_input": [
            "TikTok developer app",
            "Approved Login Kit scopes",
            "Product access approval for comments or engagement data",
        ],
        "sources": [
            "https://developers.tiktok.com/doc/overview/",
            "https://developers.tiktok.com/doc/login-kit-web/",
            "https://developers.tiktok.com/doc/content-posting-api-get-started/",
        ],
    },
    "linkedin": {
        "label": "LinkedIn",
        "auth_model": "LinkedIn OAuth through Marketing Developer Platform",
        "production_status": "requires_linkedin_product_access",
        "actions": {
            "comment": {
                "sync": "supported_for_authorized_member_or_organization_contexts",
                "remove": "provider_scoped_delete_only",
            },
            "reaction": {
                "sync": "supported_for_authorized_contexts",
                "remove": "provider_scoped_delete_only",
            },
            "repost": {
                "sync": "limited",
                "remove": "not_confirmed_for_bulk_automation",
            },
        },
        "required_user_input": [
            "LinkedIn developer app",
            "Marketing Developer Platform or relevant product access",
            "Organization/member authorization matching the actions",
        ],
        "sources": [
            "https://learn.microsoft.com/linkedin/",
            "https://learn.microsoft.com/linkedin/marketing/",
            "https://learn.microsoft.com/linkedin/shared/authentication/authorization-code-flow",
        ],
    },
    "x": {
        "label": "X",
        "auth_model": "X OAuth 2.0 with API access tier limits",
        "production_status": "requires_x_api_access_tier",
        "actions": {
            "reply": {
                "sync": "supported_by_posts_api_when_authorized",
                "remove": "delete_own_post_only",
            },
            "like": {
                "sync": "supported_when_tier_and_scopes_allow",
                "remove": "supported_when_tier_and_scopes_allow",
            },
            "repost": {
                "sync": "supported_when_tier_and_scopes_allow",
                "remove": "supported_when_tier_and_scopes_allow",
            },
            "bookmark": {
                "sync": "supported_when_tier_and_scopes_allow",
                "remove": "supported_when_tier_and_scopes_allow",
            },
        },
        "required_user_input": [
            "X developer project and app",
            "OAuth 2.0 client credentials",
            "API tier that includes post, like, repost, and bookmark endpoints",
        ],
        "sources": [
            "https://docs.x.com/x-api/",
            "https://docs.x.com/x-api/posts/manage-tweets/delete-post",
            "https://docs.x.com/x-api/posts/likes/manage-likes",
            "https://docs.x.com/x-api/posts/reposts/manage-reposts",
            "https://docs.x.com/x-api/bookmarks/manage-bookmarks",
        ],
    },
}
