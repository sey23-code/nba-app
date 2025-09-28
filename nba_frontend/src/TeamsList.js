import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import nbaLogo from "./assets/NBA-Logo-1969.png";

//Environment variable
const API_URL = process.env.REACT_APP_API_URL;

function TeamsList() {
  const [teams, setTeams] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    console.log("API_URL is:", API_URL);
    fetch(`${API_URL}/teams`)
      .then((res) => res.json())
      .then((data) => setTeams(data));
  }, []);

  if (teams.length === 0) return <p>Loading...</p>;

  const filterTeams = teams.filter(
    (team) =>
      team["Team Name"].toLowerCase().includes(search.toLowerCase()) ||
      team.City.toLowerCase().includes(search.toLowerCase()) ||
      team.Abbreviation.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      {/* NBA Teams header */}
      <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
        <img
          src={nbaLogo}
          alt="NBA Logo"
          style={{ width: "160px", height: "100px", marginLeft: "670px" }}
        />
        <h1 style={{ margin: 0, marginLeft: "-50px" }}>NBA Teams</h1>
      </div>

      {/* Search bar below header */}
      <input
        type="text"
        placeholder="Search teams..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginTop: "20px", padding: "6px", width: "250px" }}
      />
      <div style={{margin: "15px 0", marginLeft: "5px"}}>
        <Link to="/compare">Go to Player Comparison</Link>
    </div>
      <table>
        <thead>
          <tr>
            <th>Team Name</th>
            <th>Abbreviation</th>
            <th>City</th>
            <th>State</th>
            <th>Year Founded</th>
          </tr>
        </thead>
        <tbody>
          {filterTeams.map((team) => (
            <tr key={team["Team ID"]}>
              <td>
                <Link
                  to={`/team/${encodeURIComponent(
                    team["Nickname"].toLowerCase()
                  )}`}
                >
                  {team["Team Name"]}
                </Link>
              </td>
              <td>{team.Abbreviation}</td>
              <td>{team.City}</td>
              <td>{team.State}</td>
              <td>{team["Year Founded"]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TeamsList;
