const API_BASE_URL = "http://localhost:8000";

export const apiService = {
  async ask(user_input: string) {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input }),
    });
    if (!response.ok) throw new Error("Failed to fetch plan from orchestrator");
    return response.json();
  },

  async execute(plan: any[]) {
    const response = await fetch(`${API_BASE_URL}/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plan }),
    });
    if (!response.ok) throw new Error("Failed to execute plan");
    return response.json();
  },

  async getLogs(limit: number = 20) {
    const response = await fetch(`${API_BASE_URL}/logs?limit=${limit}`);
    if (!response.ok) throw new Error("Failed to fetch logs");
    return response.json();
  },

  async getAuthUrl() {
    const response = await fetch(`${API_BASE_URL}/auth/login`);
    if (!response.ok) throw new Error("Failed to fetch auth URL");
    return response.json();
  }
};
