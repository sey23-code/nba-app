function MatchupCard({ game }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        border: "1px solid #ddd",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        borderRadius: "12px",
        padding: "15px 20px",
        width: "500px",
        backgroundColor: "#f9f9f9",
        margin: "15px auto",
      }}
    >
      {/* 🔹 Top Row: Away vs Home Logos */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        {/* Away Team */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "6px",
            width: "100px",
          }}
        >
          <strong>{game["Away Team"]}</strong>
          <img
            src={`https://cdn.nba.com/logos/nba/${game["Away Team ID"]}/primary/L/logo.svg`}
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = `https://cdn.nba.com/logos/nba/${game["Away Team ID"]}/primary/D/logo.svg`;
            }}
            alt={`${game["Away Team"]} Logo`}
            style={{ width: "60px", height: "60px" }}
          />
        </div>

        {/* VS / Separator */}
        <div
          style={{
            fontWeight: "bold",
            fontSize: "1.4rem",
            color: "#333",
          }}
        >
          VS
        </div>

        {/* Home Team */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "6px",
            width: "100px",
          }}
        >
          <strong>{game["Home Team"]}</strong>
          <img
            src={`https://cdn.nba.com/logos/nba/${game["Home Team ID"]}/primary/L/logo.svg`}
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = `https://cdn.nba.com/logos/nba/${game["Home Team ID"]}/primary/D/logo.svg`;
            }}
            alt={`${game["Home Team"]} Logo`}
            style={{ width: "60px", height: "60px" }}
          />
        </div>
      </div>

      {/* 🔹 Bottom Row: Game Info */}
      <div style={{ textAlign: "center", marginTop: "12px" }}>
        <p style={{ margin: "3px 0", color: "#555" }}>{game["Arena"]}</p>
        <p
          style={{
            margin: "3px 0",
            fontWeight: "bold",
            color:
              game["Status"].includes("Final")
                ? "#D62828"
                : game["Status"].includes("In Progress")
                ? "#2A9D8F"
                : "#6c757d",
          }}
        >
          {game["Status"]}
        </p>
      </div>
    </div>
  );
}

export default MatchupCard;
