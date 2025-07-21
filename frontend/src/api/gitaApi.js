const API_BASE = "http://127.0.0.1:8000";

export async function getGitaVerse(sentiment) {
    const response = await fetch(`${API_BASE}/gita/`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({ sentiment }),
    });

    if (!response.ok) {
        throw new Error("Failed to fetch verse");
    }

    return await response.json();
}
