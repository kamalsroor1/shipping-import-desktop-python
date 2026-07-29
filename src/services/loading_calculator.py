"""
BP-005 – Cargo Loading Planning & Container Optimization Engine
Calculates space utilization %, payload utilization %, door clearance checks, and cargo fit recommendations.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List

class LoadingCalculationEngine:
    CONTAINER_SPECS = {
        "20GP": {"capacity_cbm": 33.2, "max_payload_kg": 28200, "door_w_cm": 234, "door_h_cm": 228, "int_l_cm": 589, "int_w_cm": 235, "int_h_cm": 239},
        "40GP": {"capacity_cbm": 67.7, "max_payload_kg": 26730, "door_w_cm": 234, "door_h_cm": 228, "int_l_cm": 1203, "int_w_cm": 235, "int_h_cm": 239},
        "40HC": {"capacity_cbm": 76.4, "max_payload_kg": 26580, "door_w_cm": 234, "door_h_cm": 258, "int_l_cm": 1203, "int_w_cm": 235, "int_h_cm": 269},
        "45HC": {"capacity_cbm": 86.0, "max_payload_kg": 27700, "door_w_cm": 234, "door_h_cm": 258, "int_l_cm": 1355, "int_w_cm": 235, "int_h_cm": 269},
    }

    @classmethod
    def evaluate_container_fit(cls, total_cbm: float, total_gross_weight_kg: float, max_pkg_w_cm: float = 0, max_pkg_h_cm: float = 0, container_type: str = "40HC") -> Dict[str, Any]:
        spec = cls.CONTAINER_SPECS.get(container_type, cls.CONTAINER_SPECS["40HC"])
        
        cap_cbm = spec["capacity_cbm"]
        max_payload = spec["max_payload_kg"]
        
        space_util_pct = min(100.0, round((total_cbm / cap_cbm) * 100.0, 2)) if cap_cbm > 0 else 0.0
        payload_util_pct = min(100.0, round((total_gross_weight_kg / max_payload) * 100.0, 2)) if max_payload > 0 else 0.0
        
        rem_cbm = max(0.0, round(cap_cbm - total_cbm, 4))
        rem_payload_kg = max(0.0, round(max_payload - total_gross_weight_kg, 2))

        door_pass = (max_pkg_w_cm <= spec["door_w_cm"]) and (max_pkg_h_cm <= spec["door_h_cm"])

        if total_gross_weight_kg > max_payload:
            status = "Overweight"
            msg = f"Cargo weight ({total_gross_weight_kg} kg) exceeds maximum payload ({max_payload} kg)."
        elif total_cbm > cap_cbm:
            status = "Partial Fit"
            msg = f"Cargo volume ({total_cbm} CBM) exceeds container capacity ({cap_cbm} CBM). Additional container required."
        elif not door_pass:
            status = "Oversized"
            msg = f"Package dimensions ({max_pkg_w_cm}x{max_pkg_h_cm} cm) exceed door clearance ({spec['door_w_cm']}x{spec['door_h_cm']} cm)."
        else:
            status = "Fit"
            msg = "Cargo completely fits within container dimensions and weight capacity."

        return {
            "container_type": container_type,
            "status": status,
            "status_message": msg,
            "total_cbm": total_cbm,
            "container_capacity_cbm": cap_cbm,
            "remaining_cbm": rem_cbm,
            "space_utilization_pct": space_util_pct,
            "total_gross_weight_kg": total_gross_weight_kg,
            "max_payload_kg": max_payload,
            "remaining_payload_kg": rem_payload_kg,
            "payload_utilization_pct": payload_util_pct,
            "door_clearance_passed": door_pass
        }
