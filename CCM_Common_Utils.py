import requests, json, csv
import pandas as pd
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col, when
from pyspark.sql import functions as F

class common_utils:
    def __init__(self, logger) -> None:
        """
        :param logger: current active logger
        """
        self.logger = logger
        self.logger.info("Common Utils Class initialized")

    def rename_columns(self, df, rename_map):
        """
        :param df: spark df to apply rename function
        :param rename_map: a dictionary containing the rename map with keys as intial column names and values as final column names
        :return: spark df with renamed columns as per the provided rename_map
        """
        """
        function to rename the columns of a spark df using the provided rename_map json
        """

        for old, new in rename_map.items():
            if old in df.columns:
                df = df.withColumnRenamed(old, new)
        return df

    def detect_badcustomerinformation_entries(self, df_info_transformed, schema_name, badcustomerdetailsinformation,
                                               customer_column, tenant_column, environment_column,
                                               customer_ccm_version_column, sftp_folder_column,
                                               ccm_customer_month_format_column, ccm_customer_day_format_column,
                                               tenant_id_column):
        """
        Identifies conflicting customer+tenant+environment records from the transformed
        customer registration DataFrame, overwrites the bad customer details table with
        the detected invalid records, and returns the invalid records DataFrame.

        :param df_info_transformed: Transformed customer registration DataFrame
                                    (with Tenant and Environment columns already concatenated)
        :param schema_name: The database schema name
        :param badcustomerdetailsinformation: Target bad customer details table name
        :param customer_column: Column name for Customer
        :param tenant_column: Column name for Tenant
        :param environment_column: Column name for Environment
        :param customer_ccm_version_column: Column name for CCM version
        :param sftp_folder_column: Column name for SFTP folder
        :param ccm_customer_month_format_column: Column name for month format
        :param ccm_customer_day_format_column: Column name for day format
        :param tenant_id_column: Column name for Tenant ID
        :return: df_invalid — DataFrame of invalid customer+tenant+environment records
        """
        df_invalid = (
            df_info_transformed
            .groupBy(customer_column, tenant_column, environment_column)
            .agg(
                F.countDistinct(customer_ccm_version_column).alias("version_count"),
                F.countDistinct(sftp_folder_column).alias("sftp_count"),
                F.countDistinct(ccm_customer_month_format_column).alias("month_count"),
                F.countDistinct(ccm_customer_day_format_column).alias("day_count"),
                F.countDistinct(tenant_id_column).alias("tenantid_count"),
                F.sum(when((col(sftp_folder_column).isNull()) | (col(sftp_folder_column) == ""), 1).otherwise(0)).alias("null_sftp_count"),
                F.sum(when((col(customer_ccm_version_column).isNull()) | (col(customer_ccm_version_column) == ""), 1).otherwise(0)).alias("null_version_count")
            )
            .filter(
                (col("version_count") > 1) |
                (col("sftp_count") > 1) |
                (col("month_count") > 1) |
                (col("day_count") > 1) |
                (col("tenantid_count") > 1) |
                (col("null_sftp_count") > 0) |
                (col("null_version_count") > 0)
            )
            .select(customer_column, tenant_column, environment_column)
            .dropDuplicates()
        )

        # Overwrite the bad customer details table with the current set of invalid records
        df_invalid.write.mode("overwrite").insertInto(f"{schema_name}.{badcustomerdetailsinformation}")
        self.logger.info(f"Bad customer details table overwritten with {df_invalid.count()} invalid record(s).")

        return df_invalid

    def execute_api(self, payload, headers, url, mode):
        """
        Helper function to execute REST API calls.
        """
        self.logger.info(f"API Call: {mode} {url}")
        self.logger.info(f"Headers: {headers}")
        self.logger.info(f"Payload: {payload}")

        try:
            resp = requests.request(
                mode, url, headers=headers, data=json.dumps(payload), verify=False
            )
            #self.logger.info(f"Raw Response Status: {resp.status_code}")
            #self.logger.info(f"Raw Response Text: {resp.text}")
            try:
                resp_json = resp.json()
                self.logger.info(f"Parsed JSON Response: {resp_json}")
                return resp, resp_json
            except json.JSONDecodeError:
                self.logger.info(f"Failed to parse JSON response. Status: {resp.status_code}, Text: {resp.text}")
                return resp, {}

        except Exception as e:
            self.logger.info(f"API Execution Failed: {e}")
            return type('obj', (object,), {'status_code': 500, 'text': 'Connection Error'}), {}

    def create_dataframe_from_api(self, resp):
        """
        Parses metadata to create an empty DataFrame with correct column headers.
        """
        columns = []
        query_response_dataframe = pd.DataFrame()

        if resp.get("Meta") and resp.get("Data"):
            self.logger.info("The Query response is not empty. Parsing Metadata...")

            # Fetch Dimensions
            self.logger.info("Fetching Dimension Attributes...")
            for column in resp["Meta"]:
                self.logger.info(f"Meta Column: {column}")
                if "DimensionName" in column and "AttributeName" in column:
                    col_name = "[{0}].[{1}]".format(column["DimensionName"], column["AttributeName"])
                    columns.append(col_name)

            self.logger.info(f"Final Column List: {columns}")
            query_response_dataframe = pd.DataFrame(columns=columns)
            self.logger.info("Successfully created the empty Dataframe structure.")

        elif not resp.get("Meta") and not resp.get("Data"):
            self.logger.warning("The Query response is empty (No Data/Meta found).")
        else:
            self.logger.warning("Response has unexpected structure. Meta: %s, Data: %s", resp.get("Meta"),
                                resp.get("Data"))

        return query_response_dataframe

    def populate_rows(self, resp, response_data):
        """
        Parses the 'Data' section to fill the DataFrame rows.
        """
        self.logger.info("Starting to populate DataFrame rows...")
        try:
            rows_list = []
            if "Data" in resp:
                for row_data in resp["Data"]:
                    row = []
                    k = 0

                    # Loop: Extract Dimension Members
                    while "C{0}".format(k) in row_data:
                        cell = row_data["C{0}".format(k)]
                        if "Name" in cell:
                            row.append(cell["Name"])
                        elif "Value" in cell:
                            row.append(cell["Value"])
                        k += 1

                    rows_list.append(row)

            if rows_list:
                new_rows = pd.DataFrame(rows_list, columns=response_data.columns)

                if response_data.empty:
                    response_data = new_rows
                    self.logger.info(f"Successfully populated DataFrame with {len(rows_list)} rows.")
                else:
                    response_data = pd.concat([response_data, new_rows], ignore_index=True)
                    self.logger.info(f"Successfully appended {len(rows_list)} rows.")

        except Exception as e:
            self.logger.info(f"Error populating rows: {e}")

        return response_data

    def save_df_as_file_in_cloud(self, df, file_path, separator):
        """
        Saves Pandas DataFrame to a cloud location as CSV file

        Args:
            df: Pandas DataFrame to save
            file_path: Full cloud file path (e.g., "abfss://container@account.dfs.core.windows.net/path/file.csv")
            separator: delimiter for the csv file

        Returns:
            tuple: (filename, status) where status is "success" or "failed"
        """

        if file_path.startswith("gs"):
            try:
                df.to_csv(
                    file_path,
                    index=False,
                    quotechar="'",
                    quoting=csv.QUOTE_ALL,
                    sep=separator,
                    escapechar='\\'
                )
                self.logger.info(f"Successfully saved DataFrame to google cloud: {file_path}")
                return file_path.split("/")[-1], "success"

            except Exception as e:
                self.logger.info(f"Failed to save DataFrame to google cloud: {e}")
                return file_path.split("/")[-1], "failed"

        elif file_path.startswith("abfss") or file_path.startswith("abfs")or file_path.startswith("wasbs") or file_path.startswith("wasb"):
            try:
                import adlfs
                # Extract account name from ADLS path
                account_name = file_path.split("@")[1].split(".dfs")[0]
                # Create filesystem connection
                fs = adlfs.AzureBlobFileSystem(account_name=account_name, anon=False)
                # Write CSV to ADLS
                with fs.open(file_path, "w") as f:
                    df.to_csv(
                        f,
                        index=False,
                        quotechar="'",
                        quoting=csv.QUOTE_ALL,
                        sep=separator,
                        escapechar='\\'
                    )
                self.logger.info(f"Successfully saved DataFrame to azure cloud: {file_path}")
                return file_path.split("/")[-1], "success"

            except Exception as e:
                self.logger.info(f"Failed to save DataFrame to azure cloud: {e}")
                return file_path.split("/")[-1], "failed"

        elif file_path.startswith("s3"):
            pass

        else:
            try:
                df.to_csv(
                    file_path,
                    index=False,
                    quotechar="'",
                    quoting=csv.QUOTE_ALL,
                    sep=separator,
                    escapechar='\\'
                )
                self.logger.info(f"Successfully saved DataFrame to cloud: {file_path}")
                return file_path.split("/")[-1], "success"

            except Exception as e:
                self.logger.info(f"Failed to save DataFrame to cloud: {e}")
                return file_path.split("/")[-1], "failed"


    def read_file_as_df_from_cloud(self,file_path, separator, dtype=None, quotechar="'"):
        """
        Reads a CSV file from cloud as a pandas df

        Args:
            file_path: Full cloud file path (e.g., "abfss://container@account.dfs.core.windows.net/path/file.csv")
            separator: delimiter for the csv file
            dtype: a json of column wise datatypes

        Returns:
            DataFrame: a pandas df of the read csv file
        """

        if file_path.startswith("gs"):
            try:
                df = pd.read_csv(
                    file_path,
                    sep=separator,
                    quotechar=quotechar,
                    quoting=csv.QUOTE_ALL,
                    on_bad_lines="skip",
                    low_memory=False,
                    index_col=False,
                    dtype=dtype
                )
                self.logger.info(f"Successfully read file from {file_path}")
                return df

            except Exception as e:
                self.logger.info(f"Failed to read file from google cloud: {e}")
                return None

        elif file_path.startswith("abfss") or file_path.startswith("abfs") or file_path.startswith(
                "wasbs") or file_path.startswith("wasb"):
            try:
                import adlfs
                # Extract account name from ADLS path
                account_name = file_path.split("@")[1].split(".dfs")[0]
                # Create filesystem connection
                fs = adlfs.AzureBlobFileSystem(account_name=account_name, anon=False)

                # read csv from ADLS
                with fs.open(file_path, "rb") as f: #.split(".net/")[-1]
                    df =  pd.read_csv(
                        f,
                        sep=separator,
                        quotechar=quotechar,
                        quoting=csv.QUOTE_ALL,
                        on_bad_lines="skip",
                        low_memory=False,
                        index_col=False,
                        dtype=dtype
                    )
                self.logger.info(f"Successfully read file from {file_path}")
                return df

            except Exception as e:
                self.logger.info(f"Failed to read file from azure cloud: {e}")
                return None

        elif file_path.startswith("s3"):
            pass

        else:
            try:
                df = pd.read_csv(
                    file_path,
                    sep=separator,
                    quotechar=quotechar,
                    quoting=csv.QUOTE_ALL,
                    on_bad_lines="skip",
                    low_memory=False,
                    index_col=False,
                    dtype=dtype
                )
                self.logger.info(f"Successfully read file from {file_path}")
                return df

            except Exception as e:
                self.logger.info(f"Failed to read file from cloud: {e}")
                return None
    
    def parse_tenant_list_json(self, tenant_list_json):
        """
        Parse and validate tenant list JSON string.
        
        Args:
            tenant_list_json: JSON string containing tenant configurations
            
        Returns:
            list: Parsed tenant list
            
        Raises:
            ValueError: If JSON is invalid or empty
        """
        try:
            tenant_list = json.loads(tenant_list_json)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse tenant list JSON: {e}")
            raise ValueError(f"Invalid JSON in tenant_list parameter: {e}")
        
        if not tenant_list or len(tenant_list) == 0:
            self.logger.warning("Tenant list is empty - no tenants to process")
            raise ValueError("Tenant list is empty")
        
        return tenant_list
    
    def create_master_schema(self, master_cols):
        """
        Create schema for master table.
        
        Args:
            master_cols: Dictionary containing master table column names
            
        Returns:
            StructType: Schema for master table
        """
        return StructType([
            StructField(master_cols["tenant_id"],         StringType(), False),
            StructField(master_cols["tenant_name"],        StringType(), True),
            StructField(master_cols["environment"],        StringType(), True),
            StructField(master_cols["last_timestamp"],     StringType(), True),
            StructField(master_cols["pending_timestamp"],  StringType(), True)
        ])

    def prepare_tenant_configurations(self, spark, tenant_list_json, df_customer_reg, config_yaml):
        """
        Prepare tenant configurations from JSON and join with customer registration.
        All column names are resolved internally from config_yaml — no column params needed.

        Args:
            spark:            SparkSession object
            tenant_list_json: JSON string containing tenant list from paramset
            df_customer_reg:  DataFrame with customer registration data (stg_customerregistration)
            config_yaml:      Central config dict (already loaded in calling class __init__)

        Returns:
            list: List of tenant configuration dicts, one per Tenant_ID
        """
        tenant_name_col      = config_yaml["Tenant_Name"]
        tenant_id_col        = config_yaml["Tenant_ID"]
        etl_username_col     = config_yaml["ETL_Username"]
        etl_password_col     = config_yaml["ETL_Password"]
        customer_col         = config_yaml["Customer"]
        environment_col      = config_yaml["Environment"]
        ls_url_col           = config_yaml["LS_URL"]
        tenant_type_col      = config_yaml["Tenant_Type"]
        environment_type_col = config_yaml["Environment_Type"]
        sftp_folder_col      = config_yaml["SFTP_Folder"]

        batch_cfg = config_yaml.get("BatchUsageLogsDataLake", {})
        integration_server_name_col = batch_cfg.get("integration_server_name")
        solution_col         = config_yaml.get("Solution_Column")
        integration_type_col = config_yaml.get("Integration_Type")

        # Assigned Config Build — used by TenantConfigurationDataLake
        # AsBuild_Column is a list: [db_col_name, display_name], e.g. ["Assigned_Config_Build", "Assigned Config Build"]
        abuild_col_cfg = config_yaml.get("TenantConfigurationDataLake", {}).get("ABuild_Column")
        abuild_db_col  = abuild_col_cfg[0] if isinstance(abuild_col_cfg, list) else abuild_col_cfg

        # ── Parse tenant list JSON ─────────────────────────────────────────────
        tenant_list = self.parse_tenant_list_json(tenant_list_json)

        # ── Build tenant DataFrame from ParamSet ───────────────────────────────
        tenant_schema = StructType([
            StructField(tenant_name_col,  StringType(), True),
            StructField(tenant_id_col,    StringType(), True),
            StructField(etl_username_col, StringType(), True),
            StructField(etl_password_col, StringType(), True)
        ])
        tenant_df = spark.createDataFrame(tenant_list, schema=tenant_schema)
        self.logger.info(f"Created tenant DataFrame with {tenant_df.count()} tenants from ParamSet")

        # ── Build select columns ───────────────────────────────────────────────
        select_cols = [
            col(f"t.{tenant_id_col}").alias("Tenant_ID"),
            col(f"t.{tenant_name_col}").alias("Tenant_Name"),
            col(f"c.{customer_col}").alias("Customer_Name"),
            col(f"c.{environment_col}").alias("Environment_Name"),
            col(f"c.{tenant_type_col}").alias("Tenant_Type"),
            col(f"c.{environment_type_col}").alias("Environment_Type"),
            col(f"c.{ls_url_col}").alias("Tenant_URL"),
            col(f"c.{sftp_folder_col}").alias("SFTP_Folder"),  
            col(f"t.{etl_username_col}").alias("ETL_Username"),
            col(f"t.{etl_password_col}").alias("ETL_Password")
        ]
        # Workspace_Name = Integration_Server_Name from stg_customerregistration.
        # Written into every IN Int3 record so the STG join on server_name resolves correctly.
        if integration_server_name_col:
            select_cols.append(col(f"c.{integration_server_name_col}").alias("Workspace_Name"))
        if solution_col:
            select_cols.append(col(f"c.{solution_col}").alias("Solution"))
        if integration_type_col:
            select_cols.append(col(f"c.{integration_type_col}").alias("IntegrationType"))
        # Assigned Config Build — needed by TenantConfigurationDataLake API path
        # AsCBuildColumn[1] ("Assigned Config Build") is used as the dict key in tenant_config
        if abuild_db_col and abuild_col_cfg:
            abuild_display_name = abuild_col_cfg[1] if isinstance(abuild_col_cfg, list) else abuild_db_col
            select_cols.append(col(f"c.{abuild_db_col}").alias(abuild_display_name))

        # ── Join on Tenant_ID + Tenant_Name (prevents TBI data bleed) ─────────
        joined = tenant_df.alias("t").join(
            df_customer_reg.alias("c"),
            (col(f"t.{tenant_id_col}").cast("string") == col(f"c.{tenant_id_col}").cast("string")) &
            (col(f"t.{tenant_name_col}") == col(f"c.{tenant_name_col}")),
            how="inner"
        ).select(*select_cols)

        # One row per Tenant_ID — URL/credentials are identical across rows for same tenant
        complete_tenant_config = joined.dropDuplicates(["Tenant_ID"])

        tenant_config_count = complete_tenant_config.count()
        self.logger.info(f"Successfully joined {tenant_config_count} tenants with customer registration data")

        tenant_configs = [dict(row.asDict()) for row in complete_tenant_config.collect()]
        for cfg in tenant_configs:
            self.logger.info(
                f"Tenant_ID={cfg.get('Tenant_ID')} | Tenant_Name={cfg.get('Tenant_Name')} | "
                f"Customer={cfg.get('Customer_Name')} | SFTP_Folder={cfg.get('SFTP_Folder')} | "
                f"Workspace_Name={cfg.get('Workspace_Name')} | URL={cfg.get('Tenant_URL')}"
            )
        self.logger.info(f"Loaded configuration for {len(tenant_configs)} tenants")

        return tenant_configs
    
    
    def get_last_timestamp_function(self, master_timestamp_dict):
        """
        Create a closure function to get last timestamp for a tenant.
        
        Args:
            master_timestamp_dict: Dictionary with tenant timestamps
            
        Returns:
            function: Function that takes tenant_id and returns last timestamp
        """
        def get_last_timestamp(tenant_id):
            """Get last processed timestamp for tenant from master table."""
            timestamp = master_timestamp_dict.get(tenant_id)
            if timestamp:
                self.logger.info(f"Found last_processed_timestamp for {tenant_id}: {timestamp}")
            else:
                self.logger.info(f"No last_processed_timestamp for {tenant_id} - will use offset")
            return timestamp
        
        return get_last_timestamp
    
    def create_timestamp_lookup(self, df_master, master_cols):
        """
        Create optimized timestamp lookup dictionary from master table.
        Handles empty master tables gracefully.

        Args:
            df_master: Master DataFrame with timestamps (may be empty)
            master_cols: Dictionary containing master table column names
            
        Returns:
            dict: Dictionary mapping tenant_id to last_processed_timestamp
        """
        self.logger.info("Creating optimized timestamp lookup from master table...")
        master_timestamp_dict = {}
        master_count = df_master.count()
        if master_count > 0:
            master_rows = df_master.select(
                master_cols["tenant_id"],
                master_cols["last_timestamp"]     
            ).collect()
            
            for row in master_rows:
                master_timestamp_dict[row[master_cols["tenant_id"]]] = row[master_cols["last_timestamp"]]  
                
            self.logger.info(f"Loaded {len(master_timestamp_dict)} tenant timestamps from master table")
        else:
            self.logger.info("Master table is empty - first run, all tenants will use offset-based timestamps")

        return master_timestamp_dict

    def build_sftp_upload_func(self, mode,
                               sftp_host, sftp_port,
                               sftp_username, sftp_password,
                               root_path="",
                               sftp_cols_map=None,
                               sep="^",
                               quoting_all=False):
        """
        Build and return a per-tenant SFTP upload callable for hybrid mode.
        :param mode:          'local' or 'hybrid'
        :param sftp_host:     Central SFTP host
        :param sftp_port:     Central SFTP port
        :param sftp_username: Central SFTP username
        :param sftp_password: Central SFTP password
        :param root_path:     Central SFTP root path, e.g. "/root"
        :param sftp_cols_map: Dict mapping filename prefix -> ordered list of column names
        :param sep:           CSV delimiter written into the uploaded file (default "^")
        :param quoting_all:   If True, quote all fields with double-quotes (matches prod format)
        :returns:             Callable(tenant_config, records, filename) or None
        """
        if mode != 'hybrid':
            return None

        if not all([sftp_host, sftp_username, sftp_password]):
            self.logger.warning(
                "[Hybrid] build_sftp_upload_func returning None — "
                "central_sftp_host, central_sftp_username, and central_sftp_password "
                "are all required for hybrid mode"
            )
            return None

        self.logger.info(
            f"[Hybrid] SFTP upload active — host={sftp_host}, root={root_path}, sep={repr(sep)}, quoting_all={quoting_all}"
        )

        def sftp_upload_func(tenant_config, records, filename):
            self.upload_tenant_data_to_sftp(
                tenant_config=tenant_config,
                records=records,
                filename=filename,
                sftp_host=sftp_host,
                sftp_port=sftp_port,
                sftp_username=sftp_username,
                sftp_password=sftp_password,
                root_path=root_path,
                sftp_cols_map=sftp_cols_map,
                sep=sep,
                quoting_all=quoting_all,
            )

        return sftp_upload_func

    def _run_sftp_session(self, host, port, username, password, remote_path, file_buffer):
        from io import BytesIO
        from ssh2.session import Session
        from ssh2.sftp import (LIBSSH2_FXF_WRITE, LIBSSH2_FXF_CREAT, LIBSSH2_FXF_TRUNC,
                            LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IWUSR)
        import socket
        import traceback

        sess = None
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)                           
            sock.connect((host, int(port)))

            sess = Session()
            sess.set_blocking(True)                          
            sess.handshake(sock)
            sess.userauth_password(username, password.encode("utf-8"))
            sftp = sess.sftp_init()

            flags       = LIBSSH2_FXF_WRITE | LIBSSH2_FXF_CREAT | LIBSSH2_FXF_TRUNC
            permissions = LIBSSH2_SFTP_S_IRUSR | LIBSSH2_SFTP_S_IWUSR
            remote_file = sftp.open(remote_path, flags, permissions)

            while True:
                chunk = file_buffer.read(1024 * 1024)
                if not chunk:
                    break
                remote_file.write(chunk)

            remote_file.close()
            self.logger.info(f"[Hybrid] Successfully uploaded to {remote_path}")

        except Exception as e:
            self.logger.error(
                f"[Hybrid] SFTP upload failed for {remote_path} (local unaffected): "
                f"{type(e).__name__}: {repr(e)}\n{traceback.format_exc()}" 
            )

        finally:
            try:
                if sess:
                    sess.disconnect()
                if sock:
                    sock.close()
                self.logger.info(f"[Hybrid] SFTP session closed for {remote_path}")
            except Exception:
                pass

    def upload_tenant_data_to_sftp(self, tenant_config, records, filename,
                                    sftp_host, sftp_port,
                                    sftp_username, sftp_password,
                                    root_path="",
                                    sftp_cols_map=None,
                                    sep="^",
                                    quoting_all=False):
        """
        Upload a single tenant's processed records to central SFTP as a CSV or JSON.
        :param tenant_config:  Tenant config dict — must contain Customer_Name, SFTP_Folder
        :param records:        List of dicts OR dict with 'records' key (datamodel shape)
        :param filename:       Exact filename, e.g. "TenantLogs_URBN_T1.csv"
        :param sftp_host:      Central SFTP host
        :param sftp_port:      Central SFTP port
        :param sftp_username:  Central SFTP username
        :param sftp_password:  Central SFTP password
        :param root_path:      Central SFTP root path, e.g. "/root"
        :param sftp_cols_map:  Dict mapping filename prefix -> ordered column list
        :param sep:            CSV delimiter (default ",")
        :param quoting_all:    If True, quote all fields with double-quotes (matches prod format)
        """
        import json
        import pandas as pd
        from io import BytesIO

        customer    = tenant_config.get("Customer_Name")
        sftp_folder = tenant_config.get("SFTP_Folder")

        if not customer or not sftp_folder:
            self.logger.warning(
                f"[Hybrid] upload_tenant_data_to_sftp skipped — "
                f"missing Customer_Name or SFTP_Folder in tenant_config: {tenant_config}"
            )
            return

        # Normalise records — some workers return {'records': [...], ...}
        if isinstance(records, dict) and 'records' in records:
            records = records['records']

        if not records:
            self.logger.info(f"[Hybrid] No records for {filename} — skipping upload")
            return

        remote_path = f"{root_path}/{customer}/{sftp_folder}/ToCCM/{filename}"
        self.logger.info(
            f"[Hybrid] Uploading {filename} "
            f"for tenant {tenant_config.get('Tenant_ID')} "
            f"→ {sftp_host}:{sftp_port}{remote_path}"
        )

        # Serialise: JSON written as-is; everything else is ^-delimited CSV
        file_buffer = BytesIO()
        if filename.endswith(".json"):
            file_buffer.write(json.dumps(records, ensure_ascii=False, indent=4).encode("utf-8"))
        else:
            try:
                df_pandas = pd.DataFrame(records)
                if sftp_cols_map:
                    prefix = filename.split("_")[0]
                    cols = sftp_cols_map.get(prefix)
                    if cols:
                        for c in cols:
                            if c not in df_pandas.columns:
                                df_pandas[c] = ""
                        df_pandas = df_pandas[cols]
                    else:
                        self.logger.warning(
                            f"[Hybrid] No sftp_cols_map entry for prefix '{prefix}' "
                            f"({filename}) — uploading all columns as-is"
                        )
                if quoting_all:
                    df_pandas.to_csv(
                        file_buffer, index=False, sep=sep,
                        quotechar='"', quoting=csv.QUOTE_ALL
                    )
                else:
                    df_pandas.to_csv(file_buffer, index=False, sep=sep)
            except Exception as e:
                self.logger.error(f"[Hybrid] Failed to build DataFrame for {filename}: {e}")
                return

        file_buffer.seek(0)
        self._run_sftp_session(sftp_host, sftp_port, sftp_username, sftp_password,
                               remote_path, file_buffer)

    def upload_config_backup_to_central_sftp(self, zip_bytes, customer, sftp_folder,
                                              central_sftp_host, central_sftp_port,
                                              central_sftp_username, central_sftp_password,
                                              root_path):
        """
        Stream pre-downloaded config backup ZIP bytes to the central SFTP server.
        :param zip_bytes:             Raw ZIP bytes from get_tenant_config_backup()
        :param customer:              Customer name (used in ZIP filename and path)
        :param sftp_folder:           SFTP folder name (used in remote path)
        :param central_sftp_host:     Central SFTP host
        :param central_sftp_port:     Central SFTP port
        :param central_sftp_username: Central SFTP username
        :param central_sftp_password: Central SFTP password
        :param root_path:             SFTP root path, e.g. "/root"
        """
        from io import BytesIO

        filename    = f"ConfigBackup_{customer}_{sftp_folder}.zip"
        remote_path = f"{root_path}/{customer}/{sftp_folder}/ToCCM/{filename}"

        self.logger.info(
            f"[Hybrid] Uploading {filename} ({len(zip_bytes)} bytes) "
            f"→ {central_sftp_host}:{central_sftp_port}{remote_path}"
        )

        self._run_sftp_session(central_sftp_host, central_sftp_port,
                               central_sftp_username, central_sftp_password,
                               remote_path, BytesIO(zip_bytes))