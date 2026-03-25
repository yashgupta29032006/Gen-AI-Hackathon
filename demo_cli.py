import httpx
import asyncio
import json
import sys

BASE_URL = "http://localhost:8000"

async def demo():
    print("Welcome to FlowOS Demo CLI")
    print("-" * 30)
    
    query = input("Enter your request (e.g., 'Schedule a catchup today at 5pm and remind me to buy milk'): ")
    
    async with httpx.AsyncClient() as client:
        # Step 1: Ask Orchestrator for a plan
        print("\n[Orchestrator] Analyzing request...")
        try:
            response = await client.post(f"{BASE_URL}/ask", json={"user_input": query}, timeout=30.0)
            response.raise_for_status()
            plan_data = response.json()
        except Exception as e:
            print(f"Error connecting to FlowOS: {e}")
            return

        print(f"\nGoal: {plan_data.get('goal')}")
        print("Proposed Plan:")
        for i, step in enumerate(plan_data.get('plan', []), 1):
            print(f"  {i}. {step['agent'].capitalize()}: {step['action']} ({step['params']})")
        
        confirm = input("\nExecute this plan? (y/n): ")
        if confirm.lower() != 'y':
            print("Execution cancelled.")
            return

        # Step 2: Execute the plan
        print("\n[Workflow] Executing plan...")
        try:
            exec_response = await client.post(f"{BASE_URL}/execute", json={"plan": plan_data['plan']}, timeout=30.0)
            exec_response.raise_for_status()
            result = exec_response.json()
        except Exception as e:
            print(f"Execution error: {e}")
            return

        print("\nExecution Results:")
        for action in result.get('actions_taken', []):
            if "error" in action:
                print(f"  - ERROR: {action['error']}")
            else:
                print(f"  - {action['agent']}: {action['action']} -> {action['result']}")

        # Step 3: Verify logs
        print("\n[Memory] Fetching recent logs...")
        logs_response = await client.get(f"{BASE_URL}/logs?limit=5")
        logs = logs_response.json()
        for log in logs:
            print(f"  [{log['time']}] {log['agent']}: {log['action']}")

if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\nExiting...")
