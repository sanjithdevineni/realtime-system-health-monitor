from typing import Dict, Optional, Literal

FaultMode = Literal["NONE", "HIGH_CPU", "HIGH_ERROR_RATE", "DOWN"]

# service_name -> fault mode

_faults: Dict[str, FaultMode] = {}

def set_fault(service_name: str, mode: FaultMode) -> None:
    _faults[service_name] = mode

def get_fault(service_name: str) -> FaultMode:
    return _faults.get(service_name, "NONE")

def clear_fault(service_name: str) -> None:
    _faults[service_name] = "NONE"