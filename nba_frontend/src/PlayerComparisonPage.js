import PlayerComparison from "./PlayerComparison";
import { useState, useEffect } from "react";
import PlayerCard from "./PlayerCard";
import { Link } from "react-router-dom";

//Environment variable
const API_URL = process.env.REACT_APP_API_URL;

function PlayerComparisonPage() {
  const [search1, setSearch1] = useState("");
  const [search2, setSearch2] = useState("");
  const [players, setPlayers] = useState([]);
  const [selected1, setSelected1] = useState(null);
  const [selected2, setSelected2] = useState(null);
  const [data1, setData1] = useState(null);
  const [data2, setData2] = useState(null);
  const [loading1, setLoading1] = useState(false);
  const [loading2, setLoading2] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/players`)
      .then((res) => res.json())
      .then(setPlayers);
  }, []);

  useEffect(() => {
    if (selected1) {
      setLoading1(true);
      fetch(`${API_URL}/players/${selected1.ID}/stats`)
        .then((res) => res.json())
        .then((data) => setData1(data))
        .finally(() => setLoading1(false));
    }
  }, [selected1]);

  useEffect(() => {
    if (selected2) {
      setLoading2(true);
      fetch(`${API_URL}/players/${selected2.ID}/stats`)
        .then((res) => res.json())
        .then((data) => setData2(data))
        .finally(() => setLoading2(false));
    }
  }, [selected2]);

  const filterPlayer1 = search1
    ? players
        .filter((p) =>
          p["Full Name"].toLowerCase().includes(search1.toLowerCase())
        )
        .slice(0, 6)
    : [];

  const filterPlayer2 = search2
    ? players
        .filter((p) =>
          p["Full Name"].toLowerCase().includes(search2.toLowerCase())
        )
        .slice(0, 6)
    : [];

  return (
    <div>
      {/* Comparison header */}
      <h1 style={{ textAlign: "center" }}>Compare Two Players</h1>

      {/* Search boxes side by side */}
      <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop: 40 }}>
  <div style={{ display: "flex", gap: 80, maxWidth: 900, width: "100%", justifyContent: "center" }}>
    {/* Player 1 */}
    <div style={{ textAlign: "center", width: 220 }}>
      <h2 style={{marginTop: "-40px"}}>Player 1</h2>
      <div style={{ position: "relative" }}>
        <input
          value={search1}
          onChange={(e) => setSearch1(e.target.value)}
          placeholder="Search player1..."
          style={{ height: "50%", width: "80%", padding: 8, border: "2px solid #000", marginLeft: "-8px" }}
        />
        {search1 && filterPlayer1.length > 0 && (
          <div
            style={{
              position: "absolute",
              top: "40%",
              left: "3.7%",
              width: "87.5%",
              background: "#fff",
              border: "2px solid #000",
              borderRadius: 3,
              maxHeight: 85,
              overflowY: "auto",
              zIndex: 10
            }}
          >
            {filterPlayer1.map((p) => (
              <div
                key={p.ID}
                onClick={() => { setSelected1(p); setSearch1(p["Full Name"]); }}
                style={{ padding: 8, cursor: "pointer", borderBottom: "1px solid #eee" }}
                onMouseOver={(e) => (e.currentTarget.style.background = "#f0f0f0")}
                onMouseOut={(e) => (e.currentTarget.style.background = "#fff")}
              >
                {p["Full Name"]}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>

    {/* Player 2 */}
    <div style={{ textAlign: "center", width: 220 }}>
      <h2 style={{marginTop: "-40px"}}>Player 2</h2>
      <div style={{ position: "relative" }}>
        <input
          value={search2}
          onChange={(e) => setSearch2(e.target.value)}
          placeholder="Search player2..."
          style={{ height: "50%", width: "80%", padding: 8, border: "2px solid #000", marginLeft: "-8px" }}
        />
        {search2 && filterPlayer2.length > 0 && (
          <div
            style={{
              position: "absolute",
              top: "40%",
              left: "3.7%",
              width: "87.5%",
              background: "#fff",
              border: "2px solid #000",
              borderRadius: 3,
              maxHeight: 85,
              overflowY: "auto",
              zIndex: 10,
            }}
          >
            {filterPlayer2.map((p) => (
              <div
                key={p.ID}
                onClick={() => { setSelected2(p); setSearch2(p["Full Name"]); }}
                style={{ padding: 8, cursor: "pointer", borderBottom: "1px solid #eee"}}
                onMouseOver={(e) => (e.currentTarget.style.background = "#f0f0f0")}
                onMouseOut={(e) => (e.currentTarget.style.background = "#fff")}
              >
                {p["Full Name"]}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  </div>
</div>

      {/* Comparison */}
      {data1 && data2 && (
        <div style={{ marginTop: "50px" }}>
          <h2 style={{ textAlign: "center" , marginTop: "20px"}}>Career Comparison</h2>

          {/* Player cards above chart */}
          <div style={{ display: "flex", justifyContent: "center", gap: "30px" }}>
            <PlayerCard playerId={selected1.ID} data={data1} />
            <PlayerCard playerId={selected2.ID} data={data2} />
          </div>

          {/* Chart below */}
          <div style={{ marginTop: "40px" }}>
            <PlayerComparison player1={data1} player2={data2} />
          </div>
        </div>
      )}
      <Link to="/">
                Back To Teams List
    </Link> 
    </div>
  );
}

export default PlayerComparisonPage;
