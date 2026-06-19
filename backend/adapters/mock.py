from datetime import datetime, timezone

try:
    from backend.adapters.base import ProviderAdapter
    from backend.capabilities import CAPABILITY_MATRIX
except ModuleNotFoundError:
    from adapters.base import ProviderAdapter
    from capabilities import CAPABILITY_MATRIX


class MockProviderAdapter(ProviderAdapter):
    """Simulates provider work without calling external APIs."""

    def __init__(self, provider_id):
        self.provider_id = provider_id

    def sync_interactions(self, account):
        return {
            "provider": self.provider_id,
            "account": account["handle"],
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "mode": "mock",
        }

    def remove_interaction(self, interaction):
        return {
            "provider": self.provider_id,
            "interaction_id": interaction["id"],
            "provider_ref": interaction.get("provider_ref") or interaction["id"],
            "status": "removed",
            "mode": "mock",
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_capabilities(self):
        return CAPABILITY_MATRIX[self.provider_id]


def adapter_for(provider_id):
    return MockProviderAdapter(provider_id)
