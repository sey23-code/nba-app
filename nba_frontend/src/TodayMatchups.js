import { useState, useEffect } from "react";
import MatchupCard from "./MatchupCard";
import { Link } from "react-router-dom";

const API_URL = process.env.REACT_APP_API_URL;
function TodayMatchups() {
    const [games, setGames] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        setLoading(true);
        fetch(`${API_URL}/games/today`)
        .then((res) => res.json())
        .then((data) => setGames(data.games || []))
        .catch((err) => console.error("Error loading games:", err))
        .finally(() => setLoading(false));
    }, []);

    if (loading) return <p>Loading...</p>;

    return (
        <div>
            {/* Shows Matchups */}
            <h1 style={{ textAlign: "center" }}>Today's Matchups</h1>
            {games.map((game) => (
                <MatchupCard key={game["Game ID"]} game={game} />
            ))}
            <Link to="/">
                Back To Teams List
            </Link> 
        </div>
        
    )
}

export default TodayMatchups