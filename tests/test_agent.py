import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agent import create_graph_agent, ZabbixAlert

class TestAgentUnit(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Compile the graph agent once for all tests
        cls.agent = create_graph_agent().compile()

        # Load test cases from JSON file
        with open("data/test_cases.json", "r") as f:
            cls.test_cases = json.load(f)

    async def test_alert_processing(self):
        """Iterate through test cases and verify agent behavior (Async)"""
        for case in self.test_cases:
            with self.subTest(case_name=case["name"]):
                print(f"\n[Testing Case]: {case['name']}")

                # Prepare the payload
                alert_payload = ZabbixAlert(**case["payload"])

                # Run the agent ASYNC
                result = await self.agent.ainvoke({"zabbix_alert": alert_payload})

                
                # Verify Router Decision
                decision = result["router_decision"]
                self.assertEqual(
                    decision.category, 
                    case["expected_category"],
                    f"Expected category {case['expected_category']}, but got {decision.category}"
                )
                
                # Verify Ticket Generation
                ticket = result["easyvista_ticket"]
                self.assertIsNotNone(ticket.title)
                self.assertIsNotNone(ticket.details)
                
                # Check for keywords in the resolution details (retrieved from RAG)
                found_keywords = [
                    kw for kw in case["expected_keywords"] 
                    if kw.lower() in ticket.details.lower() or kw.lower() in ticket.summary.lower()
                ]
                
                print(f"   Category: {decision.category} (OK)")
                print(f"   Keywords matched: {found_keywords}")
                
                # We expect at least one relevant keyword from the manual to be present in the ticket
                self.assertTrue(
                    len(found_keywords) > 0, 
                    f"No expected keywords {case['expected_keywords']} found in the ticket details."
                )

if __name__ == "__main__":
    unittest.main()
