const API_BASE = "http://localhost:8000/api";

export async function sendCommand(
    command: string,
    payload?: Record<string, string>
) {
    const response = await fetch(`${API_BASE}/command`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            command,
            payload,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Command failed");
    }

    return response.json();
}