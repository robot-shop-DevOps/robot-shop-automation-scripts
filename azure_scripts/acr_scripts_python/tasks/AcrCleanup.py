import datetime

from azure_scripts.container_registry.Filter import Filter
from azure_scripts.container_registry.ContainerRegistry import ContainerRegistry
from azure_scripts.utils.logger import Logger

class AcrCleanup:

    def __init__(self, filter: Filter, container_registry: ContainerRegistry, log_level: str = "INFO"):
        self.filter = filter
        self.container_registry = container_registry
        self.logger = Logger(log_level)

    def _acr_tags_cleanup(
        self,
        repository: str,
        end_date: datetime, 
        start_date: datetime = None
    ) -> None:
        
        self.logger.info(
            f"Cleaning ACR tags for repository {repository} between {start_date} and {end_date}"
        )
        
        tags = self.filter._fetch_tags_between_dates(
            repository=repository,
            end_date=end_date,
            start_date=start_date
        )

        if not tags:
            self.logger.info(f"No tags found to delete in repository {repository}")
            return

        for tag in tags:
            tag_name = tag.name
            self.logger.info(f"Deleting tag {tag_name} from {repository}")

            self.container_registry._delete_tag(
                repository=repository,
                tag=tag_name
            )

    def _acr_manifests_cleanup(
        self,
        repository: str,
        end_date: datetime, 
        start_date: datetime = None
    ) -> None:
        
        self.logger.info(
            f"Cleaning ACR manifests for repository {repository} between {start_date} and {end_date}"
        )
        
        manifests = self.filter._fetch_manifests_between_dates(
            repository=repository,
            end_date=end_date,
            start_date=start_date
        )

        if not manifests:
            self.logger.info(f"No manifests found to delete in repository {repository}")
            return

        for manifest in manifests:
            digest = manifest.digest
            self.logger.info(f"Deleting manifest digest {digest} from {repository}")

            self.container_registry._delete_manifest(
                repository=repository,
                tag_or_digest=digest
            )