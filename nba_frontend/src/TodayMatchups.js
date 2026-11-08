import { useState, useEffect } from "react";
import MatchupCard from "./MatchupCard";
import { Link } from "react-router-dom";

const API_URL = process.env.REACT_APP_API_URL;
function TodayMatchups() {
    const [games, setGames] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        let active = true;
        const fetchGames = async () => {
            try {
                const response = await fetch(`${API_URL}/games/today`);
                if (!response.ok) {
                    throw new Error("Failed to fetch games");
                }
                const data = await response.json();
                if (active) {
                    setGames(data.games || []);
                }
            } catch (err) {
                console.error("Error loading games:", err);
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        };

    // Fetch games when the page first loads
    fetchGames();

    // Fetch updated games every 30 seconds
    const interval = setInterval(fetchGames, 30000);

    // Stop refreshing when the component unmounts
    return () => {
        active = false;
        clearInterval(interval);
    };
}, []);

    if (loading) return <p>Loading...</p>;

    return (
        <div>
            <Link to="/">
                Back To Teams List
            </Link> 
            {/* Shows Matchups */}
            <h1 style={{ textAlign: "center" }}>Today's Matchups</h1>
            {games.map((game) => (
                <MatchupCard key={game["Game ID"]} game={game} />
            ))}
        </div>
        
    )
}

export default TodayMatchups