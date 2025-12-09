from azure.identity import EnvironmentCredential

from azure_scripts.utils.logger import Logger

class Authentication:

    def __init__(self, method, log_level="INFO"):
        self.method = method
        self.log_level = log_level
        self.logger = Logger(level=self.log_level)

        self.logger.debug(f"Authentication initialized with method: {self.method}")


    def _environment_credential(self):
        self.logger.debug("Creating EnvironmentCredential")
        try:
            credential = EnvironmentCredential()
            self.logger.info("EnvironmentCredential created successfully")
            self.logger.debug(f"Credential: {credential}")
            
            return credential
        except Exception as e:
            self.logger.error(f"Failed to create EnvironmentCredential: {e}")
            raise


    def _get_credential(self):
        self.logger.info(f"Fetching credential using method: {self.method}")

        try:
            if self.method == "EnvironmentCredential":
                return self._environment_credential()

            self.logger.error(f"Unsupported authentication method requested: {self.method}")
            raise ValueError(f"Unsupported auth method: {self.method}")

        except Exception as e:
            self.logger.error(f"Error while getting credential: {e}")
            raise