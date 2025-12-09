from azure_scripts.utils.Parser import Parser
from azure_scripts.auth.Authentication import Authentication
from azure_scripts.container_registry.ContainerRegistry import ContainerRegistry
from azure_scripts.container_registry.Filter import Filter
from azure_scripts.tasks.AcrCleanup import AcrCleanup

def main():
    args = Parser().parse()
    auth = Authentication(
        "EnvironmentCredential", 
        log_level=args.log_level
    )
    cred = auth._get_credential()

    if args.resource == "acr":
        registry = ContainerRegistry(
            auth=cred, 
            acr_endpoint=args.acr_endpoint,
            log_level=args.log_level
        )

        filter = Filter(
            container_registry=registry,
            log_level=args.log_level
        )

        cleanup = AcrCleanup(
            filter=filter, 
            container_registry=registry,
            log_level=args.log_level
        )

        if args.command == "cleanup-tags":
            cleanup._acr_tags_cleanup(
                repository=args.repo,
                end_date=args.end_date,
                start_date=args.start_date
            )

        elif args.command == "cleanup-manifests":
            cleanup._acr_manifests_cleanup(
                repository=args.repo,
                end_date=args.end_date,
                start_date=args.start_date
            )


if __name__ == "__main__":
    main()