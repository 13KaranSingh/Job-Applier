from packages.adapters.ats.greenhouse import GreenhouseAdapter
from packages.adapters.ats.lever import LeverAdapter
from packages.adapters.companies.amazon import AmazonAdapter
from packages.adapters.companies.citadel import CitadelAdapter
from packages.adapters.companies.google import GoogleAdapter
from packages.adapters.companies.hrt import HRTAdapter
from packages.adapters.companies.imc import IMCAdapter
from packages.adapters.companies.jane_street import JaneStreetAdapter
from packages.adapters.companies.optiver import OptiverAdapter

ADAPTER_REGISTRY = {
    "amazon": AmazonAdapter,
    "google": GoogleAdapter,
    "greenhouse": GreenhouseAdapter,
    "lever": LeverAdapter,
    "jane-street": JaneStreetAdapter,
    "citadel": CitadelAdapter,
    "hrt": HRTAdapter,
    "imc": IMCAdapter,
    "optiver": OptiverAdapter,
}

