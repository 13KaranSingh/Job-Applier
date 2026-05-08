from packages.adapters.ats.greenhouse import GreenhouseAdapter
from packages.adapters.ats.lever import LeverAdapter
from packages.adapters.generic import GenericCareersAdapter
from packages.adapters.companies.amazon import AmazonAdapter
from packages.adapters.companies.citadel import CitadelAdapter
from packages.adapters.companies.citadel_securities import CitadelSecuritiesAdapter
from packages.adapters.companies.databricks import DatabricksAdapter
from packages.adapters.companies.drw import DRWAdapter
from packages.adapters.companies.google import GoogleAdapter
from packages.adapters.companies.hrt import HRTAdapter
from packages.adapters.companies.imc import IMCAdapter
from packages.adapters.companies.jane_street import JaneStreetAdapter
from packages.adapters.companies.jump import JumpAdapter
from packages.adapters.companies.meta import MetaAdapter
from packages.adapters.companies.microsoft import MicrosoftAdapter
from packages.adapters.companies.optiver import OptiverAdapter
from packages.adapters.companies.sig import SIGAdapter
from packages.adapters.companies.stripe import StripeAdapter
from packages.adapters.companies.two_sigma import TwoSigmaAdapter

ADAPTER_REGISTRY = {
    "generic-careers": GenericCareersAdapter,
    "amazon": AmazonAdapter,
    "google": GoogleAdapter,
    "meta": MetaAdapter,
    "microsoft": MicrosoftAdapter,
    "stripe": StripeAdapter,
    "databricks": DatabricksAdapter,
    "greenhouse": GreenhouseAdapter,
    "lever": LeverAdapter,
    "jane-street": JaneStreetAdapter,
    "citadel": CitadelAdapter,
    "citadel-securities": CitadelSecuritiesAdapter,
    "hrt": HRTAdapter,
    "imc": IMCAdapter,
    "optiver": OptiverAdapter,
    "two-sigma": TwoSigmaAdapter,
    "jump": JumpAdapter,
    "sig": SIGAdapter,
    "drw": DRWAdapter,
}
