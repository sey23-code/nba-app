import { useState } from "react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";


function RosterList() {
    const [rosterData, setRosterData] = useState({team_name: "", players: []})
    const { teamId } = useParams();
    const [search, setSearch]= useState("");
    useEffect(() => {
        fetch(`http://127.0.0.1:8000/teams/${teamId}/players`)
            .then(res => res.json())
            .then(data => {
                console.log("Fetched data:", data);
                setRosterData(data);
           });       
    },  [teamId]);
    const filterPlayers = (rosterData.players || []).filter(player =>
        player["Player Name"] &&
        player["Player Name"].toLowerCase().includes(search.toLowerCase()))
    return (
    <div>
        {/* NBA Teams header*/}
        <h1>{rosterData.team_name} Roster</h1>
        <div style={{ paddingTop: "0px", textAlign: "center" }}>
            <img
                src={`https://cdn.nba.com/logos/nba/${rosterData.team_id}/primary/L/logo.svg`}
                alt={`${rosterData.team_name} Logo`}
                style={{ width: "160px", height: "135px", marginTop: "-22px"}}
            />
        </div>
            <input
                type="text"
                placeholder="Search players..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <table>
                <thead>
                    <tr>
                        <th>Player Name</th>
                        <th>Jersey Number</th>
                        <th>Position</th>
                        <th>Height</th>
                        <th>Weight</th>
                        <th>College Attended</th>
                        </tr>
                </thead>
                <tbody>
                    {filterPlayers.map(player => (
                        <tr key = {player["Player ID"]}>
                            <td>
                                <Link to={`/player/${player["Player ID"]}?team=${teamId}`}>
                                    {player["Player Name"]}
                                </Link>
                            </td>
                            <td>{player["Jersey Number"]}</td>
                            <td>{player["Position"]}</td>
                            <td>{player["Height"]}</td>
                            <td>{player["Weight"]}</td>
                            <td>{player["College Attended"]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <Link to="/">
                Back To Teams List
            </Link> 
        </div>
    );    
}
export default RosterList