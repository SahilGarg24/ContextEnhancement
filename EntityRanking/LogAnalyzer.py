import math

from antlr4 import CommonTokenStream
from ibpl_grammar_listener.o9IBPLLexer import o9IBPLLexer
from urllib.parse import urlparse
from ibpl_grammar_listener.o9IBPLParser import o9IBPLParser
from ibpl_grammar_listener.QuerySegregatorListener import (
    QueryInfoListener, ListErrorReporter, SyntaxError, ErrorStrategy
)
from ibpl_grammar_listener.CaseInsensitiveStringStream import CaseInsensitiveStringStream
from antlr4.tree.Tree import ParseTreeWalker
# from CCM_Common_Utils import common_utils
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import re, os
import hashlib
import pandas as pd
from pandas import DataFrame, options, concat, merge
from collections import defaultdict
from re import sub
from dateutil import tz
from time import time
from datetime import datetime
from logging import getLogger

options.mode.chained_assignment = None
common_utils=""

# ---------------------------------------------------------------------------
# Column name constants
# ---------------------------------------------------------------------------
MESSAGE             = "Message"
SERVER              = "Server"
LOGGER              = "Logger"
RID                 = "RId"
SID                 = "SId"
USER_ID             = "LUId"
TIMESTAMP           = "Timestamp"
LEVEL               = "Level"
THREAD              = "Thread"
DAY                 = "Day"

SCS_PLAN_CONFIG     = "o9.GraphCube.Plugins.SupplyChainSolver.plan.PlanConfig"
SCS_PLAN_CACHE      = "o9.GraphCube.Plugins.SupplyChainSolver.plan.PlanCache"
SCS_UTIL            = "o9.GraphCube.util.Utilities"
PLUG                = "o9.GraphCube.Plugins.AbstractPlugin"
SCS_PLAN            = "o9.GraphCube.Plugins.SupplyChainSolver.plan.Plan"
SCS_LOGGER_PREFIX   = "o9.GraphCube.Plugins.SupplyChainSolver."
_LOGGER             = "o9_logger"

READ_TIME           = "Read Time"
PROCESSING_TIME     = "Processing time"
WRITE_TIME          = "Write Time"
PLUGIN_NAME         = "Plugin Name"
QUERY               = "Query"
START_TIME          = "StartTime"
END_TIME            = "EndTime"
VERSION_SAVE        = "VersionToSave"
NUM_EXECUTORS       = "NumberOfSaveExecutedForDay"
DUR_IN_MINUTES      = "DurationInMinutes"
DUR_MM_SS           = "DurationMMSS"
INVOCATIONS         = "Invocations"
EXECUTIONS          = "Executions"
NUM_OPS             = "Number Of Non Null Ops"
PLUGIN_RUN_DIVISION = "Plugin Run Division"
PLUGIN_RUN_DURATION = "Plugin Run Duration"

Records             = "Records"
Value               = "Value"
AGG_VAL             = False
Category            = "Category"
Solver_Parameter    = True
Format              = "%Y-%m-%d"
max_characters      = 4000

# ---------------------------------------------------------------------------
# Empty-DataFrame column schemas for each output file type
# ---------------------------------------------------------------------------
_OUTPUT_SCHEMAS = {
    "Queries": [
        RID, THREAD, USER_ID, QUERY, START_TIME, END_TIME,
        DUR_IN_MINUTES, DUR_MM_SS, DAY,
    ],
    "Computation": [
        RID, THREAD, USER_ID, QUERY, DUR_IN_MINUTES, DUR_MM_SS,
        INVOCATIONS, EXECUTIONS, NUM_OPS, START_TIME, DAY,
    ],
    "SegmentedSolverDetails": [
        RID, THREAD, USER_ID, QUERY, DUR_IN_MINUTES, DUR_MM_SS, START_TIME, DAY,
    ],
    "SolverRunTimes": [
        RID, THREAD, USER_ID, QUERY, DUR_IN_MINUTES, DUR_MM_SS,
        Records, START_TIME, DAY, PLUGIN_NAME, PLUGIN_RUN_DIVISION, PLUGIN_RUN_DURATION,
    ],
    "SolverStats": [RID, THREAD, USER_ID, DAY, QUERY, Value, Category],
    "SaveStats":   [DAY, START_TIME, END_TIME, VERSION_SAVE, NUM_EXECUTORS],
    "ErrorStats":  [RID, QUERY, "Error", "Exception"],
}

