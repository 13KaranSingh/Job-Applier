from packages.adapters.ats.greenhouse import GreenhouseAdapter


class DatabricksAdapter(GreenhouseAdapter):
    source_name = "Databricks Careers"
    source_slug = "databricks"

