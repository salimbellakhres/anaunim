from abc import ABC, abstractmethod


class ProviderAdapter(ABC):
    """Contract implemented by every social provider adapter."""

    provider_id: str

    @abstractmethod
    def sync_interactions(self, account):
        """Return the latest interactions visible to this account."""

    @abstractmethod
    def remove_interaction(self, interaction):
        """Remove one interaction at the provider and return an action result."""

    def remove_many(self, interactions):
        """Default batch implementation. Real adapters can add batching/rate limits."""
        return [self.remove_interaction(interaction) for interaction in interactions]

    @abstractmethod
    def get_capabilities(self):
        """Return production capability metadata for this provider."""
