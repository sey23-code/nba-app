import { useState, useEffect } from "react";
import { useParams, Link, useSearchParams } from "react-router-dom";

//Environment variable
const API_URL = process.env.REACT_APP_API_URL;

function PlayerStats() {
  const { playerId } = useParams();
  const [data, setData] = useState({
    player_name: "",
    career_average: {},
    stats: [],
    message: ""
  });
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const teamId = searchParams.get("team");

  useEffect(() => {
    setLoading(true);
    fetch(`${API_URL}/players/${playerId}/stats`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        //Sort seasons by descending order
        const sortSeasons = [...data.stats].sort((a,b) => { 
          return b.SEASON_ID.localeCompare(a.SEASON_ID)
        });
        setData({
          ...data,
          stats: sortSeasons
        });
      })
      .catch((error) => {
        console.error("Error: ", error);
        setData({
          player_name: "Unknown Player",
          career_average: {},
          stats: [],
          message: "Error loading player stats."
        });
      })
      .finally(() => setLoading(false));
  }, [playerId, setData]);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      {/* Players header */}
      <h1>{data.player_name} Stats</h1>

      {data.message ? (
        <p>{data.message}</p>
      ) : (
        <>
          <div
            style={{
              border: "3px solid #000",
              width: "500px",
              height:"250px",
              borderRadius: "8px",
              padding: "10px",
              margin: "20px auto",
              textAlign: "center",
              backgroundColor: "#f9f9f9",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              boxShadow: "0 4px 8px rgba(0,0,0,2)",
              position: "relative"
            }}
          >
            {/* NBA Player image */}
            <div style={{flex: "0 0 auto"}}>
            <img
              src={`https://cdn.nba.com/headshots/nba/latest/260x190/${playerId}.png`}
              alt={`${data.player_name}`}
              style={{ width: "195px", height: "140px", position: "absolute", top: "90px", right: "20px" }}
            />
            </div>
            {/* NBA Player Career Averages */}
            <div style={{textAlign: "left", top: "180px", left: "50px"}}>
              <h2 style={{ top: "10px", right: "50px" }}>{data.player_name}</h2>
              <p style= {{marginBottom: "4px", marginRight: "-325px"}}>
                <strong>Career Averages</strong>
              </p>
              <p style= {{margin: "2px 0", marginRight: "-325px"}}>PPG: {data.career_average?.PPG ?? "N/A"}</p>
              <p style= {{margin: "2px 0", marginRight: "-325px"}}>APG: {data.career_average?.APG ?? "N/A"}</p>
              <p style= {{margin: "2px 0", marginRight: "-325px"}}>RPG: {data.career_average?.RPG ?? "N/A"}</p>
              <p style= {{margin: "2px 0", marginRight: "-325px"}}>SPG: {data.career_average?.SPG ?? "N/A"}</p>
              <p style= {{margin: "2px 0", marginRight: "-325px"}}>BPG: {data.career_average?.BPG ?? "N/A"}</p>
            </div>
          </div>

          {/* Player stats table */}
          <table>
            <thead>
              <tr>
                <th>Season</th>
                <th>Team</th>
                <th>Games Played</th>
                <th>PPG</th>
                <th>APG</th>
                <th>RPG</th>
                <th>SPG</th>
                <th>BPG</th>
              </tr>
            </thead>
            <tbody>
              {Array.isArray(data.stats) && data.stats.length > 0 ? (
                data.stats.map((season, index) => (
                  <tr key={index}>
                    <td>{season.SEASON_ID}</td>
                    <td>{season.TEAM_ABBREVIATION}</td>
                    <td>{season.GP}</td>
                    <td>{season.PPG}</td>
                    <td>{season.APG}</td>
                    <td>{season.RPG}</td>
                    <td>{season.SPG}</td>
                    <td>{season.BPG}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8">No stats available for this player.</td>
                </tr>
              )}
            </tbody>
          </table>
        </>
      )}

      {teamId && <Link to={`/team/${teamId}`}>Back To Roster</Link>}
    </div>
  );
}

export default PlayerStats;