# ---------------------------------------------------------------------------
# Duration formatting helper
# ---------------------------------------------------------------------------
def _format_mmss(total_seconds) -> str:
    """Format a numeric seconds value as MM:SS. Returns '' for None/NaN."""
    try:
        s   = float(total_seconds)
        m   = int(s // 60)
        sec = int(round(s % 60))
        return f"{m:02}:{sec:02}"
    except (TypeError, ValueError):
        return ""


# ---------------------------------------------------------------------------
# Module-level worker — must NOT be an instance method so ProcessPoolExecutor
# can pickle it without dragging the whole LogAnalyzer instance along.
# ---------------------------------------------------------------------------
# def _apply_segregation_worker(expression: str) -> list[dict]:
#     """
#     Parse and walk one IBPL expression in a worker process.
#     Always returns a plain list of result dicts (never a tuple).
#     """
#     input_stream = CaseInsensitiveStringStream(expression)
#     lexer        = o9IBPLLexer(input_stream)
#     token_stream = CommonTokenStream(lexer)
#     parser       = o9IBPLParser(token_stream)
#
#     error_reporter = ListErrorReporter(raise_on_error=True)
#     parser.removeErrorListeners()
#     parser.addErrorListener(error_reporter)
#     parser._errHandler = ErrorStrategy()
#
#     try:
#         tree = parser.statement()
#     except Exception as e:
#         print(f"[parse error] {e!r:.120}")
#         return []
#
#     listener = QueryInfoListener(members_only=False)
#     walker   = ParseTreeWalker()
#     try:
#         walker.walk(listener, tree)
#         return listener.results
#     except Exception as e:
#         print(f"[walk error] {e!r:.120}")
#         return []

def _apply_segregation_worker_batch(batch: list[tuple[str, str, str]]) -> list[dict]:
    """
    Parse and walk a batch of (expression, rid, exec_type) in one worker call.
    """
    batch_results = []

    for expression, rid, exec_type in batch:
        input_stream = CaseInsensitiveStringStream(expression)
        lexer        = o9IBPLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser       = o9IBPLParser(token_stream)

        error_reporter = ListErrorReporter(raise_on_error=True)
        parser.removeErrorListeners()
        parser.addErrorListener(error_reporter)
        parser._errHandler = ErrorStrategy()

        try:
            tree = parser.statement()
        except Exception as e:
            print(f"[parse error] rid={rid} {e!r:.120}")
            continue  # skip bad record, don't kill the whole batch

        listener = QueryInfoListener(members_only=False)
        walker   = ParseTreeWalker()
        try:
            walker.walk(listener, tree)
            for r in listener.results:
                r[RID]              = rid
                r["execution_type"] = exec_type
            batch_results.extend(listener.results)
        except Exception as e:
            print(f"[walk error] rid={rid} {e!r:.120}")
            continue

    return batch_results
# ===========================================================================
# LogAnalyzer
# ===========================================================================
class LogAnalyzer:

    # -----------------------------------------------------------------------
    # Configurable filter pattern lists.
    # Kept as class attributes so they can be overridden per-instance if needed.
    # -----------------------------------------------------------------------
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

    def __init__(self):
        self.logger = getLogger("o9_logger")
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

    # -----------------------------------------------------------------------
    # Internal utilities
    # -----------------------------------------------------------------------

    def _safe_call(self, func, *args, label: str = "") -> pd.DataFrame:
        """Call func(*args); return an empty DataFrame on any exception."""
        try:
            result = func(*args)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            self.logger.info(f"Error in {label}: {e}")
            return pd.DataFrame()

    def _build_post_filename(self, tenant_metadata: dict) -> tuple[dict, str]:
        """
        Extract tenant keys and build the canonical PostFileName string.
        Returns (tenant_details_dict, post_filename).
        """
        keys = ["CustomerName", "TenantID", "TenantName", "EnviName"]
        tenant_details = {k: tenant_metadata[k] for k in keys}
        intermediate_suffix = (
            f"{tenant_metadata['TenantID']}"
            f"_{tenant_metadata['TenantName']}"
            f"_{tenant_metadata['EnviName']}"
        ).replace("-", "_")
        post_filename = f"{tenant_metadata['CustomerName']}_{intermediate_suffix}"
        return tenant_details, post_filename

    def _save_output(
        self,
        df: pd.DataFrame,
        prefix: str,
        post_filename: str,
        outputfolderpath: str,
        tenant_details: dict,
        utils,
        sort_by: str = None,
        clean_whitespace: bool = False,
    ) -> None:
        """
        Enrich df with tenant columns, optionally sort/clean, then save to cloud.
        Falls back to an empty DataFrame with the correct schema if df is empty/None.
        """
        if df is None or len(df) == 0:
            df = pd.DataFrame(columns=_OUTPUT_SCHEMAS[prefix])
        else:
            if sort_by:
                df.sort_values(by=sort_by, ascending=False, inplace=True)
            if clean_whitespace:
                df = df.replace(r"\r+|\n+|\t+", " ", regex=True)

        try:
            df = self.adding_extra_column_attributes(df, tenant_details)
        except Exception as e:
            self.logger.info(f"Exception while adding columns for {prefix}: {e}")

        file_path = f"{outputfolderpath.rstrip('/')}/{prefix}_{post_filename}.csv"
        filename, status = utils.save_df_as_file_in_cloud(df, file_path, separator=",")
        self.logger.info(f"Saved {filename}, status: {status}")

    def _run_and_save_all(
        self,
        logData: pd.DataFrame,
        tenant_details: dict,
        post_filename: str,
        outputfolderpath: str,
        utils,
    ) -> None:
        """
        Run QPA core and save every output file.
        Shared by QPA_Analysis (file-based) and QPA_Analysis_local (DataFrame-based).
        """
        (
            queriesDF, computationDF, segmentedSolverDF,
            solverRunTimesDF, SolverPlanCacheDF, SaveStat, errorStatsDF,
        ) = self._run_qpa_core(logData)

        self._save_output(
            queriesDF,         "Queries",                post_filename, outputfolderpath,
            tenant_details, utils, sort_by=DUR_IN_MINUTES, clean_whitespace=True,
        )
        self._save_output(
            computationDF,     "Computation",            post_filename, outputfolderpath,
            tenant_details, utils, sort_by=DUR_IN_MINUTES,
        )
        self._save_output(
            segmentedSolverDF, "SegmentedSolverDetails", post_filename, outputfolderpath,
            tenant_details, utils, sort_by=DUR_IN_MINUTES,
        )
        self._save_output(
            solverRunTimesDF,  "SolverRunTimes",         post_filename, outputfolderpath,
            tenant_details, utils,
        )
        self._save_output(
            SolverPlanCacheDF, "SolverStats",            post_filename, outputfolderpath,
            tenant_details, utils,
        )
        self._save_output(
            SaveStat,          "SaveStats",              post_filename, outputfolderpath,
            tenant_details, utils,
        )

    # -----------------------------------------------------------------------
    # Public: QPA Analysis — cloud file input
    # -----------------------------------------------------------------------

    def QPA_Analysis(self, jsonfilepath: str, csvfilepath: str, outputfolderpath: str) -> None:
        """
        Central CCM mode.
        Reads tenant JSON and log CSV from cloud storage, runs QPA, saves output files.
        """
        try:
            tenant_details_raw = self.read_json_from_path(jsonfilepath)
            if tenant_details_raw is None:
                self.logger.info(f"Could not read JSON file: {jsonfilepath}")
                return

            tenant_details, post_filename = self._build_post_filename(tenant_details_raw)
            self.logger.info(f"PostFileName: {post_filename}")

            init_time = time()
            utils     = common_utils(self.logger)
            logData   = utils.read_file_as_df_from_cloud(csvfilepath, separator=",", dtype=None, quotechar='"')

            self._run_and_save_all(logData, tenant_details, post_filename, outputfolderpath, utils)
            self.logger.info(f"Time Taken: {time() - init_time:.2f}s")

        except pd.errors.EmptyDataError as e:
            self.logger.info(f"Empty data error: {e}")
        except Exception as e:
            self.logger.info(f"An error occurred in QPA_Analysis: {e}")

    # -----------------------------------------------------------------------
    # Public: QPA Analysis — local DataFrame input
    # -----------------------------------------------------------------------

    def QPA_Analysis_local(
        self,
        log_dataframe: pd.DataFrame,
        tenant_metadata: dict,
        outputfolderpath: str,
    ) -> None:
        """
        Local CCM mode.
        Accepts logs as a pandas DataFrame (already fetched from the API).
        No file reading; everything else mirrors QPA_Analysis exactly.
        """
        try:
            if log_dataframe is None or tenant_metadata is None:
                raise ValueError(
                    "log_dataframe and tenant_metadata are required for QPA_Analysis_local"
                )

            self.logger.info("QPA_Analysis_local running in LOCAL (DataFrame) mode")
            tenant_details, post_filename = self._build_post_filename(tenant_metadata)
            self.logger.info(f"PostFileName (LOCAL mode): {post_filename}")

            init_time = time()
            utils     = common_utils(self.logger)
            logData   = log_dataframe.copy()

            self._run_and_save_all(logData, tenant_details, post_filename, outputfolderpath, utils)
            self.logger.info(f"Time Taken: {time() - init_time:.2f}s")

        except Exception as e:
            self.logger.info(f"An error occurred in QPA_Analysis_local: {e}")

    # -----------------------------------------------------------------------
    # Public: obfuscation
    # -----------------------------------------------------------------------

    def obfuscate_entries(self, logdata: pd.DataFrame) -> pd.DataFrame:
        """
        Replace sensitive business data (member names) in log messages with
        short SHA-256 hashes.
        """
        logdata = logdata.copy()
        # extract_ibpl_query_expressions now returns (expr, exec_type) tuples;
        # obfuscation only needs the expression string.
        logdata["ibpl_expr"] = logdata[MESSAGE].apply(
            lambda m: (self.extract_ibpl_query_expressions(m) or (None,))[0]
        )
        filtered_column      = logdata.dropna(subset=["ibpl_expr"])[["ibpl_expr"]]

        master_member: set = set()
        bad_rows:      set = set()

        for idx, expr in filtered_column["ibpl_expr"].items():
            try:
                self.extract_members_or_fact(expr, master_member)
            except ValueError:
                bad_rows.add(idx)

        if bad_rows:
            self.logger.info(f"Dropping {len(bad_rows)} invalid IBPL rows...")
            logdata = logdata.drop(index=list(bad_rows))

        obfuscated = self.hash_sensitive_data(logdata=logdata, memberset=master_member)
        return obfuscated.drop("ibpl_expr", axis=1)

    # -----------------------------------------------------------------------
    # Public: master filter
    # -----------------------------------------------------------------------

    # Logger substrings whose WARN rows carry no actionable information and are
    # excluded from the error/warn pass-through to keep ErrorStats clean.
    _WARN_NOISE_LOGGERS: list = [
        "server.memory.cache.MemoryNode",   # -ve RefCount spam, purely internal
        "Plugins.RScript.RScriptDynamicArgs",  # misconfigured MaxMessageLength setting, not a query failure
    ]

    def logs_masterfilter(self, logdata: pd.DataFrame, etluser_id: int = None) -> pd.DataFrame:
        """
        Filter the raw log DataFrame to only the rows relevant to QPA.
        Uses a single pre-compiled regex built at __init__ time.

        Error/warn pass-through:
          - ALL Level == ERROR rows are always included.
          - Level == WARN rows are included except those from loggers listed in
            _WARN_NOISE_LOGGERS (MemoryNode refcount spam etc.).
        """
        msg_series   = logdata[MESSAGE].astype(str)
        log_series   = logdata[LOGGER].astype(str)
        level_series = logdata[LEVEL].astype(str)

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
            filtered = filtered[filtered[USER_ID] != etluser_id]

        return filtered

    # -----------------------------------------------------------------------
    # log_analyzer_controller
    # -----------------------------------------------------------------------

    def log_analyzer_controller(self, logdata: pd.DataFrame, max_workers: int = os.cpu_count(), load_balancing_factor: int = 6):
        """
        Run the full pipeline: filter → IBPL extraction → QPA.
        Returns (query_info_df, queriesDF, computationDF, segmentedSolverDF,
                 solverRunTimesDF, SolverPlanCacheDF, SaveStat).
        """
        currlogdata = logdata.copy()

        filtered_logs = self.logs_masterfilter(currlogdata)
        print(f"Length of filtered logs: {len(filtered_logs)}")
        self.logger.info(f"Length of filtered logs: {len(filtered_logs)}")
        qpa_input = filtered_logs.copy()

        # Unpack (expression, execution_type) tuples; rows that return None are dropped.
        parsed = filtered_logs[MESSAGE].apply(self.extract_ibpl_query_expressions)
        filtered_logs["ibpl_expr"]      = parsed.apply(lambda v: v[0] if v is not None else None)
        filtered_logs["execution_type"] = parsed.apply(lambda v: v[1] if v is not None else None)

        valid         = filtered_logs.dropna(subset=["ibpl_expr"])
        expr_meta     = list(zip(valid["ibpl_expr"], valid[RID], valid["execution_type"]))
        self.logger.info(f"Expressions to process: {len(expr_meta)}")
        print(f"Expressions to process: {len(expr_meta)}")
        self.logger.info(f"Using {max_workers} worker processes")

        final_results: list[dict] = []
        # ── # records per worker task ────────────────────────────────────────
        BATCH_SIZE = math.ceil( len(expr_meta) / (max_workers * load_balancing_factor) )
        print(f"Worked out batch size: {BATCH_SIZE}")
        self.logger.info(f"Worked out batch size: {BATCH_SIZE}")

        def _make_batches(items, batch_size):
            for i in range(0, len(items), batch_size):
                yield items[i: i + batch_size]

        with ProcessPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(_apply_segregation_worker_batch, batch): batch
                for batch in _make_batches(expr_meta, BATCH_SIZE)
            }

            for future in as_completed(futures):
                try:
                    rows = future.result()  # already has rid + exec_type stamped in
                    final_results.extend(rows)
                    print("A batch got completed and results are collected")
                except Exception as e:
                    self.logger.info(f"[future error] {e!r:.120}")
                    print(f"[future error] {e!r:.120}")

        # with ProcessPoolExecutor(max_workers=max_workers) as pool:
        #     # Map each future back to the (rid, execution_type) of its source row.
        #     futures = {
        #         pool.submit(_apply_segregation_worker, expr): (rid, exec_type)
        #         for expr, rid, exec_type in expr_meta
        #     }
        #     for future in as_completed(futures):
        #         # completed += 1
        #         # if completed % 500 == 0:
        #         #     self.logger.info(f"  {completed}/{len(expr_meta)} done …")
        #         rid, exec_type = futures[future]
        #         try:
        #             rows = future.result()
        #             for r in rows:
        #                 r[RID]              = rid
        #                 r["execution_type"] = exec_type
        #             final_results.extend(rows)
        #         except Exception as e:
        #             self.logger.info(f"[future error] {e!r:.120}")
        #             print(f"[future error] {e!r:.120}")

        self.logger.info(f"Total results collected: {len(final_results)}")
        print(f"Total results collected: {len(final_results)}")

        query_info_file = pd.DataFrame(
            columns=[
                RID, "execution_type",
                "query", "query_type", "dim_attrs", "named_sets", "measures",
                "coalesce_measures", "lead_offsets", "filters", "object", "arguments", "formulae", "members",
            ],
            data=final_results,
        )

        (
            queriesDF, computationDF, segmentedSolverDF,
            solverRunTimesDF, SolverPlanCacheDF, SaveStat, errorStatsDF,
        ) = self._run_qpa_core(qpa_input)

        return (
            query_info_file, queriesDF, computationDF,
            segmentedSolverDF, solverRunTimesDF, SolverPlanCacheDF, SaveStat, errorStatsDF,
        )

    # -----------------------------------------------------------------------
    # IBPL extraction & member collection
    # -----------------------------------------------------------------------

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

    def extract_members_or_fact(self, expression: str, memberset: set) -> None:
        """
        Parse an IBPL expression and add all member names to memberset.
        Raises ValueError if parsing fails.
        """
        input_stream = CaseInsensitiveStringStream(expression)
        lexer        = o9IBPLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser       = o9IBPLParser(token_stream)

        parser.removeErrorListeners()
        parser.addErrorListener(ListErrorReporter(raise_on_error=True))

        try:
            tree = parser.statement()
        except Exception:
            raise ValueError("INVALID_IBPL_EXPRESSION")

        listener = QueryInfoListener(members_only=True)
        walker   = ParseTreeWalker()
        try:
            walker.walk(listener, tree)
        except Exception as e:
            self.logger.info(f"Exception while walking the parse tree: {e}")
            return

        for result in listener.results:
            memberset.update(result.get("members", []))

    def hash_sensitive_data(self, logdata: pd.DataFrame, memberset: set) -> pd.DataFrame:
        """
        Replace every member name in the Message column with a 16-char SHA-256 digest.
        """
        clean_members = [
            m.strip('"').lstrip("[").rstrip("]")
            for m in memberset
            if m is not None
        ]
        if not clean_members:
            return logdata

        member_hash_map = {
            m: hashlib.sha256(m.encode("utf-8")).hexdigest()[:16]
            for m in clean_members
        }
        pattern = re.compile("|".join(re.escape(m) for m in clean_members))
        logdata[MESSAGE] = (
            logdata[MESSAGE]
            .astype(str)
            .apply(lambda msg: pattern.sub(lambda match: member_hash_map[match.group(0)], msg))
        )
        return logdata

    # -----------------------------------------------------------------------
    # Cloud I/O helpers
    # -----------------------------------------------------------------------

    def get_base_path(self, file_path: str, depth: int = 2) -> str:
        parsed     = urlparse(file_path)
        path_parts = parsed.path.strip("/").split("/")
        return f"{parsed.scheme}://{parsed.netloc}/{'/'.join(path_parts[:depth])}"

    def read_json_from_path(self, file_path: str):
        self.logger.info(f"Attempting to read JSON from path: {file_path}")
        base_path = self.get_base_path(file_path)
        try:
            if file_path.startswith("gs://"):
                import gcsfs
                fs = gcsfs.GCSFileSystem()
                with fs.open(file_path, "r") as f:
                    return json.load(f)
            elif file_path.startswith(("abfss://", "abfs://")):
                import adlfs
                account = base_path.split("@")[1].split(".dfs")[0]
                fs = adlfs.AzureBlobFileSystem(account_name=account, anon=False)
                with fs.open(file_path, "r") as f:
                    return json.load(f)
            else:
                with open(file_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to read or parse JSON from {file_path}: {e}")
            return None

    # -----------------------------------------------------------------------
    # QPA core
    # -----------------------------------------------------------------------

    def _run_qpa_core(self, logData: pd.DataFrame):
        """
        Run all QPA sub-analyses on a filtered log DataFrame.
        Returns a 7-tuple: (queriesDF, computationDF, segmentedSolverDF,
                             solverRunTimesDF, SolverPlanCacheDF, SaveStat,
                             errorStatsDF).
        Each element is always a DataFrame (possibly empty).
        """
        if len(logData) == 0:
            self.logger.info("No data found for the time specified.")
            return tuple(pd.DataFrame() for _ in range(7))

        logData = logData.reset_index()
        self.logger.info(f"Timestamp dtype before conversion: {logData[TIMESTAMP].dtype}")
        logData[TIMESTAMP] = pd.to_datetime(logData[TIMESTAMP], errors="coerce", utc=True)
        self.logger.info(f"Timestamp dtype after conversion:  {logData[TIMESTAMP].dtype}")
        logData = logData.dropna(subset=[TIMESTAMP])

        queriesDF         = self._safe_call(self.getQueries,              logData, label="getQueries")
        computationDF     = self._safe_call(self.getComputations,         logData, label="getComputations")
        segmentedSolverDF = self._safe_call(self.getSolverSegmentsDetail, logData, label="getSolverSegmentsDetail")
        solverRunTimesDF  = self._safe_call(self.getCombinedRunTimes,     logData, label="getCombinedRunTimes")
        SolverPlanCacheDF = self._safe_call(self.getSolverPlanCache,      logData, label="getSolverPlanCache")
        SaveStat          = self._safe_call(self.getSaveStat,             logData, label="getSaveStat")
        errorStatsDF      = self._safe_call(self.getErrorStats,           logData, label="getErrorStats")

        return queriesDF, computationDF, segmentedSolverDF, solverRunTimesDF, SolverPlanCacheDF, SaveStat, errorStatsDF

    # -----------------------------------------------------------------------
    # Queries — vectorized via merge
    # -----------------------------------------------------------------------

    def getQueries(self, _data: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Getting Queries...")

        uid        = "_uid"
        start_logs = _data[_data[MESSAGE].str.contains("Query Received: {", regex=False, na=False)].copy()
        end_logs   = _data[_data[MESSAGE].str.contains("CPU TIME: {",       regex=False, na=False)].copy()

        if start_logs.empty:
            return pd.DataFrame()

        start_logs[uid]          = start_logs[MESSAGE].str.split(":", n=2).str[1]
        end_split                = end_logs[MESSAGE].str.split(":", n=3)
        end_logs[uid]            = end_split.str[1]
        end_logs[DUR_IN_MINUTES] = (
            end_split.str[2].str.replace("ms", "", regex=False).str.strip().astype(float) / 60000
        )

        merged = merge(
            start_logs,
            end_logs[[uid, TIMESTAMP, DUR_IN_MINUTES]],
            on=uid, how="left", suffixes=("", "_end"),
        )

        merged[QUERY] = (
            merged[MESSAGE]
            .str.replace(r"Query Received: \{.*?\}:", "", regex=True)
            .str.replace("^", "", regex=False)
            .str.strip()
            .str[:max_characters]
        )
        merged[DUR_IN_MINUTES] = merged[DUR_IN_MINUTES].fillna(0).round(4)
        merged[DUR_MM_SS]      = (merged[DUR_IN_MINUTES] * 60).apply(_format_mmss)
        merged[START_TIME]     = merged[TIMESTAMP].dt.tz_convert(tz.tzlocal())
        merged[END_TIME]       = (
            pd.to_datetime(merged[f"{TIMESTAMP}_end"], utc=True, errors="coerce")
            .dt.tz_convert(tz.tzlocal())
        )
        merged[DAY] = merged[TIMESTAMP].dt.strftime(Format)

        return merged[[RID, THREAD, USER_ID, QUERY, START_TIME, END_TIME, DUR_IN_MINUTES, DUR_MM_SS, DAY]]

    # -----------------------------------------------------------------------
    # Computations — vectorized (three sources consolidated)
    # -----------------------------------------------------------------------

    def getComputations(self, _data: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Getting Computations...")
        parts = []

        # Part 1 — SCS solver ms-lines
        scs = _data[
            (_data[LOGGER] == SCS_PLAN_CONFIG) & _data[MESSAGE].str.endswith("ms", na=False)
        ].copy()
        if not scs.empty:
            tmp                  = scs[MESSAGE].str.split("time", n=1)
            scs[QUERY]           = ("Plugin instance SupplyChainSolver " + tmp.str[0].str.strip()).str[:max_characters]
            scs[DUR_IN_MINUTES]  = (tmp.str[1].str.replace("ms", "", regex=False).str.strip().astype(float) / 60000).round(4)
            scs[DUR_MM_SS]       = (scs[DUR_IN_MINUTES] * 60).apply(_format_mmss)
            scs[INVOCATIONS]     = None
            scs[EXECUTIONS]      = None
            scs[NUM_OPS]         = None
            scs[START_TIME]      = scs[TIMESTAMP].dt.tz_convert(tz.tzlocal())
            scs[DAY]             = scs[TIMESTAMP].dt.strftime(Format)
            parts.append(scs[[RID, THREAD, USER_ID, QUERY, DUR_IN_MINUTES, DUR_MM_SS,
                               INVOCATIONS, EXECUTIONS, NUM_OPS, START_TIME, DAY]])

        # Part 2 — Computation execution time logs (vectorized prev-row join)
        comp = _data[_data[MESSAGE].str.contains("Computation execution time", regex=False, na=False)].copy()
        if not comp.empty:
            comp[DUR_IN_MINUTES] = (
                comp[MESSAGE]
                .str.extract(r"Computation execution time:\s*([\d.,]+)\s*s", expand=False)
                .str.replace(",", "", regex=False)
                .astype(float) / 60
            ).round(4)

            has_query    = comp[MESSAGE].str.contains("Query :", regex=False, na=False)
            has_finished = ~has_query & comp[MESSAGE].str.contains(
                "Finished executing plug-in instance", regex=False, na=False
            )
            comp[QUERY] = None
            comp.loc[has_query, QUERY] = (
                comp.loc[has_query, MESSAGE]
                .str.split("Query :", n=1).str[1]
                .str.split("Computation execution time", n=1).str[0]
                .str.replace("^", "", regex=False).str.strip().str[:max_characters]
            )
            comp.loc[has_finished, QUERY] = (
                "Plugin instance " +
                comp.loc[has_finished, MESSAGE]
                .str.split("Finished executing plug-in instance", n=1).str[1]
                .str.split("Computation execution time", n=1).str[0]
                .str.strip()
            ).str[:max_characters]

            comp[DUR_MM_SS]  = (comp[DUR_IN_MINUTES] * 60).apply(_format_mmss)
            comp[START_TIME] = comp[TIMESTAMP].dt.tz_convert(tz.tzlocal())
            comp[DAY]        = comp[TIMESTAMP].dt.strftime(Format)

            invoc_re = re.compile(
                r"invocations:\s*(\d+);\s*executions:\s*(\d+);\s*non-null no ops:\s*(\d+)",
                re.IGNORECASE,
            )
            prev_msgs = _data[MESSAGE].reindex(comp.index - 1)
            prev_msgs.index = comp.index
            extracted = prev_msgs.str.extract(invoc_re, expand=True)
            extracted.columns = [INVOCATIONS, EXECUTIONS, NUM_OPS]
            comp[[INVOCATIONS, EXECUTIONS, NUM_OPS]] = extracted.values

            missing = comp[INVOCATIONS].isna()
            if missing.any():
                prev2_msgs = _data[MESSAGE].reindex(comp.index[missing] - 2)
                prev2_msgs.index = comp.index[missing]
                extracted2 = prev2_msgs.str.extract(invoc_re, expand=True)
                extracted2.columns = [INVOCATIONS, EXECUTIONS, NUM_OPS]
                comp.loc[missing, [INVOCATIONS, EXECUTIONS, NUM_OPS]] = extracted2.values

            parts.append(comp[[RID, THREAD, USER_ID, QUERY, DUR_IN_MINUTES, DUR_MM_SS,
                                INVOCATIONS, EXECUTIONS, NUM_OPS, START_TIME, DAY]])

        # Part 3 — AbstractPlugin Elapsed Compute Time
        active = _data[
            (_data[LOGGER] == PLUG) & _data[MESSAGE].str.contains("Elapsed Compute Time", na=False)
        ].copy()
        if not active.empty:
            tmp                  = active[MESSAGE].str.split("=", n=1)
            active[QUERY]        = tmp.str[0].str.replace("^", "", regex=False).str[:max_characters]
            active[DUR_IN_MINUTES] = (tmp.str[1].str.replace("s", "", regex=False).str.strip().astype(float) / 60).round(4)
            active[DUR_MM_SS]    = (active[DUR_IN_MINUTES] * 60).apply(_format_mmss)
            active[INVOCATIONS]  = ""
            active[EXECUTIONS]   = ""
            active[NUM_OPS]      = ""
            active[START_TIME]   = active[TIMESTAMP].dt.tz_convert(tz.tzlocal())
            active[DAY]          = active[TIMESTAMP].dt.strftime(Format)
            parts.append(active[[RID, THREAD, USER_ID, QUERY, DUR_IN_MINUTES, DUR_MM_SS,
                                  INVOCATIONS, EXECUTIONS, NUM_OPS, START_TIME, DAY]])

        return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()

    # -----------------------------------------------------------------------
    # Solver segments — LogParser approach
    #
    # Replaces: getSolverSegmentsDetail (flag/index-based) + getSegmentApply
    # With:     solver-run detection by RId+Thread (avoids cross-contamination),
    #           _extract_relevant_solver_details for structured segment content,
    #           per-segment start/end timing kept from original logic.
    # -----------------------------------------------------------------------

    def getSolverSegmentsDetail(self, _data: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Getting Solver Data...")

        scs_logs = _data[
            _data[LOGGER].str.contains(SCS_LOGGER_PREFIX, na=False, regex=False)
        ]
        if scs_logs.empty:
            return pd.DataFrame()

        msgs             = scs_logs[MESSAGE]
        solver_start_log = scs_logs[msgs.str.contains("Started plan execution of plugin",  na=False, regex=False)]
        solver_end_log   = scs_logs[msgs.str.contains("Total Solver run time",             na=False, regex=False)]

        output_dict = defaultdict(list)

        for start_idx, detail in solver_start_log.iterrows():
            rid    = detail[RID]
            thread = detail[THREAD]

            end_candidates = solver_end_log[
                (solver_end_log.index > start_idx)
                & (solver_end_log[RID] == rid)
                & (solver_end_log[THREAD] == thread)
            ]
            if end_candidates.empty:
                self.logger.info(f"Incomplete solver log for RId {rid}; skipping.")
                continue

            end_idx      = end_candidates.index[-1]
            solver_slice = scs_logs.loc[start_idx:end_idx]
            solver_msgs  = solver_slice[MESSAGE]

            # Depth per segment — lightweight scalar, not redundant with SolverStats
            solver_depth = solver_msgs.str.extractall(
                r"Segment:\s*\[(\d+)\]\.\s*Depth of Supply Chain\s*is\s*:\s*(?P<depth>\d+)$"
            ).reset_index(drop=True)
            solver_depth.columns = ["Segment", "Depth"]
            depth_lookup = (
                solver_depth.set_index("Segment")["Depth"].to_dict()
                if not solver_depth.empty else {}
            )

            # Per-segment timing from Started/Finished planning segment pairs
            seg_start_rows = solver_slice[
                solver_msgs.str.contains("Started planning segment", na=False, regex=False)
            ]

            for _, seg_row in seg_start_rows.iterrows():
                seg_id   = str(seg_row[MESSAGE]).split("Started planning segment")[-1].strip()
                start_ts = seg_row[TIMESTAMP]

                seg_end = solver_slice[
                    solver_msgs.str.contains(
                        f"Finished planning segment {re.escape(seg_id)}", na=False
                    )
                ]

                dur_min  = None
                dur_secs = None
                if not seg_end.empty:
                    end_ts   = seg_end.iloc[0][TIMESTAMP]
                    dur_secs = (end_ts - start_ts).total_seconds()
                    dur_min  = round(dur_secs / 60, 4)

                depth_val = depth_lookup.get(seg_id)
                query_str = f"Segment: [{seg_id}]"
                if depth_val is not None:
                    query_str += f"\nDepth of Supply Chain: {depth_val}"

                output_dict[RID].append(rid)
                output_dict[THREAD].append(thread)
                output_dict[USER_ID].append(detail[USER_ID])
                output_dict[QUERY].append(query_str)
                output_dict[DUR_IN_MINUTES].append(dur_min)
                output_dict[DUR_MM_SS].append(_format_mmss(dur_secs) if dur_secs is not None else None)
                output_dict[START_TIME].append(start_ts.astimezone(tz.tzlocal()))
                output_dict[DAY].append(detail[TIMESTAMP].strftime(Format))

        return DataFrame.from_dict(output_dict)

    # -----------------------------------------------------------------------
    # Plugin run times — query_received lookup built inline (no instance state)
    # -----------------------------------------------------------------------

    def _build_query_received_lookup(self, _data: pd.DataFrame) -> dict:
        """
        Build the (RId, PluginName) → exec-message dict that getPluginRunTimes needs.

        Replaces the old processLogFile + consolidatedOutputLog pipeline:
        same extraction logic, same output, but as a local dict — no intermediate
        DataFrame, no instance variable, no separate preprocessing pass.
        """
        query_received    = {}
        query_received_re = re.compile(
            r"(?i)Query Received:\s*\{[^}]*\}:\s*(Exec plugin instance.*?;)"
        )
        plugin_name_re    = re.compile(
            r"Exec plugin instance(?: \[(.*?)\]| (\S+))", re.IGNORECASE
        )
        exec_plugin_re    = re.compile(r"(Exec plugin instance.*?;)", re.IGNORECASE | re.DOTALL)
        ibpl_re           = re.compile(r"IBPL body generated for parameterized", re.IGNORECASE)
        create_re         = re.compile(r"Create Procedure", re.IGNORECASE)

        cleaned = _data[MESSAGE].str.replace(r"\s+", " ", regex=True).str.strip()

        # Source 1 — Query Received lines
        extracted = cleaned.str.extract(query_received_re.pattern, flags=re.IGNORECASE, expand=False)
        df1_idx   = extracted[extracted.notnull()].index
        for idx in df1_idx:
            exec_msg = extracted[idx]
            m        = plugin_name_re.search(exec_msg)
            plugin   = (m.group(1) or m.group(2)) if m else "Unknown"
            plugin   = plugin.strip("[]") if plugin else "Unknown"
            query_received.setdefault((_data.at[idx, RID], plugin), exec_msg)

        # Sources 2 & 3 — IBPL and Create Procedure lines
        for mask in [cleaned.str.contains(ibpl_re, na=False),
                     cleaned.str.contains(create_re, na=False)]:
            for idx in _data[mask].index:
                msg = cleaned[idx]
                for match in exec_plugin_re.findall(msg):
                    m      = re.search(r"Exec plugin instance (\S+)", match, re.IGNORECASE)
                    plugin = m.group(1).strip("[]") if m else "Unknown"
                    query_received.setdefault((_data.at[idx, RID], plugin), match)

        return query_received

    def getPluginRunTimes(self, _data: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Getting Plugin Data...")

        # Build lookup inline — no processLogFile call, no instance state
        query_received = self._build_query_received_lookup(_data)

        output_dict = defaultdict(list)

        def _dedup(start_msg: str) -> pd.DataFrame:
            return (
                _data[_data[MESSAGE].str.startswith(start_msg, na=False)]
                .drop_duplicates(subset=RID)
                .reset_index(drop=True)
            )

        lp_time              = _dedup("Finished executing plug-in instance")
        batch_job_submit_time = _dedup("Got batch-job submit response")
        exec_plugin_time      = _dedup("Started executing plug-in instance")
        finished_script_time  = _dedup("Finished script execution on")
        write_to_ls_time      = _dedup("Finished executing plug-in instance")

        common_rids = (
            set(lp_time[RID]) & set(batch_job_submit_time[RID])
            & set(exec_plugin_time[RID]) & set(finished_script_time[RID])
            & set(write_to_ls_time[RID])
        )

        def _filter_sort(df):
            return df[df[RID].isin(common_rids)].sort_values(RID).reset_index(drop=True)

        lp_time               = _filter_sort(lp_time)
        batch_job_submit_time = _filter_sort(batch_job_submit_time)
        exec_plugin_time      = _filter_sort(exec_plugin_time)
        finished_script_time  = _filter_sort(finished_script_time)
        write_to_ls_time      = _filter_sort(write_to_ls_time)

        for idx, row in lp_time.iterrows():
            comp_time = re.split(r"\[.*?]", row[MESSAGE])[1].split(":")

            bjs_time = datetime.fromisoformat(str(batch_job_submit_time[TIMESTAMP][idx]))
            epi_time = datetime.fromisoformat(str(exec_plugin_time[TIMESTAMP][idx]))
            fst_time = datetime.fromisoformat(str(finished_script_time[TIMESTAMP][idx]))
            wtl_time = datetime.fromisoformat(str(write_to_ls_time[TIMESTAMP][idx]))

            read_time  = abs(bjs_time - epi_time)
            plan_time  = abs(fst_time - bjs_time)
            write_time = abs(wtl_time - fst_time)

            query = comp_time[0].split("Computation")[0]
            KEY   = (row[RID], query.replace(" ", "").replace("^", "")[:max_characters])
            if KEY not in query_received:
                self.logger.info(f"Skipping RID {row[RID]} — KEY {KEY} not found")
                continue

            duration_sec = float(comp_time[1].replace(",", "").replace("s.", "").strip())
            duration_min = round(duration_sec / 60, 3)

            output_dict[RID].append(row[RID])
            output_dict[THREAD].append(row[THREAD])
            output_dict[USER_ID].append(row[USER_ID])
            output_dict[QUERY].append(query_received[KEY])
            output_dict[DUR_IN_MINUTES].append(duration_min)
            output_dict[DUR_MM_SS].append(_format_mmss(duration_sec))
            output_dict[Records].append(None)
            output_dict[START_TIME].append(row[TIMESTAMP].astimezone(tz.tzlocal()))
            output_dict[DAY].append(row[TIMESTAMP].strftime(Format))
            output_dict[PLUGIN_NAME].append(query.replace(" ", "").replace("^", "")[:max_characters])
            output_dict[PLUGIN_RUN_DIVISION].append("Total Plugin Run Time")
            output_dict[PLUGIN_RUN_DURATION].append(duration_min)

            for div, td in zip(
                ["Total Read Time", "Total Processing Time", "Total Write Time"],
                [read_time, plan_time, write_time],
            ):
                div_secs = td.total_seconds()
                div_min  = round(div_secs / 60, 3)
                output_dict[RID].append(row[RID])
                output_dict[THREAD].append(row[THREAD])
                output_dict[USER_ID].append(row[USER_ID])
                output_dict[QUERY].append(query_received[KEY])
                output_dict[DUR_IN_MINUTES].append(div_min)
                output_dict[DUR_MM_SS].append(_format_mmss(div_secs))
                output_dict[Records].append(None)
                output_dict[START_TIME].append(row[TIMESTAMP].astimezone(tz.tzlocal()))
                output_dict[DAY].append(row[TIMESTAMP].strftime(Format))
                output_dict[PLUGIN_NAME].append(query.replace(" ", "").replace("^", "")[:max_characters])
                output_dict[PLUGIN_RUN_DIVISION].append(div)
                output_dict[PLUGIN_RUN_DURATION].append(div_min)

        return pd.DataFrame.from_dict(output_dict).drop_duplicates()

    def getSolverRunTimes(self, _data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract solver run timing stats per solver run.

        Replaces the old index-arithmetic approach with LogParser's start/end pair
        detection scoped by RId+Thread, using _extract_solver_details for the plugin
        name and _extract_solver_summary for all "Total X ms / Total X = N" stats.
        Each stat becomes one row in the output.
        """
        self.logger.info("Getting Solver Run Time...")
        output_dict = defaultdict(list)

        scs_logs = _data[
            _data[LOGGER].str.contains(SCS_LOGGER_PREFIX, na=False, regex=False)
        ]
        if scs_logs.empty:
            return pd.DataFrame()

        msgs             = scs_logs[MESSAGE]
        solver_start_log = scs_logs[msgs.str.contains("Started plan execution of plugin", na=False, regex=False)]
        solver_end_log   = scs_logs[msgs.str.contains("Total Solver run time",            na=False, regex=False)]

        for start_idx, detail in solver_start_log.iterrows():
            rid    = detail[RID]
            thread = detail[THREAD]

            end_candidates = solver_end_log[
                (solver_end_log.index > start_idx)
                & (solver_end_log[RID] == rid)
                & (solver_end_log[THREAD] == thread)
            ]
            if end_candidates.empty:
                self.logger.info(f"Incomplete solver log for RId {rid}; skipping.")
                continue

            end_idx      = end_candidates.index[-1]
            solver_slice = scs_logs.loc[start_idx:end_idx]

            plugin_name, _, _ = self._extract_solver_details(detail[MESSAGE])
            plugin_name = plugin_name or "Unknown"

            summary = self._extract_solver_summary(solver_slice)
            for stat_name, stat_val in summary.items():
                # Float values come from ms → seconds conversion; ints are counts
                is_timing = isinstance(stat_val, float)
                dur_min   = round(stat_val / 60, 3) if is_timing else None
                output_dict[RID].append(rid)
                output_dict[THREAD].append(thread)
                output_dict[USER_ID].append(detail[USER_ID])
                output_dict[QUERY].append(None)
                output_dict[DUR_IN_MINUTES].append(dur_min)
                output_dict[DUR_MM_SS].append(_format_mmss(stat_val) if is_timing else None)
                output_dict[Records].append(None)
                output_dict[START_TIME].append(detail[TIMESTAMP].astimezone(tz.tzlocal()))
                output_dict[DAY].append(detail[TIMESTAMP].strftime(Format))
                output_dict[PLUGIN_NAME].append(plugin_name)
                output_dict[PLUGIN_RUN_DIVISION].append(stat_name)
                output_dict[PLUGIN_RUN_DURATION].append(stat_val)

        return DataFrame.from_dict(output_dict).drop_duplicates()

    def getCombinedRunTimes(self, _data: pd.DataFrame) -> pd.DataFrame:
        plugin_times = self._safe_call(self.getPluginRunTimes, _data, label="getPluginRunTimes")
        solver_times = self._safe_call(self.getSolverRunTimes, _data, label="getSolverRunTimes")
        return pd.concat([plugin_times, solver_times], ignore_index=True)

    # -----------------------------------------------------------------------
    # Solver plan cache / stats
    #
    # One solver-run loop (scoped by RId+Thread) emits four categories:
    #   "Solver Parameter"   — str.extractall (replaces old flag-based iteration)
    #   "Memory Utilization" — _extract_solver_memory_usage (start/end + per segment)
    #   "Solver Input"       — comma-joined input measure names
    #   "Solver Output"      — comma-joined output measure names
    # Outside that loop: "Static Parameter", "Output Stats", "LP Solver logs".
    # -----------------------------------------------------------------------

    def getSolverPlanCache(self, Plandata: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Getting Solver Stats...")
        output_dict = defaultdict(list)

        # --- Static Parameters (SCS_PLAN_CACHE rows) ---
        plan_cache = Plandata[Plandata[LOGGER] == SCS_PLAN_CACHE]
        for _, d in plan_cache.iterrows():
            tmp = d[MESSAGE].split(".")[-1].split(":")
            if len(tmp) < 2:
                continue
            output_dict[RID].append(d[RID])
            output_dict[THREAD].append(d[THREAD])
            output_dict[USER_ID].append(d[USER_ID])
            output_dict[DAY].append(d[TIMESTAMP].strftime(Format))
            output_dict[QUERY].append(tmp[0].replace(" ", "").replace("^", "")[:max_characters])
            output_dict[Value].append(tmp[1])
            output_dict[Category].append("Static Parameter")

        # --- Per-solver-run: Solver Params, Memory, Input/Output Measures ---
        # Single loop over all solver runs (scoped by RId+Thread) handles:
        #   "Solver Parameter"  — str.extractall (replaces old flag-based sentinel iteration)
        #   "Memory Utilization"— _extract_solver_memory_usage (replaces old scsutil loop)
        #   "Solver Input"      — input measure names, comma-joined
        #   "Solver Output"     — output measure names, comma-joined
        scs_logs = Plandata[
            Plandata[LOGGER].str.contains(SCS_LOGGER_PREFIX, na=False, regex=False)
        ]
        solver_start_log = scs_logs[
            scs_logs[MESSAGE].str.contains("Started plan execution of plugin", na=False, regex=False)
        ]
        solver_end_log = scs_logs[
            scs_logs[MESSAGE].str.contains("Total Solver run time", na=False, regex=False)
        ]

        for start_idx, detail in solver_start_log.iterrows():
            rid    = detail[RID]
            thread = detail[THREAD]
            day    = detail[TIMESTAMP].strftime(Format)

            end_candidates = solver_end_log[
                (solver_end_log.index > start_idx)
                & (solver_end_log[RID] == rid)
                & (solver_end_log[THREAD] == thread)
            ]
            if end_candidates.empty:
                continue
            end_idx      = end_candidates.index[-1]
            solver_slice = scs_logs.loc[start_idx:end_idx]
            solver_msgs  = solver_slice[MESSAGE]

            details = self._extract_relevant_solver_details(solver_msgs)

            def _append(query_val, value_val, category_val):
                output_dict[RID].append(rid)
                output_dict[THREAD].append(thread)
                output_dict[USER_ID].append(detail[USER_ID])
                output_dict[DAY].append(day)
                output_dict[QUERY].append(str(query_val).replace("^", "")[:max_characters])
                output_dict[Value].append(str(value_val))
                output_dict[Category].append(category_val)

            # Solver Parameters
            if Solver_Parameter:
                for _, param_row in details["Solver Params"].iterrows():
                    _append(param_row["Solver Parameter"], param_row["Value"], "Solver Parameter")

            # Memory Utilization — start/end overall + per segment
            mem_msgs = solver_msgs[
                solver_msgs.str.contains(
                    "Private memory size of plugin instance WSupplyChainSolver",
                    na=False, regex=False
                )
            ]
            start_mem, end_mem, segmented = self._extract_solver_memory_usage(mem_msgs)
            if start_mem or end_mem:
                _append("Start Memory", f"{start_mem}GB", "Memory Utilization")
                _append("End Memory",   f"{end_mem}GB",   "Memory Utilization")
            for _, seg_row in segmented.iterrows():
                seg_label = f"Segmented Memory [Segment {seg_row['Segment']}]"
                seg_value = f"{seg_row['Start Memory (GB)']}GB - {seg_row['End Memory (GB)']}GB"
                _append(seg_label, seg_value, "Memory Utilization")

            # Input Measures
            input_measures = details["Solver Inputs Measures"]
            if not input_measures.empty:
                measure_list = ", ".join(input_measures["Input Measure"].dropna().unique())
                _append("Input Measures", measure_list, "Solver Input")

            # Output Measures
            output_measures = details["Solver Outputs Measures"]
            if not output_measures.empty:
                measure_list = ", ".join(output_measures["Output Measure"].dropna().unique())
                _append("Output Measures", measure_list, "Solver Output")

            # WIP counts — not captured by existing input_pattern (no Instance/Segment prefix)
            wip_pattern = re.compile(
                r"Number of ((?:Planned|Locked) (?:Production|Consumption|Capacity) WIPs)\s*:\s*(\d+)",
                re.IGNORECASE,
            )
            wip_extracted = solver_msgs.str.extractall(wip_pattern)
            if not wip_extracted.empty:
                wip_extracted.columns = ["WIP Type", "Count"]
                wip_extracted = wip_extracted.reset_index(drop=True)
                for _, wip_row in wip_extracted.iterrows():
                    _append(
                        f"Number of {wip_row['WIP Type']}",
                        wip_row["Count"],
                        "Solver Input Count",
                    )

        # --- Output Stats (SCS_PLAN rows with Instance prefix) ---
        output_stats = Plandata[Plandata[LOGGER] == SCS_PLAN]
        output_stats = output_stats[output_stats[MESSAGE].str.startswith("Instance", na=False)]
        flag = False
        for _, row in output_stats.iterrows():
            tmp = row[MESSAGE].split(".")[2]
            if flag:
                parts = tmp.split("=")
                if len(parts) < 2:
                    continue
                output_dict[RID].append(row[RID])
                output_dict[THREAD].append(row[THREAD])
                output_dict[USER_ID].append(row[USER_ID])
                output_dict[DAY].append(row[TIMESTAMP].strftime(Format))
                output_dict[QUERY].append(parts[0].replace("^", "")[:max_characters])
                output_dict[Value].append(parts[1])
                output_dict[Category].append("Output Stats")
            if "Finished Zero qty RCA export" in tmp:
                flag = True
            if " Number of Build Ahead buckets saved by Adaptive SS " in tmp:
                flag = False

        # --- LP Solver logs (o9_logger rows starting with "No") ---
        lp_logs = Plandata[
            (Plandata[LOGGER] == _LOGGER) & Plandata[MESSAGE].str.startswith("No", na=False)
        ]
        for _, row in lp_logs.iterrows():
            tmp = row[MESSAGE].split(":")
            if len(tmp) < 2:
                continue
            output_dict[RID].append(row[RID])
            output_dict[THREAD].append(row[THREAD])
            output_dict[USER_ID].append(row[USER_ID])
            output_dict[DAY].append(row[TIMESTAMP].strftime(Format))
            output_dict[QUERY].append(tmp[0].replace("^", "")[:max_characters])
            output_dict[Value].append(tmp[1])
            output_dict[Category].append("LP Solver logs")

        return DataFrame.from_dict(output_dict)

    # -----------------------------------------------------------------------
    # Solver helper methods — ported from LogParser
    # -----------------------------------------------------------------------

    @staticmethod
    def _extract_solver_details(msg: str) -> tuple:
        """
        Parse a solver start message for plugin name, platform version, and run type.
        Returns (plugin_name, platform_version, run_type) — any may be None.
        """
        pattern = re.compile(
            r"Started plan execution of plugin \[([^\]]+)\]: \[([^\]]+)\].*\[([A-Z_]+)\]"
        )
        m = pattern.search(msg)
        if m:
            return m.group(1), m.group(2), m.group(3)
        return None, None, None

    def _extract_solver_summary(self, log: pd.DataFrame) -> dict:
        """
        Summarize numeric and timing entries from a solver log slice.
        Parses 'Total ...' lines ending in 'ms' or containing 'key = value'.
        Noisy/structural lines are excluded before extraction.
        """
        remove_str = [
            "Input Measure :", "Output Measure :",
            "Private memory size of plugin instance",
            "demands for Plan Generation Process.",
            "Detected cycle at ItemLocation",
            ". Number of", "nodes for Inventory Planning.",
            "]. Processed ", "]. Started", "]. Finished",
            "Opened Scs Node writer using file:",
            "Closed edge writer using file:",
            "Persisted SCS nodes",
            "Started persisting pegged flows (",
            "Closed Scs Data Row writer using file:",
            "Opened Scs Data Row writer using file:",
            "Finished persisting pegged flows",
            "Getting exporter for plan",
        ]
        msgs = log[MESSAGE]
        mask = msgs.str.contains("|".join(map(re.escape, remove_str)), na=False)
        lines = log[~mask & msgs.str.contains("Total ", na=False)][MESSAGE].unique()

        solver_summary = {}
        for line in lines:
            line = line.strip()
            if line.endswith("ms"):
                m = re.match(r"(.+?)\s+(\d+)\s*ms$", line)
                if m:
                    solver_summary[m.group(1).strip()] = round(int(m.group(2)) / 1000, 3)
                continue
            m = re.match(r"(.+?)=\s*(\d+)$", line)
            if m:
                solver_summary[m.group(1).strip()] = int(m.group(2))

        return solver_summary

    def _extract_relevant_solver_details(self, log_msg: pd.Series) -> dict:
        """
        Extract structured solver details from a message Series using str.extractall.

        Returns a dict with keys:
            "Cycle"                  — DataFrame(Item, Location)
            "Solver Inputs"          — DataFrame(Segment, Input Name, Value)
            "Solver Inputs Measures" — DataFrame(Input Measure)
            "Solver Outputs Measures"— DataFrame(Output Measure)
            "Solver Depth"           — DataFrame(Segment, Value)
            "Solver Params"          — DataFrame(Solver Parameter, Value)
        """
        # Cycle detection
        cycle_mask = log_msg.str.contains("Detected cycle at ItemLocation", na=False, regex=False)
        cycle_df   = log_msg[cycle_mask].str.extract(
            r"ItemLocation\s+([A-Za-z0-9_\-]+),\s*([A-Za-z0-9_\-]+)"
        )
        cycle_df.columns = ["Item", "Location"]

        # Solver params (indented key:value lines)
        solver_params = log_msg.str.extractall(r"^ {4}([A-Za-z0-9 _]+?)\s*:(\w*)\s*$")
        solver_params.reset_index(level=1, drop=True, inplace=True)
        solver_params.columns = ["Solver Parameter", "Value"]

        # Solver inputs per segment
        solver_inputs = log_msg.str.extractall(
            r"^Instance:\s*\[([^\]]+)\]\.\s*"
            r"Segment:\s*\[(\d+)\]\.\s*"
            r"Number of ([A-Za-z ]+)\s*:\s*(\d+)"
        )
        solver_inputs.columns = ["instance", "Segment", "Input Name", "Value"]
        solver_inputs["Segment"] = solver_inputs["Segment"].astype(int)
        solver_inputs["Value"]   = solver_inputs["Value"].astype(int)
        solver_inputs = solver_inputs[["Segment", "Input Name", "Value"]]
        solver_inputs.reset_index(level=1, drop=True, inplace=True)

        # Depth per segment
        solver_depth = log_msg.str.extractall(
            r"Segment:\s*\[(\d+)\]\.\s*Depth of Supply Chain\s*is\s*:\s*(?P<depth>\d+)$"
        )
        solver_depth.reset_index(drop=True, inplace=True)
        solver_depth.columns = ["Segment", "Value"]

        # Input / output measures
        solver_inputs_measures = log_msg.str.extractall(
            r"Input Measure\s*:\s*Measure\.\[(.*?)\]"
        )
        solver_inputs_measures.reset_index(level=1, drop=True, inplace=True)
        solver_inputs_measures.columns = ["Input Measure"]

        solver_output_measures = log_msg.str.extractall(
            r"Output Measure\s*:\s*Measure\.\[(.*?)\]"
        )
        solver_output_measures.reset_index(level=1, drop=True, inplace=True)
        solver_output_measures.columns = ["Output Measure"]

        return {
            "Cycle":                   cycle_df,
            "Solver Inputs":           solver_inputs,
            "Solver Inputs Measures":  solver_inputs_measures,
            "Solver Outputs Measures": solver_output_measures,
            "Solver Depth":            solver_depth,
            "Solver Params":           solver_params,
        }

    def _extract_solver_memory_usage(self, log: pd.Series) -> tuple:
        """
        Extract min/max memory overall and per segment from
        'Private memory size of plugin instance WSupplyChainSolver' messages.

        Returns (start_memory_gb, end_memory_gb, segmented_DataFrame).
        """
        log_df         = log.to_frame()
        start_memory   = 0
        end_memory     = 0
        segmented_mem  = pd.DataFrame()

        if len(log_df) == 0:
            return start_memory, end_memory, segmented_mem

        log_df["memory_gb"] = (
            log_df[MESSAGE].str.extract(r"([\d.]+)\s*GB").astype(float)
        )
        log_df["Segment"] = (
            log_df[MESSAGE].str.extract(r"Segment\[(\d+)\]").astype("Int64")
        )
        start_memory  = log_df["memory_gb"].min()
        end_memory    = log_df["memory_gb"].max()
        segmented_mem = (
            log_df.dropna(subset=["Segment"])
            .groupby("Segment")["memory_gb"]
            .agg(start_memory="min", end_memory="max")
            .reset_index()
            .rename(columns={"start_memory": "Start Memory (GB)", "end_memory": "End Memory (GB)"})
        )
        return start_memory, end_memory, segmented_mem

    # -----------------------------------------------------------------------
    # Save stats
    # -----------------------------------------------------------------------

    @staticmethod
    def processStat(message: str):
        match = re.search(r'"Data":{[^}]+}', message)
        return json.loads(f"{{{match.group(0)}}}") if match else None

    @staticmethod
    def extract_fields(dicT: dict):
        data = dicT.get("Data", {})
        return data.get("SaveEndTime"), data.get("SaveStartTime"), data.get("VersionsToSave")

    def getSaveStat(self, _data: pd.DataFrame):
        self.logger.info("Getting Save Stats...")
        _data = _data.copy()
        _data[DAY] = _data[TIMESTAMP].dt.strftime(Format)

        data_savestat = _data[_data[MESSAGE].str.contains("Save Stats", na=False)]
        if not data_savestat.empty:
            data_savestat = data_savestat.groupby([DAY])[MESSAGE].last().reset_index()
            try:
                data_savestat[MESSAGE] = data_savestat[MESSAGE].apply(self.processStat)
                try:
                    data_savestat[[END_TIME, START_TIME, VERSION_SAVE]] = (
                        data_savestat[MESSAGE].apply(lambda x: pd.Series(self.extract_fields(x)))
                    )
                except Exception as e:
                    self.logger.info(f"Error in extract_fields: {e}")
            except Exception as e:
                self.logger.info(f"Error in processStat: {e}")
        else:
            data_savestat = pd.DataFrame()

        data_save = _data[
            _data[MESSAGE].str.contains("Query Received:", case=False, na=False)
            & _data[MESSAGE].str.contains(r"Save\(\);", case=False, na=False)
        ]
        data_save = (
            data_save.groupby([DAY]).size().reset_index(name=NUM_EXECUTORS)
            if not data_save.empty else pd.DataFrame()
        )

        if not data_savestat.empty and not data_save.empty:
            output = pd.merge(data_savestat, data_save, on=[DAY], how="left")
            output.drop(columns=MESSAGE, inplace=True)
            return output
        if not data_savestat.empty:
            return data_savestat.assign(**{NUM_EXECUTORS: ""})
        if not data_save.empty:
            for col in [END_TIME, START_TIME, VERSION_SAVE]:
                data_save.insert(1, col, "")
            return data_save
        return None

    # -----------------------------------------------------------------------
    # Error stats
    # -----------------------------------------------------------------------

    def getErrorStats(self, _data: pd.DataFrame) -> pd.DataFrame:
        """
        Collect all ERROR rows, grouped by RId, into one row per request.

        Output columns:
            RId    — request identifier
            Query  — the "Query Received" text for this RId (None if absent)
            Errors — JSON-serialised list of dicts, one per ERROR row for this RId,
                     sorted by Timestamp ascending:
                       [
                         {"error": "<message narrative>", "exception": "<trace or null>"},
                         ...
                       ]
                     "exception" is None when neither the Exception column nor an
                     embedded stack trace is present for that row.

        Message parsing extracts a clean narrative into "error" and any available
        stack/exception detail into "exception", using four strategies in order:
            1. Exception column non-null  → exception = Exception column value
            2. Newline-embedded stack     → split on first \r?\n;
               if the first line also contains an inline ":    at " marker, that
               is further split so the narrative is clean.
            3. Inline ":    at " marker   → split at the colon (IBPLQueryExecutor)
            4. Inline ", exception = "    → split at the keyword (RScriptGeneralized)

        Pure stack-frame rows (Message starts with "at " after stripping) are
        dropped before grouping — they contain no narrative.
        """
        self.logger.info("Getting Error Stats...")

        # ERROR only — WARN excluded.
        error_rows = _data[_data[LEVEL].astype(str) == "ERROR"].copy()
        if error_rows.empty:
            return pd.DataFrame(columns=_OUTPUT_SCHEMAS["ErrorStats"])

        # Drop rows with a null or system null-UUID RId — these are background
        # infrastructure errors not tied to any user request.
        _NULL_UUID = "00000000-0000-0000-0000-000000000000"
        error_rows = error_rows[
            error_rows[RID].notna()
            & (error_rows[RID].astype(str).str.strip() != "")
            & (error_rows[RID].astype(str).str.strip() != _NULL_UUID)
        ]
        if error_rows.empty:
            return pd.DataFrame(columns=_OUTPUT_SCHEMAS["ErrorStats"])

        # Ensure Timestamp is sortable.
        error_rows[TIMESTAMP] = pd.to_datetime(error_rows[TIMESTAMP], errors="coerce", utc=True)

        # Query lookup — first "Query Received" line per RId from the full dataset.
        query_map: dict = {}
        qr_pattern = re.compile(
            r"Query Received:\s*\{[^}]*\}:\s*(.*)", re.DOTALL | re.IGNORECASE
        )
        for _, row in _data[
            _data[MESSAGE].str.contains("Query Received:", regex=False, na=False)
        ].iterrows():
            rid = row[RID]
            if rid not in query_map:
                m = qr_pattern.search(str(row[MESSAGE]))
                if m:
                    query_map[rid] = m.group(1).strip()[:max_characters]

        has_exc_col      = "Exception" in _data.columns
        _newline_re      = re.compile(r"\r?\n", re.MULTILINE)
        _inline_stack_re = re.compile(r":\s{2,}at\s+\w")
        _inline_exc_re   = re.compile(r",?\s*exception\s*=\s*", re.IGNORECASE)

        def _parse_row(msg: str, exc_col_val: str):
            """Return (error_narrative, exception_text_or_None) for one ERROR row."""
            exc_val = (
                exc_col_val
                if exc_col_val and exc_col_val.lower() != "nan"
                else None
            )
            if exc_val:
                error = _newline_re.split(msg, maxsplit=1)[0].strip()
                exception = exc_val
            elif "\n" in msg or "\r\n" in msg:
                parts      = _newline_re.split(msg, maxsplit=1)
                first_line = parts[0].strip()
                rest       = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
                m_stack    = _inline_stack_re.search(first_line)
                if m_stack:
                    error     = first_line[:m_stack.start()].strip()
                    tail      = first_line[m_stack.start() + 1:].strip()
                    exception = (tail + "\n" + rest) if rest else tail
                else:
                    error     = first_line
                    exception = rest
            else:
                m_stack = _inline_stack_re.search(msg)
                if m_stack:
                    error     = msg[:m_stack.start()].strip()
                    exception = msg[m_stack.start() + 1:].strip()
                else:
                    m_exc = _inline_exc_re.search(msg)
                    if m_exc:
                        error     = msg[:m_exc.start()].strip()
                        exception = msg[m_exc.end():].strip() or None
                    else:
                        error     = msg
                        exception = None
            return error, exception

        # Parse every non-stack-frame ERROR row into a flat records list.
        flat: list[dict] = []
        for _, row in error_rows.iterrows():
            msg = str(row[MESSAGE]).strip()
            if re.match(r"at\s+\S", msg):   # pure stack-frame continuation — drop
                continue
            exc_col = str(row["Exception"]).strip() if has_exc_col else ""
            error, exception = _parse_row(msg, exc_col)
            flat.append({
                RID:         row[RID],
                TIMESTAMP:   row[TIMESTAMP],
                "error":     error,
                "exception": exception,
            })

        if not flat:
            return pd.DataFrame(columns=_OUTPUT_SCHEMAS["ErrorStats"])

        flat_df = pd.DataFrame(flat)
        flat_df = flat_df.sort_values([RID, TIMESTAMP]).reset_index(drop=True)

        # Group by RId — one row per request with two parallel sparse dicts.
        #
        # "Error"     : {1: msg, 2: msg, 3: msg, …}  — every error in order
        # "Exception" : {2: trace, …}                 — only keys where a
        #               trace exists; absent keys mean no exception for that
        #               position. Keys are shared so correspondence is exact.
        records = []
        for rid, grp in flat_df.groupby(RID, sort=True):
            # Skip RIds that have no corresponding Query Received entry — the
            # error is not attributable to a user-initiated query.
            query = query_map.get(rid)
            if query is None:
                continue
            error_dict     = {}
            exception_dict = {}
            for i, (_, r) in enumerate(grp.iterrows(), start=1):
                error_dict[i] = r["error"]
                exc = r["exception"] if pd.notna(r["exception"]) else None
                if exc is not None:
                    exception_dict[i] = exc
            records.append({
                RID:         rid,
                QUERY:       query,
                "Error":     json.dumps(error_dict),
                "Exception": json.dumps(exception_dict) if exception_dict else None,
            })

        return pd.DataFrame(records, columns=_OUTPUT_SCHEMAS["ErrorStats"])

    # -----------------------------------------------------------------------
    # Misc utilities
    # -----------------------------------------------------------------------

    @staticmethod
    def format_filename_suffix(list_of_names: list) -> str:
        return "_".join(sub(r"[^\w\s]", "_", str(n)).strip() for n in list_of_names)

    def adding_extra_column_attributes(self, extraDf: DataFrame, dict_of_headers: dict) -> DataFrame:
        if any(h in extraDf.columns for h in dict_of_headers):
            return extraDf
        new_cols = DataFrame({h: [v] * len(extraDf) for h, v in dict_of_headers.items()})
        return concat([new_cols, extraDf], axis=1)