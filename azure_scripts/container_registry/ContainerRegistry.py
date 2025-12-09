from azure.containerregistry import ContainerRegistryClient, ArtifactTagProperties, ArtifactManifestProperties
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

from azure_scripts.utils.logger import Logger
from azure_scripts.auth.Authentication import Authentication

class ContainerRegistry:

    def __init__(self, auth: Authentication, acr_endpoint: str, log_level="INFO"):
        self.auth = auth
        self.acr_endpoint = acr_endpoint
        self.logger = Logger(log_level)


    def _get_client(self) -> ContainerRegistryClient:
        self.logger.debug("Initializing ContainerRegistryClient")
        client = ContainerRegistryClient(
            endpoint=self.acr_endpoint,
            credential=self.auth
        )

        self.logger.debug("ContainerRegistryClient initialized")
        return client
    

    def _list_tag_properties(self, repository: str) -> list[ArtifactTagProperties]:
        self.logger.info(f"Listing tag properties for repository: {repository}")

        client = self._get_client()

        try:
            tag_props = list(client.list_tag_properties(repository))
            self.logger.info(f"Found {len(tag_props)} tags in {repository}")
            return tag_props
        
        except ResourceNotFoundError:
            self.logger.error(f"Repository {repository} not found")
            return []
        
        except Exception as e:
            self.logger.error(f"Failed to list tag properties: {e}")
            return []
        
        
    def _list_manifest_properties(self, repository: str) -> list[ArtifactManifestProperties]:
        self.logger.info(f"Listing manifest properties for repository: {repository}")
        client = self._get_client()

        try:
            manifest_props = list(client.list_manifest_properties(repository))
            self.logger.info(f"Found {len(manifest_props)} manifests in {repository}")
            return manifest_props
        
        except ResourceNotFoundError:
            self.logger.error(f"Repository {repository} not found")
            return []
        
        except Exception as e:
            self.logger.error(f"Failed to list manifest properties: {e}")
            return [] 
        

    def _delete_tag(self, repository: str, tag: str) -> None:
        self.logger.info(f"Deleting tag {tag} from repository {repository}")
        client = self._get_client()

        try:
            client.delete_tag(repository=repository, tag=tag)
        
        except HttpResponseError as http_err:
            self.logger.error(f"Unable to delete tag: {http_err}")

        status = self._verify_tag_deletion(
            repository=repository,
            tag=tag
        )

        if status:
            self.logger.info(f"Successfully deleted tag {tag} from repository {repository}")
        else:
            self.logger.error(f"Unable to delete tag {tag} from repository {repository}")


    def _delete_manifest(self, repository: str, tag_or_digest: str) -> None:
        self.logger.info(f"Deleting manifest {tag_or_digest} from repository {repository}")
        client = self._get_client()

        try:
            client.delete_manifest(repository, tag_or_digest)

        except HttpResponseError as http_err:
            self.logger.error(f"Unable to delete manifest: {http_err}")

        status = self._verify_manifest_deletion(
            repository=repository,
            manifest=tag_or_digest
        )

        if status:
            self.logger.info(f"Successfully deleted manifest {tag_or_digest} from repository {repository}")
        else:
            self.logger.error(f"Unable to delete manifest {tag_or_digest} from repository {repository}")

            
    def _verify_tag_deletion(self, repository: str, tag: str) -> bool:
        self.logger.debug(f"Verifying deletion for tag {tag} from repository {repository}")

        try:
            _ = self._get_tag_property(
                repository=repository,
                tag=tag
            )
            return False
        
        except ResourceNotFoundError:
            return True
        

    def _verify_manifest_deletion(self, repository: str, manifest: str) -> bool:
        self.logger.debug(f"Verifying deletion for manifest {manifest} from repository {repository}")

        try:
            _ = self._get_manifest_property(
                repository=repository,
                manifest=manifest
            )
            return False
        
        except ResourceNotFoundError:
            return True
        

    def _get_tag_property(self, repository: str, tag: str) -> ArtifactTagProperties:
        self.logger.info(f"Fetching properties for tag '{tag}' in '{repository}'")

        client = self.get_client()

        try:
            props = client.get_tag_properties(repository, tag)
            self.logger.debug(f"Tag '{tag}' metadata: {props}")
            return props

        except ResourceNotFoundError:
            self.logger.error(f"Tag '{tag}' not found in repository '{repository}'")
            return None

        except Exception as e:
            self.logger.error(f"Failed to fetch tag properties: {e}")
            return None
        
        
    def _get_manifest_property(self, repository: str, manifest: str) -> ArtifactManifestProperties:
        self.logger.info(f"Fetching properties for manifest '{manifest}' in '{repository}'")

        client = self.get_client()

        try:
            props = client.get_manifest_properties(repository, manifest)
            self.logger.debug(f"Manifest '{manifest}' metadata: {props}")
            return props

        except ResourceNotFoundError:
            self.logger.error(f"Manifest '{manifest}' not found in repository '{repository}'")
            return None

        except Exception as e:
            self.logger.error(f"Failed to fetch manifest properties: {e}")
            return None