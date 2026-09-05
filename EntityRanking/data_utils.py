import json
from collections import defaultdict
from zipfile import ZipFile
import pandas as pd
import re

SCS_UTIL            = "o9.GraphCube.util.Utilities"
PLUG                = "o9.GraphCube.Plugins.AbstractPlugin"
SCS_LOGGER_PREFIX   = "o9.GraphCube.Plugins.SupplyChainSolver."

class data_extraction_utils():
    _MSG_FILTER_PATTERNS: list = [
        "Query Received",
        r"Finished computation \[\d+\] Guid \[[0-9a-fA-F-]+\]",
        "Computation execution time",
        "CPU TIME:",
        "invocations",
        "executions",
        "non-null no ops",
        r"\[Segment :",
        "Depth of Supply Chain",
        "Save Stats",
        r"Save\(\);",
        # Required by _build_query_received_lookup (Source 2) to associate
        # plugin names with query expressions for getPluginRunTimes.
        # Not emitted by any of the known logger names so must be caught here.
        "IBPL body generated for parameterized",
    ]
    _MSG_STARTSWITH_PATTERNS: list = [
        "Finished executing plug-in instance",
        "Got batch-job submit response",
        "Started executing plug-in instance",
        "Finished script execution on",
        "create procedure",
        "create parameterized procedure",
    ]
    _LOGGER_FILTER_PATTERNS: list = [
        # Broad prefix catches ALL SupplyChainSolver sub-loggers (solver.Solver,
        # graph.Graph, plan.Plan, plan.PlanConfig, plan.PlanCache, etc.).
        # getSolverSegmentsDetail / getSolverRunTimes / getSolverPlanCache all
        # filter on SCS_LOGGER_PREFIX as a substring — listing only the five
        # specific fully-qualified names left every other SCS sub-logger evicted.
        SCS_LOGGER_PREFIX,
        SCS_UTIL,
        PLUG,
    ]
    _WARN_NOISE_LOGGERS: list = [
        "server.memory.cache.MemoryNode",  # -ve RefCount spam, purely internal
        "Plugins.RScript.RScriptDynamicArgs",  # misconfigured MaxMessageLength setting, not a query failure
    ]
    def __init__(self):
        self.MESSAGE = "Message"
        self.LOGGER = "Logger"
        self.LEVEL = "Level"
        self.USER_ID = "LUId"
        self._master_filter_re = self._compile_master_filter()

    def _compile_master_filter(self) -> re.Pattern:
        """
        Build one compiled regex from all message filter patterns.
        startswith patterns are anchored with ^ so they behave correctly in alternation.
        """
        parts = []
        for p in self._MSG_FILTER_PATTERNS:
            parts.append(p if re.search(r'[\\()\[\]{}+*?.|^$]', p) else re.escape(p))
        for p in self._MSG_STARTSWITH_PATTERNS:
            parts.append(f"^{re.escape(p)}")
        return re.compile("|".join(parts), re.IGNORECASE)


    def logs_masterfilter(self, logdata: pd.DataFrame, etluser_id: int = None) -> pd.DataFrame:
        """
        Filter the raw log DataFrame to only the rows relevant to QPA.
        Uses a single pre-compiled regex built at __init__ time.

        Error/warn pass-through:
          - ALL Level == ERROR rows are always included.
          - Level == WARN rows are included except those from loggers listed in
            _WARN_NOISE_LOGGERS (MemoryNode refcount spam etc.).
        """
        msg_series   = logdata[self.MESSAGE].astype(str)
        log_series   = logdata[self.LOGGER].astype(str)
        level_series = logdata[self.LEVEL].astype(str)

        msg_filter    = msg_series.str.contains(self._master_filter_re, na=False)
        logger_filter = log_series.str.contains(
            "|".join(map(re.escape, self._LOGGER_FILTER_PATTERNS)),
            case=False, regex=True, na=False,
        )
        o9_logger_filter = (log_series == "o9_logger") & msg_series.str.startswith("No")

        # Pass through all ERROR rows and actionable WARN rows.
        # WARN rows from noise loggers (MemoryNode etc.) are excluded — they are
        # high-volume internal signals with no value in QPA output.
        is_error = level_series == "ERROR"
        is_warn  = level_series == "WARN"
        noise_logger = log_series.str.contains(
            "|".join(map(re.escape, self._WARN_NOISE_LOGGERS)),
            case=False, regex=True, na=False,
        )
        error_warn_filter = is_error | (is_warn & ~noise_logger)

        reject_ddl = msg_series.str.contains(
            r"^Query Received:.*ddl\{", case=False, regex=True, na=False
        )

        combined = (msg_filter | logger_filter | o9_logger_filter | error_warn_filter) & ~reject_ddl
        filtered = logdata[combined].copy()

        if etluser_id is not None:
            filtered = filtered[filtered[self.USER_ID] != etluser_id]

        return filtered

    def extract_ibpl_query_expressions(self, text: str):
        """
        Extract the IBPL query string from a raw log message line.
        Returns (expression, execution_type) or None if the line is not relevant.

        execution_type values:
            "computation"      — any Finished/Started computation line
            "query"            — Query Received: {...}: lines
            "create procedure" — create procedure / create parameterized procedure lines

        Handled computation formats (in priority order):
            1. "Finished computation [N]. Query : <expr> Computation execution time: X s"
               — expression is everything between "Query :" and "Computation execution time:"
            2. "Finished computation [N] Guid [uuid] : <expr>"
               — expression is everything after the colon (GUID-based format, no trailing marker)
            3. "Started computation [N] Guid [uuid] : <expr>"
               — expression is everything after the colon
        """
        if not isinstance(text, str):
            return None
        text = text.strip()

        # Format 1 — "Finished computation [N]. Query : <expr> Computation execution time: X s"
        # Expression ends at "Computation execution time:" so that timing suffix is stripped.
        m = re.match(
            r"Finished computation \[\d+\]\.\s*Query\s*:\s*(.*?)\s*Computation execution time:",
            text, re.DOTALL | re.IGNORECASE,
        )
        if m:
            return m.group(1).strip(), "computation"

        # Format 2 — "Finished computation [N] Guid [uuid] : <expr>"
        m = re.match(
            r"Finished computation \[\d+\] Guid \[[0-9a-fA-F-]+\]\s*:\s*(.*)",
            text, re.DOTALL,
        )
        if m:
            return m.group(1).strip(), "computation"

        # Format 3 — "Started computation [N] Guid [uuid] : <expr>"
        m = re.match(
            r"Started computation \[\d+\] Guid \[[0-9a-fA-F-]+\]\s*:\s*(.*)",
            text, re.DOTALL,
        )
        if m:
            return m.group(1).strip(), "computation"

        # Query Received
        m = re.match(r"Query Received: \{[0-9.]+\}: (.*)", text, re.DOTALL)
        if m:
            return m.group(1).strip(), "query"

        # Create / create parameterized procedure
        lower = text.lower()
        if lower.startswith("create procedure") or lower.startswith("create parameterized procedure"):
            return text, "create procedure"

        return None

    def get_measure_and_dim_attrs_stats_from_tenantlogs(self, logdata: pd.DataFrame):
        """
        :param logdata: tenant_log_csv
        :return: measures global occurence count and number of users referred by count
        """
        logdata = self.logs_masterfilter(logdata)
        logdata["Queries"] = logdata.dropna(subset=["Message"])["Message"].apply(self.extract_ibpl_query_expressions)
        logdata["Queries"] = logdata["Queries"].apply(lambda x: x[0] if isinstance(x, tuple) else x)
        ibpl_query_logs = logdata.dropna(subset=["Queries"])[["Queries", "LUId"]]

        # ------------------------------------------------
        logs_for_measures  = ibpl_query_logs.copy()
        logs_for_measures["Measures"] = logs_for_measures["Queries"].apply(lambda x: re.findall(r"Measure\.\[(.*?)\]", x))
        # print(logs_for_measures)
        measure_logs = logs_for_measures[logs_for_measures["Measures"].map(len) > 0][["Measures", "LUId"]]
        # measure_logs.to_csv("measures_in_query_per_userid.csv", index=False)

        measure_expanded = measure_logs.explode("Measures")
        # print(measure_expanded)
        measure_expanded["Measures"] = measure_expanded["Measures"].str.strip()

        measure_stats = (
            measure_expanded
            .groupby("Measures")
            .agg(
                Global_Freq=("Measures", "size"),
                User_Freq=("LUId", "nunique")
            )
            .reset_index()
            .rename(columns={"Measures": "Measure"})
        )
        measure_stats = measure_stats[["Measure", "Global_Freq", "User_Freq"]]

        #--------------------------------------------------

        def _extract_dimattrs(query_text):
            if not isinstance(query_text, str):
                return []

            # Pattern 1 — fully bracketed: [DimName].[AttrName]
            p1 = re.findall(r"\[([^\]]+)\]\.\[([^\]]+)\]", query_text)

            # Pattern 2 — partially bracketed: DimName.[AttrName]
            # Excludes the keyword "Measure" so Measure.[...] is never captured.
            p2 = re.findall(r"\b(?!Measure\b)([A-Za-z][A-Za-z0-9_]*)\.\[([^\]]+)\]", query_text)

            # Normalise both to [DimName].[AttrName] and deduplicate within the query
            seen = set()
            for dim, attr in p1 + p2:
                seen.add(f"[{dim.strip()}].[{attr.strip()}]")
            return list(seen)

        logs_for_dimattrs = ibpl_query_logs.copy()
        logs_for_dimattrs["DimAttrs"] = logs_for_dimattrs["Queries"].apply(_extract_dimattrs)

        dimattr_logs = logs_for_dimattrs[logs_for_dimattrs["DimAttrs"].map(len) > 0][["DimAttrs", "LUId"]]
        # dimattr_logs.to_csv("dimattrs_in_query_per_userid.csv", index=False)

        dimattr_expanded = dimattr_logs.explode("DimAttrs")
        dimattr_expanded["DimAttrs"] = dimattr_expanded["DimAttrs"].str.strip()

        dimattr_stats = (
            dimattr_expanded
            .groupby("DimAttrs")
            .agg(
                Global_Freq=("DimAttrs", "size"),
                User_Freq=("LUId", "nunique")
            )
            .reset_index()
            .rename(columns={"DimAttrs": "DimAttr"})
        )
        dimattr_stats = dimattr_stats[["DimAttr", "Global_Freq", "User_Freq"]]

        return measure_stats.drop_duplicates(), dimattr_stats.drop_duplicates()


    def get_view_stats_from_adoptionlogs(self, adoptiondata: pd.DataFrame):
        """
        :param adoptiondata: adoption_log_csv
        :return: pages global occurence count and number of users referred by count
        """
        _required = {"View", "User", "UsageDuration"}
        if adoptiondata.empty or not _required.issubset(adoptiondata.columns):
            print("WARNING: Adoption data is empty or missing required columns — returning empty view stats.")
            return pd.DataFrame(columns=["View", "Global_Freq", "User_Freq", "Usage"])

        adoptiondata = adoptiondata[["View", "User", "UsageDuration"]]
        adoptiondata = adoptiondata.dropna(subset=["View"])
        adoptiondata["UsageDuration"] = (
            pd.to_timedelta(adoptiondata["UsageDuration"], errors="coerce")
            .dt.total_seconds()
            .fillna(0)
        )
        adoptiondata["View"] = adoptiondata["View"].str.strip()

        adoption_stats = (
            adoptiondata
            .groupby("View")
            .agg(
                Global_Freq=("View", "size"),
                User_Freq=("User", "nunique"),
                Usage = ("UsageDuration", "sum")
            )
            .reset_index()
        )
        adoption_stats = adoption_stats[["View", "Global_Freq", "User_Freq", "Usage"]]

        return adoption_stats.drop_duplicates()


    def get_widget_stats_from_psrlogs(self, psrdata: pd.DataFrame):
        """
        :param psrdata: psr_log_csv
        :return: widgets global occurence count and number of users referred by count
        """
        _required = {"report", "user_email"}
        if psrdata.empty or not _required.issubset(psrdata.columns):
            print("WARNING: PSR data is empty or missing required columns — returning empty widget stats.")
            return pd.DataFrame(columns=["Widget", "Global_Freq", "User_Freq"])

        psrdata = psrdata[["report", "user_email"]]
        psrdata = psrdata.dropna(subset=["report"])
        psrdata["report"] = psrdata["report"].str.strip()

        psr_stats = (
            psrdata
            .groupby("report")
            .agg(
                Global_Freq=("report", "size"),
                User_Freq=("user_email", "nunique")
            )
            .reset_index()
        )
        psr_stats = psr_stats[["report", "Global_Freq", "User_Freq"]]
        psr_stats = psr_stats.rename(columns={"report": "Widget"})

        return psr_stats.drop_duplicates()


    def get_wml_from_legacy(self, data):
        pagewidgetdata = []
        for workspace in data["Layout"]["Workspaces"]:
            for page in workspace["Pages"]:
                for view in page["Views"]:
                    for viewWidget in view["ViewWidgetDefinitions"]:
                        pagewidgetdata.append({
                            "View": view.get("Title"), #Name
                            "Widget": viewWidget.get("Name"),
                            "WidgetId": viewWidget.get("WidgetDefinitionId")
                        })

        widgetmeasureData = []
        for widget in data["Layout"]["WidgetDefinitions"]:
            matchingWidgetModel = next(
                x for x in data["Layout"]["WidgetModels"]
                if x["Id"] == widget["WidgetModelId"]
            )
            widgetModelConfig = matchingWidgetModel["ConfigJson"]
            MeasList = []
            if "RegularMeasures" in widgetModelConfig:
                MeasList.extend(
                    x for x in widgetModelConfig["RegularMeasures"] if "Name" in x
                )
            if "TransientMeasures" in widgetModelConfig:
                MeasList.extend(
                    x for x in widgetModelConfig["TransientMeasures"] if "Name" in x
                )

            for x in MeasList:
                widgetmeasureData.append({
                    "WidgetId": widget.get("Id"),
                    "Measure": x.get("Name")
                })

        df_pagewidget = pd.DataFrame(pagewidgetdata)
        df_widgetmeasure = pd.DataFrame(widgetmeasureData)
        final_df = pd.merge(
            df_pagewidget,
            df_widgetmeasure,
            on="WidgetId",
            how="outer"
        )
        # final_df.to_csv("test3.csv", index=False)

        return final_df.dropna(subset="View")


    def get_wml_from_splits(self, workspaces, view_widget_definitions, widget_definitions, widget_models):
        pagewidgetdata = []
        for workspace in workspaces:
            for page in workspace["Pages"]:
                for view in page["Views"]:
                    for viewWidget in view_widget_definitions:
                        if viewWidget["ViewId"] == view["Id"]:
                            pagewidgetdata.append({
                                "View": view.get("Title"), #Name
                                "Widget": viewWidget.get("Name"),
                                "WidgetId": viewWidget.get("WidgetDefinitionId")
                            })

        widgetmeasureData = []
        for widget in widget_definitions:
            matchingWidgetModel = next(
                x for x in widget_models
                if x["Id"] == widget["WidgetModelId"]
            )
            widgetModelConfig = matchingWidgetModel["ConfigJson"]
            MeasList = []
            if "RegularMeasures" in widgetModelConfig:
                MeasList.extend(
                    x for x in widgetModelConfig["RegularMeasures"] if "Name" in x
                )
            if "TransientMeasures" in widgetModelConfig:
                MeasList.extend(
                    x for x in widgetModelConfig["TransientMeasures"] if "Name" in x
                )

            for x in MeasList:
                widgetmeasureData.append({
                    "WidgetId": widget.get("Id"),
                    "Measure": x.get("Name")
                })

        df_pagewidget = pd.DataFrame(pagewidgetdata)
        df_widgetmeasure = pd.DataFrame(widgetmeasureData)
        final_df = pd.merge(
            df_pagewidget,
            df_widgetmeasure,
            on="WidgetId",
            how="outer"
        )

        return final_df.dropna(subset="View")


    def get_widgetmeasureslist_from_config(self, configfile: str):
        """
        :param configfile: config zip file path
        :return: relation of page, widget and measures as per the config file
        """
        if not configfile.lower().endswith('.zip'):
            print('Please provide zipped JSON file. You provided ' + configfile)
            raise ValueError('Please provide zipped JSON file')
        inputZip = ZipFile(configfile)
        jsonFilesList = list(
            filter(lambda x: x.lower().endswith('.json'), inputZip.namelist())
        )
        if len(jsonFilesList) == 0:
            print('No JSON file in zip provided -' + configfile)
            raise ValueError('No json file in zip provided')

        if "_legacy.json" in jsonFilesList:
            jsonFileName = "_legacy.json"
            print('Reading json file ' + jsonFileName)
            with inputZip.open(jsonFileName) as dataFile:
                jsonData = json.load(dataFile)

            return self.get_wml_from_legacy(jsonData)

        elif jsonFilesList[0].startswith("o9"):
            jsonFileName = jsonFilesList[0]
            print('Reading json file ' + jsonFileName)
            with inputZip.open(jsonFileName) as dataFile:
                jsonData = json.load(dataFile)

            return self.get_wml_from_legacy(jsonData)

        else:
            print('Reading json files: workspaces.json, view_widget_definitions.json, widget_definitions.json, widget_models.json')
            with inputZip.open("workspaces.json") as wsFile:
                wsData = json.load(wsFile)
            with inputZip.open("view_widget_definitions.json") as vwdFile:
                vwdData = json.load(vwdFile)
            with inputZip.open("widget_definitions.json") as wdFile:
                wdData = json.load(wdFile)
            with inputZip.open("widget_models.json") as wmFile:
                wmData = json.load(wmFile)

            return self.get_wml_from_splits(wsData, vwdData, wdData, wmData)


    def get_md_from_legacy(self, data):
        measuresdata = []
        for plan in data["Plans"]:
            for measuregroup in plan["MeasureGroups"]:
                grain_string = ""
                for dimusages in measuregroup["DimensionUsages"]:
                    curr_grain = f"[{dimusages['DimensionName']}].[{dimusages['AttributeName']}]"
                    if grain_string == "":
                        grain_string = curr_grain
                    else:
                        grain_string += ", " + curr_grain
                for measure in measuregroup["Measures"]:
                    translation_string = []
                    if measure.get("MeasureTranslations", []):
                        for measureT in measure.get("MeasureTranslations", []):
                            translation_string.append(f"{measureT['MeasureName']}")

                    measuresdata.append(
                        {
                            "Measure": measure.get("MeasureName"),
                            "Translation": str(translation_string),
                            "Description": measure.get("MeasureDescription"),
                            "MeasureGroup": measuregroup.get("MeasureGroupName"),
                            "Grain": grain_string,
                        }
                    )

        return pd.DataFrame(measuresdata).dropna(subset="Measure")


    def get_md_from_splits(self, mddata, mgData, duData, mtData):
        duMap = self.build_map(duData,"MeasureGroupId")
        mtMap = self.build_map(mtData,"MeasureId")

        mgroupsdata = []
        for mGroup in mgData:
            grain_string = ""
            for dimusages in duMap.get(mGroup.get("Id"), []):
                curr_grain = f"[{dimusages['DimensionName']}].[{dimusages['AttributeName']}]"
                if grain_string == "":
                    grain_string = curr_grain
                else:
                    grain_string += ", " + curr_grain
            mgroupsdata.append(
                {
                    "MeasureGroup": mGroup.get("MeasureGroupName"),
                    "Grain": grain_string,
                    "Id": mGroup.get("Id"),
                }
            )

        measuresdata = []
        for measure in mddata:
            translation_string = []
            if mtMap.get(measure.get("Id"), []):
                for mtElement in mtMap.get(measure.get("Id"), []):
                    translation_string.append(f"{mtElement['MeasureName']}")
            measuresdata.append(
                {
                    "Measure": measure.get("MeasureName"),
                    "Translation": str(translation_string),
                    "Description": measure.get("MeasureDescription"),
                    "MGId": measure.get("MeasureGroupId")
                }
            )

        df_mgroups = pd.DataFrame(mgroupsdata)
        df_measures = pd.DataFrame(measuresdata)
        final_df = pd.merge(
            df_mgroups,
            df_measures,
            left_on="Id",
            right_on="MGId",
            how="outer"
        )

        return final_df.dropna(subset="Measure")


    def get_measuredescriptions_from_config(self, configfile: str):
        """
        :param configfile: config zip file path
        :return: relation of measures and their descriptions as per the config file
        """
        if not configfile.lower().endswith('.zip'):
            print('Please provide zipped JSON file. You provided ' + configfile)
            raise ValueError('Please provide zipped JSON file')
        inputZip = ZipFile(configfile)
        jsonFilesList = list(
            filter(lambda x: x.lower().endswith('.json'), inputZip.namelist())
        )
        if len(jsonFilesList) == 0:
            print('No JSON file in zip provided -' + configfile)
            raise ValueError('No json file in zip provided')

        if "_legacy.json" in jsonFilesList:
            jsonFileName = "_legacy.json"
            print('Reading json file ' + jsonFileName)
            with inputZip.open(jsonFileName) as dataFile:
                jsonData = json.load(dataFile)

            return self.get_md_from_legacy(jsonData)

        elif jsonFilesList[0].startswith("o9"):
            jsonFileName = jsonFilesList[0]
            print('Reading json file ' + jsonFileName)
            with inputZip.open(jsonFileName) as dataFile:
                jsonData = json.load(dataFile)

            return self.get_md_from_legacy(jsonData)

        else:
            print('Reading json file: measures.json')
            with inputZip.open("measures.json") as mdFile:
                mdData = json.load(mdFile)
            with inputZip.open("measure_groups.json") as mgFile:
                mgData = json.load(mgFile)
            with inputZip.open("dimension_usages.json") as duFile:
                duData = json.load(duFile)
            with inputZip.open("measure_translations.json") as duFile:
                mtData = json.load(duFile)

            return self.get_md_from_splits(mdData, mgData, duData, mtData)

    def build_map(self, data_list, key_field):
        result_map = defaultdict(list)

        for row in data_list:
            if key_field in row:
                result_map[row[key_field]].append(row)

        return result_map