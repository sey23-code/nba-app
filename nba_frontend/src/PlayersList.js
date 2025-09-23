import { useState } from "react";
import { useEffect } from "react";

function PlayersList() {
    const [players, setPlayers] = useState([])
    useEffect(() => {
        fetch("http://127.0.0.1:8000/players")
            .then(res => res.json())
            .then(data => setPlayers(data))
    }, []);
    return (
        <div>
            {/*Players header*/}
            <h1>NBA Players</h1>
            <table>
                <thead>
                    <tr>
                        <th>Player Name</th>
                    </tr>
                </thead>
                <tbody>
                    {players.map(player => (
                        <tr key = {player["Player ID"]}>
                            <td>{player["Player Name"]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );    
}
export default PlayersList