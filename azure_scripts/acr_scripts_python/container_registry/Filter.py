import datetime
from azure.containerregistry import ArtifactTagProperties, ArtifactManifestProperties

from azure_scripts.container_registry.ContainerRegistry import ContainerRegistry
from azure_scripts.utils.logger import Logger

class Filter:

    def __init__(self, container_registry: ContainerRegistry, log_level: str="INFO"):
        self.container_registry = container_registry
        self.logger = Logger(log_level)


    def _fetch_tags_between_dates(
        self, 
        repository: str, 
        end_date: datetime, 
        start_date: datetime = None
    ) -> list[ArtifactTagProperties]:
        
        self.logger.info(
            f"Filtering tags in {repository} between {start_date} and {end_date}"
        )

        final_tags = []

        tags = self.container_registry._list_tag_properties(
            repository=repository
        )

        if not tags:
            return final_tags

        for tag in tags:
            tag_name = tag.name

            props = self.container_registry._get_tag_property(
                repository=repository,
                tag=tag_name    
            )

            if not props:
                continue

            created = props.created_on
            self.logger.debug(f"Tag {tag_name} created_on={created}")

            if created >= end_date:
                self.logger.debug(
                    f"Tag {tag_name} ignored (created_on={created} >= end_date={end_date})"
                )
                continue

            if start_date and created <= start_date:
                self.logger.debug(
                    f"Tag {tag_name} ignored (created_on={created} <= start_date={start_date})"
                )
                continue

            self.logger.debug(f"Tag {tag_name} added to filtered results.")
            final_tags.append(tag)

        self.logger.info(f"Total filtered tags: {len(final_tags)}")
        return final_tags
    

    def _fetch_manifests_between_dates(
        self, 
        repository: str, 
        end_date: datetime, 
        start_date: datetime = None
    ) -> list[ArtifactManifestProperties]:
        
        self.logger.info(
            f"Filtering manifests in {repository} between {start_date} and {end_date}"
        )

        final_manifests = []

        manifests = self.container_registry._list_manifest_properties(
            repository=repository
        )

        if not manifests:
            return final_manifests

        for manifest in manifests:
            digest = manifest.digest

            props = self.container_registry._get_manifest_property(
                repository=repository,
                manifest=digest   
            )

            if not props:
                continue

            created = props.created_on
            self.logger.debug(f"Digest {digest} created_on={created}")

            if created >= end_date:
                self.logger.debug(
                    f"Digest {digest} ignored (created_on={created} >= end_date={end_date})"
                )
                continue

            if start_date and created <= start_date:
                self.logger.debug(
                    f"Digest {digest} ignored (created_on={created} <= start_date={start_date})"
                )
                continue

            self.logger.debug(f"Digest {digest} added to filtered results.")
            final_manifests.append(manifest)

        self.logger.info(f"Total filtered manifests: {len(final_manifests)}")
        return final_manifests