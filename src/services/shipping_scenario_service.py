"""
BP-007 – Shipping Scenarios Evaluation & Warehouse Arrival Projection Service
Calculates vessel lead time, ready for shipping buffer, line delays, total warehouse transit days, and average warehouse ETA across N carrier quotes.
"""

from datetime import date, timedelta
from typing import List, Dict, Any

class ShippingScenarioEvaluator:
    @staticmethod
    def evaluate_scenario(
        crd_date: date,
        sailing_date: date,
        arrival_date: date,
        avg_form4_days: int = 3,
        avg_clearance_days: int = 4,
        expected_line_delay_days: int = 2,
        provider_name: str = "",
        vessel_name: str = ""
    ) -> Dict[str, Any]:
        vessel_lead_time = max(0, (arrival_date - sailing_date).days)
        ready_for_shipping_days = max(0, (sailing_date - crd_date).days)
        
        expected_total_days_to_warehouse = (
            avg_form4_days +
            avg_clearance_days +
            expected_line_delay_days +
            vessel_lead_time +
            ready_for_shipping_days
        )
        
        expected_warehouse_arrival_date = crd_date + timedelta(days=expected_total_days_to_warehouse)

        return {
            "provider_name": provider_name,
            "vessel_name": vessel_name,
            "crd_date": crd_date.isoformat(),
            "sailing_date": sailing_date.isoformat(),
            "arrival_date": arrival_date.isoformat(),
            "vessel_lead_time_days": vessel_lead_time,
            "ready_for_shipping_days": ready_for_shipping_days,
            "avg_form4_days": avg_form4_days,
            "avg_clearance_days": avg_clearance_days,
            "expected_line_delay_days": expected_line_delay_days,
            "expected_total_days_to_warehouse": expected_total_days_to_warehouse,
            "expected_warehouse_arrival_date": expected_warehouse_arrival_date.isoformat()
        }

    @classmethod
    def evaluate_all_scenarios(
        cls,
        crd_date: date,
        options: List[Dict[str, Any]],
        avg_form4_days: int = 3,
        avg_clearance_days: int = 4
    ) -> Dict[str, Any]:
        if not options:
            return {"scenarios": [], "average_expected_days_to_warehouse": 0, "average_expected_arrival_date": crd_date.isoformat()}

        evaluated_scenarios = []
        total_days_sum = 0

        for opt in options:
            res = cls.evaluate_scenario(
                crd_date=crd_date,
                sailing_date=opt["sailing_date"],
                arrival_date=opt["arrival_date"],
                avg_form4_days=avg_form4_days,
                avg_clearance_days=avg_clearance_days,
                expected_line_delay_days=opt.get("expected_line_delay_days", 2),
                provider_name=opt.get("provider_name", "Carrier"),
                vessel_name=opt.get("vessel_name", "Vessel")
            )
            evaluated_scenarios.append(res)
            total_days_sum += res["expected_total_days_to_warehouse"]

        avg_days = round(total_days_sum / len(options))
        avg_arrival_date = crd_date + timedelta(days=avg_days)

        sorted_scenarios = sorted(evaluated_scenarios, key=lambda x: x["expected_warehouse_arrival_date"])

        return {
            "crd_date": crd_date.isoformat(),
            "total_options_evaluated": len(options),
            "scenarios": sorted_scenarios,
            "earliest_arrival_date": sorted_scenarios[0]["expected_warehouse_arrival_date"],
            "latest_arrival_date": sorted_scenarios[-1]["expected_warehouse_arrival_date"],
            "average_expected_days_to_warehouse": avg_days,
            "average_expected_arrival_date": avg_arrival_date.isoformat(),
            "recommended_scenario": sorted_scenarios[0]
        }
